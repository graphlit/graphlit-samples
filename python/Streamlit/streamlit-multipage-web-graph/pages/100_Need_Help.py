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
        st.markdown("If you run into any problems, you can delete your data to start over.  Be aware, this deletes *all* the data in your project.")

        submit_reset = st.form_submit_button("Reset project")

        if submit_reset:
            session_state.clear_session_state()
            
            with st.spinner('Deleting workflows... Please wait.'):             
                helpers.run_async_task(client.delete_all_workflows)

            with st.spinner('Deleting conversations... Please wait.'):             
                helpers.run_async_task(client.delete_all_conversations)

            with st.spinner('Deleting specifications... Please wait.'):             
                helpers.run_async_task(client.delete_all_specifications)

            with st.spinner('Deleting feeds... Please wait.'):  
                helpers.run_async_task(client.delete_all_feeds)
                
            with st.spinner('Deleting contents... Please wait.'):             
                helpers.run_async_task(client.delete_all_contents)

            with st.spinner('Deleting observables... Please wait.'):             
                helpers.run_async_task(client.delete_all_observables)
