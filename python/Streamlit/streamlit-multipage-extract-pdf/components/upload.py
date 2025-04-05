import streamlit as st
import time
from other import client
from datetime import datetime

async def handle_upload(uri):
    st.session_state['content_done'] = False

    if st.session_state['workflow_id'] is None:
        error_message = await client.create_workflow()

        if error_message is not None:
            st.error(f"Failed to create workflow. {error_message}")
            return

    if st.session_state['content_id'] is not None:
        with st.spinner('Deleting existing content... Please wait.'):
            await client.delete_content()
        st.session_state["content_id"] = None

    start_time = time.time()

    with st.spinner('Ingesting document... Please wait.'):
        error_message = await client.ingest_file(uri)

        if error_message is not None:
            st.error(f"Failed to ingest file [{uri}]. {error_message}")
        else:
            duration = time.time() - start_time

            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")

            st.success(f"Document ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

    st.session_state["content_done"] = True
