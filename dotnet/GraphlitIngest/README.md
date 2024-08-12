## Configuration
- Copy appsettings.template.json to appsettings.json.
- Assign your project credentials to GRAPHLIT_ORGANIZATION_ID, GRAPHLIT_ENVIRONMENT_ID, GRAPHLIT_JWT_SECRET
- Optionally, assign your OpenAI (OPENAI_API_KEY) or Anthropic API keys (ANTHROPIC_API_KEY) if you want to use your own LLM accounts. Also, you can configure your preferred vision-enabled model be assigning ANTHROPIC_MODEL or OPENAI_MODEL._

## Usage

Parse document, audio or image files or web pages.

```
graphlit-ingest parse -i "https://graphlitplatform.blob.core.windows.net/samples/Attention%20Is%20All%20You%20Need.1706.03762.pdf"
```

### Command-Line Options

#### Source 

You can provide a URI to a file or web page, or a local file path on your computer.

```
-i [uri]

-i [local file path]
```

#### Output File Path

Provide a local file path to write the parsed output from the source.

```
-o [local file path]
```

#### Output Format

Provide the format for the parse output, either Markdown or the Graphlit JSON format.

```
-f Markdown

-f JSON
```

#### Preparation Type

Choose the preparation type, either LLM-based preparation or default (which uses Azure AI Document Intelligence for PDF, DOCX, PPTX).

```
-p LLM

-p Default
```

#### LLM Type

Choose the LLM to be used for LLM-based preparation. By default, Anthropic uses the Sonnet 3.5 model, and OpenAI uses the GPT-4o 08-06 model. For most use cases, Anthropic Sonnet 3.5 currently gives more accurate document preparation.

```
-l Anthropic

-l OpenAI
```

#### Summarization Type

Choose the summarization type of the parsed source.

```
-s [Summary | Keywords | Bullets | Headlines | Posts | Questions | Chapters ]
```

Chapters only applies to audio or video files, which have been transcribed.