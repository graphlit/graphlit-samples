import { Types } from 'graphlit-client';
import { ConversationRoleTypes } from 'graphlit-client/dist/generated/graphql-types';

// Files
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
  status: FileResponseStatus;
  reason: string;
};

export type ApiPromptFilesRequest = {
  files: FileData[];
};

export type ApiPromptFilesResponse = {
  fileResults: FileResponseResult[];
};

// Conversation
export type ApiNewConversationRequest = {
  name: string;
  specificationId: string;
};

export type ApiPromptRequest = {
  conversationId?: string;
  prompt: string;
  specificationId: string;
};

export type ApiPromptResponse = {
  conversationId: string | null;
  promptResults: Types.PromptConversationMutation | null;
};

export type CitationType =
  | NonNullable<
      NonNullable<
        NonNullable<
          Types.PromptConversationMutation['promptConversation']
        >['message']
      >['citations']
    >[number]
  | null;

export type Message = {
  message: string | undefined;
  role: ConversationRoleTypes;
  citations?: CitationType[] | null;
};

export type Conversation = {
  conversationId?: string;
  messages: Message[];
};
