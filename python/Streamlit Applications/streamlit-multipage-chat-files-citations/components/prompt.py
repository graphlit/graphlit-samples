import streamlit as st
from other import client

async def handle_prompt(prompt):
    if st.session_state['specification_id'] is None:
        error_message = await client.create_specification()

        if error_message is not None:
            st.error(f"Failed to create specification. {error_message}")
            return

    if st.session_state['conversation_id'] is None:
        error_message = await client.create_conversation()

        if error_message is not None:
            st.error(f"Failed to create conversation. {error_message}")
            return

    message, citations, error_message = await client.prompt_conversation(prompt)

    return message, citations, error_message
