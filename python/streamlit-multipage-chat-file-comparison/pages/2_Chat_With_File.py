import streamlit as st
from other import helpers
from components import prompt, header, sidebar, session_state
#from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")
else:
    if st.session_state['content_done'] == True:
        if "cohere_messages" not in st.session_state:
            st.session_state.cohere_messages = []

        if "anthropic_messages" not in st.session_state:
            st.session_state.anthropic_messages = []

        if "groq_messages" not in st.session_state:
            st.session_state.groq_messages = []

    if user_prompt := st.chat_input("Ask me anything about your content.", key="chat_input"):
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.session_state['content_done'] == True:
                with st.container(border=True):
                    st.subheader('Cohere Command R')

                # render previous messages
                for message in st.session_state.cohere_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                st.session_state.cohere_messages.append({"role": "user", "content": user_prompt})
                    
                # render user prompt
                with st.chat_message("user"):
                    st.markdown(user_prompt)
                
                message, error_message = helpers.run_async_task(prompt.handle_cohere_prompt, user_prompt)

                if error_message is not None:
                    st.error(f"Failed to prompt conversation. {error_message}")
                else:
                    # prompt conversation
                    with st.chat_message("assistant"):
                        st.session_state.cohere_messages.append({"role": "assistant", "content": message})

                        # render assistant message
                        st.markdown(message)
            else:
                st.info("Please ingest file to chat with.")   

        with col2:
            if st.session_state['content_done'] == True:
                with st.container(border=True):
                    st.subheader('Anthropic Claude 3 Haiku')

                # render previous messages
                for message in st.session_state.anthropic_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                st.session_state.anthropic_messages.append({"role": "user", "content": user_prompt})
                    
                # render user prompt
                with st.chat_message("user"):
                    st.markdown(user_prompt)
                
                message, error_message = helpers.run_async_task(prompt.handle_anthropic_prompt, user_prompt)

                if error_message is not None:
                    st.error(f"Failed to prompt conversation. {error_message}")
                else:
                    # prompt conversation
                    with st.chat_message("assistant"):
                        st.session_state.anthropic_messages.append({"role": "assistant", "content": message})

                        # render assistant message
                        st.markdown(message)
            else:
                st.info("Please ingest file to chat with.")   

        with col3:
            if st.session_state['content_done'] == True:
                with st.container(border=True):
                    st.subheader('Groq LLaMA 3 70b')

                # render previous messages
                for message in st.session_state.groq_messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

                st.session_state.groq_messages.append({"role": "user", "content": user_prompt})
                    
                # render user prompt
                with st.chat_message("user"):
                    st.markdown(user_prompt)
                
                message, error_message = helpers.run_async_task(prompt.handle_groq_prompt, user_prompt)

                if error_message is not None:
                    st.error(f"Failed to prompt conversation. {error_message}")
                else:
                    # prompt conversation
                    with st.chat_message("assistant"):
                        st.session_state.groq_messages.append({"role": "assistant", "content": message})

                        # render assistant message
                        st.markdown(message)
            else:
                st.info("Please ingest file to chat with.")   
