"use client";

import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  ExternalLink,
  Zap,
  MessageSquare,
  Code,
  Eye,
  Image,
  Search,
  Video,
  Crown,
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
    trend: "up" | "down" | "stable"; // Tendência
    delta: number; // Mudança de posição/score
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
      { model: "Gemini 3 Pro", organization: "Google", score: 1492, trend: "up", delta: 12 },
      { model: "Grok 4.1 Thinking", organization: "xAI", score: 1482, trend: "up", delta: 8 },
      { model: "Claude Opus 4.5", organization: "Anthropic", score: 1466, trend: "stable", delta: 0 },
    ],
  },
  {
    id: "webdev",
    name: "WebDev",
    icon: <Code size={14} />,
    color: "#00D4FF",
    topModels: [
      { model: "Claude Opus 4.5 Thinking", organization: "Anthropic", score: 1493, trend: "up", delta: 15 },
      { model: "Claude Opus 4.5", organization: "Anthropic", score: 1472, trend: "stable", delta: 0 },
      { model: "Gemini 3 Pro", organization: "Google", score: 1471, trend: "up", delta: 5 },
    ],
  },
  {
    id: "vision",
    name: "Vision",
    icon: <Eye size={14} />,
    color: "#A855F7",
    topModels: [
      { model: "Gemini 3 Pro", organization: "Google", score: 1398, trend: "up", delta: 10 },
      { model: "Gemini 2.5 Pro", organization: "Google", score: 1362, trend: "down", delta: -3 },
      { model: "ChatGPT-4o", organization: "OpenAI", score: 1348, trend: "up", delta: 6 },
    ],
  },
  {
    id: "text-to-image",
    name: "Text-to-Image",
    icon: <Image size={14} />,
    color: "#10B981",
    topModels: [
      { model: "GPT-5 Image", organization: "OpenAI", score: 1285, trend: "up", delta: 20 },
      { model: "Imagen 4", organization: "Google", score: 1248, trend: "stable", delta: 0 },
      { model: "DALL-E 4", organization: "OpenAI", score: 1220, trend: "down", delta: -5 },
    ],
  },
  {
    id: "search",
    name: "Search",
    icon: <Search size={14} />,
    color: "#F59E0B",
    topModels: [
      { model: "Gemini 2.5 Pro Grounding", organization: "Google", score: 1312, trend: "up", delta: 8 },
      { model: "o3-search", organization: "OpenAI", score: 1298, trend: "up", delta: 12 },
      { model: "Grok 4 Search", organization: "xAI", score: 1285, trend: "stable", delta: 0 },
    ],
  },
  {
    id: "text-to-video",
    name: "Text-to-Video",
    icon: <Video size={14} />,
    color: "#EC4899",
    topModels: [
      { model: "Veo 3.1 Audio", organization: "Google", score: 1245, trend: "up", delta: 18 },
      { model: "Sora 2 Pro", organization: "OpenAI", score: 1228, trend: "up", delta: 7 },
      { model: "Veo 3", organization: "Google", score: 1215, trend: "down", delta: -2 },
    ],
  },
];

// Escala fixa para todos os gráficos
const MAX_ELO_SCALE = 1500;

// Componente de barra de progresso com escala fixa
function ScoreBar({ 
  score, 
  color 
}: { 
  score: number; 
  color: string;
}) {
  // Escala fixa de 1500 para todos - leitura consistente
  const percentage = (score / MAX_ELO_SCALE) * 100;
  
  return (
    <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="h-full rounded-full"
        style={{ backgroundColor: color }}
      />
    </div>
  );
}

// Componente de indicador de tendência
function TrendIndicator({ trend, delta }: { trend: "up" | "down" | "stable"; delta: number }) {
  if (trend === "up") {
    return (
      <span className="flex items-center gap-0.5 text-[9px] text-emerald-400">
        <TrendingUp size={10} />
        +{delta}
      </span>
    );
  }
  if (trend === "down") {
    return (
      <span className="flex items-center gap-0.5 text-[9px] text-red-400">
        <TrendingDown size={10} />
        {delta}
      </span>
    );
  }
  return (
    <span className="flex items-center gap-0.5 text-[9px] text-white/30">
      <Minus size={10} />
    </span>
  );
}

export default function AIPulseDashboard() {
  // Calcular score máximo para as barras de progresso
  const maxScore = Math.max(...ARENA_CATEGORIES.flatMap(c => c.topModels.map(m => m.score)));

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
              <p className="text-xs text-white/50">LMArena Leaderboards • Atualizado: 29/11/2025</p>
            </div>
          </div>
          
          {/* Link externo */}
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

        {/* Leaderboard Cards Grid com Barras de Progresso */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {ARENA_CATEGORIES.map((category, catIndex) => (
            <motion.div
              key={category.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: catIndex * 0.05 }}
              className="glass-card rounded-xl p-3 border border-white/5 hover:border-white/10 transition-all"
            >
              {/* Category Header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-1.5">
                  <span style={{ color: category.color }}>{category.icon}</span>
                  <span className="text-xs font-medium text-white/70">{category.name}</span>
                </div>
                {/* Badge do líder */}
                <Crown size={12} className="text-electric-amber/60" />
              </div>

              {/* Top 3 Models com Barras - Escala fixa de 2000 */}
              <div className="space-y-2.5">
                {category.topModels.map((model, index) => (
                  <div key={model.model} className="space-y-1">
                    {/* Nome e Score */}
                    <div className="flex items-center gap-1.5">
                      <span
                        className={`w-4 h-4 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 ${
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
                      <div className="flex items-center gap-1.5">
                        <TrendIndicator trend={model.trend} delta={model.delta} />
                        <span className="text-[10px] font-mono text-white/50">{model.score}</span>
                      </div>
                    </div>
                    {/* Barra de Progresso - Escala fixa de 2000 */}
                    <ScoreBar score={model.score} color={category.color} />
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
