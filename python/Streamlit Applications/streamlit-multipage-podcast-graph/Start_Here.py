import streamlit as st
from components import header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit import Graphlit

st.set_page_config(
    page_title="Graphlit Demo Application",
    page_icon="💡",
    layout="wide"
)

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

col1, col2 = st.columns(2)

with col1:
    with st.form("credentials_form"):
        st.markdown("### 💡 Start here:")

        st.info("Locate connection information for your project in the [Graphlit Developer Portal](https://portal.graphlit.dev/)")

        st.text_input("Organization ID", value=st.session_state['organization_id'], key="organization_id", type="password")
        st.text_input("Preview Environment ID", value=st.session_state['environment_id'], key="environment_id", type="password")
        st.text_input("Secret", value=st.session_state['jwt_secret'], key="jwt_secret", type="password")

        submit_credentials = st.form_submit_button("Generate Token")

        if submit_credentials:
            if st.session_state['jwt_secret'] and st.session_state['environment_id'] and st.session_state['organization_id']:
                # Initialize Graphlit client
                graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

                st.session_state['graphlit'] = graphlit
                st.session_state['token'] = graphlit.token

                st.switch_page("pages/1_Ingest_Podcast_RSS.py")
            else:
                st.error("Please fill in all the connection information.")

            st.markdown("**Python SDK code example:**")

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

                graphlit = Graphlit(
                    organization_id="{organization-id}", 
                    environment_id="{environment-id}", 
                    jwt_secret="{jwt-secret}"
                )

                """)
