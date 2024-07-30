import { Types } from 'graphlit-client';
import { ConversationRoleTypes } from 'graphlit-client/dist/generated/graphql-types';

export type FileData = {
  name: string;
  base64: string;
  mimeType: string;
  url: string;
};

export enum FileResponseStatus {
  OK = 'OK',
  FAILED = 'FAILED',
}

export type FileResponseResult = {
  id?: string;
  status: FileResponseStatus;
  reason: string;
};

export type ApiPromptFilesRequest = {
  files: FileData[];
};

export type ApiPromptResponse = {
  conversationId: string | null;
  promptResults: Types.PromptConversationMutation | null;
};

export type Message = {
  message: string | undefined;
  role: ConversationRoleTypes;
};

export type Conversation = {
  conversationId?: string;
  messages: Message[];
};
