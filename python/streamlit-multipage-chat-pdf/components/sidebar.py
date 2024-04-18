import streamlit as st

def create_sidebar():
    with st.sidebar:
        st.info("""
                ### ✅ Demo Instructions
                - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
                - **Step 1:** Generate Graphlit project token.
                - **Step 2:** Select a PDF, or fill in your own document URL.
                - **Step 3:** Enter a prompt to ask about the document using [OpenAI GPT-4 Turbo 128k](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) LLM.
                """)

        st.markdown("""
            [Support on Discord](https://discord.gg/ygFmfjy3Qx)            
            [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
            [More information](https://www.graphlit.com)      
            """)
