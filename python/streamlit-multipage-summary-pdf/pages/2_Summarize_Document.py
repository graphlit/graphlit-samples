import streamlit as st
from other import helpers
from components import summarize, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

summarizations = {
    "Detailed summary": SummarizationTypes.SUMMARY,
    "Bullet points": SummarizationTypes.BULLETS,
    "Followup questions": SummarizationTypes.QUESTIONS,
    "Social media posts": SummarizationTypes.POSTS,
    "Custom summarization prompt": SummarizationTypes.CUSTOM
}

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['content_done'] == True:
            with st.form("summarize_data_form"):
                selected_summarization = st.selectbox("Select a summary type:", options=list(summarizations.keys()))
                
                summarization_prompt = st.text_area("Or enter your own summarization prompt:", key='summarization_prompt', height=200)

                summarization_type = summarizations[selected_summarization]

                submit_summarization = st.form_submit_button("Summarize")

                if submit_summarization:
                    helpers.run_async_task(summarize.handle_summarize, summarization_type, summarization_prompt)
        else:
            st.info("Please upload a file to summarize.")   

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

                    summarization_prompt = "{summarization-prompt}"
                    summarization_type = SummarizationTypes.SUMMARY

                    # NOTE: Filtering uploaded content by `content-id`.
                    # Using specification by `specification-id`

                    response = await graphlit.client.summarize_contents(
                        filter=ContentFilter(
                            id="{content-id}"
                        ),
                        summarizations=[
                            SummarizationStrategyInput(
                                type=summarization_type,
                                prompt=summarization_prompt,
                                specification=EntityReferenceInput(
                                    id="{specification_id}"
                                )
                            )
                        ]
                    )

                    """)
