'use client';

import { useEffect, useRef, useState } from 'react';
import * as React from 'react';
import {
  ConversationMessage,
  ConversationResults,
  ConversationRoleTypes,
  GetConversationQuery,
} from 'graphlit-client/dist/generated/graphql-types';

import ChatPlaceholder from '@/components/ChatPlaceholder';
import ConversationList from '@/components/ConversationList';
import { Message } from '@/components/Message';
import PromptControls from '@/components/PromptControls';
import { Sidebar } from '@/components/Sidebar';
import { useLayout } from '@/context/Layout';
import { ApiPromptResponse, FileData, Message as MessageType } from '@/types';

export default function Home() {
  // Use the isSidebarOpen value from the Layout context
  const { isSidebarOpen } = useLayout();

  // State variables for handling conversations and chat functionality
  const [conversations, setConversations] = useState<
    ConversationResults['results'] | []
  >([]);
  const [conversationsLoading, setConversationsLoading] = useState(false);

  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<MessageType[]>([]);

  const [prompt, setPrompt] = useState<string>('');
  const [files, setFiles] = useState<FileData[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Function to scroll to the bottom of the chat container
  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  };

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to fetch the list of conversations
  const getConversations = async () => {
    setConversationsLoading(true);

    const response = await fetch('/api/conversation');

    if (!response.ok) {
      setConversationsLoading(false);
      console.error('Error fetching conversations');
      return;
    }

    const data = (await response.json()) as ConversationResults;
    setConversations(data.results);
    setConversationsLoading(false);
  };

  // Fetch conversations when the component mounts
  useEffect(() => {
    void getConversations();
  }, []);

  // Handle file input changes and convert files to base64 format
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

    const messages = messageData.map(({ message, role }) => ({
      message,
      role,
    }));

    if (conversationData) {
      setPrompt('');
      setFiles([]);
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

    // Add the user message to the chat
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
        body: JSON.stringify({ files: inputFiles }),
      });

      if (!fileResponse.ok) {
        console.error(fileResponse.statusText);
      }
    }

    // Handle sending the prompt
    if (inputPrompt) {
      const promptResponse = await fetch('/api/conversation/prompt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversationId: conversationId,
          prompt: inputPrompt,
        }),
      });

      if (!promptResponse.ok) {
        console.error(promptResponse.statusText);
        setIsSubmitting(false);
        return;
      }

      // Refresh conversation list if new conversation created
      if (!conversationId) {
        void getConversations();
      }

      const promptData = (await promptResponse.json()) as ApiPromptResponse;

      // Update conversation ID and add assistant's response to the chat
      setConversationId(promptData.conversationId);
      setMessages((m) => [
        ...m,
        {
          message:
            promptData.promptResults?.promptConversation?.message?.message ??
            '',
          role: ConversationRoleTypes.Assistant,
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
        {/* Chat placeholder */}
        {messages.length === 0 && <ChatPlaceholder />}

        {/* Display messages */}
        {messages.length > 0 && (
          <div
            className="w-full flex-grow overflow-y-auto m-auto pb-28"
            ref={chatContainerRef}
          >
            <div className="max-w-screen-md m-auto">
              {messages.map(({ message, role }, index) => (
                <Message key={index} message={message} role={role} />
              ))}
            </div>
          </div>
        )}

        {/* Prompt controls for input and file handling */}
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
