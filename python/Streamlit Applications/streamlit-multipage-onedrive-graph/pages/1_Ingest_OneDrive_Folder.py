import streamlit as st
from other import helpers
from components import feed, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['refresh_token'] and st.session_state['token']:
            if st.session_state["onedrive_folder_done"] is False:
                with st.spinner("Loading OneDrive folders..."):
                    helpers.run_async_task(feed.handle_onedrive_folders)

            if st.session_state["onedrive_folder_done"]:
                folder_name = st.session_state["onedrive_folder_name"]

                st.info(f"Using OneDrive folder [{folder_name}]")

                with st.form("data_feed_form"):
                    colA, colB = st.columns(2)

                    with colA:    
                        submit_content = st.form_submit_button("Create OneDrive Feed",type="primary")
                    with colB:
                        reset_content = st.form_submit_button("Reset",type="secondary")

                    if submit_content:
                        helpers.run_async_task(feed.handle_onedrive_feed)

                        st.switch_page("pages/2_Visualize_Knowledge_Graph.py")

                    if reset_content:
                        st.session_state["onedrive_folder_done"] = False

                        st.rerun()

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

                    input = FeedInput(
                        name=f"OneDrive: {folder-id}",
                        type=FeedTypes.SITE,
                        site=SiteFeedPropertiesInput(
                            type=FeedServiceTypes.ONE_DRIVE,
                            oneDrive=OneDriveFeedPropertiesInput(
                                refreshToken="{refresh-token}",
                                folderId="{folder-id}"
                            )
                        ),
                        workflow=EntityReferenceInput(
                            id="{workflow-id}"
                        ),
                        schedulePolicy=FeedSchedulePolicyInput(
                            recurrenceType=TimedPolicyRecurrenceTypes.REPEAT,
                            repeatInterval="PT1M"
                        )
                    )

                    response = await graphlit.client.create_feed(input)
                    
                    """)
