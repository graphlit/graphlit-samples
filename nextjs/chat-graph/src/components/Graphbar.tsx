import React, { useEffect, useState } from 'react';
import {
  faChevronRight,
  faProjectDiagram,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button, Tooltip } from '@nextui-org/react';

import NetworkChart from '@/components/EChartsGraph';
import { Message as MessageType } from '@/types';

interface GraphbarProps {
  isOpen: boolean;
  toggleDrawer: () => void;
  messages?: MessageType[];
}

export function Graphbar({ isOpen, toggleDrawer, messages }: GraphbarProps) {
  const [showButton, setShowButton] = useState(!isOpen);
  const [isFullyOpen, setIsFullyOpen] = useState(false); // Track when the drawer is fully open
  const [hasGraphData, setHasGraphData] = useState(false); // Track if the last message has graph data

  // Check if the last message has graph data
  useEffect(() => {
    if (messages && messages.length) {
      const lastMessage = messages[messages.length - 1];
      if (
        lastMessage?.graph &&
        lastMessage.graph.nodes?.length &&
        lastMessage.graph.edges?.length
      ) {
        setHasGraphData(true);
      } else {
        setHasGraphData(false);
      }
    } else {
      setHasGraphData(false);
    }
  }, [messages]);

  // Delay showing the button when the drawer closes and hide it immediately when opening
  useEffect(() => {
    if (!isOpen) {
      const timer = setTimeout(() => {
        setShowButton(true);
        setIsFullyOpen(false); // Set fully open state to false when closing
      }, 500); // Show button after 500ms delay when closing the drawer
      return () => clearTimeout(timer); // Cleanup on unmount or when isOpen changes
    } else {
      setShowButton(false); // Hide button immediately when opening the drawer
      // Set a delay to indicate when the drawer is fully open
      const timer = setTimeout(() => {
        setIsFullyOpen(true); // Set to true when drawer transition completes
      }, 300); // Match this to the transition duration
      return () => clearTimeout(timer); // Cleanup on unmount or when isOpen changes
    }
  }, [isOpen]);

  return (
    <>
      {/* Persist the button after 500ms when the drawer is closed */}
      {showButton && (
        <div className="absolute right-6 top-4 z-10">
          <Tooltip
            content={hasGraphData ? 'Prompt Graph' : 'No graph data available'}
            placement="left"
          >
            <Button
              className={`rounded-md bg-gray-100 ${hasGraphData ? 'bg-primary text-white' : 'bg-gray-100'}`}
              onClick={toggleDrawer}
              isIconOnly
              disabled={!hasGraphData}
            >
              <FontAwesomeIcon icon={faProjectDiagram} />
            </Button>
          </Tooltip>
        </div>
      )}

      <div
        className={`fixed top-18 right-0 h-full border-b-light-background border-l ${
          isOpen ? 'w-[460px] translate-x-0' : 'w-0 translate-x-full'
        } transition-all duration-300 ease-in-out transform`}
        style={{ backgroundColor: '#fff', zIndex: 2 }}
      >
        {isOpen && (
          <div className="absolute top-4 left-4">
            <Button
              className="rounded-md bg-gray-100"
              onClick={toggleDrawer}
              isIconOnly
            >
              <FontAwesomeIcon icon={faChevronRight} />
            </Button>
          </div>
        )}

        <div className="px-4 pt-16 h-full flex flex-col">
          {/* Only render NetworkChart when the drawer is fully open */}
          {isFullyOpen && hasGraphData && <NetworkChart messages={messages} />}
        </div>
      </div>
    </>
  );
}
