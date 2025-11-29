"use client";

import { createContext, useContext, ReactNode } from 'react';
import { useEdition } from '@/hooks/useEdition';
import { Edition, EditionsIndex } from '@/lib/editions';

interface EditionContextType {
  edition: Edition | null;
  editionsIndex: EditionsIndex | null;
  isLoading: boolean;
  error: string | null;
  selectedDate: string | null;
  selectEdition: (date: string) => void;
  refresh: () => void;
}

const EditionContext = createContext<EditionContextType | undefined>(undefined);

export function EditionProvider({ children }: { children: ReactNode }) {
  const editionData = useEdition();

  return (
    <EditionContext.Provider value={editionData}>
      {children}
    </EditionContext.Provider>
  );
}

export function useEditionContext() {
  const context = useContext(EditionContext);
  if (context === undefined) {
    throw new Error('useEditionContext must be used within an EditionProvider');
  }
  return context;
}
