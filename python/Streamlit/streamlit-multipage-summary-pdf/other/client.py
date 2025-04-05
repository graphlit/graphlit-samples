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

async def delete_content(id):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_content(id)

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

    try:
        _ = await graphlit.client.delete_workflow(st.session_state['workflow_id'])

        st.session_state['workflow_id'] = None
    except GraphQLClientError as e:
        return str(e)

    return None

async def create_specification():
    input = SpecificationInput(
        name="Summarization",
        type=SpecificationTypes.COMPLETION,
        serviceType=ModelServiceTypes.ANTHROPIC,
        searchType=SearchTypes.VECTOR,
        anthropic=AnthropicModelPropertiesInput(
            model=AnthropicModels.CLAUDE_3_HAIKU,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
        )
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

    try:
        _ = await graphlit.client.delete_specification(st.session_state['specification_id'])

        st.session_state['specification_id'] = None
    except GraphQLClientError as e:
        return str(e)

    return None

async def summarize_contents(summarization_type: Optional[SummarizationTypes], summarization_prompt):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.summarize_contents(
            filter=ContentFilter(
                id=st.session_state['content_id']
            ),
            summarizations=[
                SummarizationStrategyInput(
                    type=summarization_type,
                    prompt=summarization_prompt,
                    specification=EntityReferenceInput(
                        id=st.session_state["specification_id"]
                    )
                )
            ]
        )

        if response.summarize_contents is None or response.summarize_contents.count == 0:
            return "No summary generated.", None

        return "\n\n".join(item.text for content in response.summarize_contents for item in content.items), None
    except GraphQLClientError as e:
        return None, str(e)

