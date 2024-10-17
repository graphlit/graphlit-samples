import {
  icon,
  IconDefinition,
  library,
} from '@fortawesome/fontawesome-svg-core';
import {
  faBan,
  faBook,
  faBug,
  faBuilding,
  faCalendarAlt,
  faCapsules,
  faChartBar,
  faCode,
  faCog,
  faComment,
  faCube,
  faDatabase,
  faDna,
  faEnvelope,
  faFileAlt,
  faGlobe,
  faHeartbeat,
  faImage,
  faNewspaper,
  faRobot,
  faSearch,
  faStethoscope,
  faTag,
  faUser,
  faVial,
  faVideo,
  faVolumeUp,
  faWrench,
} from '@fortawesome/free-solid-svg-icons';
import { Types } from 'graphlit-client';
import {
  ConversationResults,
  Specification,
  SpecificationResults,
  Workflow,
} from 'graphlit-client/dist/generated/graphql-types';
import prettyBytes from 'pretty-bytes';

import { CitationType } from '@/types';

import { defaultSpec, specifications as specConfigs } from './constants';

library.add(
  faFileAlt,
  faTag,
  faUser,
  faBuilding,
  faGlobe,
  faCube,
  faCog,
  faDatabase,
  faCalendarAlt,
  faHeartbeat,
  faBook,
  faCapsules,
  faDna,
  faSearch,
  faBan,
  faVial,
  faRobot,
  faStethoscope,
  faWrench,
  faEnvelope,
  faCode,
  faVideo,
  faVolumeUp,
  faImage,
  faNewspaper,
  faBug
);

// Fetches a list of conversations from the API
export const getConversations = async () => {
  const response = await fetch('/api/conversation');
  if (!response.ok) {
    console.error('Error fetching conversations');
    return;
  }
  const data = (await response.json()) as ConversationResults;
  return data.results;
};

// Seeds new specifications by sending a request to the API
export const seedSpecifications = async () => {
  const response = await fetch('/api/specifications', { method: 'POST' });
  if (!response.ok) {
    console.error('Error seeding specifications');
    return;
  }
  const data = (await response.json()) as SpecificationResults;
  return data.results;
};

export const seedWorkflows = async () => {
  const response = await fetch('/api/workflows', { method: 'POST' });
  if (!response.ok) {
    console.error('Error fetching workflows');
    return;
  }
  return (await response.json()) as Workflow;
};

// Merges fetched specifications with predefined configurations
export const mergeSpecsConfig = (specifications: Specification[]) => {
  return specConfigs.map((specConfig) => {
    return specifications.find(
      (spec) => spec.name === specConfig.name
    ) as Specification;
  });
};

// Retrieves the default specification from the fetched specifications
export const mergeDefaultSpecConfig = (specifications: Specification[]) => {
  return specifications.find(
    (spec) => spec.name === defaultSpec.name
  ) as Specification;
};

// Generates a conversation name based on the current date and time
export const conversationName = () => {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  const ampm = hours >= 12 ? 'PM' : 'AM';
  hours = hours % 12;
  hours = hours ? hours : 12;
  // @ts-ignore
  hours = String(hours).padStart(2, '0');

  return `Conversation ${year}-${month}-${day} ${hours}:${minutes}:${seconds} ${ampm}`;
};

// Selects an emoji based on content and file types
export const selectEmoji = (
  contentType?: Types.Maybe<Types.ContentTypes>,
  fileType?: Types.Maybe<Types.FileTypes>
): string => {
  const contentEmojiMap: { [key: string]: string } = {
    FILE: '📄',
    PAGE: '🌐',
    MESSAGE: '💬',
    TEXT: '📝',
    POST: '📰',
    EMAIL: '📧',
    EVENT: '📅',
    ISSUE: '🐛',
  };

  const fileEmojiMap: { [key: string]: string } = {
    VIDEO: '🎥',
    AUDIO: '🎵',
    IMAGE: '🖼️',
    DOCUMENT: '📃',
    EMAIL: '📧',
    CODE: '💻',
    DATA: '📊',
  };

  if (contentType === 'FILE' && fileType) {
    return fileEmojiMap[fileType] || '📄';
  } else if (contentType) {
    return contentEmojiMap[contentType] || '📄';
  }

  return '📄';
};

// Extracts key information from a citation for UI display
export const getCitationParts = (citation: CitationType) => {
  const emoji = selectEmoji(
    citation?.content?.type,
    citation?.content?.fileType
  );

  return {
    emoji,
    name: citation?.content?.name,
    size: citation?.content?.fileSize
      ? prettyBytes(citation?.content?.fileSize)
      : undefined,
    text: citation?.text,
  };
};

// Emoji mappings
export const selectGraphEmoji = (entityType: string): string => {
  const observableEmojiMap: { [key: string]: string } = {
    CONTENT: '📄',
    LABEL: '🏷️',
    PERSON: '🧑',
    ORGANIZATION: '🏢',
    PLACE: '🌍',
    PRODUCT: '🛍️',
    SOFTWARE: '💻',
    REPO: '🗂️',
    EVENT: '🎉',
    MEDICAL_STUDY: '📊',
    MEDICAL_CONDITION: '🤒',
    MEDICAL_GUIDELINE: '📜',
    MEDICAL_DRUG: '💊',
    MEDICAL_DRUG_CLASS: '🧬',
    MEDICAL_INDICATION: '🔍',
    MEDICAL_CONTRAINDICATION: '🚫',
    MEDICAL_TEST: '🧪',
    MEDICAL_DEVICE: '🦾',
    MEDICAL_THERAPY: '🩺',
    MEDICAL_PROCEDURE: '🔧',
  };

  return observableEmojiMap[entityType] || '📄'; // Default to a document icon
};

