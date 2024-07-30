import * as React from 'react';
import Image from 'next/image';
import { Chip } from '@nextui-org/react';
import { ConversationRoleTypes } from 'graphlit-client/dist/generated/graphql-types';

import { Message as MessageType } from '@/types';

export function Message({ message, role }: MessageType) {
  // Render user message
  if (role === ConversationRoleTypes.User) {
    return (
      <div className="flex justify-end mt-8 mr-2">
        <Chip className="relative max-w-[70%] rounded-3xl bg-[#f4f4f4] px-5 py-5">
          <p className="text-base">{message}</p>
        </Chip>
      </div>
    );
  }

  // Render assistant message
  return (
    <div className="flex mt-8 ml-5">
      <div className="w-full max-w-10">
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
        {message?.split('\n').map((line, index) => (
          <p key={index} className="mt-4 ml-4 text-base">
            {line}
          </p>
        ))}
      </div>
    </div>
  );
}
