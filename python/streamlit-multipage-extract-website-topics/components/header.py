import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Analyze website for topics. Will scrape website, and read a maximum of 10 pages via web sitemap. Entity extraction is done with [Azure AI Language](https://azure.microsoft.com/en-us/products/ai-services/ai-language).")
