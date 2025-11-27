/**
 * Tipos TypeScript para IANIA IA NEWS
 * Baseado na estrutura da newsletter
 */

export type Video = {
  video_id: string;
  title: string;
  channel: string;
  duration: string; // em minutos, ex: "11.0"
  views: string; // formatado, ex: "42.9K"
  viewCount: number; // número bruto
  summary: string;
  keyPoints: string[];
  url: string;
  thumbnail?: string;
  publishedAt: string;
  likeCount?: number;
  commentCount?: number;
};

export type Category = {
  id: string;
  emoji: string; // ex: "🚀"
  name: string; // ex: "Novos Modelos e Atualizações"
  description: string;
  videoCount: number;
  videos: Video[];
  imagePrompt?: string; // Prompt para geração multimodal
  imageUrl?: string; // URL da imagem gerada
};

export type Edition = {
  id: string;
  weekLabel: string; // ex: "Semana de 24/11/2025"
  dateRange: string; // ex: "24–30 nov 2025"
  tagline: string;
  collectedAt: string;
  totalVideos: number;
  categories: Category[];
  summaryHighlights: {
    categoryName: string;
    emoji: string;
    videoCount: number;
  }[];
};

export type TabType = "current" | "categories" | "archive";

// Mapeamento de categorias com seus metadados
export const CATEGORY_META: Record<
  string,
  {
    emoji: string;
    description: string;
    imagePrompt: string;
  }
> = {
  "novos-modelos": {
    emoji: "🚀",
    description: "Últimas novidades em modelos de IA, releases e atualizações de LLMs",
    imagePrompt:
      "abstract 3D brain made of glowing polygons, representing new AI models, dark background with electric blue highlights",
  },
  "produtos-empresas": {
    emoji: "🏢",
    description: "Lançamentos, features e anúncios de empresas de IA e tecnologia",
    imagePrompt:
      "modern tech company building with holographic AI logos, neon purple and blue lights, futuristic corporate aesthetic",
  },
  "automacao-workflows": {
    emoji: "⚙️",
    description: "Ferramentas e técnicas para automatizar processos com IA",
    imagePrompt:
      "flowing diagram of nodes and arrows with neon circuits, automation workflow visualization, dark tech background",
  },
  "ides-agentes": {
    emoji: "💻",
    description: "Editores de código, agentes de IA para programação e ferramentas de desenvolvimento",
    imagePrompt:
      "code editor in dark mode with glowing AI assistant orb, programming interface with neon syntax highlighting",
  },
  notebooklm: {
    emoji: "📓",
    description: "Conteúdo específico sobre NotebookLM do Google e suas aplicações",
    imagePrompt:
      "digital notebook with AI-powered pages, glowing notes and connections, Google colors with dark theme",
  },
  "arquitetura-design": {
    emoji: "🏗️",
    description: "Arquitetura de sistemas de IA, design patterns e melhores práticas",
    imagePrompt:
      "architectural blueprint of AI system with glowing connections, technical diagrams, cyber purple highlights",
  },
  "cursos-treinamentos": {
    emoji: "🎓",
    description: "Cursos, tutoriais e conteúdo educacional sobre IA e tecnologia",
    imagePrompt:
      "graduation cap with digital particles, learning path visualization, educational tech aesthetic with neon accents",
  },
  "ferramentas-dev": {
    emoji: "🔧",
    description: "Bibliotecas, frameworks e ferramentas para desenvolvedores",
    imagePrompt:
      "developer toolbox with glowing tools, code libraries and frameworks, technical dark theme with electric blue",
  },
  "ferramentas-midia": {
    emoji: "🎨",
    description: "Ferramentas de IA para criação de imagens, vídeos, áudio e design",
    imagePrompt:
      "creative studio with AI-generated art, media creation tools, colorful gradients with dark background",
  },
  noticias: {
    emoji: "📰",
    description: "Notícias do setor, análises de mercado e discussões sobre o futuro da IA",
    imagePrompt:
      "digital newspaper with holographic headlines, AI news feed, modern journalism aesthetic with neon highlights",
  },
  outros: {
    emoji: "📌",
    description: "Conteúdo relevante que não se encaixa nas categorias principais",
    imagePrompt:
      "abstract collection of diverse tech icons, miscellaneous AI topics, organized chaos with neon organization",
  },
};
