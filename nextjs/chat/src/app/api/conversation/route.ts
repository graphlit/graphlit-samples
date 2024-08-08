import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';
import { ConversationTypes } from 'graphlit-client/dist/generated/graphql-types';

import { ApiNewConversationRequest } from '@/types';

// Handle GET request
export async function GET() {
  // Initialize the Graphlit client
  const client = new Graphlit();

  // Query the Graphlit client for conversations
  const conversationResults = await client.queryConversations();

  // Extract the conversations from the results
  const response = conversationResults.conversations;

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(response), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}

// Handle POST request
export async function POST(req: NextRequest) {
  // Parse the request body as ApiNewRequest
  const data = (await req.json()) as ApiNewConversationRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  // Create graphlit conversation
  const conversationResults = await client.createConversation({
    name: data.name,
    specification: { id: data.specificationId },
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
}
