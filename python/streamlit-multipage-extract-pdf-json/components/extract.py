import streamlit as st
from datetime import datetime
import time
from other import client

async def handle_extract():        
    if st.session_state['specification_id'] is not None:
        with st.spinner('Deleting existing specification... Please wait.'):
            await client.delete_specification()
        st.session_state["specification_id"] = None

    if st.session_state['specification_id'] is None:
        error_message = await client.create_specification("extractJSON", st.session_state["schema"])

        if error_message is not None:
            st.error(f"Failed to create specification. {error_message}")
        else:
            start_time = time.time()

            with st.spinner('Extracting JSON... Please wait.'):
                response, error_message = await client.extract_contents()
            
                if error_message is not None:
                    st.error(f"Failed to extract JSON. {error_message}")
                    return

                if response is not None:
                    st.subheader("Extracted JSON (with page-level extraction):")
                    st.json(response)
                else:
                    st.text("No JSON was extracted.")

                duration = time.time() - start_time

                current_time = datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")

                st.success(f"JSON extraction took {duration:.2f} seconds. Finished at {formatted_time} UTC.")
    