import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def ingest_file(uri):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.ingest_uri(uri, is_synchronous=True, workflow=EntityReferenceInput(id=st.session_state['workflow_id']))
        
        st.session_state['content_id'] = response.ingest_uri.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def get_content():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.get_content(st.session_state['content_id'])
        
        return response.content, None
    except GraphQLClientError as e:
        return None, str(e)

async def delete_content():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_content(st.session_state['content_id'])

    st.session_state['content_id'] = None

async def delete_all_contents():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_contents()

async def create_workflow():
    input = WorkflowInput(
        name="Azure AI Document Intelligence",
        preparation=PreparationWorkflowStageInput(
            jobs=[
                PreparationWorkflowJobInput(
                    connector=FilePreparationConnectorInput(
                        type=FilePreparationServiceTypes.AZURE_DOCUMENT_INTELLIGENCE,
                        azureDocument=AzureDocumentPreparationPropertiesInput(
                            model=AzureDocumentIntelligenceModels.LAYOUT
                        )
                    )
                )
            ]
        ),
        extraction=ExtractionWorkflowStageInput(
            jobs=[
                ExtractionWorkflowJobInput(
                    connector=EntityExtractionConnectorInput(
                        type=EntityExtractionServiceTypes.AZURE_COGNITIVE_SERVICES_TEXT,
                        extractedTypes=[
                            ObservableTypes.PERSON,
                            ObservableTypes.ORGANIZATION
                        ]
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
