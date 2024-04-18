import streamlit as st
from other import helpers
from components import summarize, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['feed_done'] == True:
            with st.form("summarize_data_form"):
                submit_summarization = st.form_submit_button("Generate Chapters")

                if submit_summarization:
                    helpers.run_async_task(summarize.handle_summarize)
        else:
            st.info("Please ingest a video to generate chapters.")   

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
                                        
                    response = await graphlit.client.summarize_contents(
                        filter=ContentFilter(
                            types=[ContentTypes.FILE],
                            feeds=[
                                EntityReferenceFilter(
                                    id="{feed-id}"
                                )
                            ]
                        ),
                        summarizations=[
                            SummarizationStrategyInput(
                                type=SummarizationTypes.CHAPTERS,
                                specification=EntityReferenceInput(
                                    id="{specification-id}"
                                )
                            )
                        ]
                    )

                    """)
