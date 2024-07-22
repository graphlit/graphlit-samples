import { FC, useState } from 'react';
import { Maybe } from '@graphql-tools/utils';
import { Tab, Tabs } from '@nextui-org/react';
import { GetContentQuery } from 'graphlit-client/dist/generated/graphql-types';
import { CopyBlock, dracula } from 'react-code-blocks';
import Markdown from 'react-markdown';

interface ContentProps {
  markdown?: Maybe<string>;
  json: GetContentQuery['content'];
}

const Content: FC<ContentProps> = ({ markdown, json }) => {
  const [activeTab, setActiveTab] = useState<string | number>('markdown');

  return (
    <Tabs
      aria-label="Response Options"
      selectedKey={activeTab}
      onSelectionChange={setActiveTab}
    >
      <Tab key="markdown" title="Markdown">
        <div className="h-[600px] overflow-y-scroll bg-gray-50 p-4 rounded-xl">
          <Markdown>{markdown}</Markdown>
        </div>
      </Tab>
      <Tab key="json-response" title="JSON Response">
        <div className="h-[600px] overflow-y-scroll rounded-xl">
          <CopyBlock
            text={JSON.stringify(json, null, 2)}
            language="json"
            showLineNumbers={true}
            theme={dracula}
            codeBlock
          />
        </div>
      </Tab>
    </Tabs>
  );
};

export default Content;
