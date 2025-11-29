"use client";

import { ReactNode } from 'react';
import { EditionProvider } from '@/contexts/EditionContext';

export default function Providers({ children }: { children: ReactNode }) {
  return (
    <EditionProvider>
      {children}
    </EditionProvider>
  );
}
