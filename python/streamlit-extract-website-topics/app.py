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
if 'workflow_id' not in st.session_state:
    st.session_state['workflow_id'] = None
if 'feed_id' not in st.session_state:
    st.session_state['feed_id'] = None
if 'feed_done' not in st.session_state:
    st.session_state['feed_done'] = None
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""

def query_contents_facets():
    # Define the GraphQL mutation
    query = """
    query QueryContents($filter: ContentFilter) {
        contents(filter: $filter) {
            facets { 
                facet 
                type
                observable {
                    type 
                    observable {
                        id
                        name 
                    } 
                } 
                count
            }
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        "filter": {
            "offset": 0,
            "limit": 0,
            "feeds": {
                "id": st.session_state['feed_id']
            }
        },
        "facets": [ 
            { 
                "facet": "OBSERVABLE" 
            } 
        ],
    }

    response = st.session_state['client'].request(query=query, variables=variables)

    st.json(response)

    if 'contents' in response['data'] and 'facets' in response['data']['contents']:
        return response['data']['contents']['facets']
    
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
                        "type": "MODEL_TEXT",
                        "extractedTypes": [ "LABEL" ]
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

def create_feed(uri):
    mutation = """
    mutation CreateFeed($feed: FeedInput!, $workflow: EntityReferenceInput) {
        createFeed(feed: $feed, workflow: $workflow) {
            id
            name
            state
            type
        }
    }
    """
    variables = {
        "feed": {
            "type": "WEB",
            "web": {
                "uri": uri,
                "readLimit": 10
            },
            "name": uri,
            "workflow": {
                "id": st.session_state['workflow_id']
            }
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

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Analyze website for topics. Will scrape website, and read a maximum of 10 pages via sitemap.xml.")

if st.session_state['token'] is None:
    st.info("To get started, generate a token to connect to your Graphlit project.")

websites = {
    "OpenAI Blog": "https://openai.com/blog", # can't have www.openai.com, otherwise nothing found in sitemap
    "Anthropic News": "https://www.anthropic.com/news",
    "Mistral News": "https://mistral.ai/news/",
    "Groq Blog": "https://wow.groq.com/blog/"
}
    
with st.form("data_feed_form"):
    selected_website = st.selectbox("Select a Website:", options=list(websites.keys()))
    
    website_uri = st.text_input("Or enter your own Website URL", key='website_uri')

    uri = website_uri if website_uri else websites[selected_website]

    submit_data = st.form_submit_button("Submit")

    # Now, handle actions based on submit_data outside the form's scope
    if submit_data and uri:
        st.session_state['feed_done'] = False

        if st.session_state['token']:
            st.session_state['uri'] = uri
            
            # Clean up previous session state
            if st.session_state['feed_id'] is not None:
                with st.spinner('Deleting existing feed... Please wait.'):
                    delete_feed()
                st.session_state["feed_id"] = None

            if st.session_state['workflow_id'] is None:
                error_message = create_workflow()

                if error_message is not None:
                    st.error(f"Failed to create workflow. {error_message}")

            error_message = create_feed(uri)

            if error_message is not None:
                st.error(error_message)
            else:
                start_time = time.time()

                # Display spinner while processing
                with st.spinner('Ingesting website... Please wait.'):
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

                st.success(f"Website ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                content_facets = query_contents_facets()

                st.session_state['content_facets'] = content_facets

                placeholder = st.empty()
        else:
            st.error("Please fill in all the connection information.")

if st.session_state['feed_done'] == True:
    if st.session_state['token']:
        st.markdown(f"**Website URI:** {uri}")

        content_facets = st.session_state['content_facets']

        if content_facets is not None:
            st.header('Topics observed in website:')

#            display_facets_as_chart(content_facets)

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Fill in the website URI.
        - **Step 3:** Click to analyze website topics using Azure OpenAI GPT-4 Turbo 128k LLM.     
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
        [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
        [More information](https://www.graphlit.com)      
        """)