import {
  AnthropicModels,
  AzureOpenAiModels,
  CohereModels,
  GroqModels,
  MistralModels,
  ModelServiceTypes,
  OpenAiModels,
  ReplicateModels,
  SpecificationInput,
  SpecificationTypes,
} from 'graphlit-client/dist/generated/graphql-types';

// Define the default model configuration
export const defaultSpec: SpecificationInput = {
  type: SpecificationTypes.Completion, // Type of the specification
  serviceType: ModelServiceTypes.OpenAi, // Service type
  openAI: { model: OpenAiModels.Gpt4 }, // Model specific configuration for OpenAI
  name: `${ModelServiceTypes.OpenAi} ${OpenAiModels.Gpt4}`, // Name of the specification
};

// Define anthropic models as an array of SpecificationInputs
export const anthropicSpecs: SpecificationInput[] = [
  AnthropicModels.Claude_2,
  AnthropicModels.Claude_2_0,
  AnthropicModels.Claude_2_1,
  AnthropicModels.Claude_3Haiku,
  AnthropicModels.Claude_3Opus,
  AnthropicModels.Claude_3Sonnet,
  AnthropicModels.ClaudeInstant_1,
  AnthropicModels.ClaudeInstant_1_2,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.Anthropic,
    anthropic: { model }, // Model specific configuration for Anthropic
    name: `${ModelServiceTypes.Anthropic} ${model}`, // Name of the specification
  })
);

// Define Azure OpenAI models as an array of SpecificationInputs
export const azureOpenAiSpecs: SpecificationInput[] = [
  AzureOpenAiModels.Gpt4,
  AzureOpenAiModels.Gpt4Turbo_128K,
  AzureOpenAiModels.Gpt35Turbo_16K,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.AzureOpenAi,
    azureOpenAI: { model }, // Model specific configuration for Azure OpenAI
    name: `${ModelServiceTypes.AzureOpenAi} ${model}`, // Name of the specification
  })
);

// Define Cohere models as an array of SpecificationInputs
export const cohereSpecs: SpecificationInput[] = [
  CohereModels.CommandR,
  CohereModels.CommandRPlus,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.Cohere,
    cohere: { model }, // Model specific configuration for Cohere
    name: `${ModelServiceTypes.Cohere} ${model}`, // Name of the specification
  })
);

// Define Groq models as an array of SpecificationInputs
export const groqSpecs: SpecificationInput[] = [
  GroqModels.Llama_3_8B,
  GroqModels.Llama_3_70B,
  GroqModels.Mixtral_8X7BInstruct,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.Groq,
    groq: { model }, // Model specific configuration for Groq
    name: `${ModelServiceTypes.Groq} ${model}`, // Name of the specification
  })
);

// Define Mistral models as an array of SpecificationInputs
export const mistralSpecs: SpecificationInput[] = [
  MistralModels.MistralLarge,
  MistralModels.MistralMedium,
  MistralModels.MistralSmall,
  MistralModels.Mixtral_8X7BInstruct,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.Mistral,
    mistral: { model }, // Model specific configuration for Mistral
    name: `${ModelServiceTypes.Mistral} ${model}`, // Name of the specification
  })
);

// Define OpenAI models as an array of SpecificationInputs
export const openAiSpecs: SpecificationInput[] = [
  OpenAiModels.Gpt4,
  OpenAiModels.Gpt4O_128K,
  OpenAiModels.Gpt4O_128K_20240513,
  OpenAiModels.Gpt4_0613,
  OpenAiModels.Gpt4_32K,
  OpenAiModels.Gpt4_32K_0613,
  OpenAiModels.Gpt4Turbo_128K,
  OpenAiModels.Gpt4Turbo_128K_0125,
  OpenAiModels.Gpt4Turbo_128K_1106,
  OpenAiModels.Gpt4Turbo_128K_20240409,
  OpenAiModels.Gpt4TurboVision_128K_1106,
  OpenAiModels.Gpt35Turbo_16K,
  OpenAiModels.Gpt35Turbo_16K_0125,
  OpenAiModels.Gpt35Turbo_16K_0613,
  OpenAiModels.Gpt35Turbo_16K_1106,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.OpenAi,
    openAI: { model }, // Model specific configuration for OpenAI
    name: `${ModelServiceTypes.OpenAi} ${model}`, // Name of the specification
  })
);

// Define Replicate models as an array of SpecificationInputs
export const replicateSpecs: SpecificationInput[] = [
  ReplicateModels.Llama_2_7B,
  ReplicateModels.Llama_2_7BChat,
  ReplicateModels.Llama_2_13B,
  ReplicateModels.Llama_2_13BChat,
  ReplicateModels.Llama_2_70B,
  ReplicateModels.Llama_2_70BChat,
  ReplicateModels.Mistral_7B,
  ReplicateModels.Mistral_7BInstruct,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.Replicate,
    replicate: { model }, // Model specific configuration for Replicate
    name: `${ModelServiceTypes.Replicate} ${model}`, // Name of the specification
  })
);

// Combine all specification inputs into a single array
export const specifications: SpecificationInput[] = [
  /** Anthropic */
  ...anthropicSpecs,
  /** AzureOpenAi */
  ...azureOpenAiSpecs,
  /** Cohere */
  ...cohereSpecs,
  /** Groq */
  ...groqSpecs,
  /** Mistral */
  ...mistralSpecs,
  /** OpenAi */
  ...openAiSpecs,
  /** Replicate */
  ...replicateSpecs,
];
