import * as React from 'react';
import { useEffect } from 'react';
import Image from 'next/image';
import { faCopy } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Chip } from '@nextui-org/react';
import { ConversationRoleTypes } from 'graphlit-client/dist/generated/graphql-types';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import ReactMarkdown from 'react-markdown';

import { Message as MessageType } from '@/types';

// Component to render a message, which could be from the user or assistant
export function Message({
  message,
  role,
  index: messageIndex,
}: MessageType & { index: number }) {
  const [copied, setCopied] = React.useState(false);
  const [containsCodeBlock, setContainsCodeBlock] = React.useState(false);

  useEffect(() => {
    setContainsCodeBlock(message ? /```/.test(message) : false);
  }, [message]);

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

  // Render the assistant's message
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
      <div className="flex-1 space-y-2 overflow-hidden relative">
        {/* Copy button */}
        {containsCodeBlock && message && (
          <div className="absolute top-0 right-0">
            <CopyToClipboard text={message} onCopy={() => setCopied(true)}>
              <button className="p-2 text-gray-500 hover:text-gray-700 transition-colors">
                <FontAwesomeIcon icon={faCopy} className="w-4 h-4" />
              </button>
            </CopyToClipboard>
          </div>
        )}
        {/* Render message text as Markdown */}
        <ReactMarkdown className="mt-4 ml-4 text-base">{message}</ReactMarkdown>
      </div>
    </div>
  );
}
