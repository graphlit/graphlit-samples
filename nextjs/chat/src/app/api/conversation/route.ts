import { Graphlit } from 'graphlit-client';

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
