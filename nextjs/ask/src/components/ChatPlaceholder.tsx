import React from 'react';
import Image from 'next/image';
import { faComments, faUpload } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const ChatPlaceholder = () => (
  <div className="flex-grow flex justify-center items-center">
    <div>
      <div className="flex justify-center">
        <Image
          src="/images/graphlit-logo.svg"
          width={40}
          height={20}
          alt="Graphlit logo"
        />
      </div>
      <div className="mt-4">
        <p className="m-0.5 text-2xl text-gray-400 font-bold">
          What can we help you with?
        </p>
        <p className="m-0.5 text-lg text-gray-400">
          You can ask for code examples from the Graphlit Python SDK,
          <br />
          or ask anything about the Graphlit Platform.
        </p>
      </div>
    </div>
  </div>
);

export default ChatPlaceholder;
