import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

import { ApiPromptRequest, ApiPromptResponse } from '@/types';

// Handle POST request
export async function POST(req: NextRequest) {
  // Parse the request body as ApiPromptRequest
  const data = (await req.json()) as ApiPromptRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  // Send the prompt to the conversation
  const promptResults = await client.promptConversation(
    data.prompt,
    data.conversationId
  );

  // Prepare the response object
  const response: ApiPromptResponse = {
    conversationId: promptResults.promptConversation?.conversation?.id ?? null,
    promptResults,
  };

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(response), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
