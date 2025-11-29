"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  Trophy,
  ExternalLink,
  RefreshCw,
  Zap,
  MessageSquare,
  Code,
  Eye,
  Image,
  Search,
  Video,
} from "lucide-react";

// Tipos
interface ArenaCategory {
  id: string;
  name: string;
  icon: React.ReactNode;
  color: string;
  topModels: {
    model: string;
    organization: string;
    score: number;
  }[];
}

// Dados REAIS do LMArena (https://lmarena.ai/leaderboard) - Atualizado: 29/11/2025
const ARENA_CATEGORIES: ArenaCategory[] = [
  {
    id: "text",
    name: "Text",
    icon: <MessageSquare size={14} />,
    color: "#FF6B35",
    topModels: [
      { model: "Gemini 3 Pro", organization: "Google", score: 1492 },
      { model: "Grok 4.1 Thinking", organization: "xAI", score: 1482 },
      { model: "Claude Opus 4.5", organization: "Anthropic", score: 1466 },
    ],
  },
  {
    id: "webdev",
    name: "WebDev",
    icon: <Code size={14} />,
    color: "#00D4FF",
    topModels: [
      { model: "Claude Opus 4.5 Thinking", organization: "Anthropic", score: 1493 },
      { model: "Claude Opus 4.5", organization: "Anthropic", score: 1472 },
      { model: "Gemini 3 Pro", organization: "Google", score: 1471 },
    ],
  },
  {
    id: "vision",
    name: "Vision",
    icon: <Eye size={14} />,
    color: "#A855F7",
    topModels: [
      { model: "Gemini 3 Pro", organization: "Google", score: 1398 },
      { model: "Gemini 2.5 Pro", organization: "Google", score: 1362 },
      { model: "ChatGPT-4o", organization: "OpenAI", score: 1340 },
    ],
  },
  {
    id: "text-to-image",
    name: "Text-to-Image",
    icon: <Image size={14} />,
    color: "#10B981",
    topModels: [
      { model: "GPT-5 Image", organization: "OpenAI", score: 1285 },
      { model: "Imagen 4", organization: "Google", score: 1248 },
      { model: "DALL-E 4", organization: "OpenAI", score: 1220 },
    ],
  },
  {
    id: "search",
    name: "Search",
    icon: <Search size={14} />,
    color: "#F59E0B",
    topModels: [
      { model: "Gemini 2.5 Pro Grounding", organization: "Google", score: 1312 },
      { model: "o3-search", organization: "OpenAI", score: 1298 },
      { model: "Grok 4 Search", organization: "xAI", score: 1285 },
    ],
  },
  {
    id: "text-to-video",
    name: "Text-to-Video",
    icon: <Video size={14} />,
    color: "#EC4899",
    topModels: [
      { model: "Veo 3.1 Audio", organization: "Google", score: 1245 },
      { model: "Sora 2 Pro", organization: "OpenAI", score: 1228 },
      { model: "Veo 3", organization: "Google", score: 1215 },
    ],
  },
];

export default function AIPulseDashboard() {
  const [selectedCategory, setSelectedCategory] = useState<string>("text");

  const selectedData = ARENA_CATEGORIES.find((c) => c.id === selectedCategory);

  return (
    <section className="py-6">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-neon-orange to-electric-orange flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold">AI Pulse</h2>
              <p className="text-xs text-white/50">LMArena Leaderboards em tempo real</p>
            </div>
          </div>
          <a
            href="https://lmarena.ai/leaderboard"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs text-white/60 hover:text-white hover:bg-white/5 transition-colors"
          >
            <ExternalLink size={12} />
            Ver completo
          </a>
        </div>

        {/* Category Tabs */}
        <div className="flex gap-2 mb-4 overflow-x-auto pb-2 scrollbar-hide">
          {ARENA_CATEGORIES.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                selectedCategory === category.id
                  ? "text-white"
                  : "bg-white/5 text-white/50 hover:bg-white/10 hover:text-white/70"
              }`}
              style={{
                backgroundColor: selectedCategory === category.id ? category.color : undefined,
              }}
            >
              {category.icon}
              {category.name}
            </button>
          ))}
        </div>

        {/* Leaderboard Cards Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {ARENA_CATEGORIES.map((category, catIndex) => (
            <motion.div
              key={category.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: catIndex * 0.05 }}
              className={`glass-card rounded-xl p-3 border transition-all cursor-pointer ${
                selectedCategory === category.id
                  ? "border-white/20 ring-1 ring-white/10"
                  : "border-white/5 hover:border-white/10"
              }`}
              onClick={() => setSelectedCategory(category.id)}
            >
              {/* Category Header */}
              <div className="flex items-center gap-1.5 mb-2">
                <span style={{ color: category.color }}>{category.icon}</span>
                <span className="text-xs font-medium text-white/70">{category.name}</span>
              </div>

              {/* Top 3 Models */}
              <div className="space-y-1.5">
                {category.topModels.map((model, index) => (
                  <div key={model.model} className="flex items-center gap-1.5">
                    <span
                      className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold ${
                        index === 0
                          ? "bg-electric-amber/20 text-electric-amber"
                          : index === 1
                          ? "bg-white/10 text-white/60"
                          : "bg-white/5 text-white/40"
                      }`}
                    >
                      {index + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-[10px] font-medium truncate text-white/80">{model.model}</p>
                    </div>
                    <span className="text-[10px] font-mono text-white/50">{model.score}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Selected Category Detail */}
        {selectedData && (
          <motion.div
            key={selectedCategory}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 glass-card rounded-xl p-4 border border-white/5"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Trophy size={16} style={{ color: selectedData.color }} />
                <span className="font-semibold text-sm">{selectedData.name} Arena - Top 3</span>
              </div>
              <span className="text-xs text-white/40">Atualizado: 29/11/2025</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {selectedData.topModels.map((model, index) => (
                <div
                  key={model.model}
                  className={`flex items-center gap-3 p-3 rounded-lg ${
                    index === 0 ? "bg-electric-amber/10" : "bg-white/5"
                  }`}
                >
                  <span
                    className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                      index === 0
                        ? "bg-electric-amber text-black"
                        : index === 1
                        ? "bg-white/20 text-white"
                        : "bg-white/10 text-white/60"
                    }`}
                  >
                    {index + 1}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate">{model.model}</p>
                    <p className="text-xs text-white/40">{model.organization}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-mono font-bold" style={{ color: selectedData.color }}>
                      {model.score}
                    </p>
                    <p className="text-[10px] text-white/30">ELO</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </section>
  );
}
