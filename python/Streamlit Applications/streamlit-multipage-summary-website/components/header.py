import streamlit as st

def create_header():
    st.image("https://graphlitplatform.blob.core.windows.net/samples/graphlit-logo.svg", width=128)
    st.title("Graphlit Platform")
    st.markdown("Generate summary of website. Will scrape website, and read a maximum of 10 pages via web sitemap. Summary generated with the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.")
