import streamlit as st
import requests
import jwt
from datetime import datetime
import json
import time
from graphlit_client import Graphlit

# Initialize session state variables if not already done
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'uri' not in st.session_state:
    st.session_state['uri'] = None
if 'specification_id' not in st.session_state:
    st.session_state['specification_id'] = None
if 'workflow_id' not in st.session_state:
    st.session_state['workflow_id'] = None
if 'content_id' not in st.session_state:
    st.session_state['content_id'] = None
if 'content_done' not in st.session_state:
    st.session_state['content_done'] = None    
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""

def ingest_file(uri):
    # Define the GraphQL mutation
    mutation = """
    mutation IngestUri($uri: URL!, $workflow: EntityReferenceInput, $isSynchronous: Boolean) {
        ingestUri(uri: $uri, workflow: $workflow, isSynchronous: $isSynchronous) {
            id
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "isSynchronous": True, # wait for content to be ingested
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

    st.session_state['content_id'] = response['data']['ingestUri']['id']

    return None

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

def delete_all_contents():
    # Define the GraphQL mutation
    query = """
    mutation DeleteAllContents() {
        deleteAllContents() {
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
            name
            state
            type
            serviceType
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
            "name": "Summarization"
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
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
        "id": st.session_state['specification_id']
    }
    response = st.session_state['client'].request(query=query, variables=variables)

def generate_summary(summarization_type, summarization_prompt):
    # Define the GraphQL mutation
    mutation = """
    mutation SummarizeContents($summarizations: [SummarizationStrategyInput!]!, $filter: ContentFilter) {
    summarizeContents(summarizations: $summarizations, filter: $filter) {
        items {
            text
        }
    }
    }
    """

    # Define the variables for the mutation
    variables = {
    "filter": {
        "types": [
            "FILE"
        ],
        "contents": [
            { 
                "id": st.session_state["content_id"]
            }
        ]
    },
    "summarizations": [
        {
            "type": summarization_type,
            "prompt": summarization_prompt,
            "specification": {
                "id": st.session_state["specification_id"]
            }
        }
    ]
    }

    response = st.session_state['client'].request(query=mutation, variables=variables)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        st.error(error_message)
        return "No summary was generated."

    if 'summarizeContents' in response['data'] and len(response['data']['summarizeContents']) > 0:
        return "\n\n".join(item['text'] for content in response['data']['summarizeContents'] for item in content['items'])
    
    return "No summary was generated."

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Summarize any PDF, DOCX, or PPTX file. Summary generated with the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")

# A dictionary mapping PDF names to their PDF URIs
pdfs = {
    "Attention is all you need": "https://graphlitplatform.blob.core.windows.net/samples/Attention%20Is%20All%20You%20Need.1706.03762.pdf",
    "Unifying Large Language Models and Knowledge Graphs: A Roadmap": "https://graphlitplatform.blob.core.windows.net/samples/Unifying%20Large%20Language%20Models%20and%20Knowledge%20Graphs%20A%20Roadmap-2306.08302.pdf",
    "On Approximate Nearest Neighbour Selection for Multi-Stage Dense Retrieval": "https://arxiv.org/pdf/2108.11480.pdf"
}
    
with st.form("data_content_form"):
    selected_pdf = st.selectbox("Select a PDF:", options=list(pdfs.keys()))
    
    document_uri = st.text_input("Or enter your own URL to a file (i.e. PDF, DOCX, PPTX):", key='pdf_uri')

    uri = document_uri if document_uri else pdfs[selected_pdf]

    submit_content = st.form_submit_button("Submit")

    # Now, handle actions based on submit_data outside the form's scope
    if submit_content and uri:
        if st.session_state['token']:
            st.session_state['uri'] = uri
            
            # Clean up previous session state
            if st.session_state['workflow_id'] is None:
                error_message = create_workflow()

                if error_message is not None:
                    st.error(f"Failed to create workflow. {error_message}")

            if st.session_state['content_id'] is not None:
                with st.spinner('Deleting existing content... Please wait.'):
                    delete_content()
                st.session_state["content_id"] = None

            start_time = time.time()

            # Display spinner while processing
            with st.spinner('Ingesting document... Please wait.'):
                error_message = ingest_file(uri)

                if error_message is not None:
                    st.error(f"Failed to ingest file [{uri}]. {error_message}")
                else:
                    # Once done, notify the user
                    st.session_state["content_done"] = True

                    duration = time.time() - start_time

                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%H:%M:%S")

                    st.success(f"Document ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

            placeholder = st.empty()
        else:
            st.error("Please fill in all the connection information.")

summarizations = {
    "Detailed summary": "SUMMARY",
    "Bullet points": "BULLETS",
    "Followup questions": "QUESTIONS",
    "Social media posts": "POSTS",
}

with st.form("summarize_data_form"):
    selected_summarization = st.selectbox("Select a summary type:", options=list(summarizations.keys()))
    
    summarization_prompt = st.text_area("Or enter your own summarization prompt:", key='summarization_prompt', height=300)

    summarization_type = summarizations[selected_summarization]

    submit_summarization = st.form_submit_button("Summarize")

    if st.session_state['content_done'] == True:
        if st.session_state['token']:
            if st.session_state['specification_id'] is not None:
                with st.spinner('Deleting existing specification... Please wait.'):
                    delete_specification()
                st.session_state["specification_id"] = None

            error_message = create_specification()

            if error_message is not None:
                st.error(error_message)
            else:
                start_summary_time = time.time()

                with st.spinner('Generating summary... Please wait.'):
                    if summarization_prompt is not None:
                        summarization_type = "CUSTOM"

                    summary = generate_summary(summarization_type, summarization_prompt)

                    placeholder.markdown(summary)

                    summary_duration = time.time() - start_summary_time

                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%H:%M:%S")

                    st.success(f"Summary generation took {summary_duration:.2f} seconds. Finished at {formatted_time} UTC.")

with st.form("clear_data_form"):
    st.markdown("If you run into any problems, or exceeded your Free Tier project quota, you can delete all your contents to start over.  Be aware, this deletes *all* the contents in your project.")

    submit_reset = st.form_submit_button("Reset project")

    if submit_reset:
        if st.session_state['token']:
            with st.spinner('Deleting contents... Please wait.'):
                delete_all_contents()

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Select a PDF, or fill in your own document URL.
        - **Step 3:** Click to generate summary of file using [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.     
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