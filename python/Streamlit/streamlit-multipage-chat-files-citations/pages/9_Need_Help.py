import streamlit as st
from other import client, helpers
from components import header, sidebar, session_state

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    with st.form("clear_data_form"):
        st.markdown("If you run into any problems, or exceeded your Free Tier project quota, you can delete all your contents to start over.  Be aware, this deletes *all* the contents in your project.")

        submit_reset = st.form_submit_button("Reset project")

        if submit_reset:
            with st.spinner('Deleting contents... Please wait.'):  
                helpers.run_async_task(client.delete_all_contents)
