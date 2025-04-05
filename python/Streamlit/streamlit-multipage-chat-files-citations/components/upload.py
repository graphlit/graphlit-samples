import streamlit as st
import time
from datetime import datetime
import base64
import os
from other import client

async def handle_upload(uploaded_file):
    st.session_state['content_done'] = False

    if st.session_state['workflow_id'] is None:
        error_message = await client.create_workflow()

        if error_message is not None:
            st.error(f"Failed to create workflow. {error_message}")

    if st.session_state['content_id'] is not None:
        with st.spinner('Deleting existing content... Please wait.'):
            await client.delete_content()
        st.session_state["content_id"] = None

    start_time = time.time()
        
    # Read the file content
    file_content = uploaded_file.getvalue()
    
    base64_content = base64.b64encode(file_content).decode('utf-8')

    file_name = uploaded_file.name

    # Split the file name into the name and extension
    content_name, _ = os.path.splitext(file_name)

    with st.spinner('Ingesting file... Please wait.'):
        error_message = await client.ingest_file(content_name, uploaded_file.type, base64_content)

        if error_message is not None:
            st.error(f"Failed to ingest file. {error_message}")
        else:
            duration = time.time() - start_time

            current_time = datetime.now()
            formatted_time = current_time.strftime("%H:%M:%S")

            st.success(f"File ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

    st.session_state["content_done"] = True
