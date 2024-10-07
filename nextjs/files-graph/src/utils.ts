import { Types } from 'graphlit-client';
import {
  ConversationResults,
  GraphStrategyTypes,
  Specification,
  SpecificationResults,
  SpecificationTypes,
  Workflow,
} from 'graphlit-client/dist/generated/graphql-types';
import prettyBytes from 'pretty-bytes';

import { CitationType } from '@/types';

import { defaultSpec, specifications as specConfigs } from './constants';

// Fetches a list of conversations from the API
export const getConversations = async () => {
  const response = await fetch('/api/conversation');
  if (!response.ok) {
    console.error('Error fetching conversations');
    return;
  }
  const data = (await response.json()) as ConversationResults;
  return data.results;
};

// Fetches a list of specifications from the API
export const getSpecifications = async () => {
  const response = await fetch('/api/specifications');
  if (!response.ok) {
    console.error('Error fetching specifications');
    return;
  }
  const data = (await response.json()) as SpecificationResults;
  return data.results;
};

// Seeds new specifications by sending a request to the API
export const seedSpecifications = async () => {
  const response = await fetch('/api/specifications', { method: 'POST' });
  if (!response.ok) {
    console.error('Error seeding specifications');
    return;
  }
  const data = (await response.json()) as SpecificationResults;
  return data.results;
};

export const seedWorkflows = async () => {
  const response = await fetch('/api/workflows', { method: 'POST' });
  if (!response.ok) {
    console.error('Error fetching workflows');
    return;
  }
  return (await response.json()) as Workflow;
};

export const updateSpecifications = async (specifications: Specification[]) => {
  const completionSpecs = specifications.filter(
    (spec) => spec.type === SpecificationTypes.Completion
  );

  const requestSpecs = completionSpecs.map((spec: Specification) => ({
    id: spec.id,
    strategy: null,
    graphStrategy: { type: GraphStrategyTypes.ExtractEntitiesGraph },
  }));

  const response = await fetch('/api/specifications', {
    method: 'PUT',
    body: JSON.stringify(requestSpecs),
  });

  if (!response.ok) {
    console.error('Error updating specifications');
    return;
  }

  const data = (await response.json()) as SpecificationResults;

  return data.results;
};

// Merges fetched specifications with predefined configurations
export const mergeSpecsConfig = (specifications: Specification[]) => {
  return specConfigs.map((specConfig) => {
    return specifications.find(
      (spec) => spec.name === specConfig.name
    ) as Specification;
  });
};

// Retrieves the default specification from the fetched specifications
export const mergeDefaultSpecConfig = (specifications: Specification[]) => {
  return specifications.find(
    (spec) => spec.name === defaultSpec.name
  ) as Specification;
};

// Generates a conversation name based on the current date and time
export const conversationName = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  // @ts-ignore
  hours = String(hours).padStart(2, '0');

  return `Conversation ${year}-${month}-${day} ${hours}:${minutes}:${seconds} ${ampm}`;
};

// Selects an emoji based on content and file types
export const selectEmoji = (
  contentType?: Types.Maybe<Types.ContentTypes>,
  fileType?: Types.Maybe<Types.FileTypes>
): string => {
  const contentEmojiMap: { [key: string]: string } = {
    FILE: '📄',
    PAGE: '🌐',
    MESSAGE: '💬',
    TEXT: '📝',
    POST: '📰',
    EMAIL: '📧',
    EVENT: '📅',
    ISSUE: '🐛',
  };

  const fileEmojiMap: { [key: string]: string } = {
    VIDEO: '🎥',
    AUDIO: '🎵',
    IMAGE: '🖼️',
    DOCUMENT: '📃',
    EMAIL: '📧',
    CODE: '💻',
    DATA: '📊',
  };

  if (contentType === 'FILE' && fileType) {
    return fileEmojiMap[fileType] || '📄';
  } else if (contentType) {
    return contentEmojiMap[contentType] || '📄';
  }

  return '📄';
};

// Extracts key information from a citation for UI display
export const getCitationParts = (citation: CitationType) => {
  const emoji = selectEmoji(
    citation?.content?.type,
    citation?.content?.fileType
  );

  return {
    emoji,
    name: citation?.content?.name,
    size: citation?.content?.fileSize
      ? prettyBytes(citation?.content?.fileSize)
      : undefined,
    text: citation?.text,
  };
};
