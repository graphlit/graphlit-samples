import streamlit as st
import requests
import jwt
from datetime import datetime
import json
import time
from urllib.parse import urlparse, parse_qs
from graphlit_client import Graphlit

# Initialize session state variables if not already done
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'identifier' not in st.session_state:
    st.session_state['identifier'] = None
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

def create_feed(identifier):
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
            "type": "YOU_TUBE",
            "youtube": {
                "type": "VIDEO",
                "videoIdentifiers": [
                    identifier
                ],
                "readLimit": 1
            },
            "name": identifier
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

def get_content_metadata_by_feed():
    # Define the GraphQL mutation
    query = """
    query QueryContents($filter: ContentFilter) {
        contents(filter: $filter) {
            results {
                id
                state
                audio {
                    title
                    series
                    duration
                }            
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
            "fileTypes": [
                "AUDIO"
            ],
            "feeds": [
                {
                    "id": st.session_state["feed_id"]
                }
            ]
        }
    }

    response = st.session_state['client'].request(query=query, variables=variables)

 #   st.json(response)

    if 'results' in response['data']["contents"] and len(response['data']['contents']['results']) > 0:
        return response['data']['contents']['results'][0]['audio']
    
    return None

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

def parse_uri(url):
    """
    Extracts the YouTube video ID from a given URL.

    Parameters:
    - url (str): The URL from which to extract the video ID.

    Returns:
    - str: The extracted YouTube video ID, or None if not found.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Validate the netloc to ensure it's a YouTube URL
    if 'youtube.com' in parsed_url.netloc:
        # Parse the query string
        query_string = parse_qs(parsed_url.query)
        
        # Get the video ID from the 'v' parameter
        video_id = query_string.get('v')
        
        if video_id:
            return video_id[0]
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
            "FILE"
        ],
        "feeds": [
            { 
                "id": st.session_state["feed_id"]
            }
        ]
    },
    "summarizations": [
        {
            "type": "CHAPTERS",
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
st.markdown("Generate chapters of YouTube video.")

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")

videos = {
    "Lex Fridman: w/ Sam Altman": "jvqFAi7vkBc",
    "Lex Fridman w/ Yan Lecun": "5t1vTLU7s40",
    "TWiML AI Podcast w/ Ben Prystawski": "MRwLhpqkSUM",
    "Andrew Huberman w/ Dr. Cal Newport": "p4ZfkezDTXQ",
    "60 Minutes: Geoffrey Hinton": "qrvK_KuIeJk"
}

with st.form("data_feed_form"):
    selected_video = st.selectbox("Select a YouTube video:", options=list(videos.keys()))

    video_uri = st.text_input("Or enter your own YouTube video URL", key='video_uri')
    video_identifier = parse_uri(video_uri)

    # Assuming parse_uri returns None if no identifier is found
    identifier = video_identifier if video_identifier else videos[selected_video]

    submit_data = st.form_submit_button("Submit")

    if submit_data and identifier:
        if st.session_state['token']:
            st.session_state['identifier'] = identifier
            
            if st.session_state['feed_id'] is not None:
                with st.spinner('Deleting existing feed... Please wait.'):
                    delete_feed()
                st.session_state["feed_id"] = None

            if st.session_state['specification_id'] is not None:
                with st.spinner('Deleting existing specification... Please wait.'):
                    delete_specification()
                st.session_state["specification_id"] = None

            error_message = create_feed(identifier)

            if error_message is not None:
                st.error(error_message)
            else:
                start_time = time.time()

                # Display spinner while processing
                with st.spinner('Ingesting YouTube video... Will be slow because of YouTube rate-limiting. Please wait.'):
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

                st.success(f"YouTube video ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

                st.markdown(f"**YouTube video URL:** https://www.youtube.com/watch?v={identifier}")

                metadata = get_content_metadata_by_feed()

#                st.json(metadata)

                if metadata is not None:
                    video_title = metadata["title"]
                    video_series = metadata["series"]
                    video_duration = metadata["duration"]

                    if video_title is not None:
                        st.markdown(f"**Video:** {video_title}")

                    if video_series is not None:
                        st.markdown(f"**Channel:** {video_series}")

                    st.markdown(f"**Duration:** {video_duration}")

                placeholder = st.empty()

                error_message = create_specification()

                if error_message is not None:
                    st.error(error_message)
                else:
                    start_summary_time = time.time()

                    with st.spinner('Generating YouTube video chapters... Please wait.'):
                        summary = generate_summary()
                        placeholder.markdown(summary)

                        summary_duration = time.time() - start_summary_time
        
                        current_time = datetime.now()
                        formatted_time = current_time.strftime("%H:%M:%S")

                        st.success(f"YouTube video chapter generation took {summary_duration:.2f} seconds. Finished at {formatted_time} UTC.")
        else:
            st.error("Please fill in all the connection information.")

with st.form("clear_data_form"):
    st.markdown("If you run into any problems, or exceeded your project quota, you can delete all your feeds and content to start over.  Be aware, this deletes *all* the content in your project.")

    submit_reset = st.form_submit_button("Reset project")

    if submit_reset:
        if st.session_state['token']:
            with st.spinner('Deleting feeds... Please wait.'):
                delete_all_feeds()

            with st.spinner('Deleting contents... Please wait.'):
                delete_all_contents()

with st.sidebar:
    st.info("""
        ### Demo Instructions
        - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
        - **Step 1:** Generate Graphlit project token.
        - **Step 2:** Fill in the YouTube video identifier.
        - **Step 3:** Click to generate chapters from YouTube video using [Deepgram](https://www.deepgram.com) audio transcription and [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.     
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