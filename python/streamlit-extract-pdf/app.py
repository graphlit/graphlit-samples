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
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""
if 'content_done' not in st.session_state:
    st.session_state['content_done'] = None
if 'document_markdown' not in st.session_state:
    st.session_state['document_markdown'] = None
if 'document_metadata' not in st.session_state:
    st.session_state['document_metadata'] = None
if 'document_observations' not in st.session_state:
    st.session_state['document_observations'] = None

def ingest_file(uri):
    # Define the GraphQL mutation
    mutation = """
    mutation IngestFile($uri: URL!, $workflow: EntityReferenceInput, $isSynchronous: Boolean) {
        ingestFile(uri: $uri, workflow: $workflow, isSynchronous: $isSynchronous) {
            id
            markdown
            document {
                title
                keywords
                author
                pageCount
            }
            observations {
                type
                occurrences {
                    type
                    pageIndex
                }
                observable {
                    name
                }
            } 
			            
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
        return None, None, None, error_message

    st.session_state['content_id'] = response['data']['ingestFile']['id']

    return response['data']['ingestFile']['document'], response['data']['ingestFile']['markdown'], response['data']['ingestFile']['observations'], None

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
            "extraction": {
                "jobs": [
                    {
                    "connector": {
                        "type": "AZURE_COGNITIVE_SERVICES_TEXT",
                        "extractedTypes": [ "ORGANIZATION", "PERSON" ]
                    }
                    }
                ]
            },
            "name": "Entity Extraction"
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

def display_observations_as_chips(observations):
    # Group observations by type
    result = {}
    
    # Define a fixed color lookup table for observable types
    colors = {
        "LABEL": "#FFD700",  # Gold
        "PERSON": "#FF6347",  # Tomato
        "ORGANIZATION": "#4682B4",  # SteelBlue
        # Define more types and their colors as needed
    }
    
    for observation in observations:
        observation_type = observation['type']
        observable_name = observation['observable']['name']

        if observation_type not in result:
            result[observation_type] = []
        
        result[observation_type].append(observable_name)
    
    # For each observation type, create a row with type label and chips
    for observation_type, observable_names in result.items():
        # Sort the list of observable names for this type
        observable_names.sort()

        # Create a row for each type
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"**{observation_type}**")
        
        with col2:
            # Fetch the color for each observation type from the lookup table
            chip_color = colors.get(observation_type, "#DDDDDD")  # Default color if type not found
            
            # Adjust chip style and layout
            chips = ''.join([
                f"<span style='padding: 8px 12px; background-color: {chip_color}; border-radius: 5px; margin: 5px; display: inline-block; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-family: Arial, sans-serif; color: #FFFFFF;'>{name}</span>"
                for name in sorted(observable_names)  # Sort names before generating chips
            ])

            st.markdown(f"<div style='display: flex; flex-wrap: wrap;'>{chips}</div>", unsafe_allow_html=True)

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Extract people and companies from any PDF, DOCX, or PPTX file. Entity extraction is done with [Azure AI Language](https://azure.microsoft.com/en-us/products/ai-services/ai-language).")

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")

# A dictionary mapping PDF names to their PDF URIs
pdfs = {
    "Microsoft 10Q (March 2024)": "https://graphlitplatform.blob.core.windows.net/samples/MSFT_FY24Q1_10Q.docx",
    "Uber 10Q (March 2022)": "https://graphlitplatform.blob.core.windows.net/samples/uber_10q_march_2022.pdf",
    "Attention is all you need": "https://graphlitplatform.blob.core.windows.net/samples/Attention%20Is%20All%20You%20Need.1706.03762.pdf",
    "Unifying Large Language Models and Knowledge Graphs: A Roadmap": "https://graphlitplatform.blob.core.windows.net/samples/Unifying%20Large%20Language%20Models%20and%20Knowledge%20Graphs%20A%20Roadmap-2306.08302.pdf",
}

document_metadata = None
document_markdown = None
document_observations = None

with st.form("data_content_form"):
    selected_pdf = st.selectbox("Select a PDF:", options=list(pdfs.keys()))
    
    document_uri = st.text_input("Or enter your own URL to a file (i.e. PDF, DOCX, PPTX):", key='pdf_uri')

    uri = document_uri if document_uri else pdfs[selected_pdf]

    submit_content = st.form_submit_button("Submit")

    # Now, handle actions based on submit_data outside the form's scope
    if submit_content and uri:
        st.session_state.messages = []
        st.session_state['content_done'] = False

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
                document_metadata, document_markdown, document_observations, error_message = ingest_file(uri)

                if error_message is not None:
                    st.error(f"Failed to ingest file [{uri}]. {error_message}")
                else:
                    st.session_state['document_metadata'] = document_metadata
                    st.session_state['document_markdown'] = document_markdown
                    st.session_state['document_observations'] = document_observations

                    # Once done, notify the user
                    st.session_state["content_done"] = True

                    duration = time.time() - start_time

                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%H:%M:%S")

                    st.success(f"Document ingestion and extraction took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

            placeholder = st.empty()
        else:
            st.error("Please fill in all the connection information.")

if st.session_state['content_done'] == True:
    if st.session_state['token']:
        st.markdown(f"**Document URI:** {uri}")

        document_metadata = st.session_state['document_metadata']
        document_markdown = st.session_state['document_markdown']
        document_observations = st.session_state['document_observations']

        if document_metadata is not None:
            document_title = None
            document_author = None
            document_pageCount = None

            if 'title' in document_metadata:
                document_title = document_metadata["title"]

            if 'author' in document_metadata:
                document_author = document_metadata["author"]

            if document_title is not None:
                st.markdown(f"**Title:** {document_title}")

            if document_author is not None:
                st.markdown(f"**Author:** {document_author}")

            if document_pageCount is not None:
                st.markdown(f"**Page count:** {document_pageCount}")

        if document_markdown is not None:
            with st.expander("See document text:", expanded=False):
                st.markdown(document_markdown)
        
        if document_observations is not None:
            st.header('Entities observed in document:')

            display_observations_as_chips(document_observations)

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
        - **Step 3:** View entities extracted from document text, i.e. persons and organizations.
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