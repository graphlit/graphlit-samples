import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';

// Handle PUT request to update a conversation's specification by conversation ID
export async function PUT(
  _: NextRequest,
  { params }: { params: { id: string; specId: string } }
) {
  // Initialize the Graphlit client
  const client = new Graphlit();

  // Update the conversation with the new specification
  const response = await client.updateConversation({
    id: params.id,
    specification: { id: params.specId },
  });

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(response), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
