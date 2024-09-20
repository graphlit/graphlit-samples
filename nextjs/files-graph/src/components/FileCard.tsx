import Image from 'next/image';
import { faFile } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Button } from '@nextui-org/react';

// Define the properties for the FileCard component
interface FileCardProps {
  name: string;
  mimeType: string;
  url: string;
  isDisabled: boolean;
  onRemove: () => void;
}

// Define the FileCard component
const FileCard = ({
  name,
  mimeType,
  url,
  isDisabled,
  onRemove,
}: FileCardProps) => {
  // Check if the file is an image
  if (mimeType.includes('image')) {
    return (
      <div className="mt-2 p-2 flex bg-white rounded-md border border-gray-100">
        <Image
          className="rounded-md"
          src={url}
          alt={name}
          width={48}
          height={48}
        />
        <div className="ml-2 flex-grow">
          <p className="text-base truncate">{name}</p>
          <p className="text-xs text-gray-300">{mimeType}</p>
        </div>
        <div className="flex items-center">
          <Button
            size="sm"
            color="primary"
            radius="sm"
            variant="light"
            onClick={onRemove}
            isDisabled={isDisabled}
          >
            Remove
          </Button>
        </div>
      </div>
    );
  }

  // Render a generic file card if the file is not an image
  return (
    <div className="mt-2 p-2 flex bg-white rounded-md border border-gray-100">
      <div className="w-10 h-10 rounded bg-gray-300 flex justify-center items-center">
        <FontAwesomeIcon icon={faFile} className="text-white" />
      </div>
      <div className="ml-2 flex-grow">
        <p className="text-base truncate">{name}</p>
        <p className="text-xs text-gray-300">{mimeType}</p>
      </div>
      <div className="flex items-center">
        <Button
          size="sm"
          color="primary"
          radius="sm"
          variant="light"
          onClick={onRemove}
          isDisabled={isDisabled}
        >
          Remove
        </Button>
      </div>
    </div>
  );
};

export default FileCard;
