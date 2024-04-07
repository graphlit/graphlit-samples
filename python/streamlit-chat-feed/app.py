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
if 'feed_id' not in st.session_state:
    st.session_state['feed_id'] = None
if 'feed_done' not in st.session_state:
    st.session_state['feed_done'] = None
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

def create_feed(account_name, container_name, storage_key, prefix):
    mutation = """
    mutation CreateFeed($feed: FeedInput!) {
        createFeed(feed: $feed) {
            id
            name
            state
            type
        }
    }
    """
    variables = {
        "feed": {
            "type": "SITE",
            "site": {
                "type": "AZURE_BLOB",
                "isRecursive": False,
                "azureBlob": {
                    "accountName": account_name,
                    "containerName": container_name,
                    "storageAccessKey": storage_key,
                    "prefix": prefix
                }
            },
            "name": f"{account_name}: {container_name}"
        }
    }
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message
        
    st.session_state["feed_id"] = response['data']['createFeed']['id']
    return None

def delete_feed():
    # Define the GraphQL mutation
    query = """
    mutation DeleteFeed($id: ID!) {
        deleteFeed(id: $id) {
            id
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['feed_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def is_feed_done():
    # Define the GraphQL mutation
    query = """
    query IsFeedDone($id: ID!) {
        isFeedDone(id: $id) {
            result
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state["feed_id"]
    }
    response = st.session_state['client'].request(query=query, variables=variables)
    return response['data']['isFeedDone']['result']

def delete_all_feeds():
    # Define the GraphQL mutation
    query = """
    mutation DeleteAllFeeds() {
        deleteAllFeeds() {
            id
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
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
            "serviceType": "OPEN_AI",
            "searchType": "VECTOR",
            "openAI": {
                "model": "GPT4_TURBO_128K",
                "temperature": 0.1,
                "probability": 0.2,
                "completionTokenLimit": 2048
            },
            "strategy": { 
                "embedCitations": True,
            },
            "promptStrategy": { 
                "type": "REWRITE" # rewrite for semantic search
            },
            "retrievalStrategy": {
                "type": "CONTENT",
                "contentLimit": 10,
                "enableExpandedRetrieval": True
            },
            "rerankingStrategy": {
                "serviceType": "COHERE"
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

def create_conversation():
    # Define the GraphQL mutation
    mutation = """
    mutation CreateConversation($conversation: ConversationInput!) {
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
            "filter": {
                "feeds":[
                    {
                        "id": st.session_state['feed_id']                        
                    }
                ]
            },
            "name": "Conversation"
        }
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return error_message

    st.session_state['conversation_id'] = response['data']['createConversation']['id']

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

def prompt_conversation(prompt):
    # Define the GraphQL mutation
    mutation = """
    mutation PromptConversation($prompt: String!, $id: ID) {
    promptConversation(prompt: $prompt, id: $id) {
        message {
            message
        }
    }
    }
    """

    # Define the variables for the mutation
    variables = {
        "prompt": prompt,
        "id": st.session_state['conversation_id']
    }

    # Send the GraphQL request with the JWT token in the headers
    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return None, error_message

    message = response['data']['promptConversation']['message']['message']

    return message, None
       
st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Chat with files in an Azure storage container.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).  Chat completion uses the [OpenAI GPT-4 Turbo 128k](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) LLM.")

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")

with st.form("data_content_form"):    
    account_name = st.text_input("Enter your Azure storage account name", key='account_name')
    container_name = st.text_input("Enter your Azure blob container name", key='container_name')
    storage_key = st.text_input("Enter your Azure storage access key", key='storage_key')
    prefix = st.text_input("Optionally, enter the relative path within the Azure blob container", key='prefix')

    submit_content = st.form_submit_button("Submit")

    # Now, handle actions based on submit_data outside the form's scope
    if submit_content and account_name and container_name and storage_key:
        st.session_state.messages = []
        st.session_state['feed_done'] = False

        if st.session_state['token']:            
            # Clean up previous session state
            if st.session_state['workflow_id'] is None:
                error_message = create_workflow()

                if error_message is not None:
                    st.error(f"Failed to create workflow. {error_message}")

            if st.session_state['feed_id'] is not None:
                with st.spinner('Deleting existing feed... Please wait.'):
                    delete_feed()
                st.session_state["feed_id"] = None

            start_time = time.time()

            error_message = create_feed(account_name, container_name, storage_key, prefix)

            if error_message is not None:
                st.error(error_message)
            else:
                start_time = time.time()

                # Display spinner while processing
                with st.spinner('Ingesting feed... Please wait.'):
                    done = False
                    time.sleep(5)
                    while not done:
                        done = is_feed_done()

                        # Wait a bit before checking again
                        if not done:
                            time.sleep(2)
                # Once done, notify the user
                st.session_state["feed_done"] = True

                duration = time.time() - start_time

                current_time = datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")

                st.success(f"Feed ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                placeholder = st.empty()
        else:
            st.error("Please fill in all the connection information.")

with st.form("clear_data_form"):
    st.markdown("If you run into any problems, or exceeded your Free Tier project quota, you can delete all your feeds (and ingested content) to start over.  Be aware, this deletes *all* the feeds in your project.")

    submit_reset = st.form_submit_button("Reset project")

    if submit_reset:
        if st.session_state['token']:
            with st.spinner('Deleting feeds... Please wait.'):
                delete_all_feeds()

if st.session_state['feed_done'] == True:
    if st.session_state['token']:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if st.session_state['specification_id'] is None:
            error_message = create_specification()

            if error_message is not None:
                st.error(f"Failed to create specification. {error_message}")

        if st.session_state['conversation_id'] is None:
            error_message = create_conversation()

            if error_message is not None:
                st.error(f"Failed to create conversation. {error_message}")

        try:
            if prompt := st.chat_input("Ask me anything about your content."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    response, error_message = prompt_conversation(prompt)
                    
                    if error_message is not None:
                        st.error(f"Failed to prompt conversation. {error_message}")
                    else:
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
        except:
            st.warning("You need to generate a token before chatting with your content.")

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Enter your Azure blob storage connection information.
        - **Step 3:** Enter a prompt to ask about the files using [OpenAI GPT-4 Turbo 128k](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) LLM.
        """)

    with st.form("credentials_form"):
        st.markdown("## 💡 Start here:")
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
        [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
        [More information](https://www.graphlit.com)      
        """)