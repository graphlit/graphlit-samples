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

def get_content():
    # Define the GraphQL mutation
    query = """
    query GetContent($id: ID!) {
        content(id: $id) {
            id
            state
            markdown
            document {
                title
                keywords
                author
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
        "id": st.session_state['content_id']
    }

    response = st.session_state['client'].request(query=query, variables=variables)

 #   st.json(response)

    if 'content' in response['data']:
        return response['data']['content']['document'], response['data']['content']['markdown'], response['data']['content']['observations']
    
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

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        return None, error_message

    return response['data']['isContentDone']['result'], None

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

def ingest_file(uri):
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
        # Create a row for each type
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.markdown(f"**{observation_type}**")
        
        with col2:
            # Fetch the color for each observation type from the lookup table
            chip_color = colors.get(observation_type, "#DDDDDD")  # Default color if type not found
            
            # Adjust chip style and layout
            chips = ''.join([f"<span style='padding: 8px 10px; background-color: {chip_color}; border-radius: 5px; margin: 5px; display: inline-block;'>{name}</span>" for name in observable_names])
            st.markdown(f"<div style='display: flex; flex-wrap: wrap;'>{chips}</div>", unsafe_allow_html=True)

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Extract people and companies from any PDF, DOCX, or PPTX file.")

if st.session_state['token'] is None:
    st.info("To get started, generate a token to connect to your Graphlit project.")

# A dictionary mapping PDF names to their PDF URIs
pdfs = {
    "Uber 10Q (March 2022)": "https://graphlitplatform.blob.core.windows.net/samples/uber_10q_march_2022.pdf",
}

document_metadata = None
document_markdown = None

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

            else:
                error_message = ingest_file(uri)

                if error_message is not None:
                    st.error(f"Failed to ingest file [{uri}]. {error_message}")
                else:
                    start_time = time.time()

                # Display spinner while processing
                with st.spinner('Ingesting document... Please wait.'):
                    done = False
                    time.sleep(2)
                    while not done:
                        done, error_message = is_content_done()

                        if error_message is not None:
                            st.error(f"Failed to wait for content to be done. {error_message}")
                            done = True                                

                        # Wait a bit before checking again
                        if not done:
                            time.sleep(2)
                # Once done, notify the user
                st.session_state["content_done"] = True

                duration = time.time() - start_time

                current_time = datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")

                st.success(f"Document ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                document_metadata, document_markdown, document_observations = get_content()

                st.session_state['document_metadata'] = document_metadata
                st.session_state['document_markdown'] = document_markdown
                st.session_state['document_observations'] = document_observations

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
            document_title = document_metadata["title"]
            document_author = document_metadata["author"]

            if document_title is not None:
                st.markdown(f"**Title:** {document_title}")

            if document_author is not None:
                st.markdown(f"**Author:** {document_author}")

        if document_markdown is not None:
            with st.expander("See document text:", expanded=False):
                st.markdown(document_markdown)
        
        if document_observations is not None:
            st.header('People and organizations observed in document:')

            display_observations_as_chips(document_observations)

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Select a PDF, or fill in your own document URL.
        - **Step 3:** TODO
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