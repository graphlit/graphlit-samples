'use client';

import { useEffect, useRef, useState } from 'react';
import * as React from 'react';
import {
  ConversationRoleTypes,
  CreateConversationMutation,
} from 'graphlit-client/dist/generated/graphql-types';

import ChatPlaceholder from '@/components/ChatPlaceholder';
import { Message } from '@/components/Message';
import PromptControls from '@/components/PromptControls';
import { ApiPromptResponse, Message as MessageType } from '@/types';
import { conversationName } from '@/utils';

export default function Home() {
  // State for managing conversations and chat functionality
  const [conversationId, setConversationId] = useState<
    string | null | undefined
  >(null);
  const [messages, setMessages] = useState<MessageType[]>([]);

  const [prompt, setPrompt] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Scroll to the bottom of the chat container
  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  };

  // Scroll to the bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending a new message or prompt
  const handleSend = async () => {
    const inputPrompt = prompt;

    setIsSubmitting(true);
    setPrompt('');

    // Add the user's message to the chat
    if (inputPrompt) {
      setMessages((m) => [
        ...m,
        { message: inputPrompt, role: ConversationRoleTypes.User },
      ]);
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
          }),
        });

        if (!conversationResponse.ok) {
          const conversationError = (await conversationResponse.json()) as {
            error?: string;
          };

          setMessages((m) => [
            ...m,
            {
              message: conversationError?.error ?? '',
              role: ConversationRoleTypes.Assistant,
            },
          ]);

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
          },
        ]);

        setIsSubmitting(false);
        return;
      }

      const promptData = (await promptResponse.json()) as ApiPromptResponse;

      // Update conversation state if a new conversation was created
      if (!conversationId && cId) {
        setConversationId(cId);
      }

      // Add the assistant's response to the chat
      setMessages((m) => [
        ...m,
        {
          message:
            promptData.promptResults?.askGraphlit?.message?.message ?? '',
          role: ConversationRoleTypes.Assistant,
        },
      ]);
    }

    setIsSubmitting(false);
  };

  return (
    <>
      <main className="w-full flex flex-col h-[calc(100vh-65px)]">
        <div className="flex-1 overflow-hidden flex flex-col">
          {messages.length === 0 && <ChatPlaceholder />}

          {messages.length > 0 && (
            <div className="flex-1 overflow-y-auto" ref={chatContainerRef}>
              <div className="max-w-screen-md m-auto">
                {messages.map(({ message, role }, index) => (
                  <Message
                    key={index}
                    message={message}
                    role={role}
                    index={index}
                  />
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="w-full bg-white mt-auto">
          <div className="w-full max-w-screen-md m-auto">
            <PromptControls
              isSubmitting={isSubmitting}
              prompt={prompt}
              onPrompt={setPrompt}
              onSend={handleSend}
            />
          </div>
        </div>
      </main>
    </>
  );
}
