import streamlit as st
from datetime import datetime
import time
from other import client

async def handle_feed(uri):
    st.session_state['feed_done'] = False

    if st.session_state['workflow_id'] is None:
        error_message = await client.create_workflow()

        if error_message is not None:
            st.error(f"Failed to create workflow. {error_message}")
            return

    if st.session_state['feed_id'] is not None:
        with st.spinner('Deleting existing feed... Please wait.'):
            await client.delete_feed()
        st.session_state["feed_id"] = None

    start_time = time.time()

    error_message = await client.create_feed(uri)

    if error_message is not None:
        st.error(error_message)
    else:
        st.session_state['feed_done'] = True