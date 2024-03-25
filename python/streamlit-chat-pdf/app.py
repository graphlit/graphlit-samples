import streamlit as st
import requests
import jwt
from datetime import datetime
import json
import time
from graphlit_client import Graphlit

# Initialize session state variables if not already done
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'workflow_id' not in st.session_state:
    st.session_state['workflow_id'] = None
if 'content_id' not in st.session_state:
    st.session_state['content_id'] = None
if 'specification_id' not in st.session_state:
    st.session_state['specification_id'] = None
if 'conversation_id' not in st.session_state:
    st.session_state['conversation_id'] = None
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""
if 'content_done' not in st.session_state:
    st.session_state['content_done'] = None

def get_content_metadata():
    # Define the GraphQL mutation
    query = """
    query GetContent($id: ID!) {
        content(id: $id) {
            id
            state
            document {
                title
                keywords
                author
            }            
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['content_id']
    }

    response = st.session_state['client'].request(query=query, variables=variables)

 #   st.json(response)

    if 'content' in response['data']:
        return response['data']['content']['document']
    
    return None

def is_content_done():
    # Define the GraphQL mutation
    query = """
    query IsContentDone($id: ID!) {
        isContentDone(id: $id) {
            result
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state["content_id"]
    }
    response = st.session_state['client'].request(query=query, variables=variables)
    return response['data']['isContentDone']['result']

def delete_content():
    # Define the GraphQL mutation
    query = """
    mutation DeleteContent($id: ID!) {
        deleteContent(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['content_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_content(uri):
    # Define the GraphQL mutation
    mutation = """
    mutation IngestFile($uri: URL!, $workflow: EntityReferenceInput) {
        ingestFile(uri: $uri, workflow: $workflow) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "uri": uri,
        "workflow": {
            "id": st.session_state['workflow_id']
        }
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['content_id'] = response['data']['ingestFile']['id']

    return None

def delete_workflow():
    # Define the GraphQL mutation
    query = """
    mutation DeleteWorkflow($id: ID!) {
        deleteWorkflow(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['workflow_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_workflow():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateWorkflow($workflow: WorkflowInput!) {
        createWorkflow(workflow: $workflow) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "workflow": {
            "preparation": {
            "jobs": [
                {
                "connector": {
                    "type": "AZURE_DOCUMENT_INTELLIGENCE",
                    "azureDocument": {
                        "model": "LAYOUT"
                    }
                }
                }
            ]
            },
            "name": "Azure AI Document Intelligence"
        }
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['workflow_id'] = response['data']['createWorkflow']['id']

    return None

def delete_specification():
    # Define the GraphQL mutation
    query = """
    mutation DeleteSpecification($id: ID!) {
        deleteSpecification(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['specification_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_specification():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateSpecification($specification: SpecificationInput!) {
        createSpecification(specification: $specification) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "specification": {
            "type": "COMPLETION",
            "serviceType": "ANTHROPIC",
            "anthropic": {
                "model": "CLAUDE_3_HAIKU",
                "temperature": 0.5,
                "probability": 0.2,
                "completionTokenLimit": 2048
            },
            "name": "Completion"
        }
    }

    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['specification_id'] = response['data']['createSpecification']['id']

    return None

def delete_conversation():
    # Define the GraphQL mutation
    query = """
    mutation DeleteConversation($id: ID!) {
        deleteConversation(id: $id) {
            id
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['conversation_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def create_conversation():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateConversation($conversation: ConversationInput) {
    createConversation(conversation: $conversation) {
        id
    }
    }
    """

    variables = {
        "conversation": {
            "specification": {
                "id": st.session_state['specification_id']
            },
            "name": "Conversation"
        }
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['client'].request(query=mutation, variables=variables)
    st.session_state['conversation_id'] = response['data']['createConversation']['id']
    return response

def prompt_conversation(prompt):
    # Define the GraphQL mutation
    mutation = """
    mutation PromptConversation($prompt: String!, $id: ID) {
    promptConversation(prompt: $prompt, id: $id) {
        conversation {
            id
        }
        message {
            role
            author
            message
            tokens
            completionTime
        }
        messageCount
    }
    }
    """

    # Define the variables for the mutation
    if st.session_state['conversation_id']:
        variables = {
            "prompt": prompt,
            "id": st.session_state['conversation_id']
        }
    else:
        variables = {
            "prompt": prompt
            }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['client'].request(query=mutation, variables=variables)
    st.session_state['conversation_id'] = response['data']['promptConversation']['conversation']['id']
    return response
       
st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Chat with PDF.")

if st.session_state['token'] is None:
    st.info("To get started, generate a token to connect to your Graphlit project.")

# A dictionary mapping PDF names to their PDF URIs
pdfs = {
    "Attention is all you need": "https://graphlitplatform.blob.core.windows.net/samples/Attention%20Is%20All%20You%20Need.1706.03762.pdf",
    "Uber 10Q (March 2022)": "https://graphlitplatform.blob.core.windows.net/samples/uber_10q_march_2022.pdf",
    "Unifying Large Language Models and Knowledge Graphs: A Roadmap": "https://graphlitplatform.blob.core.windows.net/samples/Unifying%20Large%20Language%20Models%20and%20Knowledge%20Graphs%20A%20Roadmap-2306.08302.pdf",
}

with st.form("data_content_form"):
    selected_pdf = st.selectbox("Select a PDF:", options=list(pdfs.keys()))
    
    pdf_uri = st.text_input("Or enter your own PDF URL", key='pdf_uri')

    uri = pdf_uri if pdf_uri else pdfs[selected_pdf]

    submit_content = st.form_submit_button("Submit")

    # Now, handle actions based on submit_data outside the form's scope
    if submit_content and uri:
        if st.session_state['token']:
            st.session_state['uri'] = uri
            
            # Clean up previous session state
            if st.session_state['conversation_id'] is not None:
                with st.spinner('Deleting existing conversation... Please wait.'):
                    delete_conversation()
                st.session_state["conversation_id"] = None

            if st.session_state['specification_id'] is not None:
                with st.spinner('Deleting existing specification... Please wait.'):
                    delete_specification()
                st.session_state["specification_id"] = None

            if st.session_state['workflow_id'] is not None:
                with st.spinner('Deleting existing workflow... Please wait.'):
                    delete_workflow()
                st.session_state["workflow_id"] = None

            if st.session_state['content_id'] is not None:
                with st.spinner('Deleting existing content... Please wait.'):
                    delete_content()
                st.session_state["content_id"] = None

            error_message = create_workflow()

            if error_message is not None:
                st.error(error_message)
            else:
                error_message = create_content(uri)

                if error_message is not None:
                    st.error(error_message)
                else:
                    start_time = time.time()

                    # Display spinner while processing
                    with st.spinner('Ingesting PDF... Please wait.'):
                        done = False
                        time.sleep(5)
                        while not done:
                            done = is_content_done()

                            # Wait a bit before checking again
                            if not done:
                                time.sleep(2)
                    # Once done, notify the user
                    st.session_state["content_done"] = True

                    duration = time.time() - start_time

                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%H:%M:%S")

                    st.success(f"PDF ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                    metadata = get_content_metadata()

    #                st.json(metadata)

                    st.markdown(f"**PDF URI:** {uri}")

                    if metadata is not None:
                        pdf_title = metadata["title"]
                        pdf_author = metadata["author"]

                        if pdf_title is not None:
                            st.markdown(f"**Title:** {pdf_title}")

                        if pdf_author is not None:
                            st.markdown(f"**Author:** {pdf_author}")

                    placeholder = st.empty()

                    error_message = create_specification()

                    if error_message is not None:
                        st.error(error_message)
                    else:
                        error_message = create_conversation();

                        if error_message is not None:
                            st.error(error_message)
        else:
            st.error("Please fill in all the connection information.")

if st.session_state['content_done'] == True:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    try:
        if prompt := st.chat_input("Ask me anything about this PDF."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                result = prompt_conversation(prompt)
                
                response = result['data']['promptConversation']['message']['message']
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    except:
        st.warning("You need to generate a token before chatting with your PDF.")

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Select a PDF, or fill in your own PDF URL.
        - **Step 3:** Enter a prompt to ask about your PDF.
        """)

    with st.form("credentials_form"):
        st.info("Locate connection information for your project in the [Graphlit Developer Portal](https://portal.graphlit.dev/)")

        st.text_input("Organization ID", value=st.session_state['organization_id'], key="organization_id")
        st.text_input("Preview Environment ID", value=st.session_state['environment_id'], key="environment_id")
        st.text_input("Secret", value=st.session_state['secret_key'], key="secret_key")

        submit_credentials = st.form_submit_button("Generate Token")
        
        if submit_credentials:
            if st.session_state['secret_key'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                st.session_state['client'] = Graphlit(environment_id=st.session_state['environment_id'], organization_id=st.session_state['organization_id'], secret_key=st.session_state['secret_key'])
                st.session_state['token'] = st.session_state['client'].token

                st.success("Token generated successfully.")
            else:
                st.error("Please fill in all the connection information.")

    st.markdown("""
        [Support on Discord](https://discord.gg/ygFmfjy3Qx)            
        [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup)            
        [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
        [More information](https://www.graphlit.com)      
        """)