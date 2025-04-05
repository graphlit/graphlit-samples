import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Summarize any PDF, DOCX, or PPTX file. Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence). Summary generated with the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
