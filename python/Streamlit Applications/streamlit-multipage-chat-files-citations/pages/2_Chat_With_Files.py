import streamlit as st
from other import helpers
from components import prompt, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['content_done'] == True:
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
                
                message, citations, error_message = helpers.run_async_task(prompt.handle_prompt, user_prompt)

                if error_message is not None:
                    st.error(f"Failed to prompt conversation. {error_message}")
                else:
                    # prompt conversation
                    with st.chat_message("assistant"):
                        st.session_state.messages.append({"role": "assistant", "content": message})

                        # render assistant message
                        st.markdown(message)

                        # render citations
                        if citations is not None:
                            helpers.render_citations(citations)
        else:
            st.info("Please ingest files to chat with.")   

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
                overflow-x: auto;
                width: 100%;
                font-size: 12px;
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    # NOTE: Using LLM via `specification-id`
                    
                    input = ConversationInput(
                        name="Conversation",
                        specification=EntityReferenceInput(
                            id="{specification-id}"
                        )
                    )

                    response = await graphlit.client.create_conversation(input)

                    """)
