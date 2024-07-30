import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

import { ApiScrapeRequest } from '@/types';

export const maxDuration = 120; // Maximum duration to process the request (in seconds)

// Handle POST request
export async function POST(req: NextRequest) {
  try {
    // Parse the request body as ApiScrapeRequest
    const data = (await req.json()) as ApiScrapeRequest;

    // Initialize the Graphlit client
    const client = new Graphlit();

    // Ingest the URI into the Graphlit client
    const response = await client.ingestUri(
      data.uri,
      undefined,
      undefined,
      true
    );

    if (response.ingestUri?.id) {
      // Fetch the content using the provided ID
      const content = await client.getContent(response.ingestUri?.id);

      // Clean up the content from the client
      await client.deleteContent(response.ingestUri?.id);

      // Return the content with status 200
      return new Response(JSON.stringify(content.content), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }

    // Return a "Not Found" response if the ID is not found
    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    // Return a response with status 500 for internal server errors
    console.error('Error processing request:', error);

    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
