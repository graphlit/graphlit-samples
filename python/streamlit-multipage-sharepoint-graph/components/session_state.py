import streamlit as st

def reset_session_state():
    # required: global session state
    if 'environment_id' not in st.session_state:
        st.session_state['environment_id'] = None
    if 'organization_id' not in st.session_state:
        st.session_state['organization_id'] = None
    if 'jwt_secret' not in st.session_state:
        st.session_state['jwt_secret'] = None

    if 'graphlit' not in st.session_state:
        st.session_state['graphlit'] = None
    if 'token' not in st.session_state:
        st.session_state['token'] = None

    if 'app' not in st.session_state:
        st.session_state['app'] = None
    if 'refresh_token' not in st.session_state:
        st.session_state['refresh_token'] = None

    # app-specific session state
    if 'workflow_id' not in st.session_state:
        st.session_state['workflow_id'] = None
    if 'feed_id' not in st.session_state:
        st.session_state['feed_id'] = None
    if 'feed_done' not in st.session_state:
        st.session_state['feed_done'] = None    
    if 'specification_id' not in st.session_state:
        st.session_state['specification_id'] = None
    if 'conversation_id' not in st.session_state:
        st.session_state['conversation_id'] = None

    if 'sharepoint_account_name' not in st.session_state:
        st.session_state['sharepoint_account_name'] = None
    if 'sharepoint_library_name' not in st.session_state:
        st.session_state['sharepoint_library_name'] = None
    if 'sharepoint_library_id' not in st.session_state:
        st.session_state['sharepoint_library_id'] = None
    if 'sharepoint_library_done' not in st.session_state:
        st.session_state['sharepoint_library_done'] = False
    if 'sharepoint_folder_name' not in st.session_state:
        st.session_state['sharepoint_folder_name'] = None
    if 'sharepoint_folder_id' not in st.session_state:
        st.session_state['sharepoint_folder_id'] = None
    if 'sharepoint_folder_done' not in st.session_state:
        st.session_state['sharepoint_folder_done'] = False

def clear_session_state():
    # app-specific session state
    st.session_state['workflow_id'] = None
    st.session_state['specification_id'] = None
    st.session_state['conversation_id'] = None

    st.session_state['sharepoint_account_name'] = None
    st.session_state['sharepoint_library_name'] = None
    st.session_state['sharepoint_library_id'] = None
    st.session_state['sharepoint_library_done'] = False
    st.session_state['sharepoint_folder_name'] = None
    st.session_state['sharepoint_folder_id'] = None
    st.session_state['sharepoint_folder_done'] = False
