import { Graphlit } from 'graphlit-client';
import {
  ContentTypes,
  EntityExtractionServiceTypes,
  SpecificationTypes,
  SummarizationTypes,
} from 'graphlit-client/dist/generated/graphql-types';

import { extractionSpec } from '@/constants';

// Handle POST requests
export async function POST() {
  const client = new Graphlit();

  let existingWorkflows = await client.queryWorkflows();

  let workflowMatch = existingWorkflows?.workflows?.results?.find(
    (workflow) => workflow?.name === 'Chat Graph Entity Extraction'
  );

  if (!workflowMatch) {
    const existingSpecs = await client.querySpecifications();

    const specMatch = existingSpecs?.specifications?.results?.find(
      (spec) =>
        spec?.type === SpecificationTypes.Extraction &&
        spec?.name === extractionSpec.name
    );

    if (!specMatch) {
      return new Response('Missing extraction spec', {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      });
    }

    await client.createWorkflow({
      name: 'Chat Graph Entity Extraction',
      ingestion: {
        if: {
          types: [ContentTypes.File],
        },
      },
      preparation: {
        summarizations: [
          {
            type: SummarizationTypes.Custom,
            prompt:
              'Generate a single short Google search query to locate additional material relevant to this content.',
            items: 1,
          },
        ],
      },
      extraction: {
        jobs: [
          {
            connector: {
              type: EntityExtractionServiceTypes.ModelText,
              modelText: {
                specification: {
                  id: specMatch.id,
                },
              },
            },
          },
        ],
      },
    });

    existingWorkflows = await client.queryWorkflows();

    workflowMatch = existingWorkflows?.workflows?.results?.find(
      (workflow) => workflow?.name === 'Chat Graph Entity Extraction'
    );
  }

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(workflowMatch), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
