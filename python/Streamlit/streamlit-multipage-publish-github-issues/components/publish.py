import streamlit as st
import time
from other import client
from datetime import datetime

async def publish_contents(prompt):
    if st.session_state['specification_id'] is not None:
        with st.spinner('Deleting existing specification... Please wait.'):
            await client.delete_specification()
        st.session_state["specification_id"] = None

    if st.session_state['specification_id'] is None:
        error_message = await client.create_specification()

        if error_message is not None:
            st.error(f"Failed to create specification. {error_message}")
            return

    summary_type = time.time()

    placeholder = st.empty()

    with st.spinner('Publishing GitHub Issues report... Please wait.'):
        summary, error_message = await client.publish_contents(prompt)

        if error_message is not None:
            st.error(error_message)
            return

        if summary is not None:
            placeholder.markdown(summary)
        else:
            st.write("No summary was generated.")

        summary_duration = time.time() - summary_type

        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")

        st.success(f"GitHub Issues report generation took {summary_duration:.2f} seconds. Finished at {formatted_time} UTC.")
