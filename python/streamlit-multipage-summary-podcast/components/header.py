import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Generate chapters for latest podcast episode from RSS feed. Chapters generated with the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
