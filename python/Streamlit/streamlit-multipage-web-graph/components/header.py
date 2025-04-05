import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Chat with website, using GraphRAG with knowledge graph built from extracted entities. Entity extraction and chat completion uses the [OpenAI](https://www.openai.com) GPT-4o LLM.")
