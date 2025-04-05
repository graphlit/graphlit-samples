import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

videos = {
    "Lex Fridman: w/ Sam Altman": "jvqFAi7vkBc",
    "Lex Fridman w/ Yan Lecun": "5t1vTLU7s40",
    "TWiML AI Podcast w/ Ben Prystawski": "MRwLhpqkSUM",
    "Andrew Huberman w/ Dr. Cal Newport": "p4ZfkezDTXQ",
    "60 Minutes: Geoffrey Hinton": "qrvK_KuIeJk"
}

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("data_feed_form"):    
            selected_video = st.selectbox("Select a YouTube video:", options=list(videos.keys()))

            video_uri = st.text_input("Or enter your own YouTube video URL", key='video_uri')
            video_identifier = helpers.parse_uri(video_uri)

            # Assuming parse_uri returns None if no identifier is found
            identifier = video_identifier if video_identifier else videos[selected_video]

            submit_content = st.form_submit_button("Submit")

            if submit_content and identifier and st.session_state['token']:
                helpers.run_async_task(feed.handle_feed, identifier)

                st.switch_page("pages/2_Generate_Chapters.py")

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    input = FeedInput(
                        name=identifier,
                        type=FeedTypes.YOU_TUBE,
                        youtube=YouTubeFeedPropertiesInput(
                            type=YouTubeTypes.VIDEO,
                            videoIdentifiers=[
                                identifier
                            ],
                            readLimit=1
                        )
                    )
                    response = await graphlit.client.create_feed(input)

                    """)
