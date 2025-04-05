import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Chat with any uploaded files, with citations.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).  Chat completion uses the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
