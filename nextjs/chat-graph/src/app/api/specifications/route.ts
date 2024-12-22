import { Graphlit } from 'graphlit-client';
import {
  DeepseekModels,
  GraphStrategyTypes,
  ModelServiceTypes,
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
      spec?.type === SpecificationTypes.Extraction &&
      spec?.name === extractionSpec.name
  );

  if (!specMatch) {
    await client.createSpecification(extractionSpec);
  }

  const completionSpecs =
    existingSpecs?.specifications?.results?.filter(
      (spec) => spec?.type === SpecificationTypes.Completion
    ) || [];
  //
  let create: SpecificationInput[] = [];
  let update: SpecificationUpdateInput[] = [];

  specifications.forEach((spec) => {
    const matchingSpec = completionSpecs.find(
      (completionSpec) => completionSpec?.name === spec.name
    );

    if (matchingSpec) {
      update.push({
        id: matchingSpec.id,
        serviceType: matchingSpec.serviceType,
        anthropic:
          matchingSpec.serviceType === ModelServiceTypes.Anthropic
            ? { model: matchingSpec?.anthropic?.model }
            : undefined,
        azureOpenAI:
          matchingSpec.serviceType === ModelServiceTypes.AzureOpenAi
            ? { model: matchingSpec?.azureOpenAI?.model }
            : undefined,
        cohere:
          matchingSpec.serviceType === ModelServiceTypes.Cohere
            ? { model: matchingSpec?.cohere?.model }
            : undefined,
        deepseek:
          matchingSpec.serviceType === ModelServiceTypes.Deepseek
            ? {
                model:
                  (matchingSpec?.deepseek?.model ??
                  matchingSpec?.name.includes('Chat'))
                    ? DeepseekModels.Chat
                    : DeepseekModels.Coder,
              }
            : undefined,
        groq:
          matchingSpec.serviceType === ModelServiceTypes.Groq
            ? { model: matchingSpec?.groq?.model }
            : undefined,
        mistral:
          matchingSpec.serviceType === ModelServiceTypes.Mistral
            ? { model: matchingSpec?.mistral?.model }
            : undefined,
        openAI:
          matchingSpec.serviceType === ModelServiceTypes.OpenAi
            ? { model: matchingSpec?.openAI?.model }
            : undefined,
        replicate:
          matchingSpec.serviceType === ModelServiceTypes.Replicate
            ? { model: matchingSpec?.replicate?.model }
            : undefined,
        graphStrategy: {
          type: GraphStrategyTypes.ExtractEntitiesGraph,
          generateGraph: true,
        },
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
