import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

websites = {
    "OpenAI Blog": "https://openai.com/blog", # can't have www.openai.com, otherwise nothing found in sitemap
    "NVIDIA Blog": "https://blogs.nvidia.com/",
    "Call to the Pen (Baseball)": "https://calltothepen.com/"
}

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("data_feed_form"):    
            selected_website = st.selectbox("Select a Website:", options=list(websites.keys()))
            
            website_uri = st.text_input("Or enter your own Website URL", key='website_uri')

            uri = website_uri if website_uri else websites[selected_website]

            submit_content = st.form_submit_button("Submit")

            if submit_content and uri and st.session_state['token']:
                helpers.run_async_task(feed.handle_feed, uri)

                st.switch_page("pages/2_Topics.py")

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
                        type=FeedTypes.WEB,
                        web=WebFeedPropertiesInput(
                            uri=uri,
                            readLimit=10
                        )
                    )

                    response = await graphlit.client.create_feed(input)

                    """)
