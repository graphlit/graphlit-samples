'use client';

import { useEffect, useRef, useState } from 'react';
import * as React from 'react';
import {
  ConversationMessage,
  ConversationResults,
  ConversationRoleTypes,
  CreateConversationMutation,
  GetConversationQuery,
  Specification,
  SpecificationResults,
} from 'graphlit-client/dist/generated/graphql-types';

import ChatPlaceholder from '@/components/ChatPlaceholder';
import ConversationList from '@/components/ConversationList';
import { Message } from '@/components/Message';
import PromptControls from '@/components/PromptControls';
import { Sidebar } from '@/components/Sidebar';
import { SpecificationSelect } from '@/components/SpecificationSelect';
import { useLayout } from '@/context/Layout';
import { ApiPromptResponse, FileData, Message as MessageType } from '@/types';
import {
  conversationName,
  getConversations,
  mergeDefaultSpecConfig,
  mergeSpecsConfig,
  seedSpecifications,
  seedWorkflows,
} from '@/utils';

export default function Home() {
  // Access isSidebarOpen from the Layout context
  const { isSidebarOpen } = useLayout();

  // State for managing conversations and chat functionality
  const [conversations, setConversations] = useState<
    ConversationResults['results'] | []
  >([]);
  const [conversationsLoading, setConversationsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<
    string | null | undefined
  >(null);
  const [messages, setMessages] = useState<MessageType[]>([]);

  const [prompt, setPrompt] = useState<string>('');
  const [files, setFiles] = useState<FileData[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // State for managing conversation specifications
  const [specifications, setSpecifications] = useState<
    SpecificationResults['results'] | null
  >(null);
  const [specificationId, setSpecificationId] = useState<string | null>(null);

  // State for workflow id
  const [workflowId, setWorkflowId] = useState<string | null>(null);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Scroll to the bottom of the chat container
  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  };

  // Fetch conversations and specifications when the component mounts
  useEffect(() => {
    (async () => {
      setConversationsLoading(true);

      // Seed and fetch available specifications
      const seedResults = await seedSpecifications();

      if (seedResults?.length) {
        const defaultMerged = mergeDefaultSpecConfig(
          seedResults as Specification[]
        );
        const merged = mergeSpecsConfig(seedResults as Specification[]);

        setSpecificationId(defaultMerged?.id);
        setSpecifications(merged);

        const workflow = await seedWorkflows();

        setWorkflowId(workflow?.id || null);
      }

      // Fetch and set conversations
      const conversationResults = await getConversations();
      setConversations(conversationResults);
      setConversationsLoading(false);
    })();
  }, []);

  // Scroll to the bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle specification selection change
  const handleSpecificationChange = async (id: string) => {
    setSpecificationId(id);

    // Update the conversation's specification if one is selected
    if (conversationId) {
      const response = await fetch(
        `/api/conversation/${conversationId}/specification/${id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (!response.ok) {
        console.error(response.statusText);
        return;
      }
    }
  };

  // Handle file input changes and convert files to base64
  const handleFileChange = (files: File[]) => {
    const fileReaders = files.map((file) => {
      const reader = new FileReader();

      return new Promise<FileData>((resolve) => {
        reader.onload = () => {
          resolve({
            name: file.name,
            base64: (reader.result as string)
              .replace('data:', '')
              .replace(/^.+,/, ''),
            mimeType: file.type as string,
            url: reader.result as string,
          });
        };
        reader.readAsDataURL(file);
      });
    });

    Promise.all(fileReaders).then((filesData) => {
      setFiles(filesData);
    });
  };

  // Handle removing a file from the file list
  const handleRemoveFile = (index: number) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  // Handle creating a new conversation
  const handleNewConversation = () => {
    setPrompt('');
    setFiles([]);
    setConversationId(null);
    setMessages([]);
  };

  // Handle selecting a conversation and fetching its messages
  const handleSelectConversation = async (id: string) => {
    const response = await fetch(`/api/conversation/${id}`, {
      method: 'GET',
    });

    if (!response.ok) {
      console.error(response.statusText);
      return;
    }

    const conversationData =
      (await response.json()) as GetConversationQuery['conversation'];

    const messageData = conversationData?.messages as ConversationMessage[];

    const messages = messageData.map(({ message, role, citations }) => ({
      message,
      role,
      citations,
    }));

    if (conversationData) {
      setPrompt('');
      setFiles([]);
      setSpecificationId(
        conversationData?.specification?.id ??
          mergeDefaultSpecConfig(specifications as Specification[]).id
      );
      setConversationId(conversationData.id);
      setMessages(messages);
    }
  };

  // Handle deleting a conversation
  const handleDeleteConversation = async (id: string) => {
    if (conversationId === id) {
      setPrompt('');
      setFiles([]);
      setConversationId(null);
      setMessages([]);
    }

    if (conversations) {
      setConversations(conversations.filter((c) => c?.id !== id));
    }

    const response = await fetch(`/api/conversation/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      console.error(response.statusText);
    }
  };

  // Handle sending a new message or prompt
  const handleSend = async () => {
    const inputPrompt = prompt;
    const inputFiles = files;

    setIsSubmitting(true);
    setPrompt('');
    setFiles([]);

    // Add the user's message to the chat
    if (inputPrompt) {
      setMessages((m) => [
        ...m,
        { message: inputPrompt, role: ConversationRoleTypes.User },
      ]);
    }

    // Handle file upload
    if (inputFiles.length) {
      const fileResponse = await fetch('/api/files', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ files: inputFiles, workflowId }),
      });

      if (!fileResponse.ok) {
        console.error(fileResponse.statusText);
      }
    }

    // Handle sending the prompt
    if (inputPrompt) {
      let cId = conversationId;

      // Create a new conversation if none exists
      if (!cId) {
        const conversationResponse = await fetch(`/api/conversation`, {
          method: 'POST',
          body: JSON.stringify({
            name: conversationName(),
            specificationId,
          }),
        });

        if (!conversationResponse.ok) {
          console.error(conversationResponse.statusText);
          setIsSubmitting(false);
          return;
        }

        const conversationData =
          (await conversationResponse.json()) as CreateConversationMutation['createConversation'];

        cId = conversationData?.id;
      }

      const promptResponse = await fetch('/api/conversation/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversationId: cId,
          prompt: inputPrompt,
          specificationId,
        }),
      });

      if (!promptResponse.ok) {
        const promptError = (await promptResponse.json()) as {
          error?: string;
        };

        setMessages((m) => [
          ...m,
          {
            message: promptError?.error ?? '',
            role: ConversationRoleTypes.Assistant,
            citations:
              promptData.promptResults?.promptConversation?.message?.citations,
          },
        ]);

        setIsSubmitting(false);
        return;
      }

      const promptData = (await promptResponse.json()) as ApiPromptResponse;

      // Update conversation state if a new conversation was created
      if (!conversationId && cId) {
        setConversationId(cId);
        const conversationsData = await getConversations();
        setConversations(conversationsData);
      }

      // Add the assistant's response to the chat
      setMessages((m) => [
        ...m,
        {
          message:
            promptData.promptResults?.promptConversation?.message?.message ??
            '',
          role: ConversationRoleTypes.Assistant,
          citations:
            promptData.promptResults?.promptConversation?.message?.citations,
        },
      ]);
    }

    setIsSubmitting(false);
  };

  return (
    <>
      {/* Sidebar component */}
      <Sidebar isOpen={isSidebarOpen} onNewConversation={handleNewConversation}>
        <ConversationList
          conversationId={conversationId}
          conversations={conversations}
          loading={conversationsLoading}
          onDeleteConversation={handleDeleteConversation}
          onSelectConversation={handleSelectConversation}
        />
      </Sidebar>

      {/* Main content */}
      <main
        className="w-full flex flex-col relative"
        style={{ zIndex: 1, height: 'calc(100vh - 65px)' }}
      >
        {/* Specification selection */}
        {specifications && specificationId && (
          <div className="absolute flex m-4">
            <SpecificationSelect
              specifications={specifications as Specification[]}
              specificationId={specificationId}
              onChange={handleSpecificationChange}
            />
          </div>
        )}

        {/* Placeholder for empty chat */}
        {messages.length === 0 && <ChatPlaceholder />}

        {/* Chat messages */}
        {messages.length > 0 && (
          <div
            className="w-full flex-grow overflow-y-auto m-auto pb-28"
            ref={chatContainerRef}
          >
            <div className="max-w-screen-md m-auto">
              {messages.map(({ message, role, citations }, index) => (
                <Message
                  key={index}
                  message={message}
                  citations={citations}
                  role={role}
                  index={index}
                />
              ))}
            </div>
          </div>
        )}

        {/* Input controls for prompt and files */}
        <div className="w-full absolute bottom-0">
          <div className="w-full max-w-screen-md m-auto bg-white">
            <PromptControls
              files={files}
              isSubmitting={isSubmitting}
              prompt={prompt}
              onPrompt={setPrompt}
              onFileChange={handleFileChange}
              onRemoveFile={handleRemoveFile}
              onSend={handleSend}
            />
          </div>
        </div>
      </main>
    </>
  );
}
