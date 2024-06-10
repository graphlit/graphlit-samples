import streamlit as st
from datetime import datetime
import time
from other import client

async def handle_feed(name):
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

    error_message = await client.create_feed(name)

    if error_message is not None:
        st.error(error_message)
    else:
        start_time = time.time()

        with st.spinner('Ingesting website... Please wait.'):
            done = False
            time.sleep(5)
            while not done:
                done = await client.is_feed_done()

                if not done:
                    time.sleep(2)

        st.session_state["feed_done"] = True

        duration = time.time() - start_time

        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")

        st.success(f"Website ingestion took {duration:.2f} seconds. Finished at {formatted_time} UTC.")

        st.session_state['feed_done'] = True
