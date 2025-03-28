import { ChangeEvent, FC, KeyboardEvent, useRef } from 'react';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button } from '@nextui-org/react';

import FileCard from '@/components/FileCard';
import { FileData } from '@/types';

interface PromptControlsProps {
  files: FileData[];
  isSubmitting: boolean;
  prompt: string;
  onPrompt: (prompt: string) => void;
  onFileChange: (files: File[]) => void;
  onRemoveFile: (id: number) => void;
  onSend: () => void;
}

const PromptControls = ({
  files,
  isSubmitting,
  prompt,
  onPrompt,
  onFileChange,
  onRemoveFile,
  onSend,
}: PromptControlsProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  /**
   * Handle file input changes
   * @param event - ChangeEvent<HTMLInputElement>
   */
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    // Convert FileList to File array
    const files = Array.from(event.target.files || []);

    // Process file changes
    onFileChange(files);

    // Clear input value
    if (fileInputRef?.current) {
      fileInputRef.current.value = '';
    }
  };

  /**
   * Handle enter key
   * @param event - KeyboardEvent<HTMLInputElement>
   */
  const handleEnter = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && (prompt.trim() || files.length)) {
      void onSend();
    }
  };

  return (
    <div className="w-full pb-4">
      <div className="bg-gray-50 rounded-lg">
        {/* Display file cards if there are files */}
        {!!files.length && (
          <div className="p-2.5 pt-1">
            {files.map(({ name, mimeType, url }, index) => (
              <FileCard
                key={index}
                name={name}
                mimeType={mimeType}
                url={url}
                onRemove={() => onRemoveFile(index)}
                isDisabled={isSubmitting}
              />
            ))}
          </div>
        )}
        <div className="flex items-center space-x-2 rounded-md p-3">
          <div>
            {/* Hidden file input for uploading files */}
            <input
              type="file"
              className="hidden"
              id="file-input"
              multiple
              onChange={handleChange}
              ref={fileInputRef}
              disabled={isSubmitting}
            />
            <label
              htmlFor="file-input"
              className="flex items-center justify-center w-10 h-10 bg-gray-200 text-gray-700 rounded-full cursor-pointer hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <FontAwesomeIcon icon={faPlus} />
            </label>
          </div>
          <div className="w-full">
            {/* Input field for the prompt */}
            <input
              type="text"
              className="w-full focus:outline-none bg-gray-50"
              placeholder="Message Graphlit"
              value={prompt}
              onChange={(event) => onPrompt(event.target.value)}
              onKeyDown={handleEnter}
            />
          </div>
          {/* Send button */}
          <Button
            color="primary"
            radius="sm"
            onPress={() => onSend()}
            isDisabled={!prompt.trim() && !files.length}
            isLoading={isSubmitting}
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PromptControls;
