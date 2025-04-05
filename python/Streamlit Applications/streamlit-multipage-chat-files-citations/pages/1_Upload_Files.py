import streamlit as st
from other import helpers
from components import upload, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if "table_to_show" not in st.session_state:
            st.session_state["table_to_show"] = "Documents"

        table_to_show = st.radio("Supported file types", ["Documents","Audio","Video","Images","Animations","Data","Emails","Code","Packages","Other"], label_visibility="collapsed", horizontal=True, key="table_to_show")

        file_types, file_types_table, extra_info = helpers.select_file_types(table_to_show)

        with st.form("data_content_form"):
            uploaded_files = st.file_uploader("Upload files", type=file_types, accept_multiple_files=True, label_visibility="collapsed")

            if file_types_table:
                helpers.show_file_type_table(file_types_table)
                
                if extra_info:
                    st.write("")
                    st.info(extra_info)

            submit_content = st.form_submit_button("Upload")

            if submit_content and uploaded_files and st.session_state['token']:
                # Reset chat messages
                st.session_state.messages = []
            
                with st.expander("Uploaded Files", expanded=True):
                    for uploaded_file in uploaded_files:
                        helpers.run_async_task(upload.handle_upload, uploaded_file)

                    st.switch_page("pages/2_Chat_With_Files.py")

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

                    # NOTE: Ingest Base64 encoded file, synchronously.
                    # Using `workflow-id` for text extraction.
                                        
                    response = await graphlit.client.ingest_encoded_file(
                        "{name}", 
                        "{base64-data}", 
                        "{mime_type}", 
                        is_synchronous=True, 
                        workflow=EntityReferenceInput(
                            id="{workflow-id}"
                        )
                    )

                    """)
