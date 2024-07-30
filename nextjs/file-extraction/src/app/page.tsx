'use client';

import { ChangeEvent, useRef, useState } from 'react';
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Accordion, AccordionItem, Button, Divider } from '@nextui-org/react';
import { Content as ContentType } from 'graphlit-client/dist/generated/graphql-types';

import Content from '@/components/Content';
import { FileData } from '@/types';

export default function Home() {
  // Ref to access the file input element
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [responses, setResponses] = useState<ContentType[] | null>(null);

  // Trigger file input click
  const handleUploadClick = () => {
    fileInputRef?.current?.click();
  };

  /**
   * Handle file selection and upload
   * @param files - Array of files selected by the user
   */
  const handleFileChange = async (files: File[]) => {
    setResponses(null);
    setIsSubmitting(true);

    // Convert files to base64 data URLs
    const fileReaders = files.map((file) => {
      const reader = new FileReader();

      return new Promise<FileData>((resolve) => {
        reader.onload = () => {
          resolve({
            name: file.name,
            base64: (reader.result as string)
              .replace('data:', '')
              .replace(/^.+,/, ''),
            mimeType: file.type as string,
            url: reader.result as string,
          });
        };
        reader.readAsDataURL(file);
      });
    });

    const filesData = await Promise.all(fileReaders);

    // Send files data to the server
    const ingestResponse = await fetch('/api/ingest', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ files: filesData }),
    });

    if (!ingestResponse.ok) {
      console.error(ingestResponse.statusText);
    }

    const data = (await ingestResponse.json()) as ContentType[];

    setResponses(data);
    setIsSubmitting(false);
  };

  /**
   * Handle file input changes
   * @param event - ChangeEvent<HTMLInputElement>
   */
  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    // Convert FileList to File array
    const files = Array.from(event.target.files || []);

    // Process selected files
    handleFileChange(files);

    // Clear input value to allow re-uploading the same file
    if (fileInputRef?.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <main className="w-full max-w-screen-sm mx-auto pt-4 m-2 mb-8">
      <h1 className="text-2xl font-bold">Ingest File</h1>
      <p className="mt-4">
        Ingest PDFs, Excel spreadsheets, Markdown and Word documents, and more.
      </p>
      <div className="mt-2 p-3 flex items-center rounded-xl bg-gray-100">
        <FontAwesomeIcon icon={faCircleInfo} className="mr-2" />
        <p className="ml-2">
          This demo is compatible with{' '}
          <a
            className="text-primary underline"
            target="_blank"
            href="https://docs.graphlit.dev/content-types/files/documents"
          >
            Document
          </a>{' '}
          type files only.
        </p>
      </div>
      <div className="my-4">
        {/* Hidden file input for uploading files */}
        <input
          type="file"
          className="hidden"
          id="file-input"
          multiple
          accept=".pdf, .htm, .html, .mhtml, .docx, .xlsx, .pptx, .rtf, .md, .txt, .text, .csv, .tsv, .log"
          onChange={handleChange}
          ref={fileInputRef}
          disabled={isSubmitting}
        />
        <Button
          color="primary"
          radius="lg"
          size="lg"
          onPress={handleUploadClick}
          isLoading={isSubmitting}
          fullWidth
        >
          Upload
        </Button>
      </div>
      <Divider className="mt-4 mb-4" />
      {!isSubmitting && responses && (
        <>
          <Accordion variant="splitted">
            {responses.map((response, index) => (
              <AccordionItem
                key={index}
                className="w-full relative"
                title={
                  <div className="relative">
                    <p className="text font-bold overflow-hidden text-ellipsis whitespace-nowrap max-w-screen-md">
                      {response?.name}
                    </p>
                  </div>
                }
                subtitle={
                  <p className="text-gray-500 text-sm">
                    {response?.document?.title}
                  </p>
                }
              >
                <Content json={response} markdown={response.markdown} />
              </AccordionItem>
            ))}
          </Accordion>
        </>
      )}
    </main>
  );
}
