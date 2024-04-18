import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

websites = {
    "OpenAI TikToken": "https://github.com/openai/tiktoken/", # can't have www.openai.com, otherwise nothing found in sitemap
    "OpenAI Python Client": "https://github.com/openai/openai-python/",
    "Mistral Transformer": "https://github.com/mistralai/mistral-src",
    "Grok-1": "https://github.com/xai-org/grok-1/"
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
            personal_access_token = st.text_input("Enter your [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with 'Read access to issues and metadata' permissions:", type="password")

            selected_website = st.selectbox("Select a GitHub repo:", options=list(websites.keys()))
            
            website_uri = st.text_input("Or enter your own public GitHub repo URL:", key='website_uri')
            
            uri = website_uri if website_uri else websites[selected_website]

            owner, name = helpers.parse_uri(uri)

            submit_data = st.form_submit_button("Submit")

            if submit_data and owner and name and personal_access_token and st.session_state['token']:        
                helpers.run_async_task(feed.handle_feed, owner, name, personal_access_token)

                st.switch_page("pages/2_Publish.py")

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
                        name=f"{owner}: {name}",
                        type=FeedTypes.ISSUE,
                        issue=IssueFeedPropertiesInput(
                            type=FeedServiceTypes.GIT_HUB_ISSUES,
                            github=GitHubIssuesFeedPropertiesInput(
                                repositoryOwner="{owner}",
                                repositoryName="{name}",
                                personalAccessToken="{token}",
                            ),
                            readLimit=10
                        )

                    response = await graphlit.client.create_feed(input)

                    """)
