import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Extract people and companies from any PDF, DOCX, or PPTX file. Entity extraction is done with [Azure AI Language](https://azure.microsoft.com/en-us/products/ai-services/ai-language). Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).")
