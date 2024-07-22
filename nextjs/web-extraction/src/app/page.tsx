'use client';

import { useState } from 'react';
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  Accordion,
  AccordionItem,
  Button,
  Divider,
  Input,
  Tab,
  Tabs,
} from '@nextui-org/react';
import {
  Content as ContentType,
  GetContentQuery,
  QueryContentsQuery,
} from 'graphlit-client/dist/generated/graphql-types';

import Content from '@/components/Content';
import { validateUrl } from '@/utils/validateUrl';

export default function Home() {
  const [value, setValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isValidUrl, setIsValidUrl] = useState(true);
  const [activeTab, setActiveTab] = useState<string | number>('crawl');
  const [pagesCount, setPagesCount] = useState(2);
  const [responses, setResponses] = useState<ContentType[] | null>(null);
  const [readLimit, setReadLimit] = useState(5);

  // Handle URL input change and validation
  const handleUrlChange = (newValue: string) => {
    setValue(newValue);
    setIsValidUrl(validateUrl(newValue));
  };

  // Function to send the request to the API
  const handleSend = async () => {
    if (!isValidUrl || !value) return;

    setIsLoading(true);
    setResponses(null);
    setPagesCount(0);

    const route = activeTab === 'scrape' ? '/api/scrape' : '/api/crawl';

    if (activeTab === 'scrape') {
      setPagesCount(1);
    }

    try {
      const response = await fetch(route, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ uri: value, limit: readLimit }), // Use read limit state here
      });

      if (activeTab === 'scrape') {
        const data = (await response.json()) as GetContentQuery['content'];

        if (data) {
          setPagesCount(1);
          setResponses([data as ContentType]);
        }
      } else {
        const data = (await response.json()) as QueryContentsQuery['contents'];

        if (data?.results) {
          setPagesCount(data.results.length);
          setResponses(data.results as ContentType[]);
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press to trigger handleSend function
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && value) {
      handleSend();
    }
  };

  return (
    <main className="w-full max-w-screen-lg mx-auto pt-4 m-2 mb-8">
      <h1 className="text-2xl font-bold">Ingest HTML web pages</h1>
      <Tabs
        className="mt-4"
        aria-label="Demo Options"
        selectedKey={activeTab}
        onSelectionChange={setActiveTab}
      >
        <Tab key="crawl" title="Crawl">
          <p>
            Websites are a common source for online knowledge, and Graphlit
            supports creating Web feeds to ingest and index web pages from any
            website.
          </p>
          <div className="mt-2 p-3 flex items-center rounded-xl bg-gray-100">
            <FontAwesomeIcon icon={faCircleInfo} className="mr-2" />
            <p className="ml-2">
              By default, we look for a{' '}
              <b>
                <i>sitemap.xml</i>
              </b>{' '}
              file on the website you provide, and ingest all web pages found in
              the sitemap at or below the provided location in the sitemap. If
              no sitemap exists, we will ingest just the web page at the
              provided URI.
            </p>
          </div>
        </Tab>
        <Tab key="scrape" title="Scrape">
          Any web page can be ingested into Graphlit by providing the URL.
        </Tab>
      </Tabs>
      <div className="flex mt-4 relative gap-4">
        <Input
          type="url"
          label="URL"
          value={value}
          onValueChange={handleUrlChange}
          placeholder="https://www.graphlit.com/"
          variant="bordered"
          isInvalid={!isValidUrl}
          errorMessage="Please enter a valid URL"
          isRequired
          isClearable
          onKeyDown={handleKeyDown}
        />
        {activeTab === 'crawl' && (
          <div className="mb-6 max-w-[100px] w-full">
            <Input
              type="number"
              variant="bordered"
              label="Read limit"
              value={readLimit + ''}
              min={1}
              max={20}
              onChange={(e) => setReadLimit(Number(e.target.value))} // Update state on change
              onKeyDown={handleKeyDown}
            />
          </div>
        )}
        <Button
          className="h-[56px]"
          size="lg"
          color={value ? 'primary' : 'default'}
          onClick={handleSend}
          isLoading={isLoading}
          disabled={!value}
        >
          Run
        </Button>
      </div>
      <Divider className="mt-4 mb-8" />
      {!isLoading && responses && (
        <>
          {pagesCount > 1 && (
            <p className="my-4 mx-1">Total pages scraped: {pagesCount}</p>
          )}
          <Accordion variant="splitted">
            {responses.map((response, index) => (
              <AccordionItem
                key={index}
                className="w-full relative"
                title={
                  <div className="relative">
                    <p className="text font-bold overflow-hidden text-ellipsis whitespace-nowrap max-w-screen-md">
                      {response.document?.description}
                    </p>
                  </div>
                }
                subtitle={
                  <p className="text-gray-500 text-sm">{response.uri}</p>
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
