import streamlit as st
from other import client, helpers
from components import header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token in the side panel to connect to your Graphlit project.")
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['content_done'] == True:
            content, error_message = helpers.run_async_task(client.get_content)

            if error_message is not None:
                st.error(error_message)
            else:
                if content.document.title is not None:
                    st.markdown(f"**Title:** {content.document.title}")

                if content.document.author is not None:
                    st.markdown(f"**Author:** {content.document.author}")

                if content.document.page_count is not None:
                    st.markdown(f"**Page count:** {content.document.page_count}")

                if content.markdown is not None:
                    with st.expander("See document text:", expanded=False):
                        st.markdown(content.markdown)

                if content.observations is not None:
                    st.header('Entities observed in document:')

                    helpers.display_observations_as_chips(content.observations)
        else:
            st.info("Please upload a file to extract.")   

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    response = await graphlit.client.get_content("{content-id}")

                    """)
