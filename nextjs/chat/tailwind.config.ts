// noinspection ES6PreferShortImport

import type { Config } from 'tailwindcss';

import { CONSTANTS } from './src/theme/constants';
import colors from './src/theme/nextui/common';
import dark from './src/theme/nextui/dark';
import light from './src/theme/nextui/light';

const { nextui } = require('@nextui-org/react');

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      boxShadow: {
        'custom-card': '0px 1px 2px 0px rgba(0, 0, 0, 0.05)',
      },
      colors: {
        ...colors,
        dark,
        light,
      },
      fontFamily: {
        mona: ['var(--font-mona-sans)'],
        inter: ['var(--font-inter)'],
        jetBrains: ['var(--font-jetbrains-mono)'],
      },
      height: {
        'page-header-height': `${CONSTANTS.PAGE_HEADER.HEIGHT}px`,
        'log-details-height': `calc(100vh - ${CONSTANTS.PAGE_HEADER.HEIGHT}px)`,
      },
      maxHeight: {
        'logs-table-max-height': `calc(100vh - ${CONSTANTS.PAGE_HEADER.HEIGHT + 100}px)`,
      },
      minHeight: {
        'content-height': `calc(100vh - ${CONSTANTS.PAGE_HEADER.HEIGHT + 32}px)`,
        'empty-content-height': `calc(90vh - ${CONSTANTS.PAGE_HEADER.HEIGHT}px)`,
        'empty-storage-height': `calc(100vh - ${CONSTANTS.PAGE_HEADER.HEIGHT + 160}px)`,
      },
      margin: {
        'sidebar-gutter': `${CONSTANTS.SIDEBAR.WIDTH}px`,
      },
    },
  },
  darkMode: 'selector',
  variants: {
    scrollbar: ['rounded'],
  },
  plugins: [
    require('tailwind-scrollbar'),
    nextui({
      defaultTheme: 'light',
      themes: {
        light: {
          colors: {
            light,
          },
        },
        dark: {
          colors: {
            dark,
          },
        },
      },
    }),
  ],
};
export default config;
