import streamlit as st
from other import client

async def handle_anthropic_prompt(prompt):
    if st.session_state['anthropic_specification_id'] is None:
        error_message = await client.create_anthropic_specification()

        if error_message is not None:
            st.error(f"Failed to create Anthropic specification. {error_message}")
            return

    if st.session_state['anthropic_conversation_id'] is None:
        error_message = await client.create_anthropic_conversation()

        if error_message is not None:
            st.error(f"Failed to create Anthropic conversation. {error_message}")
            return

    message, error_message = await client.prompt_anthropic_conversation(prompt)

    return message, error_message

async def handle_cohere_prompt(prompt):
    if st.session_state['cohere_specification_id'] is None:
        error_message = await client.create_cohere_specification()

        if error_message is not None:
            st.error(f"Failed to create Cohere specification. {error_message}")
            return

    if st.session_state['cohere_conversation_id'] is None:
        error_message = await client.create_cohere_conversation()

        if error_message is not None:
            st.error(f"Failed to create Cohere conversation. {error_message}")
            return

    message, error_message = await client.prompt_cohere_conversation(prompt)

    return message, error_message

async def handle_groq_prompt(prompt):
    if st.session_state['groq_specification_id'] is None:
        error_message = await client.create_groq_specification()

        if error_message is not None:
            st.error(f"Failed to create Groq specification. {error_message}")
            return

    if st.session_state['groq_conversation_id'] is None:
        error_message = await client.create_groq_conversation()

        if error_message is not None:
            st.error(f"Failed to create Groq conversation. {error_message}")
            return

    message, error_message = await client.prompt_groq_conversation(prompt)

    return message, error_message
