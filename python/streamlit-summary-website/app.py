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

def create_feed(uri):
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
            "type": "WEB",
            "web": {
                "uri": uri,
                "readLimit": 10
            },
            "name": uri
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

def generate_summary():
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
            "PAGE"
        ],
        "feeds": [
            { 
                "id": st.session_state["feed_id"]
            }
        ]
    },
    "summarizations": [
        {
            "type": "SUMMARY",
            "specification": {
                "id": st.session_state["specification_id"]
            }
        }
    ]
    }

    response = st.session_state['client'].request(query=mutation, variables=variables)

#    st.json(response)

    if 'errors' in response and len(response['errors']) > 0:
        error_message = response['errors'][0]['message']
        st.error(error_message)
        return "No summary was generated."

    if 'summarizeContents' in response['data'] and len(response['data']['summarizeContents']) > 0:
        return "\n\n".join(item['text'] for content in response['data']['summarizeContents'] for item in content['items'])
    
    return "No summary was generated."

st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
st.title("Graphlit Platform")
st.markdown("Generate summary of website. Will scrape website, and read a maximum of 10 pages via sitemap.xml.")

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
        if st.session_state['token']:
            st.session_state['uri'] = uri
            
            if st.session_state['feed_id'] is not None:
                with st.spinner('Deleting existing feed... Please wait.'):
                    delete_feed()
                st.session_state["feed_id"] = None

            if st.session_state['specification_id'] is not None:
                with st.spinner('Deleting existing specification... Please wait.'):
                    delete_specification()
                st.session_state["specification_id"] = None

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

                st.markdown(f"**Website URI:** {uri}")

                placeholder = st.empty()

                error_message = create_specification()

                if error_message is not None:
                    st.error(error_message)
                else:
                    start_summary_time = time.time()

                    with st.spinner('Generating website summary... Please wait.'):
                        summary = generate_summary()
                        placeholder.markdown(summary)

                        summary_duration = time.time() - start_summary_time
        
                        current_time = datetime.now()
                        formatted_time = current_time.strftime("%H:%M:%S")

                        st.success(f"Website summary generation took {summary_duration:.2f} seconds. Finished at {formatted_time} UTC.")
        else:
            st.error("Please fill in all the connection information.")

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Fill in the website URI.
        - **Step 3:** Click to generate summary of website using [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.     
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