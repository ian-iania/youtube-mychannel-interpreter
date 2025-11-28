"use client";

import { motion } from "framer-motion";
import { ExternalLink, Sparkles } from "lucide-react";
import Image from "next/image";
import { getRandomRealNewsItems } from "@/lib/real-data";

type NewsItem = {
  id: string;
  title: string;
  channel: string;
  thumbnail: string;
  url: string;
  category: string;
  emoji: string;
};

// Mock data - será substituído por dados reais depois
const MOCK_NEWS: NewsItem[] = [
  {
    id: "1",
    title: "Claude Opus 4.5 - Novo modelo revolucionário da Anthropic",
    channel: "AI Engineer",
    thumbnail: "https://i.ytimg.com/vi/I60MFVKFMlc/hqdefault.jpg",
    url: "https://youtube.com/watch?v=I60MFVKFMlc",
    category: "Novos Modelos",
    emoji: "🚀",
  },
  {
    id: "2",
    title: "Google Gemini 3 Build Mode - Codificação gratuita com IA",
    channel: "AICodeKing",
    thumbnail: "https://i.ytimg.com/vi/pbUqW-MWVgY/hqdefault.jpg",
    url: "https://youtube.com/watch?v=pbUqW-MWVgY",
    category: "Novos Modelos",
    emoji: "🚀",
  },
  {
    id: "3",
    title: "GitHub Copilot - Novas features para desenvolvedores",
    channel: "GitHub",
    thumbnail: "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
    url: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    category: "Produtos",
    emoji: "🏢",
  },
  {
    id: "4",
    title: "OpenAI GPT-5 - Vazamento de informações sobre próximo modelo",
    channel: "AI News",
    thumbnail: "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
    url: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    category: "Notícias",
    emoji: "📰",
  },
  {
    id: "5",
    title: "Cursor AI - Nova versão com agentes autônomos",
    channel: "Tech Review",
    thumbnail: "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
    url: "https://youtube.com/watch?v=dQw4w9WgXcQ",
    category: "IDEs",
    emoji: "💻",
  },
];

interface NewsTickerProps {
  items?: NewsItem[];
  speed?: number; // segundos para completar um ciclo
}

export default function NewsTicker({ items, speed = 30 }: NewsTickerProps) {
  // Usar dados reais se items não for fornecido
  const realItems = items || getRandomRealNewsItems(10).map(video => ({
    id: video.video_id,
    title: video.title,
    channel: video.channel,
    thumbnail: `https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`,
    url: video.url,
    category: "IA News",
    emoji: "🤖",
  }));
  
  // Duplicar items para loop infinito seamless
  const duplicatedItems = [...realItems, ...realItems, ...realItems];

  return (
    <div className="w-full overflow-hidden py-8">
      {/* Container do ticker */}
      <div className="relative">
        {/* Gradient fade nas bordas */}
        <div className="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-void to-transparent z-10 pointer-events-none" />
        <div className="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-void to-transparent z-10 pointer-events-none" />

        {/* Ticker scrolling */}
        <motion.div
          className="flex gap-6"
          animate={{
            x: [0, -100 * realItems.length + "%"],
          }}
          transition={{
            x: {
              repeat: Infinity,
              repeatType: "loop",
              duration: speed,
              ease: "linear",
            },
          }}
        >
          {duplicatedItems.map((item, index) => (
            <NewsCard key={`${item.id}-${index}`} item={item} />
          ))}
        </motion.div>
      </div>
    </div>
  );
}

function NewsCard({ item }: { item: NewsItem }) {
  return (
    <motion.a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex-shrink-0 w-[400px] glass-card p-4 rounded-2xl group cursor-pointer relative overflow-hidden"
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ duration: 0.2 }}
    >
      {/* Glow effect on hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-electric-blue/0 via-electric-purple/0 to-electric-blue/0 group-hover:from-electric-blue/10 group-hover:via-electric-purple/10 group-hover:to-electric-blue/10 transition-all duration-300 rounded-2xl" />

      <div className="relative flex gap-4">
        {/* Thumbnail */}
        <div className="relative w-32 h-20 flex-shrink-0 rounded-lg overflow-hidden bg-void-light">
          <Image
            src={item.thumbnail}
            alt={item.title}
            fill
            className="object-cover"
            sizes="128px"
          />
          
          {/* Play overlay */}
          <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <ExternalLink className="w-6 h-6 text-white" />
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          {/* Category badge */}
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs">{item.emoji}</span>
            <span className="text-xs font-mono text-electric-cyan">{item.category}</span>
          </div>

          {/* Title */}
          <h3 className="font-heading font-bold text-sm text-white line-clamp-2 mb-1 group-hover:text-electric-blue transition-colors">
            {item.title}
          </h3>

          {/* Channel */}
          <p className="text-xs text-white/50 flex items-center gap-1">
            <Sparkles className="w-3 h-3" />
            {item.channel}
          </p>
        </div>
      </div>

      {/* Neon border on hover */}
      <div className="absolute inset-0 rounded-2xl border border-electric-blue/0 group-hover:border-electric-blue/50 transition-colors duration-300 pointer-events-none" />
    </motion.a>
  );
}
