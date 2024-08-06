import {
  ConversationResults,
  Specification,
  SpecificationResults,
} from 'graphlit-client/dist/generated/graphql-types';

import { defaultSpec, specifications as specConfigs } from './constants';

// Fetch all conversations from the API
export const getConversations = async () => {
  // Send a GET request to the /api/conversation endpoint
  const response = await fetch('/api/conversation');

  // Check if the response is not ok (status code is not in the range 200-299)
  if (!response.ok) {
    console.error('Error fetching conversations');
    return;
  }

  // Parse the response JSON and cast it to ConversationResults type
  const data = (await response.json()) as ConversationResults;
  // Return the results property which contains the list of conversations
  return data.results;
};

// Fetch all specifications from the API
export const getSpecifications = async () => {
  // Send a GET request to the /api/specifications endpoint
  const response = await fetch('/api/specifications');

  // Check if the response is not ok
  if (!response.ok) {
    console.error('Error fetching specifications');
    return;
  }

  // Parse the response JSON and cast it to SpecificationResults type
  const data = (await response.json()) as SpecificationResults;
  // Return the results property which contains the list of specifications
  return data.results;
};

// Seed new specifications by sending a POST request to the API
export const seedSpecifications = async () => {
  // Send a POST request to the /api/specifications endpoint
  const response = await fetch('/api/specifications', { method: 'POST' });

  // Check if the response is not ok
  if (!response.ok) {
    console.error('Error seeding specifications');
    return;
  }

  // Parse the response JSON and cast it to SpecificationResults type
  const data = (await response.json()) as SpecificationResults;
  // Return the results property which contains the list of newly seeded specifications
  return data.results;
};

// Merge the fetched specifications with the predefined spec configurations
export const mergeSpecsConfig = (specifications: Specification[]) => {
  return specConfigs.map((specConfig) => {
    // Find and return the specification that matches the current specConfig name
    return specifications.find(
      (spec) => spec.name === specConfig.name
    ) as Specification;
  });
};

// Find and return the default specification based on the default model name
export const mergeDefaultSpecConfig = (specifications: Specification[]) => {
  return specifications.find(
    (spec) => spec.name === defaultSpec.name
  ) as Specification;
};
