import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

import { ApiScrapeRequest } from '@/types';

// Handle POST request
export async function POST(req: NextRequest) {
  try {
    // Parse the request body as ApiScrapeRequest
    const data = (await req.json()) as ApiScrapeRequest;

    // Initialize the Graphlit client
    const client = new Graphlit();

    // Extract the conversations from the results
    const response = await client.ingestUri(
      data.uri,
      undefined,
      undefined,
      true
    );

    if (response.ingestUri?.id) {
      const content = await client.getContent(response.ingestUri?.id);

      // Clean up content
      await client.deleteContent(response.ingestUri?.id);

      return new Response(JSON.stringify(content.content), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }

    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Error processing request:', error);

    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
