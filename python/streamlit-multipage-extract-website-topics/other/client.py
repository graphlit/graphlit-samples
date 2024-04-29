import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def create_feed(uri):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    input = FeedInput(
        name=uri,
        type=FeedTypes.WEB,
        web=WebFeedPropertiesInput(
            uri=uri,
            readLimit=10
        ),
        workflow=EntityReferenceInput(
            id=st.session_state['workflow_id']
        )
    )

    try:
        response = await graphlit.client.create_feed(input)
        
        st.session_state['feed_id'] = response.create_feed.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def delete_feed():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_feed(st.session_state['feed_id'])

    st.session_state['feed_id'] = None
    st.session_state['feed_done'] = None

async def delete_all_feeds():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_feeds()

    st.session_state['feed_id'] = None
    st.session_state['feed_done'] = None

async def is_feed_done():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    response = await graphlit.client.is_feed_done(st.session_state['feed_id'])
    
    return response.is_feed_done.result

async def create_workflow():
    input = WorkflowInput(
        name="Azure Cognitive Services",
        extraction=ExtractionWorkflowStageInput(
            jobs=[
                ExtractionWorkflowJobInput(
                    connector=EntityExtractionConnectorInput(
                        type=EntityExtractionServiceTypes.AZURE_COGNITIVE_SERVICES_TEXT,
                    )
                )
            ]
        )
    )

    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.create_workflow(input)
        
        st.session_state['workflow_id'] = response.create_workflow.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def delete_workflow():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_workflow(st.session_state['workflow_id'])

    st.session_state['workflow_id'] = None

async def query_contents_facets():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.query_content_facets(
            filter=ContentFilter(
                offset=0,
                limit=0,
                feeds=[
                    EntityReferenceFilter(
                        id=st.session_state['feed_id']
                    )
                ]
            ), 
            facets=[
                ContentFacetInput(
                    facet=ContentFacetTypes.OBSERVABLE
                )
            ]
        )

        return response.contents.facets, None
    except GraphQLClientError as e:
        return None, str(e)
    