import streamlit as st
from other import helpers, client
from components import publish, header, sidebar, session_state
from streamlit_extras.stylable_container import stylable_container
from graphlit_api import *

session_state.reset_session_state()
sidebar.create_sidebar()

if st.session_state['token'] is not None:
    col1, col2 = st.columns(2)

    with col1:
        if st.session_state['content_done'] == True:
            content, error_message = helpers.run_async_task(client.get_content, st.session_state['content_id'])

            if error_message is not None:
                st.error(f"Failed to get content. {error_message}")
            else:
                description = content.image.description if content.image is not None else None

                if description is not None:
                    st.subheader("🔥 Roasted...")
                    st.image(image=content.image_uri, width=300)

                    voice = "QcmL8QAZyYRbd7cWpsdB" # Chloe

                    with st.spinner('Publishing audio of your roast with [ElevenLabs](https://elevenlabs.io)... Please wait.'):
                        branded_description = "You've been roasted by Graphlit. Visit us at graphlit.com to build apps like this yourself.  " + description + "  Hope you enjoyed your roast.  Try out Graphlit for free today."

                        audio_content, error_message = helpers.run_async_task(publish.handle_publish, branded_description, voice)

                        if error_message is not None:
                            st.error(f"Failed to publish audio. {error_message}")
                        else:
                            # REVIEW: get content after publishing, so audio URI is valid
                            audio_content, error_message = helpers.run_async_task(client.get_content, audio_content.id)

                            if error_message is not None:
                                st.error(f"Failed to get content. {error_message}")
                            else:       
                                st.markdown(f"**Listen to your roast:**")                       
                                st.audio(data=audio_content.audio_uri,format="audio/mp3")

                                st.markdown(f"[Download]({audio_content.audio_uri}) and share on social media!")

                    st.markdown("**Your roast:**")                       
                    st.markdown(description)
                else:
                    st.error(f"Failed to generate image description.")
        else:
            st.info("Please ingest image to roast.")

    with col2:
        st.markdown("**Python SDK code example:**")
        
        with stylable_container(
            "codeblock",
            """
            code {
                white-space: pre-wrap !important;
                overflow-x: auto;
                width: 100%;
            }
            """,
        ):
            st.code(language="python", body="""
                    from graphlit import Graphlit
                    from graphlit_api import *

                    description = "{image-description}"
                    voice = "{elevenlabs-voice-id}"

                    response = await graphlit.client.publish_text(
                        description, 
                        connector=ContentPublishingConnectorInput(
                            type=ContentPublishingServiceTypes.ELEVEN_LABS_AUDIO, 
                            format=ContentPublishingFormats.MP3, 
                            elevenLabs=ElevenLabsPublishingPropertiesInput(
                                model=ElevenLabsModels.ENGLISH_V1,
                                voice=voice
                            )
                        ), 
                        is_synchronous=True)
        
                    """)
