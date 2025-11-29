/**
 * Sistema de Edições - Carregamento e gerenciamento de edições da newsletter
 */

// Tipos
export interface EditionVideo {
  video_id: string;
  title: string;
  channel: string;
  duration: string;
  viewCount: number;
  summary: string;
  keyPoints: string[];
  url: string;
  publishedAt: string;
  likeCount: number;
  commentCount: number;
  thumbnail: string;
}

export interface EditionCategory {
  id: string;
  name: string;
  videoCount: number;
  videos: EditionVideo[];
}

export interface Edition {
  date: string;
  title: string;
  generatedAt: string;
  collectedAt: string;
  totalVideos: number;
  categories: EditionCategory[];
}

export interface EditionSummary {
  date: string;
  title: string;
  videoCount: number;
  categoryCount: number;
  generatedAt: string;
}

export interface EditionsIndex {
  latest: string;
  editions: EditionSummary[];
}

// Funções de carregamento
const EDITIONS_BASE_URL = '/editions';

/**
 * Carrega o índice de edições disponíveis
 */
export async function loadEditionsIndex(): Promise<EditionsIndex> {
  const response = await fetch(`${EDITIONS_BASE_URL}/index.json`);
  if (!response.ok) {
    throw new Error('Falha ao carregar índice de edições');
  }
  return response.json();
}

/**
 * Carrega uma edição específica por data
 */
export async function loadEdition(date: string): Promise<Edition> {
  const response = await fetch(`${EDITIONS_BASE_URL}/${date}.json`);
  if (!response.ok) {
    throw new Error(`Falha ao carregar edição ${date}`);
  }
  return response.json();
}

/**
 * Carrega a edição mais recente
 */
export async function loadLatestEdition(): Promise<Edition> {
  const index = await loadEditionsIndex();
  return loadEdition(index.latest);
}

/**
 * Formata a data para exibição
 */
export function formatEditionDate(date: string): string {
  const [year, month, day] = date.split('-');
  return `${day}/${month}/${year}`;
}

/**
 * Formata a data e hora para exibição
 */
export function formatDateTime(isoString: string): string {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}
