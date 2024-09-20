import {
  AnthropicModels,
  AzureOpenAiModels,
  CohereModels,
  DeepseekModels,
  GraphStrategyTypes,
  GroqModels,
  MistralModels,
  ModelServiceTypes,
  OpenAiModels,
  ReplicateModels,
  SpecificationInput,
  SpecificationTypes,
} from 'graphlit-client/dist/generated/graphql-types';

export const serviceTypeNames = {
  ANTHROPIC: 'Anthropic',
  AZURE_OPEN_AI: 'Azure OpenAI',
  COHERE: 'Cohere',
  DEEPSEEK: 'Deepseek',
  GROQ: 'Groq',
  MISTRAL: 'Mistral',
  OPEN_AI: 'OpenAI',
  REPLICATE: 'Replicate',
};

export const modelNames = {
  CLAUDE_2: 'Claude 2 (Latest)',
  CLAUDE_2_0: 'Claude 2.0',
  CLAUDE_2_1: 'Claude 2.1',
  CLAUDE_3_5_SONNET: 'Claude 3.5 Sonnet (Latest)',
  CLAUDE_3_HAIKU: 'Claude 3 Haiku (Latest)',
  CLAUDE_3_OPUS: 'Claude 3 Opus (Latest)',
  CLAUDE_3_SONNET: 'Claude 3 Sonnet (Latest)',
  CLAUDE_INSTANT_1: 'Claude Instant 1 (Latest)',
  CLAUDE_INSTANT_1_2: 'Claude Instant 1.2',
  COMMAND_R: 'Command R',
  COMMAND_R_PLUS: 'Command R+',
  CHAT: 'Chat',
  CODER: 'Coder',
  LLAMA_3_1_405B: 'LLaMA 3.1 405b',
  LLAMA_3_1_70B: 'LLaMA 3.1 70b',
  LLAMA_3_1_8B: 'LLaMA 3.1 8b',
  LLAMA_3_70B: 'LLaMA 3 70b',
  LLAMA_3_8B: 'LLaMA 3 8b',
  MISTRAL_LARGE: 'Large',
  MISTRAL_MEDIUM: 'Medium',
  MISTRAL_NEMO: 'Nemo',
  MISTRAL_SMALL: 'Small',
  MIXTRAL_8X7B_INSTRUCT: 'Mixtral 8x7b Instruct',
  GPT35_TURBO: 'GPT-3.5 Turbo (Latest version)',
  GPT35_TURBO_0613: 'GPT-3.5 Turbo (0613 version)',
  GPT35_TURBO_16K: 'GPT-3.5 Turbo 16k (Latest version)',
  GPT35_TURBO_16K_0125: 'GPT-3.5 Turbo 16k (0125 version)',
  GPT35_TURBO_16K_0613: 'GPT-3.5 Turbo 16k (0613 version)',
  GPT35_TURBO_16K_1106: 'GPT-3.5 Turbo 16k (1106 version)',
  GPT4: 'GPT-4 (Latest version)',
  GPT4O_128K: 'GPT-4o 128k (latest version)',
  GPT4O_128K_20240513: 'GPT-4o 128k (2024-05-13 version)',
  GPT4O_MINI_128K: 'GPT-4o Mini 128k (latest version)',
  GPT4O_MINI_128K_20240718: 'GPT-4o Mini 128k (2024-07-18 version)',
  GPT4_0613: 'GPT-4 (0613 version)',
  GPT4_32K: 'GPT-4 32k (Latest version)',
  GPT4_32K_0613: 'GPT-4 32k (0613 version)',
  GPT4_TURBO_128K: 'GPT-4 Turbo 128k (Latest version)',
  GPT4_TURBO_128K_0125: 'GPT-4 Turbo 128k (0125 version)',
  GPT4_TURBO_128K_1106: 'GPT-4 Turbo 128k (1106 version)',
  GPT4_TURBO_128K_20240409: 'GPT-4 Turbo 128k (2024-04-09 version)',
  GPT4_TURBO_VISION_128K_1106: 'GPT-4 Turbo Vision 128k (1106 version)',
  LLAMA_2_13B: 'Llama 2 13b',
  LLAMA_2_13B_CHAT: 'Llama 2 13b Chat',
  LLAMA_2_70B: 'Llama 2 70b',
  LLAMA_2_70B_CHAT: 'Llama 2 70b Chat',
  LLAMA_2_7B: 'Llama 2 7b',
  LLAMA_2_7B_CHAT: 'Llama 2 7b Chat',
  MISTRAL_7B: 'Mistral 7b',
  MISTRAL_7B_INSTRUCT: 'Mistral 7b Instruct',
};

// Define the default model configuration
export const defaultSpec: SpecificationInput = {
  type: SpecificationTypes.Completion, // Type of the specification
  serviceType: ModelServiceTypes.OpenAi, // Service type
  openAI: { model: OpenAiModels.Gpt4O_128K }, // Model specific configuration for OpenAI
  name: `${serviceTypeNames[ModelServiceTypes.OpenAi]} ${modelNames[OpenAiModels.Gpt4O_128K]}`,
  graphStrategy: {
    type: GraphStrategyTypes.ExtractEntitiesGraph,
    generateGraph: true,
  },
};

export const extractionSpec = {
  type: SpecificationTypes.Extraction,
  serviceType: ModelServiceTypes.Anthropic,
  anthropic: { model: AnthropicModels.Claude_3_5Sonnet },
  name: `${serviceTypeNames[ModelServiceTypes.Anthropic]} ${modelNames[AnthropicModels.Claude_3_5Sonnet]} Extraction`,
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.Anthropic]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.AzureOpenAi]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
  })
);

// Define Cohere models as an array of SpecificationInputs
export const deepseekSpecs: SpecificationInput[] = [
  DeepseekModels.Chat,
  DeepseekModels.Coder,
].map(
  (model): SpecificationInput => ({
    type: SpecificationTypes.Completion,
    serviceType: ModelServiceTypes.Deepseek,
    deepseek: { model }, // Model specific configuration for Cohere
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.Deepseek]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.Cohere]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.Groq]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.Mistral]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.OpenAi]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
    // @ts-ignore
    name: `${serviceTypeNames[ModelServiceTypes.Replicate]} ${modelNames[model]}`,
    graphStrategy: {
      type: GraphStrategyTypes.ExtractEntitiesGraph,
      generateGraph: true,
    },
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
  /** Deepseek */
  ...deepseekSpecs,
  /** Groq */
  ...groqSpecs,
  /** Mistral */
  ...mistralSpecs,
  /** OpenAi */
  ...openAiSpecs,
  /** Replicate */
  ...replicateSpecs,
];
