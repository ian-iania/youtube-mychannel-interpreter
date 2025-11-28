import { Edition, Category, Video } from "./types";
import { CATEGORY_META } from "./types";

/**
 * Mock data para desenvolvimento
 * Será substituído por dados reais dos 473 vídeos
 */

// Mock videos
const MOCK_VIDEOS: Video[] = [
  {
    video_id: "I60MFVKFMlc",
    title: "Claude Opus 4.5 (Fully Tested): Anthropic REALLY COOKED with this model!",
    channel: "AICodeKing",
    duration: "11.0",
    views: "14.7K",
    viewCount: 14700,
    summary: "Teste completo do novo Claude Opus 4.5, demonstrando suas capacidades impressionantes em tarefas de codificação e raciocínio.",
    keyPoints: [
      "Novo modelo supera versões anteriores em benchmarks",
      "Melhorias significativas em tarefas de código",
      "Performance excepcional em testes agentic",
    ],
    url: "https://youtube.com/watch?v=I60MFVKFMlc",
    publishedAt: "2025-11-20T10:00:00Z",
    likeCount: 1234,
    commentCount: 89,
  },
  {
    video_id: "pbUqW-MWVgY",
    title: "Google Gemini 3 Build Mode: This FULLY FREE Gemini-3 AI Coder is ACTUALLY INSANE!",
    channel: "AICodeKing",
    duration: "12.0",
    views: "15.2K",
    viewCount: 15200,
    summary: "Demonstração do novo Build Mode do Google Gemini 3, uma ferramenta gratuita de codificação com IA.",
    keyPoints: [
      "Build Mode é completamente gratuito",
      "Gera código de forma eficiente",
      "Interface intuitiva e fácil de usar",
    ],
    url: "https://youtube.com/watch?v=pbUqW-MWVgY",
    publishedAt: "2025-11-21T14:30:00Z",
    likeCount: 987,
    commentCount: 56,
  },
  {
    video_id: "eLDq5TfIHys",
    title: "Claude Just Introduced a New Way To Fix Your UI",
    channel: "AI LABS",
    duration: "11.0",
    views: "42.9K",
    viewCount: 42900,
    summary: "Claude Code apresenta nova funcionalidade para editar e melhorar interfaces de usuário geradas por IA.",
    keyPoints: [
      "Nova feature de edição de UI",
      "Workflow simplificado para ajustes de design",
      "Integração com ferramentas de desenvolvimento",
    ],
    url: "https://youtube.com/watch?v=eLDq5TfIHys",
    publishedAt: "2025-11-22T09:15:00Z",
    likeCount: 2100,
    commentCount: 145,
  },
  {
    video_id: "0Mjd8TbKzxc",
    title: "Gemini CLI 6.0: Google JUST INTEGRATED Gemini-3 into Gemini CLI & IT'S INSANE!",
    channel: "AICodeKing",
    duration: "9.0",
    views: "23.4K",
    viewCount: 23400,
    summary: "Gemini CLI agora utiliza o modelo Gemini 3, trazendo melhorias significativas para desenvolvedores.",
    keyPoints: [
      "Integração com Gemini 3",
      "Novas funcionalidades no CLI",
      "Exemplos práticos de uso",
    ],
    url: "https://youtube.com/watch?v=0Mjd8TbKzxc",
    publishedAt: "2025-11-23T11:00:00Z",
    likeCount: 1567,
    commentCount: 78,
  },
  {
    video_id: "xmbSQz-PNMM",
    title: "AIE CODE Day 2: ft Google Deepmind, Anthropic, Cursor, Netflix, Cline, OpenAI, Meta, and METR",
    channel: "AI Engineer",
    duration: "537.0",
    views: "23.3K",
    viewCount: 23300,
    summary: "Segundo dia da conferência AIE CODE com palestras de grandes empresas de IA.",
    keyPoints: [
      "Participação de líderes da indústria",
      "Discussões sobre futuro da IA",
      "Demonstrações de tecnologias de ponta",
    ],
    url: "https://youtube.com/watch?v=xmbSQz-PNMM",
    publishedAt: "2025-11-24T08:00:00Z",
    likeCount: 1890,
    commentCount: 234,
  },
];

// Mock categories
const MOCK_CATEGORIES: Category[] = [
  {
    id: "novos-modelos",
    emoji: CATEGORY_META["novos-modelos"].emoji,
    name: "Novos Modelos e Atualizações",
    description: CATEGORY_META["novos-modelos"].description,
    videoCount: 17,
    videos: MOCK_VIDEOS.slice(0, 3),
    imagePrompt: CATEGORY_META["novos-modelos"].imagePrompt,
  },
  {
    id: "produtos-empresas",
    emoji: CATEGORY_META["produtos-empresas"].emoji,
    name: "Produtos e Atualizações de Empresas",
    description: CATEGORY_META["produtos-empresas"].description,
    videoCount: 17,
    videos: MOCK_VIDEOS.slice(1, 4),
    imagePrompt: CATEGORY_META["produtos-empresas"].imagePrompt,
  },
  {
    id: "ides-agentes",
    emoji: CATEGORY_META["ides-agentes"].emoji,
    name: "IDEs e Agentes de Código",
    description: CATEGORY_META["ides-agentes"].description,
    videoCount: 15,
    videos: MOCK_VIDEOS.slice(0, 2),
    imagePrompt: CATEGORY_META["ides-agentes"].imagePrompt,
  },
  {
    id: "automacao-workflows",
    emoji: CATEGORY_META["automacao-workflows"].emoji,
    name: "Automação e Workflows",
    description: CATEGORY_META["automacao-workflows"].description,
    videoCount: 3,
    videos: MOCK_VIDEOS.slice(2, 4),
    imagePrompt: CATEGORY_META["automacao-workflows"].imagePrompt,
  },
  {
    id: "notebooklm",
    emoji: CATEGORY_META["notebooklm"].emoji,
    name: "NotebookLM",
    description: CATEGORY_META["notebooklm"].description,
    videoCount: 10,
    videos: MOCK_VIDEOS.slice(0, 2),
    imagePrompt: CATEGORY_META["notebooklm"].imagePrompt,
  },
  {
    id: "cursos-treinamentos",
    emoji: CATEGORY_META["cursos-treinamentos"].emoji,
    name: "Cursos e Treinamentos",
    description: CATEGORY_META["cursos-treinamentos"].description,
    videoCount: 51,
    videos: MOCK_VIDEOS.slice(1, 5),
    imagePrompt: CATEGORY_META["cursos-treinamentos"].imagePrompt,
  },
];

// Mock edition
export const MOCK_EDITION: Edition = {
  id: "2025-11-27",
  weekLabel: "Semana de 27/11/2025",
  dateRange: "24–30 nov 2025",
  tagline: "Sua curadoria semanal de IA e tecnologia, organizada por temas relevantes",
  collectedAt: "2025-11-27T20:22:00Z",
  totalVideos: 473,
  categories: MOCK_CATEGORIES,
  summaryHighlights: MOCK_CATEGORIES.map((cat) => ({
    categoryName: cat.name,
    emoji: cat.emoji,
    videoCount: cat.videoCount,
  })),
};

// Helper function to get random videos for ticker
export function getRandomNewsItems(count: number = 5): Video[] {
  const shuffled = [...MOCK_VIDEOS].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

// Helper function to get category by ID
export function getCategoryById(id: string): Category | undefined {
  return MOCK_CATEGORIES.find((cat) => cat.id === id);
}

// Helper function to get all videos
export function getAllVideos(): Video[] {
  return MOCK_VIDEOS;
}
