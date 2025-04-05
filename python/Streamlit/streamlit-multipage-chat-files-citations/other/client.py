import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def ingest_file(name, mime_type, data):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.ingest_encoded_file(name, data, mime_type, is_synchronous=True, workflow=EntityReferenceInput(id=st.session_state['workflow_id']))
        
        st.session_state['content_id'] = response.ingest_encoded_file.id
    except GraphQLClientError as e:
        return str(e)

    return None

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

async def create_specification():
    input = SpecificationInput(
        name="Completion",
        type=SpecificationTypes.COMPLETION,
        serviceType=ModelServiceTypes.ANTHROPIC,
        searchType=SearchTypes.VECTOR,
        anthropic=AnthropicModelPropertiesInput(
            model=AnthropicModels.CLAUDE_3_HAIKU,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
        ),
        strategy=ConversationStrategyInput(
            embedCitations=True
        ),
        promptStrategy=PromptStrategyInput(
            type=PromptStrategyTypes.OPTIMIZE_SEARCH
        ),
        retrievalStrategy=RetrievalStrategyInput(
            type=RetrievalStrategyTypes.SECTION
        ),
        rerankingStrategy=RerankingStrategyInput(
            serviceType=RerankingModelServiceTypes.COHERE
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

    _ = await graphlit.client.delete_specification(st.session_state['specification_id'])

    st.session_state['specification_id'] = None

async def create_conversation():
    input = ConversationInput(
        name="Conversation",
        specification=EntityReferenceInput(
            id=st.session_state['specification_id']
        )
    )

    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.create_conversation(input)

        st.session_state['conversation_id'] = response.create_conversation.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def delete_conversation():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_conversation(st.session_state['conversation_id'])

    st.session_state['conversation_id'] = None

async def prompt_conversation(prompt):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.prompt_conversation(prompt, st.session_state['conversation_id'])
        
        message = response.prompt_conversation.message.message
        citations = response.prompt_conversation.message.citations

        return message, citations, None
    except GraphQLClientError as e:
        return None, None, str(e)
    