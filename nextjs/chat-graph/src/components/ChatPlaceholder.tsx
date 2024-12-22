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
        <p className="m-0.5 text-gray-400">
          <FontAwesomeIcon icon={faUpload} className="mr-2" /> Upload files
        </p>
        <p className="m-0.5 text-gray-400">
          <FontAwesomeIcon icon={faComments} className="mr-1" /> Prompt for
          insights
        </p>
      </div>
    </div>
  </div>
);

export default ChatPlaceholder;
