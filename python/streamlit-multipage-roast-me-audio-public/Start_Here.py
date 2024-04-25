import streamlit as st
from other import helpers
from components import upload, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit import Graphlit

st.set_page_config(
    page_title="Roast me, by Graphlit",
    page_icon="💡",
    layout="wide"
)

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.secrets['organization_id'] is not None:
    st.session_state['organization_id'] = st.secrets['organization_id']
if st.secrets['environment_id'] is not None:
    st.session_state['environment_id'] = st.secrets['environment_id']
if st.secrets['organization_id'] is not None:
    st.session_state['jwt_secret'] = st.secrets['jwt_secret']

if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:    
    # Initialize Graphlit client
    graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

    st.session_state['graphlit'] = graphlit
    st.session_state['token'] = graphlit.token

if st.session_state['token'] is not None:
    col1, col2 = st.columns(2)

    with col1:
        file_types, file_types_table, extra_info = helpers.select_file_types("Images")

        with st.form("data_content_form"):
            uploaded_file = st.file_uploader("Upload file", type=file_types, accept_multiple_files=False, label_visibility="collapsed")

            if file_types_table:
                helpers.show_file_type_table(file_types_table)
                
                if extra_info:
                    st.write("")
                    st.info(extra_info)

            submit_content = st.form_submit_button("Upload")

            if submit_content and uploaded_file and st.session_state['token']:            
                helpers.run_async_task(upload.handle_upload, uploaded_file)

                st.switch_page("pages/1_Roast_Me.py")

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
                overflow-x: auto;
                width: 100%;
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
