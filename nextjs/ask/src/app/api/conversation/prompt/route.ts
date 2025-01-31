import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';
import { SdkTypes } from 'graphlit-client/dist/generated/graphql-types';

import { ApiPromptRequest, ApiPromptResponse } from '@/types';

// Handle POST request
export async function POST(req: NextRequest) {
  // Parse the request body as ApiPromptRequest
  const data = (await req.json()) as ApiPromptRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  try {
    // Send the prompt to the conversation
    let promptResults = await client.askGraphlit(
      data.prompt,
      undefined,
      data.conversationId
    );

    const id = promptResults.askGraphlit?.conversation?.id;

    // Prepare the response object
    const response: ApiPromptResponse = {
      conversationId: id ?? null,
      promptResults,
    };

    // Return the response with status 200 and JSON content type
    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (e: any) {
    const errorDetails = {
      message: e.message,
      graphQLErrors: e.graphQLErrors,
      networkError: e.networkError?.result?.errors,
      statusCode: e.networkError?.statusCode,
    };

    return new Response(JSON.stringify({ error: errorDetails }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
