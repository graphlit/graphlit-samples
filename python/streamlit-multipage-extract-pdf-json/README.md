# Graphlit Platform

## Extract JSON in any schema from any PDF, DOCX, or PPTX file. Tool calling done with [OpenAI GPT-4 Turbo 128k](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) LLM. Text extraction and OCR done with [Azure AI Document Intelligence](https://azure.microsoft.com/en-us/products/ai-services/ai-document-intelligence).

You can view the Streamlit application [here](https://graphlit-samples-extract-pdf-json.streamlit.app/).

### Demo Instructions
- [Sign up for Graphlit](https://docs.graphlit.dev/getting-started/signup) 🆓  
- **Step 1:** Generate Graphlit project token.
- **Step 2:** Select a PDF, or fill in your own document URL.
- **Step 3:** Enter JSON schema for data to be extracted.
- **Step 4:** View JSON extracted from document text.

[Support on Discord](https://discord.gg/ygFmfjy3Qx)            
[API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
[More information](https://www.graphlit.com)

### Run locally

```python
pip install -r requirements.txt

streamlit run Start_Here.py
```