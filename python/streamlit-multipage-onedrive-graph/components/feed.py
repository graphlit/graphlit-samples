import streamlit as st
from datetime import datetime
import time
from other import client

async def handle_onedrive_folders():
    folders, error = await client.query_onedrive_folders()

    if error is not None:
        st.error(error)

        st.session_state["onedrive_folder_done"] = False
        return
   
    options = {folder.folder_name: folder.folder_id for folder in folders}

    keys = list(options.keys())

    selected_key = st.selectbox(f'Select a OneDrive folder:', keys, placeholder="Choose a folder", index=None, key="onedrive_folders")

    if selected_key is not None:
        selected_value = options[selected_key]

        if selected_value:
            st.info(f"Selected folder [{selected_key}]: [{selected_value}]")

            st.session_state["onedrive_folder_name"] = selected_key
            st.session_state["onedrive_folder_id"] = selected_value
            st.session_state["onedrive_folder_done"] = True

            st.rerun()
        else:
            st.session_state["onedrive_folder_done"] = False

async def handle_onedrive_feed():
    if st.session_state['workflow_id'] is None:
        error_message = await client.create_workflow()

        if error_message is not None:
            st.error(f"Failed to create workflow. {error_message}")
            return

    if st.session_state['feed_id'] is not None:
        with st.spinner('Deleting existing feed... Please wait.'):
            await client.delete_feed()
        st.session_state["feed_id"] = None

    error_message = await client.create_feed(st.session_state["onedrive_folder_id"])

    if error_message is not None:
        st.error(error_message)
    else:
        st.session_state['feed_done'] = True