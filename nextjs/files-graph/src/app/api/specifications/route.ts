import { Graphlit } from 'graphlit-client';
import {
  GraphStrategyTypes,
  SpecificationInput,
  SpecificationTypes,
  SpecificationUpdateInput,
} from 'graphlit-client/dist/generated/graphql-types';

import { extractionSpec, specifications } from '@/constants';

// Handle POST requests
export async function POST() {
  const client = new Graphlit();

  const existingSpecs = await client.querySpecifications();

  const specMatch = existingSpecs?.specifications?.results?.find(
    (spec) =>
      spec.type === SpecificationTypes.Extraction &&
      spec.name === extractionSpec.name
  );

  if (!specMatch) {
    await client.createSpecification(extractionSpec);
  }

  const completionSpecs =
    existingSpecs?.specifications?.results?.filter(
      (spec) => spec?.type === SpecificationTypes.Completion
    ) || [];

  let create: SpecificationInput[] = [];
  let update: SpecificationUpdateInput[] = [];

  specifications.forEach((spec) => {
    const matchingSpec = completionSpecs.find(
      (completionSpec) => completionSpec?.name === spec.name
    );

    if (matchingSpec) {
      update.push({
        id: matchingSpec.id,
        strategy: null,
        graphStrategy: { type: GraphStrategyTypes.ExtractEntitiesGraph },
      } as SpecificationUpdateInput);
    } else {
      create.push(spec);
    }
  });

  await Promise.allSettled(
    create.map((specification) => {
      return client.createSpecification(specification);
    })
  );

  await Promise.allSettled(
    update.map((specification) => {
      return client.updateSpecification(specification);
    })
  );

  const specResponse = await client.querySpecifications();

  // Return the response with status 200 and JSON content type
  return new Response(JSON.stringify(specResponse.specifications), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}
