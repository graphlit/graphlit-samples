import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

subreddits = {
    "r/openai": "openai",
    "r/anthropic": "anthropic",
    "r/mistralai": "MistralAI",
    "r/llmdevs": "llmdevs",
    "r/chatgptcoding": "chatgptcoding",
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
            selected_subreddit = st.selectbox("Select a Reddit subreddit:", options=list(subreddits.keys()))
            
            subreddit_name = st.text_input("Or enter your own Reddit subreddit name", key='subreddit_name')

            name = subreddit_name if subreddit_name else subreddits[selected_subreddit]

            submit_content = st.form_submit_button("Submit")

            if submit_content and name and st.session_state['token']:
                helpers.run_async_task(feed.handle_feed, name)

                st.switch_page("pages/2_Generate_Followup_Questions.py")

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
                        name="{name}",
                        type=FeedTypes.REDDIT,
                        reddit=RedditFeedPropertiesInput(
                            subredditName="{name}",
                            readLimit=10
                        )
                    )

                    response = await graphlit.client.create_feed(input)

                    """)