// Function to generate an SVG string for a FontAwesome icon using its definition and color
const generateSvgIcon = (
  iconDefinition: IconDefinition,
  color: string
): string => {
  const svgIcon = icon(iconDefinition, {
    // Set the desired styles and attributes
    styles: { color },
    attributes: { fill: color },
  });

  return svgIcon.html[0]; // Returns the SVG string
};

// Function to convert an SVG string to a Base64-encoded Data URI
const svgToDataUri = (svg: string): string => {
  return `data:image/svg+xml;base64,${btoa(svg)}`;
};

// Updated lookupNodeShape function to return a Data URI for the icon
export const lookupNodeShape = (
  entityType: string,
  contentType: string | null,
  fileType: string | null
): { shape: string; icon?: string } => {
  const entityIconMap: { [key: string]: any } = {
    CONTENT: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faFileAlt, '#aec7e8')), // faFileAlt represents 'file-text'
    },
    LABEL: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faTag, '#ffbb78')),
    },
    PERSON: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faUser, '#98df8a')),
    },
    ORGANIZATION: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faBuilding, '#ff9896')),
    },
    PLACE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faGlobe, '#c5b0d5')),
    },
    PRODUCT: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faCube, '#c49c94')),
    },
    SOFTWARE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faCog, '#f7b6d2')),
    },
    REPO: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faDatabase, '#c7c7c7')),
    },
    EVENT: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faCalendarAlt, '#dbdb8d')),
    },
    MEDICAL_STUDY: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faChartBar, '#17becf')),
    },
    MEDICAL_CONDITION: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faHeartbeat, '#d62728')),
    },
    MEDICAL_GUIDELINE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faBook, '#9467bd')),
    },
    MEDICAL_DRUG: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faCapsules, '#bcbd22')),
    },
    MEDICAL_DRUG_CLASS: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faDna, '#1f77b4')),
    },
    MEDICAL_INDICATION: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faSearch, '#2ca02c')),
    },
    MEDICAL_CONTRAINDICATION: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faBan, '#ff7f0e')),
    },
    MEDICAL_TEST: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faVial, '#e377c2')),
    },
    MEDICAL_DEVICE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faRobot, '#7f7f7f')),
    },
    MEDICAL_THERAPY: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faStethoscope, '#8c564b')),
    },
    MEDICAL_PROCEDURE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faWrench, '#17becf')),
    },
  };

  const contentIconMap: { [key: string]: any } = {
    FILE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faFileAlt, '#aec7e8')),
    },
    PAGE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faGlobe, '#aec7e8')),
    },
    MESSAGE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faComment, '#aec7e8')),
    },
    TEXT: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faFileAlt, '#aec7e8')),
    },
    POST: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faNewspaper, '#aec7e8')),
    },
    EMAIL: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faEnvelope, '#aec7e8')),
    },
    EVENT: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faCalendarAlt, '#aec7e8')),
    },
    ISSUE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faBug, '#aec7e8')),
    },
  };

  const fileIconMap: { [key: string]: any } = {
    VIDEO: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faVideo, '#aec7e8')),
    },
    AUDIO: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faVolumeUp, '#aec7e8')),
    },
    IMAGE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faImage, '#aec7e8')),
    },
    DOCUMENT: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faFileAlt, '#aec7e8')),
    },
    EMAIL: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faEnvelope, '#aec7e8')),
    },
    CODE: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faCode, '#aec7e8')),
    },
    DATA: {
      shape: 'image',
      icon: svgToDataUri(generateSvgIcon(faDatabase, '#aec7e8')),
    },
  };

  if (fileType) {
    return fileIconMap[fileType] || contentIconMap.FILE;
  } else if (contentType) {
    return contentIconMap[contentType] || contentIconMap.FILE;
  } else {
    return entityIconMap[entityType] || { shape: 'circle' };
  }
};

// Color mappings
export const lookupNodeColor = (entityType: string): string => {
  const entityColorMap: { [key: string]: string } = {
    CONTENT: '#aec7e8',
    LABEL: '#ffbb78',
    PERSON: '#98df8a',
    ORGANIZATION: '#ff9896',
    PLACE: '#c5b0d5',
    PRODUCT: '#c49c94',
    SOFTWARE: '#f7b6d2',
    REPO: '#c7c7c7',
    EVENT: '#dbdb8d',
    MEDICAL_STUDY: '#17becf',
    MEDICAL_CONDITION: '#d62728',
    MEDICAL_GUIDELINE: '#9467bd',
    MEDICAL_DRUG: '#bcbd22',
    MEDICAL_DRUG_CLASS: '#1f77b4',
    MEDICAL_INDICATION: '#2ca02c',
    MEDICAL_CONTRAINDICATION: '#ff7f0e',
    MEDICAL_TEST: '#e377c2',
    MEDICAL_DEVICE: '#7f7f7f',
    MEDICAL_THERAPY: '#8c564b',
    MEDICAL_PROCEDURE: '#17becf',
  };

  return entityColorMap[entityType] || '#ffffff';
};
