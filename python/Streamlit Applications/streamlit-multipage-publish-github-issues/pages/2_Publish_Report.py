import streamlit as st
from other import helpers
from components import publish, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

default_prompt = "Write me a report of recurring themes across all GitHub issues, which can be used to group issues into workstreams.  For each theme, provide an example of issues which fall into this theme."

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['feed_done'] == True:
            with st.form("publish_data_form"):
                prompt = st.text_area("Enter a prompt to generate a report about recent GitHub issues:", key='prompt', value=default_prompt)

                submit_data = st.form_submit_button("Submit")

                if submit_data and prompt:
                    helpers.run_async_task(publish.publish_contents, prompt)
        else:
            st.info("Please ingest a GitHub repo to generate your report.")   

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

                    # NOTE: Filtering uploaded content by `feed-id`.
                    # Using specification by `specification-id`
                                        
                    response = await graphlit.client.publish_contents(
                        connector=ContentPublishingConnectorInput(
                            type=ContentPublishingServiceTypes.TEXT,
                            format=ContentPublishingFormats.MARKDOWN
                        ),
                        publish_prompt="{prompt}",
                        summary_specification=EntityReferenceInput(
                            id="{specification-id}"
                        ),
                        publish_specification=EntityReferenceInput(
                            id="{specification-id}"
                        ),
                        filter=ContentFilter(
                            types=[FeedTypes.ISSUE],
                            feeds=[
                                EntityReferenceFilter(
                                id="{feed-id}"
                                )
                            ]
                        ),
                    )

                    """)
