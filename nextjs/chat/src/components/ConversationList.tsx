import { useMemo } from 'react';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button } from '@nextui-org/react';
import dayjs from 'dayjs';
import { ConversationResults } from 'graphlit-client/dist/generated/graphql-types';

interface ConversationListProps {
  conversationId: string | null;
  conversations: ConversationResults['results'] | null | undefined;
  loading: boolean;
  onDeleteConversation: (id: string) => void;
  onSelectConversation: (id: string) => void;
}

interface GroupedConversations {
  today: ConversationResults['results'];
  yesterday: ConversationResults['results'];
  last7Days: ConversationResults['results'];
  last30Days: ConversationResults['results'];
}

/**
 * Group conversations by time frames: today, yesterday, last 7 days, and last 30 days.
 * @param conversations - The list of conversations to group.
 * @returns An object containing grouped conversations.
 */
const groupConversationsByTimeFrame = (
  conversations: ConversationResults['results']
): GroupedConversations => {
  const now = dayjs();
  const today: ConversationResults['results'] = [];
  const yesterday: ConversationResults['results'] = [];
  const last7Days: ConversationResults['results'] = [];
  const last30Days: ConversationResults['results'] = [];

  conversations?.forEach((conversation) => {
    const creationDate = dayjs(conversation?.creationDate);
    const diff = now.diff(creationDate, 'day');

    if (diff === 0) {
      today.push(conversation);
    } else if (diff === 1) {
      yesterday.push(conversation);
    } else if (diff <= 7) {
      last7Days.push(conversation);
    } else if (diff <= 30) {
      last30Days.push(conversation);
    }
  });

  return { today, yesterday, last7Days, last30Days };
};

const ConversationList = ({
  conversationId,
  conversations,
  loading,
  onDeleteConversation,
  onSelectConversation,
}: ConversationListProps) => {
  // Memoize the grouped conversations to avoid unnecessary re-calculations.
  const { today, yesterday, last7Days, last30Days } = useMemo(
    () => groupConversationsByTimeFrame(conversations ?? []),
    [conversations]
  );

  /**
   * Renders a list of conversations with a given label.
   * @param conversations - The list of conversations to render.
   * @param label - The label for the conversation group.
   * @returns A JSX element containing the rendered conversations.
   */
  const renderConversations = (
    conversations: ConversationResults['results'],
    label: string
  ) => (
    <>
      {conversations && !!conversations.length && (
        <div>
          <h3 className="text-lg font-semibold">{label}</h3>
          {conversations.map((conversation) => {
            if (!conversation) {
              return null;
            }

            return (
              <div key={conversation.id} className="flex">
                <div
                  className={`flex justify-start items-center w-full cursor-pointer rounded-md pr-0 pl-2 ${
                    conversationId === conversation.id
                      ? 'bg-gray-50'
                      : 'hover:bg-gray-50'
                  }`}
                  onClick={() => onSelectConversation(conversation.id)}
                >
                  <p className="truncate flex-grow text-left">
                    {conversation.name}
                  </p>
                  <Button
                    variant="light"
                    isIconOnly
                    onClick={() => onDeleteConversation(conversation.id)}
                    className="rounded-md"
                  >
                    <FontAwesomeIcon icon={faTrash} className="size-4" />
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </>
  );

  return (
    <div className="m-1 mt-2 flex-grow overflow-y-auto">
      {loading && (
        <div className="flex justify-center items-center mt-6">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-gray-200"></div>
        </div>
      )}
      {renderConversations(today, 'Today')}
      {renderConversations(yesterday, 'Yesterday')}
      {renderConversations(last7Days, 'Last 7 Days')}
      {renderConversations(last30Days, 'Last 30 Days')}
    </div>
  );
};

export default ConversationList;
