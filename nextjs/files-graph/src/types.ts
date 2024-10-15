import { Maybe } from '@graphql-tools/utils';
import { Types } from 'graphlit-client';
import {
  ConversationRoleTypes,
  EntityTypes,
} from 'graphlit-client/dist/generated/graphql-types';

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
  workflowId: string;
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

export type GraphType = {
  __typename?: 'Graph';
  nodes?: Array<{
    __typename?: 'GraphNode';
    id: string;
    name: string;
    type: EntityTypes;
    metadata?: string | null;
  } | null> | null;
  edges?: Array<{
    __typename?: 'GraphEdge';
    from: string;
    to: string;
    relation?: string | null;
  } | null> | null;
};

export type Message = {
  message: Maybe<string> | undefined;
  role: ConversationRoleTypes;
  citations?: CitationType[] | null;
  graph?: GraphType | null;
};

export type Conversation = {
  conversationId?: string;
  messages: Message[];
};

export interface Node {
  id: string;
  name: string;
  emoji: string;
  category: number;
  symbol?: string;
  symbolSize?: number;
  itemStyle?: { color: string };
  metadata?: {
    type?: string;
    filetype?: string;
    creationDate?: string;
    [key: string]: any;
  };
}

export interface Link {
  source: string;
  target: string;
}

export interface Category {
  name: string;
  itemStyle?: { color: string };
}

export interface GraphData {
  nodes: Node[];
  links: Link[];
  categories: Category[];
}
