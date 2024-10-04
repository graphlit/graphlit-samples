# Graphlit Platform

## Chat with any PDF, DOCX, or PPTX file.  Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence). Chat completion uses the [OpenAI GPT-4o Mini 128k](https://platform.openai.com/docs/models/gpt-4o-mini) LLM.

You can view the Streamlit application [here](https://graphlit-samples-chat-pdf.streamlit.app/).

### Demo Instructions
- **Prerequisite:** [Sign up for Graphlit 🆓](https://docs.graphlit.dev/getting-started/signup)
- **Step 1:** Generate Graphlit project token.
- **Step 2:** Select a PDF, or fill in your own document URL.
- **Step 3:** Enter a prompt to ask about the document using [OpenAI GPT-4o Mini 128k](https://platform.openai.com/docs/models/gpt-4o-mini) LLM.

[Support on Discord](https://discord.gg/ygFmfjy3Qx)            
[API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
[More information](https://www.graphlit.com)

### Run locally

```python
pip install -r requirements.txt

streamlit run Start_Here.py
```