# Uppy Demo with Next.js

This is a demo project showing how to integrate Uppy file uploader with Next.js. It demonstrates file upload capabilities using Uppy's modern and user-friendly interface.

When uploading files to Uppy, first we must initialize the Graphlit Node.js SDK. We pass the JWT bearer token generated by the SDK with the Uppy headers.

Graphlit will use the JWT to identify the Graphlit project and owner, and will ingest the uploaded file automatically.

## Features

- File upload using Uppy
- Modern UI with drag & drop support
- Progress indicators
- Multiple file upload support
- Built with Next.js

### Requirements

- Node.js 18.17 and above

### Run locally

Clone the repository:

```bash
git clone git@github.com:graphlit/graphlit-samples.git
cd nextjs/uppy
```

Install packages:

```bash
npm i
```

First, copy the `.env.example` file to `.env` and fill in the required environment variables:

- `GRAPHLIT_ORGANIZATION_ID`
- `GRAPHLIT_ENVIRONMENT_ID`
- `GRAPHLIT_JWT_SECRET`

```bash
cp .env.example .env
```

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser

## Deploy on Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fgraphlit%2Fgraphlit-samples%2Ftree%2Fmain%2Fnextjs%2Fuppy&env=GRAPHLIT_ORGANIZATION_ID,GRAPHLIT_ENVIRONMENT_ID,GRAPHLIT_JWT_SECRET&project-name=graphlit-uppy)

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.