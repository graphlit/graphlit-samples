# Graphlit Sample Applications

**Production-ready examples** showing you how to build AI applications with semantic memory.

Learn by doing with these real-world implementations of the [Graphlit Platform](https://www.graphlit.com) – from simple document Q&A to advanced RAG pipelines.

[![Start Free](https://img.shields.io/badge/Get_Started-Free_Account-6366f1)](https://portal.graphlit.dev/)
[![Documentation](https://img.shields.io/badge/Docs-docs.graphlit.dev-0ea5e9)](https://docs.graphlit.dev)
[![Discord](https://img.shields.io/discord/1095189481335816243?label=Discord&logo=discord)](https://discord.gg/ygFmfjy3Qx)

---

## 🚀 Why These Samples?

**Stop reading tutorials. Start building.**

These aren't toy examples – they're production-ready applications you can deploy and customize. Each sample demonstrates a specific use case, from document intelligence to media analysis to multi-tenant AI agents.

All samples use the **same simple API** that handles:
- ✅ Content ingestion and extraction
- ✅ Semantic search and retrieval
- ✅ RAG-powered conversations
- ✅ Multi-modal processing (PDFs, audio, video, images)
- ✅ Real-time streaming responses

---

## 📚 Sample Categories

### 🤖 Chatbots & Conversational AI

**Build AI assistants that understand your documents**

- [**Next.js Chat**](/nextjs/chat/) – Upload PDFs, audio, video and chat with them
- [**Streamlit Document Q&A**](/python/Streamlit/) – Simple UI for document-based conversations
- [**Python Notebook: RAG Basics**](/python/Notebook%20Examples/) – Learn RAG fundamentals interactively

**Perfect for:** Customer support bots, internal knowledge assistants, document analysis

---

### 📄 Content Extraction & Transformation

**Convert any content into clean, structured data**

- [**Next.js File Extraction**](/nextjs/file-extraction/) – Extract Markdown from PDFs, DOCX, PPTX
- [**Next.js Web Extraction**](/nextjs/web-extraction/) – Scrape and extract structured data from websites
- [**Python Notebook: Entity Extraction**](/python/Notebook%20Examples/) – Extract entities, relationships, and insights

**Perfect for:** Content pipelines, data migration, document processing

---

### 🌐 Web Intelligence & Monitoring

**Ingest and analyze web content at scale**

- [**Web Crawling Notebook**](/python/Notebook%20Examples/) – Crawl websites and extract knowledge
- [**RSS Feed Monitor**](/python/Notebook%20Examples/) – Track and analyze content feeds
- [**Sitemap Scraping**](/python/Streamlit/) – Bulk ingest entire websites

**Perfect for:** Competitive intelligence, content aggregation, research tools

---

### 🎙️ Media Analysis

**Transcribe and analyze audio and video**

- [**Audio Transcription Notebook**](/python/Notebook%20Examples/) – Transcribe podcasts, meetings, calls
- [**Video Processing**](/python/Notebook%20Examples/) – Extract insights from video content
- [**Multi-speaker Diarization**](/python/Notebook%20Examples/) – Identify and separate speakers

**Perfect for:** Meeting analysis, podcast search, video content platforms

---

### 🏢 Enterprise & Multi-Tenant

**Build secure, scalable applications**

- [**.NET CLI Tool**](/dotnet/GraphlitIngest/) – Bulk content ingestion for enterprises
- [**Multi-tenant Notebook**](/python/Notebook%20Examples/) – Isolate data per organization
- [**RBAC Examples**](/python/Notebook%20Examples/) – Role-based access control

**Perfect for:** SaaS applications, enterprise deployments, B2B platforms

---

## 🛠️ Quick Start

### Prerequisites

```bash
# Get your free Graphlit account (1GB free, no credit card)
https://portal.graphlit.dev/

# You'll need these credentials:
# - Organization ID
# - Environment ID
# - JWT Secret
```

### Python Samples

```bash
# Install the Graphlit client
pip install graphlit-client

# Run any Google Colab notebook - no setup needed!
# https://github.com/graphlit/graphlit-samples/tree/main/python/Notebook%20Examples
```

[![PyPI version](https://badge.fury.io/py/graphlit-client.svg)](https://badge.fury.io/py/graphlit-client)

**📓 [Browse Python Notebooks →](/python/Notebook%20Examples/)**

---

### Node.js / Next.js Samples

```bash
# Install the Graphlit client
npm install graphlit-client

# Clone and run any Next.js sample
git clone https://github.com/graphlit/graphlit-samples.git
cd graphlit-samples/nextjs/chat
npm install
npm run dev
```

[![npm version](https://badge.fury.io/js/graphlit-client.svg)](https://badge.fury.io/js/graphlit-client)

**🚀 Deploy to Vercel in one click** – Each Next.js sample includes a deploy button

**📱 [Browse Next.js Apps →](/nextjs/)**

---

### .NET Samples

```bash
# Install the Graphlit client
dotnet add package Graphlit.Client

# Run the CLI tool
cd graphlit-samples/dotnet/GraphlitIngest
dotnet run
```

[![NuGet version](https://badge.fury.io/nu/Graphlit.svg)](https://badge.fury.io/nu/Graphlit)

**💻 [Browse .NET Examples →](/dotnet/)**

---

## 🎯 Featured Samples

### 1. Document Chat Application

**Upload PDFs, audio, video and chat with them using RAG**

```bash
cd nextjs/chat
npm install && npm run dev
```

**Features:**
- Multi-format support (PDF, DOCX, audio, video)
- Real-time streaming responses
- Conversation history
- Source citations

[**View Sample →**](/nextjs/chat/)

---

### 2. Web Content Extraction

**Extract clean Markdown from any website**

```bash
cd nextjs/web-extraction
npm install && npm run dev
```

**Features:**
- Automatic web scraping
- Clean Markdown output
- Bulk processing via sitemap
- Structured data extraction

[**View Sample →**](/nextjs/web-extraction/)

---

### 3. Audio Transcription Pipeline

**Transcribe and analyze audio with speaker diarization**

```python
# Run in Google Colab
# No setup required!
```

**Features:**
- Multi-speaker detection
- Automatic summarization
- Entity extraction
- Search and retrieval

[**Open in Colab →**](/python/Notebook%20Examples/)

---

## 💡 Use Case Examples

| Use Case | Best Sample | Key Features |
|----------|-------------|--------------|
| **Customer Support Bot** | [Next.js Chat](/nextjs/chat/) | Document Q&A, Citations, Multi-tenant |
| **Content Intelligence** | [Web Extraction](/nextjs/web-extraction/) | Scraping, Structured extraction, Bulk processing |
| **Meeting Analysis** | [Audio Transcription Notebook](/python/Notebook%20Examples/) | Transcription, Summarization, Entity extraction |
| **Knowledge Base Search** | [Streamlit Apps](/python/Streamlit/) | Semantic search, Filters, RAG |
| **Document Processing** | [.NET CLI](/dotnet/GraphlitIngest/) | Bulk ingestion, Enterprise scale, Automation |

---

## 🎓 Learning Path

**New to Graphlit? Follow this path:**

1. **Start with Python Notebooks** – No setup, run in Google Colab
   - Begin with basic ingestion and search
   - Progress to RAG and conversations
   - [Browse Notebooks →](/python/Notebook%20Examples/)

2. **Build a Streamlit App** – Interactive UI examples
   - Upload files and chat
   - Web crawling demos
   - [Browse Streamlit Apps →](/python/Streamlit/)

3. **Deploy a Next.js Application** – Production-ready examples
   - Deploy to Vercel in minutes
   - Customize for your use case
   - [Browse Next.js Apps →](/nextjs/)

4. **Scale with .NET** – Enterprise integration
   - Bulk ingestion pipelines
   - Command-line tools
   - [Browse .NET Examples →](/dotnet/)

---

## 📖 Resources

### Documentation
- 📘 [**Platform Documentation**](https://docs.graphlit.dev) – Complete API reference
- 🎥 [**Video Tutorials**](https://www.youtube.com/@graphlit) – Step-by-step guides
- 💬 [**Discord Community**](https://discord.gg/ygFmfjy3Qx) – Get help from the community

### SDKs
- [**Python SDK**](https://github.com/graphlit/graphlit-client-python) – `pip install graphlit-client`
- [**TypeScript/JavaScript SDK**](https://github.com/graphlit/graphlit-client-typescript) – `npm install graphlit-client`
- [**C# / .NET SDK**](https://github.com/graphlit/graphlit-client-dotnet) – `dotnet add package Graphlit.Client`

### Platform
- 🌐 [**Graphlit Website**](https://www.graphlit.com) – Platform overview and pricing
- 🚀 [**Sign Up Free**](https://portal.graphlit.dev/) – Get started in 5 minutes
- 📊 [**Pricing**](https://www.graphlit.com/#pricing) – Free tier + usage-based plans

---

## 🤝 Contributing

Have a sample application you'd like to share? We welcome contributions!

1. Fork this repository
2. Create your sample in the appropriate directory
3. Include a README with setup instructions
4. Submit a pull request

See our [contribution guidelines](CONTRIBUTING.md) for more details.

---

## 💸 Pricing & Free Tier

**Graphlit is free to get started:**

- ✅ 1GB storage
- ✅ 1,000 content items
- ✅ 3 feeds
- ✅ 100 conversations
- ✅ Full API access
- ✅ All content types supported

**Paid plans start at $49/month** with usage-based credits for additional content.

[**View Pricing Details →**](https://www.graphlit.com/#pricing)

---

## 🆚 Why Graphlit vs DIY Solutions?

| DIY Approach | 🚀 Graphlit |
|--------------------------------------|-------------|
| Stitch together vector DB, storage, embeddings | **Complete integrated platform** |
| Manage your own infrastructure | **Fully managed, serverless** |
| Limited file format support | **True multimodal from day one** |
| Build your own ingestion pipelines | **Automated ETL for any format** |
| Handle scaling yourself | **Scales automatically** |
| Weeks of setup | **Running in 5 minutes** |

---

## 📬 Support

- 💬 **Discord**: [Join our community](https://discord.gg/ygFmfjy3Qx)
- 📧 **Email**: support@graphlit.com
- 📖 **Docs**: [docs.graphlit.dev](https://docs.graphlit.dev)
- 🐛 **Issues**: [GitHub Issues](https://github.com/graphlit/graphlit-samples/issues)

---

<div align="center">

### Ready to build your AI application?

[**Get Started Free**](https://portal.graphlit.dev/) • [**View Docs**](https://docs.graphlit.dev) • [**Join Discord**](https://discord.gg/ygFmfjy3Qx)

**Built by developers, for developers.** 🚀

</div>
