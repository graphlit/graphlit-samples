import React, { useMemo } from 'react';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  Button,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownSection,
  DropdownTrigger,
  SharedSelection,
} from '@nextui-org/react';
import {
  ModelServiceTypes,
  Specification,
} from 'graphlit-client/dist/generated/graphql-types';

import {
  anthropicSpecs,
  azureOpenAiSpecs,
  cohereSpecs,
  deepseekSpecs,
  groqSpecs,
  mistralSpecs,
  openAiSpecs,
  replicateSpecs,
  serviceTypeNames,
} from '@/constants';

// Define the props type for the SpecificationSelect component
type SpecificationSelectProps = {
  specifications: Specification[];
  specificationId: string;
  onChange: (id: string) => void;
};

// SpecificationSelect component for rendering the dropdown menu
export function SpecificationSelect({
  specifications,
  specificationId,
  onChange,
}: SpecificationSelectProps) {
  // Handle specification selection change
  const handleChange = (id: SharedSelection['currentKey']) => {
    onChange(id as string);
  };

  // Memoize the current specification name for performance optimization
  const name = useMemo(() => {
    return specifications.find((spec) => spec.id === specificationId)?.name;
  }, [specifications, specificationId]);

  return (
    <Dropdown>
      <DropdownTrigger>
        <Button variant="light" className="capitalize w-full pr-10">
          {name}
          <div className="absolute right-4">
            <FontAwesomeIcon icon={faChevronDown} />
          </div>
        </Button>
      </DropdownTrigger>
      <DropdownMenu
        aria-label="Single selection example"
        className="h-96 overflow-scroll"
        variant="flat"
        disallowEmptySelection
        selectionMode="single"
        selectedKeys={new Set([specificationId])}
        onSelectionChange={(keys) => handleChange(keys.currentKey)}
      >
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.Anthropic]}>
          {anthropicSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection
          title={serviceTypeNames[ModelServiceTypes.AzureOpenAi]}
        >
          {azureOpenAiSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.Cohere]}>
          {cohereSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.Deepseek]}>
          {deepseekSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.Groq]}>
          {groqSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.Mistral]}>
          {mistralSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.OpenAi]}>
          {openAiSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
        <DropdownSection title={serviceTypeNames[ModelServiceTypes.Replicate]}>
          {replicateSpecs.map((specConfig) => {
            const spec = specifications.find(
              (s) => s.name === specConfig.name
            ) as Specification;

            return (
              <DropdownItem key={spec.id} value={spec.id}>
                {spec.name}
              </DropdownItem>
            );
          })}
        </DropdownSection>
      </DropdownMenu>
    </Dropdown>
  );
}
