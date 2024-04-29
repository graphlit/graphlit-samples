import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def create_feed(account_name, container_name, storage_key, prefix):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    input = FeedInput(
        name=f"{account_name}: {container_name}",
        type=FeedTypes.SITE,
        site=SiteFeedPropertiesInput(
            type=FeedServiceTypes.AZURE_BLOB,
            isRecursive=False,
            azureBlob=AzureBlobFeedPropertiesInput(
                accountName=account_name,
                containerName=container_name,
                storageAccessKey=storage_key,
                prefix=prefix
            )
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
        serviceType=ModelServiceTypes.OPEN_AI,
        searchType=SearchTypes.VECTOR,
        openAI=OpenAIModelPropertiesInput(
            model=OpenAIModels.GPT4_TURBO_128K,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
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
        ),
        filter=ContentCriteriaInput(
            feeds=[
                EntityReferenceInput(  
                id=st.session_state['feed_id']
                )
            ]
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

        return message, None
    except GraphQLClientError as e:
        return None, str(e)