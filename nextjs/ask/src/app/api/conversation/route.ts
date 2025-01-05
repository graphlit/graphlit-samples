import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';
import { ConversationTypes } from 'graphlit-client/dist/generated/graphql-types';

import { ApiNewConversationRequest } from '@/types';

// Handle POST request
export async function POST(req: NextRequest) {
  // Parse the request body as ApiNewRequest
  const data = (await req.json()) as ApiNewConversationRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  try {
    // Create graphlit conversation
    const conversationResults = await client.createConversation({
      name: data.name,
      type: ConversationTypes.Content,
    });

    // Extract the conversation from the result
    const response = conversationResults.createConversation;

    // Return the response with status 200 and JSON content type
    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (e: any) {
    // Extract detailed error information
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
