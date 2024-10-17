import React from 'react';
import { faPenToSquare } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button } from '@nextui-org/react';

interface SidebarProps {
  children: React.ReactNode;
  isOpen: boolean;
  onNewConversation: () => void;
}

export function Sidebar({ children, isOpen, onNewConversation }: SidebarProps) {
  return (
    <div
      className={`flex-shrink-0 transform h-full absolute md:relative ${
        isOpen ? 'w-full md:w-[360px]' : 'w-0'
      } transition-all duration-300 ease-in-out`}
      style={{ zIndex: 2 }}
    >
      <div
        className={`fixed top-0 left-0 h-full border-b-light-background border-r w-full md:w-[360px] transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-transform duration-300 ease-in-out`}
        style={{ backgroundColor: '#fff' }}
      >
        <div className="p-4 h-full flex flex-col">
          <div className="flex justify-end pr-1">
            <Button
              isIconOnly
              onClick={onNewConversation}
              className="rounded-md bg-primary text-white"
            >
              <FontAwesomeIcon icon={faPenToSquare} />
            </Button>
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
