import streamlit as st

def create_header():
    st.header("Get roasted 🔥 by [Graphlit](https://www.graphlit.com)")

    st.markdown("Browse for a picture to upload and be roasted.")
    st.markdown("Written using the Graphlit [Python SDK](https://pypi.org/project/graphlit-client/).  Image analysis uses [OpenAI GPT-4 Turbo 128k Vision](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo).  Audio generation done with [ElevenLabs](https://elevenlabs.io).")
