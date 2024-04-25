import streamlit as st
from other import helpers
from components import upload, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

# A dictionary mapping PDF names to their PDF URIs
pdfs = {
    "Attention is all you need": "https://graphlitplatform.blob.core.windows.net/samples/Attention%20Is%20All%20You%20Need.1706.03762.pdf",
    "Unifying Large Language Models and Knowledge Graphs: A Roadmap": "https://graphlitplatform.blob.core.windows.net/samples/Unifying%20Large%20Language%20Models%20and%20Knowledge%20Graphs%20A%20Roadmap-2306.08302.pdf",
    "Microsoft 10Q (March 2024)": "https://graphlitplatform.blob.core.windows.net/samples/MSFT_FY24Q1_10Q.docx",
    "Uber 10Q (March 2022)": "https://graphlitplatform.blob.core.windows.net/samples/uber_10q_march_2022.pdf",
}

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("data_content_form"):
            selected_pdf = st.selectbox("Select a PDF:", options=list(pdfs.keys()))
            
            document_uri = st.text_input("Or enter your own URL to a file (i.e. PDF, DOCX, PPTX):", key='pdf_uri')

            uri = document_uri if document_uri else pdfs[selected_pdf]

            submit_content = st.form_submit_button("Submit")

            if submit_content and uri and st.session_state['token']:
                # Reset chat messages
                st.session_state.messages = []
            
                helpers.run_async_task(upload.handle_upload, uri)            

                st.switch_page("pages/2_Chat_With_File.py")

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
                overflow-x: auto;
                width: 100%;
                font-size: 12px;
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    # NOTE: Ingest file by URI, synchronously.
                    # Using `workflow-id` for text extraction.
                                        
                    response = await graphlit.client.ingest_uri(
                        uri="{uri}", 
                        is_synchronous=True, 
                        workflow=EntityReferenceInput(
                            id="{workflow-id}"
                        )
                    )

                    """)
