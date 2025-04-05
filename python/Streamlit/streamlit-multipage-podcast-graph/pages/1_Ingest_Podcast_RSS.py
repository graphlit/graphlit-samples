import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

# A dictionary mapping podcast names to their RSS URIs
podcasts = {
    "TWiML Podcast": "https://feeds.megaphone.fm/MLN2155636147",
    "AI in Business Podcast": "https://podcast.emerj.com/rss",
    "Data Engineering Podcast": "https://feeds.fireside.fm/dataengineering/rss",
    "Earley AI Podcast": "https://feeds.buzzsprout.com/1853100.rss"
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
            selected_podcast = st.selectbox("Select a Podcast:", options=list(podcasts.keys()))
            
            podcast_uri = st.text_input("Or enter your own Podcast RSS URL", key='podcast_uri')

            uri = podcast_uri if podcast_uri else podcasts[selected_podcast]

            submit_content = st.form_submit_button("Submit")

            if submit_content and uri and st.session_state['token']:
                helpers.run_async_task(feed.handle_feed, uri)

                st.switch_page("pages/2_Visualize_Knowledge_Graph.py")

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
                        name=uri,
                        type=FeedTypes.RSS,
                        rss=RSSFeedPropertiesInput(
                            uri="{uri}",
                            readLimit=5
                        )
                    )

                    response = await graphlit.client.create_feed(input)

                    """)
