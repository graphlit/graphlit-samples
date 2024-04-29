import streamlit as st
import json
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
    st.session_state['content_done'] = None

async def delete_all_contents():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_contents()

    st.session_state['content_id'] = None
    st.session_state['content_done'] = None

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

async def create_specification(name, schema):
    input = SpecificationInput(
        name="Extraction",
        type=SpecificationTypes.EXTRACTION,
        serviceType=ModelServiceTypes.OPEN_AI,
        searchType=SearchTypes.VECTOR,
        openAI=OpenAIModelPropertiesInput(
            model=OpenAIModels.GPT4_TURBO_128K,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
        ),
        tools=[
            ToolDefinitionInput(
                name=name,
                schema=schema
            )
        ]
    )

    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.create_specification(input)

        st.session_state['specification_id'] = response.create_specification.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def delete_specification():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_specification(st.session_state['specification_id'])

    st.session_state['specification_id'] = None

async def extract_contents():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.extract_contents(
            prompt="Extract data from text into JSON, using the tool provided. If no appropriate data is found, don't return any response.",
            specification=EntityReferenceInput(
                id=st.session_state["specification_id"]
            ),
            filter=ContentFilter(
                id=st.session_state['content_id']
            ),
        )

        if response.extract_contents is None:
            return None, None
        
        deserialized_values = []  # Initialize the list here

        for item in response.extract_contents:
            deserialized = json.loads(item.value)
            deserialized['pageNumber'] = item.page_number
            deserialized_values.append(deserialized)

        sorted_deserialized_values = sorted(deserialized_values, key=lambda x: x['pageNumber'])

        for item in sorted_deserialized_values:
            item.pop('pageNumber', None)
    
        return sorted_deserialized_values, None
    except GraphQLClientError as e:
        return None, str(e)
