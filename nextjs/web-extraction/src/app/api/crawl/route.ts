import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';
import { FeedTypes } from 'graphlit-client/dist/generated/graphql-types';

import { ApiCrawlRequest } from '@/types';

export const maxDuration = 120; // Maximum duration to wait for the feed to complete (in seconds)

// Function to check if the feed processing is complete
async function checkFeedDone(
  client: Graphlit,
  feedId: string
): Promise<boolean> {
  // Check if the feed is done using the client
  const res = await client.isFeedDone(feedId);
  return res.isFeedDone?.result ?? false;
}

// Handle POST request
export async function POST(req: NextRequest) {
  try {
    // Parse the request body as ApiCrawlRequest
    const data = (await req.json()) as ApiCrawlRequest;

    // Initialize the Graphlit client
    const client = new Graphlit();

    // Create a new feed for the specified URI
    const response = await client.createFeed({
      name: data.uri,
      type: FeedTypes.Web,
      web: {
        uri: data.uri,
        readLimit: data.limit,
      },
    });

    // Check if the feed creation was successful
    if (response.createFeed?.id) {
      const feedId = response.createFeed.id;

      // Loop to check if the feed processing is done every 5 seconds
      const startTime = Date.now();
      const maxTimeout = 60000 + data.limit * 10000; // Timeout duration (1 minute + limit-based buffer)
      let isDone = false;

      while (!isDone && Date.now() - startTime < maxTimeout) {
        isDone = await checkFeedDone(client, feedId);
        if (!isDone) {
          // Wait for 5 seconds before checking again
          await new Promise((resolve) => setTimeout(resolve, 5000));
        }
      }

      // If the feed is done, get the content from the feed
      if (isDone) {
        const contentsRes = await client.queryContents({
          feeds: [{ id: response.createFeed.id }],
        });

        // Clean up the feed after processing
        await client.deleteFeed(response.createFeed.id);

        // Return the content with status 200
        return new Response(JSON.stringify(contentsRes.contents), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
        });
      } else {
        // Return a timeout error if the feed is not done within the allotted time
        return new Response(
          JSON.stringify({ error: 'Feed processing timeout' }),
          {
            status: 504,
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
      }
    }

    // If feed creation was not successful, return the response with status 200
    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    // Log any errors and return a response with status 500
    console.error('Error processing request:', error);

    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
