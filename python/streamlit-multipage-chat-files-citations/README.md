# Graphlit Platform

## Chat with any uploaded file, with citations.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence). Chat completion uses the [Anthropic](https://www.anthropic.com) Claude 3 Haiku LLM.

You can view the Streamlit application [here](https://graphlit-samples-chat-file-citations.streamlit.app/).

### Demo Instructions
- **Prerequisite:** [Sign up for Graphlit 🆓](https://docs.graphlit.dev/getting-started/signup)
- **Step 1:** Generate Graphlit project token.
- **Step 2:** Browse for a file to upload and ingest.
- **Step 3:** Enter a prompt to ask about the file using [OpenAI GPT-4 Turbo 128k](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) LLM.

[Support on Discord](https://discord.gg/ygFmfjy3Qx)            
[API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
[More information](https://www.graphlit.com)

### Run locally

```python
pip install -r requirements.txt

streamlit run Start_Here.py
```