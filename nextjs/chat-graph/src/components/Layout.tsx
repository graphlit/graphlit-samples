'use client';

import { Navbar } from '@/components/Navbar';
import { LayoutProvider } from '@/context/Layout';

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-full h-screen">
      <LayoutProvider>
        <Navbar />
        <div className="flex relative" style={{ height: 'calc(100vh - 65px)' }}>
          {children}
        </div>
      </LayoutProvider>
    </div>
  );
}
