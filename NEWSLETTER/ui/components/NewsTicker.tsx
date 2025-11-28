"use client";

import { motion } from "framer-motion";
import { ExternalLink, Sparkles } from "lucide-react";
import Image from "next/image";
import { useState, useEffect } from "react";
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

export default function NewsTicker({ items, speed = 60 }: NewsTickerProps) {
  // Estado para items (evita hydration error)
  const [newsItems, setNewsItems] = useState<NewsItem[]>([]);
  
  // Carregar items apenas no cliente
  useEffect(() => {
    if (items) {
      setNewsItems(items);
    } else {
      const randomVideos = getRandomRealNewsItems(10).map(video => ({
        id: video.video_id,
        title: video.title,
        channel: video.channel,
        thumbnail: `https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`,
        url: video.url,
        category: "IA News",
        emoji: "🤖",
      }));
      setNewsItems(randomVideos);
    }
  }, [items]);
  
  // Mostrar loading enquanto carrega
  if (newsItems.length === 0) {
    return (
      <div className="w-full py-8">
        <div className="flex items-center justify-center h-32 glass-card rounded-2xl">
          <p className="body-sm opacity-50">Carregando notícias...</p>
        </div>
      </div>
    );
  }
  
  // Duplicar items para loop infinito seamless
  const duplicatedItems = [...newsItems, ...newsItems, ...newsItems];

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
            x: [0, -100 * newsItems.length + "%"],
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
    <motion.article
      className="relative flex-shrink-0 w-64 glass-card rounded-xl overflow-hidden group cursor-pointer"
      whileHover={{ scale: 1.02, y: -4 }}
      transition={{ duration: 0.2 }}
    >
      <a href={item.url} target="_blank" rel="noopener noreferrer" className="block">
        {/* Thumbnail - 30% menor */}
        <div className="relative h-28 overflow-hidden">
          <Image
            src={item.thumbnail}
            alt={item.title}
            fill
            className="object-cover transition-transform duration-300 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-void via-transparent to-transparent" />
        </div>

        {/* Content */}
        <div className="p-3">
          <h3 className="font-heading font-bold text-xs line-clamp-2 mb-1 group-hover:text-electric-blue transition-colors">
            {item.title}
          </h3>
          <p className="text-xs opacity-70">{item.channel}</p>
        </div>

        {/* Hover indicator */}
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-electric-blue to-electric-purple transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300" />
      </a>
    </motion.article>
  );
}
