import { KeyboardEvent } from 'react';
import { Button } from '@nextui-org/react';

interface PromptControlsProps {
  isSubmitting: boolean;
  prompt: string;
  onPrompt: (prompt: string) => void;
  onSend: () => void;
}

const PromptControls = ({
  isSubmitting,
  prompt,
  onPrompt,
  onSend,
}: PromptControlsProps) => {
  /**
   * Handle enter key
   * @param event - KeyboardEvent<HTMLInputElement>
   */
  const handleEnter = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && prompt.trim()) {
      void onSend();
    }
  };

  return (
    <div className="w-full pb-4 bg-gray-50 mb-16">
      <div className="rounded-lg bg-white p-4 shadow-md">
        <div className="w-full mb-4">
          {/* Input field for the prompt */}
          <input
            type="text"
            className="w-full bg-gray-50 p-2 border border-gray-300 rounded focus:outline-none"
            placeholder="Ask Graphlit"
            value={prompt}
            onChange={(event) => onPrompt(event.target.value)}
            onKeyDown={handleEnter}
          />
        </div>
        {/* Send button */}
        <Button
          className="bg-light-btn-primary w-full"
          radius="sm"
          onPress={() => onSend()}
          isDisabled={!prompt.trim()}
          isLoading={isSubmitting}
        >
          Send
        </Button>
      </div>
    </div>
  );
};

export default PromptControls;
