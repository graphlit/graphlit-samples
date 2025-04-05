import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def ingest_file(name, mime_type, data):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.ingest_encoded_file(
            name,
            data, 
            mime_type, 
            is_synchronous=False, # NOTE: not waiting for entity extraction workflow
            workflow=EntityReferenceInput(
                id=st.session_state['workflow_id']
            )
        )
        
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
        name="Workflow",
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
                        type=EntityExtractionServiceTypes.MODEL_TEXT,
                        extractedCount=1000
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
        name="Specification",
        type=SpecificationTypes.COMPLETION,
        serviceType=ModelServiceTypes.OPEN_AI,
        searchType=SearchTypes.VECTOR,
        openAI=OpenAIModelPropertiesInput(
            model=OpenAIModels.GPT4O_128K,
            temperature=0.1,
            probability=0.2,
            completionTokenLimit=2048,
        ),
        graphStrategy=GraphStrategyInput(
            type=GraphStrategyTypes.EXTRACT_ENTITIES_GRAPH,
            generateGraph=True
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

async def clear_conversation():
    if st.session_state['conversation_id'] is None:
        return
    
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.clear_conversation(st.session_state['conversation_id'])

async def delete_conversation():
    if st.session_state['conversation_id'] is None:
        return

    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_conversation(st.session_state['conversation_id'])

    st.session_state['conversation_id'] = None

async def prompt_conversation(prompt):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.prompt_conversation(prompt, st.session_state['conversation_id'])
        
        message = response.prompt_conversation.message.message
        graph = response.prompt_conversation.graph

        return message, graph, None
    except GraphQLClientError as e:
        return None, None, str(e)

async def query_contents_graph(search):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.query_contents_graph(
            filter=ContentFilter(
                search=search,
                searchType=SearchTypes.VECTOR
            ),
            # NOTE: required, to return the graph, even if no observable filtering
            graph=ContentGraphInput(                
            )
        )

        return response.contents.graph, None
    except GraphQLClientError as e:
        return None, str(e)

async def delete_all_feeds():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_feeds(is_synchronous=True)

async def delete_all_contents():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_contents(is_synchronous=True)

async def delete_all_workflows():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_workflows(is_synchronous=True)

async def delete_all_specifications():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_specifications(is_synchronous=True)

async def delete_all_conversations():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_conversations(is_synchronous=True)

async def delete_all_observables():
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    _ = await graphlit.client.delete_all_persons()
    _ = await graphlit.client.delete_all_organizations()
    _ = await graphlit.client.delete_all_places()
    _ = await graphlit.client.delete_all_events()
    _ = await graphlit.client.delete_all_products()
    _ = await graphlit.client.delete_all_softwares()
    _ = await graphlit.client.delete_all_repos()
    _ = await graphlit.client.delete_all_labels()
    _ = await graphlit.client.delete_all_categories()
