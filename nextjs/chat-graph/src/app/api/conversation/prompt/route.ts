import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

import { ApiPromptRequest, ApiPromptResponse } from '@/types';

// Handle POST request
export async function POST(req: NextRequest) {
  // Parse the request body as ApiPromptRequest
  const data = (await req.json()) as ApiPromptRequest;

  // Initialize the Graphlit client
  const client = new Graphlit();

  try {
    // Send the prompt to the conversation
    let promptResults = await client.promptConversation(
      data.prompt,
      data.conversationId
    );

    const id = promptResults.promptConversation?.conversation?.id;

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
  } catch (e) {
    // Return the response with status 200 and JSON content type
    // @ts-ignore
    return new Response(JSON.stringify({ error: e?.message }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
