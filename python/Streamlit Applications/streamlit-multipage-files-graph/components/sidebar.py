import streamlit as st

def create_sidebar():
    with st.sidebar:
        st.info("""
                ### ✅ Demo Instructions
                - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
                - **Step 1:** Generate Graphlit project token.
                - **Step 2:** Browse for files to upload and ingest.
                - **Step 3:** Visualize knowledge graph.
                - **Step 4:** Enter a prompt to ask about the files using [OpenAI](https://www.openai.com) GPT-4o LLM.
                """)

        st.markdown("""
            [Support on Discord](https://discord.gg/ygFmfjy3Qx)            
            [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
            [More information](https://www.graphlit.com)      
            """)
    return
