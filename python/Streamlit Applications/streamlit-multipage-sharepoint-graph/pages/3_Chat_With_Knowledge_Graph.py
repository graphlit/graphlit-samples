import streamlit as st
from other import helpers, graph_helpers, client
from components import prompt, header, sidebar, session_state
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # render previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask me anything about your content.", key="chat_input"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # render user prompt
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        message, graph, error_message = helpers.run_async_task(prompt.handle_prompt, user_prompt)

        if error_message is not None:
            st.error(f"Failed to prompt conversation. {error_message}")
        else:
            # prompt conversation
            with st.chat_message("assistant"):
                st.session_state.messages.append({"role": "assistant", "content": message})

                # render assistant message
                st.markdown(message)

                # render retrieved graph
                if graph is not None:
                    g = graph_helpers.create_pyvis_conversation_graph(graph)
                    
                    graph_helpers.display_pyvis_graph(g)

    with st.form("data_feed_form"):    
        clear_conversation = st.form_submit_button("Clear RAG conversation")

        if clear_conversation:
            st.session_state.messages = []

            helpers.run_async_task(client.clear_conversation)

            st.rerun()
