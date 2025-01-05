import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

// Handle GET request to retrieve a conversation by ID
export async function GET(
  _: NextRequest,
  { params }: { params: { id: string } }
) {
  // Initialize the Graphlit client
  const client = new Graphlit();

  // Get the conversation from the Graphlit client using the provided ID
  const getResults = await client.getConversation(params.id);

  // Extract the conversation from the results
  const response = getResults.conversation;

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(response), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
