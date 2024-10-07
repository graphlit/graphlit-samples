import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

import {
  ApiPromptFilesRequest,
  ApiPromptFilesResponse,
  FileResponseResult,
  FileResponseStatus,
} from '@/types';

export const maxDuration = 60;

// Handle POST requests
export async function POST(req: NextRequest) {
  // Parse the request body as ApiPromptFilesRequest
  const data = (await req.json()) as ApiPromptFilesRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  // Process each file by ingesting it into the Graphlit client
  const results = await Promise.allSettled(
    data.files.map(({ name, base64, mimeType }) => {
      return client.ingestEncodedFile(name, base64, mimeType, undefined, true, {
        id: data.workflowId,
      });
    })
  );

  // Prepare the response results
  const fileResults: FileResponseResult[] = [];

  // Iterate over the results and populate the fileResults array
  results.forEach((result) => {
    if (result.status === 'fulfilled') {
      fileResults.push({
        status: FileResponseStatus.OK,
        reason: '',
      });
    } else if (result.status === 'rejected') {
      fileResults.push({
        status: FileResponseStatus.FAILED,
        reason: result.reason,
      });
    }
  });

  // Create the response object
  const response: ApiPromptFilesResponse = {
    fileResults,
  };

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(response), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
