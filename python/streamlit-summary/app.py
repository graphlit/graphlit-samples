import streamlit as st
import requests
import jwt
import datetime
import json
from graphlit_client import Graphlit

# Initialize session state variables if not already done
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'summary_result' not in st.session_state:
    st.session_state['summary_result'] = None
if 'summarize_id' not in st.session_state:
    st.session_state['summarize_id'] = None
if 'client' not in st.session_state:
    st.session_state['client'] = None
if 'environment_id' not in st.session_state:
    st.session_state['environment_id'] = ""
if 'organization_id' not in st.session_state:
    st.session_state['organization_id'] = ""
if 'secret_key' not in st.session_state:
    st.session_state['secret_key'] = ""

def send_request(name, uri):
    url = 'https://data-scus.graphlit.io/api/v1/graphql'
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
                "uri": uri
            },
            "name": name
        }
    }
    response = st.session_state['client'].request(query=mutation, variables=variables)
    st.json(response)

def list_feeds():
    # Define the GraphQL mutation
    query = """
    query QueryFeeds($filter: FeedFilter!) {
        feeds(filter: $filter) {
            results {
            id
            name
            creationDate
            state
            owner {
                id
            }
            type
            reddit {
                subredditName
            }
            lastPostDate
            lastReadDate
            readCount
            schedulePolicy {
                recurrenceType
                repeatInterval
            }
            }
        }
    }
    """

    # Define the variables for the mutation
    variables = {
    "filter": {
        "offset": 0,
        "limit": 100
    }
    }
    response = st.session_state['client'].request(query=query, variables=variables)
    st.json(response)


def delete_all_feeds():
    # Define the GraphQL mutation
    query = """
    mutation DeleteAllFeeds {
        deleteAllFeeds {
            id
            state
        }
        }
    """

    # Define the variables for the mutation
    variables = {
    }
    response = st.session_state['client'].request(query=query, variables=variables)
    st.json(response)

def create_specs():
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
        "serviceType": "AZURE_OPEN_AI",
        "azureOpenAI": {
        "model": "GPT35_TURBO_16K",
        "temperature": 0.8,
        "probability": 0.2
        },
        "name": "GPT-3.5 Turbo Summarization"
    }
    }
    
    # Convert the request to JSON format
    response = st.session_state['client'].request(query=mutation, variables=variables)
    st.session_state['summarize_id'] = response['data']['createSpecification']['id']

def generate_summary(id, search):
    print(id)
    print(search)
    # Define the GraphQL mutation
    mutation = """
    mutation SummarizeContents($summarizations: [SummarizationStrategyInput!]!, $filter: ContentFilter) {
    summarizeContents(summarizations: $summarizations, filter: $filter) {
        specification {
        id
        }
        content {
        id
        }
        type
        items {
        text
        tokens
        summarizationTime
        }
        error
    }
    }
    """

    # Define the variables for the mutation
    variables = {
    "summarizations": [
        {
        "type": "SUMMARY",
        "specification": {
            "id": id
        },
        "items": 5
        },
        {
        "type": "QUESTIONS",
        "specification": {
            "id": id
        },
        "items": 5
        },
        {
        "type": "CUSTOM",
        "specification": {
            "id": id
        },
        "prompt": "Extract any named entities into JSON-LD format."
        }
    ],
    "filter": {
        "search": search,
        "queryType": "SIMPLE",
        "searchType": "HYBRID"
    }
    }

    response = st.session_state['client'].request(query=mutation, variables=variables)
    print(response)
    return response

st.title("Graphlit Platform")
st.markdown("Summarize website.")

if st.session_state['token'] is None:
    st.info("To get started, generate a token to connect to your Graphlit project.")
    
# Data feeding section
with st.form("data_feed_form"):
    name = st.text_input("Feed name")
    uri = st.text_input("Website URI")
    submit_data = st.form_submit_button("Submit")

if st.session_state['token']:
    list, delete = st.columns(2)
    with list:
        list_feed = st.button("List Feeds")
        if list_feed:
            list_feeds()
    with delete:
        delete_feed = st.button("Delete All Feeds")
        if delete_feed:
            delete_all_feeds()

if submit_data:
    if st.session_state['token'] and uri:
        send_request(name, uri)
        st.success("Your website is now being ingested.")
    else:
        st.error("Please generate a token and provide a URI.")

search = st.text_input("Search text")
submit_summary = st.button("Generate LLM summary from search results")

st.header("Summary Result")

if submit_summary:
    if st.session_state['token'] and search:
        if st.session_state['summarize_id']:
            st.json(generate_summary(st.session_state['summarize_id'], search))
            st.success("Your summary was generated successfully.")
        else:
            create_specs()
            st.json(generate_summary(st.session_state['summarize_id'], search))
            st.success("Your summary was generated successfully.")
    else:
        st.error("Please ensure you have a token and have provided a content filter.")
    
with st.sidebar:
    with st.form("credentials_form"):
        st.info("Locate connection information for your project in the [Graphlit Developer Portal](https://portal.graphlit.dev/)")
        st.session_state['secret_key'] = st.text_input("Secret Key", type="password")
        st.session_state['environment_id'] = st.text_input("Environment ID")
        st.session_state['organization_id'] = st.text_input("Organization ID")
        submit_credentials = st.form_submit_button("Generate Token")

    st.sidebar.info("""
        ### Demo Instructions                            

        For more information:
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup)
        - [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)           
        """)
        
if submit_credentials:
    if st.session_state['secret_key'] and st.session_state['environment_id'] and st.session_state['organization_id']:
        st.session_state['client'] = Graphlit(environment_id=st.session_state['environment_id'], organization_id=st.session_state['organization_id'], secret_key=st.session_state['secret_key'])
        st.session_state['token'] = st.session_state['client'].token
        print(st.session_state['token'])
        st.success("Token generated successfully.")
    else:
        st.error("Please fill in all the connection information.")
