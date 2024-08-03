import { Graphlit } from 'graphlit-client';

import { specifications } from '@/constants';

// Handle GET requests
export async function GET() {
  // Initialize the Graphlit client
  const client = new Graphlit();

  // Fetch all specifications
  const response = await client.querySpecifications();

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(response.specifications), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}

// Handle POST requests
export async function POST() {
  // Initialize the Graphlit client
  const client = new Graphlit();

  // Fetch all specifications
  const settled = await Promise.allSettled(
    specifications.map((specification) => {
      return client.createSpecification(specification);
    })
  );

  const response = settled.map((promise) => {
    if (promise.status === 'fulfilled') {
      return promise.value.createSpecification;
    }
  });

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify({ results: response }), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
