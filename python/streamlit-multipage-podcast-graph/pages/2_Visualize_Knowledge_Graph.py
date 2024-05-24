import streamlit as st
from other import client, helpers, graph_helpers
from components import header, sidebar, session_state
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()
header.create_header()

if st.session_state['token'] is None:
    st.info("💡 To get started, generate a token to connect to your Graphlit project.")
else:
    if st.session_state['token']:
        st.write("Visualize ingested content and extracted entities.")
        st.warning("Refresh knowledge graph, if none shown, as podcast episodes is ingested in the background.")

        contents_graph = None
        error_message = None

        with st.spinner("Loading knowledge graph..."):
            contents_graph, error_message = helpers.run_async_task(client.query_contents_graph, None)

        if error_message is not None:
            st.error(error_message)
        else:
            if contents_graph is not None:
                st.header('Knowledge graph:')
                                
                g = graph_helpers.create_pyvis_contents_graph(contents_graph)

                graph_helpers.display_pyvis_graph(g)
            else:
                st.error('No knowledge graph was created.')

        with st.form("data_graph_form"):
            refresh_graph = st.form_submit_button("Refresh the Knowledge Graph")

            if refresh_graph:
                st.rerun()

        with st.form("data_search_form"):
            submit_content = st.form_submit_button("Chat with the Knowledge Graph  >")

            if submit_content:
                st.switch_page("pages/3_Chat_With_Knowledge_Graph.py")
