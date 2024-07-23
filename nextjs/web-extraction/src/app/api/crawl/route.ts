import { NextRequest } from 'next/server';
import { Graphlit } from 'graphlit-client';
import { FeedTypes } from 'graphlit-client/dist/generated/graphql-types';

import { ApiCrawlRequest } from '@/types';

// Function to check if the feed is done
async function checkFeedDone(
  client: Graphlit,
  feedId: string
): Promise<boolean> {
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

    // Create the feed
    const response = await client.createFeed({
      name: data.uri,
      type: FeedTypes.Web,
      web: {
        uri: data.uri,
        readLimit: data.limit,
      },
    });

    // Check if feed ID is created
    if (response.createFeed?.id) {
      const feedId = response.createFeed.id;

      // Loop to check if feed is done every 5 seconds
      const startTime = Date.now();
      const maxTimeout = 60000 + data.limit * 10000;
      let isDone = false;

      while (!isDone && Date.now() - startTime < maxTimeout) {
        isDone = await checkFeedDone(client, feedId);
        if (!isDone) {
          // Wait for 5 seconds
          await new Promise((resolve) => setTimeout(resolve, 5000));
        }
      }

      // If the feed is done, get content from feed
      if (isDone) {
        const contentsRes = await client.queryContents({
          feeds: [{ id: response.createFeed.id }],
        });

        // Clean up feed
        await client.deleteFeed(response.createFeed.id);

        // Return the response with status 200 and JSON content type
        return new Response(JSON.stringify(contentsRes.contents), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
          },
        });
      } else {
        // If the feed is not done within 1 minute, return a timeout response
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

    // Return the response with status 200 and JSON content type
    return new Response(JSON.stringify(response), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    // Log the error and return a response with status 500
    console.error('Error processing request:', error);

    return new Response(JSON.stringify({ error: 'Internal Server Error' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }
}
