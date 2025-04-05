import streamlit as st

def create_sidebar():
    with st.sidebar:
        st.info("""
                ### ✅ Demo Instructions
                - [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
                - **Step 1:** Generate Graphlit project token.
                - **Step 2:** Fill in the GitHub repo URI, and [GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
                - **Step 3:** Click to publish report of recent GitHub Issues using [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.     
                """)

        st.markdown("""
            [Support on Discord](https://discord.gg/ygFmfjy3Qx)            
            [API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
            [More information](https://www.graphlit.com)      
            """)
