import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Extract JSON in any schema from any PDF, DOCX, or PPTX file. Tool calling done with [OpenAI GPT-4o Mini 128k](https://platform.openai.com/docs/models/gpt-4o-mini) LLM. Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).")
