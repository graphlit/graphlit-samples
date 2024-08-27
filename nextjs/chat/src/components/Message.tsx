import * as React from 'react';
import Image from 'next/image';
import { Accordion, AccordionItem, Chip } from '@nextui-org/react';
import { Key } from '@react-types/shared';
import { ConversationRoleTypes } from 'graphlit-client/dist/generated/graphql-types';

import { Message as MessageType } from '@/types';
import { getCitationParts } from '@/utils';

// Component to render a message, which could be from the user or assistant, with optional citations
export function Message({
  message,
  role,
  citations,
  index: messageIndex,
}: MessageType & { index: number }) {
  // State to manage selected keys in the Accordion component
  const [selectedKeys, setSelectedKeys] = React.useState<'all' | Set<Key>>(
    new Set([])
  );

  // Handle scrolling to the specific citation when it is clicked
  const handleCitationClick = (index: number) => {
    setSelectedKeys(new Set([`${index}`]));
    setTimeout(() => {
      const section = document.getElementById(
        `message-${messageIndex}-accordion-${index}`
      );
      section?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 500);
  };

  // Render the user's message in a Chip component if the role is 'User'
  if (role === ConversationRoleTypes.User) {
    return (
      <div className="flex justify-end mt-8 mr-2">
        <Chip className="relative max-w-[70%] rounded-3xl bg-[#f4f4f4] px-5 py-5">
          <p className="text-base">{message}</p>
        </Chip>
      </div>
    );
  }

  // Prepare citation elements for replacing placeholders in the message text
  const citationElements: { [key: string]: React.ReactNode } = {};

  if (citations?.length) {
    for (let i = 0; i < citations.length; i++) {
      citationElements[`[${i + 1}]`] = (
        <span
          className="cursor-pointer text-primary"
          onClick={() => handleCitationClick(i + 1)}
        >{`[${i + 1}]`}</span>
      );
    }
  }

  // Render the assistant's message, which may include citations
  return (
    <div className="flex mt-8 ml-5">
      {/* Assistant's avatar or logo */}
      <div className="min-w-10 max-w-10 w-10">
        <div className="border rounded-full mt-2 p-2">
          <Image
            src="/images/graphlit-logo.svg"
            width={24}
            height={24}
            alt="Graphlit logo"
          />
        </div>
      </div>
      <div>
        {/* Split message text into lines and replace citation placeholders with clickable elements */}
        {message?.split('\n').map((line, index) => (
          <p key={index} className="mt-4 ml-4 text-base">
            {line
              .split(/(\[\d\])/)
              .map((part, subIndex) =>
                citationElements[part] ? (
                  <React.Fragment key={subIndex}>
                    {citationElements[part]}
                  </React.Fragment>
                ) : (
                  part
                )
              )}
          </p>
        ))}
        {/* If citations exist, render them within an Accordion component */}
        {citations && (
          <div className="mt-2 px-2">
            <Accordion
              isCompact
              variant="splitted"
              selectedKeys={selectedKeys}
              onSelectionChange={(keys) => setSelectedKeys(keys)}
            >
              {citations.map((citation, index) => {
                const { emoji, name, size, text } = getCitationParts(citation);

                return (
                  <AccordionItem
                    id={`message-${messageIndex}-accordion-${index + 1}`}
                    key={index + 1}
                    title={
                      <div>
                        {emoji}
                        <span className="pl-4 text-sm">{name}</span>
                        <span className="pl-4 text-dark-default-200 text-xs">
                          {size}
                        </span>
                      </div>
                    }
                    className="rounded-xl px-4 bg-gray-50 shadow-none"
                  >
                    {/* Render each line of the citation text */}
                    <div className="mb-3 p-4 bg-white rounded-xl">
                      {text?.split('\n').map((line, index) => (
                        <p key={index} className="mt-2">
                          {line}
                        </p>
                      ))}
                    </div>
                  </AccordionItem>
                );
              })}
            </Accordion>
          </div>
        )}
      </div>
    </div>
  );
}
