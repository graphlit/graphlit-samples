import streamlit as st
from msal import ConfidentialClientApplication
from components import header, sidebar, session_state
from other import helpers
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

SCOPES = ["User.Read", "Files.Read.All"]

redirect_uri = st.secrets["default"]["redirect_uri"]

if not st.session_state['app']:
    app = ConfidentialClientApplication(
        st.secrets["default"]["client_id"],
        authority=f'https://login.microsoftonline.com/common',
        client_credential=st.secrets["default"]["client_secret"]
    )

    st.session_state['app'] = app

if st.query_params and 'code' in st.query_params:
    app = st.session_state['app']

    code = st.query_params['code']
    
    if st.session_state.refresh_token is None:
        result = app.acquire_token_by_authorization_code(
            code,
            SCOPES,
            redirect_uri=redirect_uri
        )

        if 'access_token' in result:
            st.session_state.refresh_token = result['refresh_token']
        else:
            st.error("Failed to get access token.")

col1, col2 = st.columns(2)

with col1:
    if not st.session_state.refresh_token:
        st.subheader("Please login...")
        st.markdown(f"<a href='{helpers.get_sign_in_url(app, SCOPES, redirect_uri)}' target=_blank>Login with your Microsoft account</a>", unsafe_allow_html=True)

        st.info("Authenticate to access your Microsoft SharePoint account. It will open a new tab where you can continue using the application.")
    else:
        if st.session_state['jwt_secret'] is None and st.session_state['environment_id'] is None and st.session_state['organization_id'] is None:
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

                        st.switch_page("pages/1_Ingest_SharePoint_Folder.py")
                    else:
                        st.error("Please fill in all the connection information.")
        else:
            # Initialize Graphlit client
            graphlit = Graphlit(organization_id=st.session_state['organization_id'], environment_id=st.session_state['environment_id'], jwt_secret=st.session_state['jwt_secret'])

            st.session_state['graphlit'] = graphlit
            st.session_state['token'] = graphlit.token

            st.switch_page("pages/1_Ingest_SharePoint_Folder.py")

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

                graphlit = Graphlit(
                    organization_id="{organization-id}", 
                    environment_id="{environment-id}", 
                    jwt_secret="{jwt-secret}"
                )

                """)
