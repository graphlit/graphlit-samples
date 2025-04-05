# Graphlit Platform

## Roast any uploaded image.

You can view the Streamlit application [here](https://graphlit-samples-roast-me-audio.streamlit.app/).

### Demo Instructions
- **Step 1:** Browse for a picture to upload and roast.
- **Step 2:** Read and listen to the roast of your uploaded picture. Image analysis uses the [OpenAI GPT-4 Turbo 128k Vision](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) LLM.  Audio generation done with [ElevenLabs](https://elevenlabs.io).

[Learn more about Graphlit](https://www.graphlit.com)      
[Support on Discord](https://discord.gg/ygFmfjy3Qx)            
[API Reference](https://docs.graphlit.dev/graphlit-data-api/api-reference)     
[Python SDK](https://pypi.org/project/graphlit-client/)

### Run locally

This application assumes that `GRAPHLIT_ORGANIZATION_ID`, `GRAPHLIT_ENVIRONMENT_ID` and `GRAPHLIT_JWT_SECRET` are assigned as environment variables, and is preconfigured for the specified project.

```python
pip install -r requirements.txt

streamlit run Start_Here.py
```