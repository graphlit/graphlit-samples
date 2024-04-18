import streamlit as st
import asyncio
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
        if st.session_state['feed_done'] == True:
            if st.session_state['token']:
                content_facets, error_message = helpers.run_async_task(client.query_contents_facets)

                if error_message is not None:
                    st.error(error_message)
                else:
                    if content_facets is not None:
                        st.header('Topics observed in website:')
                    
                        helpers.render_observable_facet_chart(content_facets)
                    else:
                        st.error('No topics observed in website.')
        else:
            st.info("Please ingest a website to extract topics.")   

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

                    # NOTE: Filtering uploaded content by `feed-id`.
                                        
                    response = await graphlit.client.query_content_facets(
                        filter=ContentFilter(
                            offset=0,
                            limit=0,
                            feeds=[
                                EntityReferenceFilter(
                                    id="{feed-id}"
                                )
                            ]
                        ), 
                        facets=[
                            ContentFacetInput(
                                facet=ContentFacetTypes.OBSERVABLE
                            )
                        ]
                    )

                    """)
