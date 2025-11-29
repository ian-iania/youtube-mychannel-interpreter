"use client";

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Calendar, ChevronDown, Check, Loader2 } from 'lucide-react';
import { EditionsIndex, formatEditionDate } from '@/lib/editions';

interface EditionSelectorProps {
  editionsIndex: EditionsIndex | null;
  selectedDate: string | null;
  onSelect: (date: string) => void;
  isLoading?: boolean;
}

export default function EditionSelector({
  editionsIndex,
  selectedDate,
  onSelect,
  isLoading = false,
}: EditionSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);

  // Mostrar loading ou placeholder enquanto carrega
  if (!editionsIndex) {
    return (
      <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/10 text-sm">
        <Loader2 size={14} className="animate-spin text-white/50" />
        <span className="text-white/50">Carregando...</span>
      </div>
    );
  }

  const selectedEdition = editionsIndex.editions.find(e => e.date === selectedDate);
  const isLatest = selectedDate === editionsIndex.latest;

  return (
    <div className="relative">
      {/* Botão do seletor */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isLoading}
        className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 border border-white/10 hover:border-white/20 transition-colors text-sm"
      >
        {isLoading ? (
          <Loader2 size={14} className="animate-spin text-white/50" />
        ) : (
          <Calendar size={14} className="text-white/50" />
        )}
        
        <span className="text-white/80">
          {selectedEdition ? formatEditionDate(selectedEdition.date) : 'Selecionar edição'}
        </span>
        
        {isLatest && (
          <span className="px-1.5 py-0.5 text-[10px] font-medium bg-acid-green/20 text-acid-green rounded">
            ATUAL
          </span>
        )}
        
        <ChevronDown 
          size={14} 
          className={`text-white/50 transition-transform ${isOpen ? 'rotate-180' : ''}`} 
        />
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <>
            {/* Overlay para fechar */}
            <div 
              className="fixed inset-0 z-40" 
              onClick={() => setIsOpen(false)} 
            />
            
            {/* Lista de edições */}
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="absolute top-full left-0 mt-2 w-64 bg-deep-space border border-white/10 rounded-xl shadow-2xl z-50 overflow-hidden"
            >
              <div className="p-2 border-b border-white/5">
                <span className="text-xs text-white/40 px-2">Edições disponíveis</span>
              </div>
              
              <div className="max-h-64 overflow-y-auto">
                {editionsIndex.editions.map((edition) => {
                  const isSelected = edition.date === selectedDate;
                  const isEditionLatest = edition.date === editionsIndex.latest;
                  
                  return (
                    <button
                      key={edition.date}
                      onClick={() => {
                        onSelect(edition.date);
                        setIsOpen(false);
                      }}
                      className={`w-full flex items-center gap-3 px-3 py-2.5 text-left hover:bg-white/5 transition-colors ${
                        isSelected ? 'bg-white/10' : ''
                      }`}
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-medium text-white">
                            {formatEditionDate(edition.date)}
                          </span>
                          {isEditionLatest && (
                            <span className="px-1.5 py-0.5 text-[10px] font-medium bg-acid-green/20 text-acid-green rounded">
                              ATUAL
                            </span>
                          )}
                        </div>
                        <div className="text-xs text-white/40 mt-0.5">
                          {edition.videoCount} vídeos • {edition.categoryCount} categorias
                        </div>
                      </div>
                      
                      {isSelected && (
                        <Check size={16} className="text-acid-green" />
                      )}
                    </button>
                  );
                })}
              </div>
              
              {editionsIndex.editions.length === 0 && (
                <div className="p-4 text-center text-white/40 text-sm">
                  Nenhuma edição disponível
                </div>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
