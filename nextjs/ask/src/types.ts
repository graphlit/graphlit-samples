import { Types } from 'graphlit-client';
import { ConversationRoleTypes } from 'graphlit-client/dist/generated/graphql-types';

// Conversation
export type ApiNewConversationRequest = {
  name: string;
};

export type ApiPromptRequest = {
  conversationId?: string;
  prompt: string;
};

export type ApiPromptResponse = {
  conversationId: string | null;
  promptResults: Types.AskGraphlitMutation | null;
};

export type Message = {
  message: string | undefined;
  role: ConversationRoleTypes;
};

export type Conversation = {
  conversationId?: string;
  messages: Message[];
};
