import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        with st.form("data_feed_form"):    
            account_name = st.text_input("Enter your Azure storage account name", key='account_name')
            container_name = st.text_input("Enter your Azure blob container name", key='container_name')
            storage_key = st.text_input("Enter your Azure storage access key", key='storage_key', type="password")
            prefix = st.text_input("Optionally, enter the relative path within the Azure blob container", key='prefix')

            submit_content = st.form_submit_button("Submit")

            if submit_content and account_name and container_name and storage_key and st.session_state['token']:
                st.session_state.messages = []

                helpers.run_async_task(feed.handle_feed, account_name, container_name, storage_key, prefix)

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
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    # NOTE: Using `workflow-id` for text extraction.
                                        
                    input = FeedInput(
                        name=f"{account_name}: {container_name}",
                        type=FeedTypes.SITE,
                        site=SiteFeedPropertiesInput(
                            type=FeedServiceTypes.AZURE_BLOB,
                            isRecursive=False,
                            azureBlob=AzureBlobFeedPropertiesInput(
                                accountName="{account_name}",
                                containerName="{container_name}",
                                storageAccessKey="{storage_key}",
                                prefix=prefix
                            )
                        ),
                        workflow=EntityReferenceInput(
                            id="{workflow-id}"
                        )
                    )

                    response = await graphlit.client.create_feed(input)

                    """)
