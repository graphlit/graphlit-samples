import streamlit as st
from typing import Optional
from graphlit import Graphlit
from graphlit_api import *

async def publish_text(description, voice):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.publish_text(
            description, 
            connector=ContentPublishingConnectorInput(
                type=ContentPublishingServiceTypes.ELEVEN_LABS_AUDIO, 
                format=ContentPublishingFormats.MP3, 
                elevenLabs=ElevenLabsPublishingPropertiesInput(model=ElevenLabsModels.ENGLISH_V1,voice=voice)
                ), 
            is_synchronous=True)
        
        return response.publish_text, None
    except GraphQLClientError as e:
        return None, str(e)
    
async def ingest_file(name, mime_type, data):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.ingest_encoded_file(name, data, mime_type, is_synchronous=True, workflow=EntityReferenceInput(id=st.session_state['workflow_id']))
        
        st.session_state['content_id'] = response.ingest_encoded_file.id
    except GraphQLClientError as e:
        return str(e)

    return None

async def get_content(id):
    graphlit: Optional[Graphlit] = st.session_state['graphlit']

    try:
        response = await graphlit.client.get_content(id)
        
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
    instructions = "Roast me. Really roast me.  Do your worst as if you were responding on Reddit r/roastme. Speak in the second person, if there a person pictured in the image. For any inappropriate, pornographic or NFSW images, say you cannot roast the image."

    input = WorkflowInput(
        name="OpenAI Image Analysis",
        extraction=ExtractionWorkflowStageInput(
            jobs=[
                ExtractionWorkflowJobInput(
                    connector=EntityExtractionConnectorInput(
                        type=EntityExtractionServiceTypes.OPEN_AI_IMAGE,
                        openAIImage=OpenAIImageExtractionPropertiesInput(
                            customInstructions=instructions
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
