import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import localFont from 'next/font/local';
import { config } from '@fortawesome/fontawesome-svg-core';
import { NextUIProvider } from '@nextui-org/react';

import '@fortawesome/fontawesome-svg-core/styles.css';
import '../../fontawesome';
import './globals.css';

import { Layout } from '@/components/Layout';

config.autoAddCss = false;

export const metadata: Metadata = {
  title: 'Ask Graphlit Sample',
  description: '',
  icons: {
    icon: '/images/favicon.ico',
  },
};

const monaSans = localFont({
  src: '../../public/fonts/Mona-Sans.woff2',
  variable: '--font-mona-sans',
});

const interVar = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const jetBrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-jetbrains-mono',
  display: 'swap',
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${monaSans.variable} ${interVar.variable} ${jetBrainsMono.variable}`}
    >
      <body className="min-h-screen">
        <NextUIProvider>
          <Layout>{children}</Layout>
        </NextUIProvider>
      </body>
    </html>
  );
}
