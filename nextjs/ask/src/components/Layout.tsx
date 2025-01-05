'use client';

import { Navbar } from '@/components/Navbar';

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-full h-screen">
      <Navbar />
      <div className="flex relative" style={{ height: 'calc(100vh - 65px)' }}>
        {children}
      </div>
    </div>
  );
}
