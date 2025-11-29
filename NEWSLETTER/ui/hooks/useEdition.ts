"use client";

import { useState, useEffect, useCallback } from 'react';
import { 
  Edition, 
  EditionsIndex, 
  loadEditionsIndex, 
  loadEdition, 
  loadLatestEdition 
} from '@/lib/editions';

interface UseEditionReturn {
  edition: Edition | null;
  editionsIndex: EditionsIndex | null;
  isLoading: boolean;
  error: string | null;
  selectedDate: string | null;
  selectEdition: (date: string) => void;
  refresh: () => void;
}

/**
 * Hook para gerenciar carregamento de edições
 * Por padrão, carrega a edição mais recente
 */
export function useEdition(): UseEditionReturn {
  const [edition, setEdition] = useState<Edition | null>(null);
  const [editionsIndex, setEditionsIndex] = useState<EditionsIndex | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  // Carrega o índice e a edição mais recente
  const loadInitialData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Carregar índice
      const index = await loadEditionsIndex();
      setEditionsIndex(index);
      setSelectedDate(index.latest);
      
      // Carregar edição mais recente
      const latestEdition = await loadEdition(index.latest);
      setEdition(latestEdition);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar edição');
      console.error('Erro ao carregar edição:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Seleciona uma edição específica
  const selectEdition = useCallback(async (date: string) => {
    if (date === selectedDate) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const editionData = await loadEdition(date);
      setEdition(editionData);
      setSelectedDate(date);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar edição');
      console.error('Erro ao carregar edição:', err);
    } finally {
      setIsLoading(false);
    }
  }, [selectedDate]);

  // Recarrega os dados
  const refresh = useCallback(() => {
    loadInitialData();
  }, [loadInitialData]);

  // Carrega dados iniciais
  useEffect(() => {
    loadInitialData();
  }, [loadInitialData]);

  return {
    edition,
    editionsIndex,
    isLoading,
    error,
    selectedDate,
    selectEdition,
    refresh,
  };
}
