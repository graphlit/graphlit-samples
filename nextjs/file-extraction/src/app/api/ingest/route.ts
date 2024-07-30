import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

import {
  ApiPromptFilesRequest,
  FileResponseResult,
  FileResponseStatus,
} from '@/types';

export const maxDuration = 60; // Maximum allowed duration for file processing

// Handle POST requests
export async function POST(req: NextRequest) {
  // Parse the request body as ApiPromptFilesRequest type
  const data = (await req.json()) as ApiPromptFilesRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  // Ingest each file and handle results
  const results = await Promise.allSettled(
    data.files.map(({ name, base64, mimeType }) =>
      client.ingestEncodedFile(name, base64, mimeType, undefined, true)
    )
  );

  // Collect results of file ingestion
  const fileResults: FileResponseResult[] = results.map((result) =>
    result.status === 'fulfilled'
      ? {
          id: result.value.ingestEncodedFile?.id,
          status: FileResponseStatus.OK,
          reason: '',
        }
      : {
          id: undefined,
          status: FileResponseStatus.FAILED,
          reason: result.reason,
        }
  );

  // Retrieve content for each ingested file
  const contentResults = await Promise.allSettled(
    fileResults.map(async ({ id, reason }) =>
      id
        ? client.getContent(id).then((content) => content.content)
        : { error: reason }
    )
  );

  // Map content retrieval results to response format
  const response = contentResults.map((result) =>
    result.status === 'fulfilled' ? result.value : result.reason
  );

  // Return response with JSON content type
  return new Response(JSON.stringify(response), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
