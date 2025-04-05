import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Generate chapters of YouTube video. Chapters generated with the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
    st.warning("Ingesting from YouTube can be slow, because of YouTube rate-limiting of audio downloads.")
