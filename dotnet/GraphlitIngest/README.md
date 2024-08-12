## Configuration: 
- Copy appsettings.template.json to appsettings.json.
- Assign your project credentials to GRAPHLIT_ORGANIZATION_ID, GRAPHLIT_ENVIRONMENT_ID, GRAPHLIT_JWT_SECRET
- Optionally, assign your OpenAI or Anthropic API keys if you want to use your own LLM accounts.

## Usage

```
graphlit-parse parse --u "https://www.example.com/document.pdf"
```

```
graphlit-parse parse --u "https://www.example.com/document.pdf" -f Markdown -o c:\temp\document.md
```

```
graphlit-parse parse --u "https://www.example.com/document.pdf" -f JSON -o c:\temp\document.json
```

```
graphlit-parse parse --u "https://www.example.com/document.pdf" -p LLM
```

```
graphlit-parse parse --u "https://www.example.com/document.pdf" -p LLM -l Anthropic
```

```
graphlit-parse parse --u "https://www.example.com/document.pdf" -p LLM -l OpenAI
```
