"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  Database,
  Cpu,
  Layers,
  Trophy,
  ExternalLink,
  RefreshCw,
  Zap,
  BarChart3,
} from "lucide-react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { REAL_EDITION, getUniqueChannelsCount } from "@/lib/real-data";

// Tipos
interface HuggingFaceStats {
  models: number;
  datasets: number;
  spaces: number;
  modelsTrend: number;
  lastUpdated: string;
}

interface LeaderboardEntry {
  rank: number;
  model: string;
  organization: string;
  elo: number;
  trend: "up" | "down" | "stable";
}

// Dados mock (em produção, viriam de APIs)
const MOCK_HF_STATS: HuggingFaceStats = {
  models: 1_234_567,
  datasets: 356_789,
  spaces: 278_456,
  modelsTrend: 12.5,
  lastUpdated: new Date().toISOString(),
};

const MOCK_LEADERBOARD: LeaderboardEntry[] = [
  { rank: 1, model: "GPT-4o", organization: "OpenAI", elo: 1287, trend: "stable" },
  { rank: 2, model: "Claude 3.5 Sonnet", organization: "Anthropic", elo: 1271, trend: "up" },
  { rank: 3, model: "Gemini 1.5 Pro", organization: "Google", elo: 1260, trend: "up" },
  { rank: 4, model: "Llama 3.1 405B", organization: "Meta", elo: 1248, trend: "down" },
  { rank: 5, model: "Command R+", organization: "Cohere", elo: 1235, trend: "stable" },
];

// Dados de crescimento para o gráfico
const GROWTH_DATA = [
  { month: "Jun", models: 800000, datasets: 280000 },
  { month: "Jul", models: 890000, datasets: 300000 },
  { month: "Aug", models: 980000, datasets: 320000 },
  { month: "Sep", models: 1050000, datasets: 335000 },
  { month: "Oct", models: 1150000, datasets: 350000 },
  { month: "Nov", models: 1234567, datasets: 356789 },
];

// Cores para o pie chart
const CATEGORY_COLORS = [
  "#FF6B35",
  "#00D4FF",
  "#A855F7",
  "#10B981",
  "#F59E0B",
  "#EC4899",
  "#6366F1",
  "#14B8A6",
  "#F97316",
  "#8B5CF6",
  "#64748B",
];

export default function AIPulseDashboard() {
  const [isLoading, setIsLoading] = useState(true);
  const [hfStats, setHfStats] = useState<HuggingFaceStats>(MOCK_HF_STATS);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>(MOCK_LEADERBOARD);

  // Preparar dados das categorias para o pie chart
  const categoryData = REAL_EDITION.categories.map((cat, index) => ({
    name: cat.name,
    value: cat.videoCount,
    color: CATEGORY_COLORS[index % CATEGORY_COLORS.length],
  }));

  useEffect(() => {
    // Simular carregamento
    const timer = setTimeout(() => setIsLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  const formatNumber = (num: number): string => {
    if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
    if (num >= 1_000) return `${(num / 1_000).toFixed(0)}K`;
    return num.toString();
  };

  return (
    <section className="py-8">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-neon-orange to-electric-orange flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold">AI Pulse</h2>
              <p className="text-sm text-white/50">Indicadores em tempo real do ecossistema de IA</p>
            </div>
          </div>
          <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm text-white/60 hover:text-white hover:bg-white/5 transition-colors">
            <RefreshCw size={14} />
            Atualizar
          </button>
        </div>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Hugging Face Stats Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="col-span-1 md:col-span-2 lg:col-span-1 glass-card rounded-2xl p-5 border border-white/5 hover:border-neon-orange/30 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <span className="text-2xl">🤗</span>
                <span className="font-semibold text-sm">Hugging Face</span>
              </div>
              <a
                href="https://huggingface.co"
                target="_blank"
                rel="noopener noreferrer"
                className="opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <ExternalLink size={14} className="text-white/40" />
              </a>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Cpu size={14} className="text-neon-orange" />
                  <span className="text-sm text-white/60">Modelos</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-lg">{formatNumber(hfStats.models)}</span>
                  <span className="flex items-center text-xs text-acid-green">
                    <TrendingUp size={12} />
                    {hfStats.modelsTrend}%
                  </span>
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Database size={14} className="text-electric-cyan" />
                  <span className="text-sm text-white/60">Datasets</span>
                </div>
                <span className="font-bold text-lg">{formatNumber(hfStats.datasets)}</span>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Layers size={14} className="text-electric-purple" />
                  <span className="text-sm text-white/60">Spaces</span>
                </div>
                <span className="font-bold text-lg">{formatNumber(hfStats.spaces)}</span>
              </div>
            </div>

            {/* Mini Chart */}
            <div className="mt-4 h-16">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={GROWTH_DATA}>
                  <defs>
                    <linearGradient id="colorModels" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FF6B35" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#FF6B35" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <Area
                    type="monotone"
                    dataKey="models"
                    stroke="#FF6B35"
                    strokeWidth={2}
                    fill="url(#colorModels)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* LLM Arena Leaderboard Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="col-span-1 md:col-span-2 lg:col-span-1 glass-card rounded-2xl p-5 border border-white/5 hover:border-electric-cyan/30 transition-colors group"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Trophy size={18} className="text-electric-amber" />
                <span className="font-semibold text-sm">LLM Arena</span>
              </div>
              <a
                href="https://lmarena.ai/leaderboard"
                target="_blank"
                rel="noopener noreferrer"
                className="opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <ExternalLink size={14} className="text-white/40" />
              </a>
            </div>

            <div className="space-y-2">
              {leaderboard.slice(0, 5).map((entry, index) => (
                <div
                  key={entry.model}
                  className="flex items-center gap-3 py-1.5 border-b border-white/5 last:border-0"
                >
                  <span
                    className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${
                      index === 0
                        ? "bg-electric-amber text-black"
                        : index === 1
                        ? "bg-white/20"
                        : index === 2
                        ? "bg-neon-orange/20 text-neon-orange"
                        : "bg-white/5 text-white/40"
                    }`}
                  >
                    {entry.rank}
                  </span>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{entry.model}</p>
                    <p className="text-xs text-white/40">{entry.organization}</p>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-sm font-mono">{entry.elo}</span>
                    {entry.trend === "up" && <TrendingUp size={12} className="text-acid-green" />}
                    {entry.trend === "down" && <TrendingDown size={12} className="text-red-400" />}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Nossa Curadoria Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="col-span-1 glass-card rounded-2xl p-5 border border-white/5 hover:border-electric-purple/30 transition-colors"
          >
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 size={18} className="text-electric-purple" />
              <span className="font-semibold text-sm">Esta Semana</span>
            </div>

            <div className="text-center mb-4">
              <div className="text-4xl font-bold gradient-text">{REAL_EDITION.totalVideos}</div>
              <p className="text-sm text-white/50">vídeos curados</p>
            </div>

            <div className="grid grid-cols-2 gap-2 text-center">
              <div className="bg-white/5 rounded-lg p-2">
                <div className="font-bold text-lg">{getUniqueChannelsCount()}</div>
                <p className="text-xs text-white/50">canais</p>
              </div>
              <div className="bg-white/5 rounded-lg p-2">
                <div className="font-bold text-lg">{REAL_EDITION.categories.length}</div>
                <p className="text-xs text-white/50">categorias</p>
              </div>
            </div>
          </motion.div>

          {/* Distribuição por Categoria */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="col-span-1 glass-card rounded-2xl p-5 border border-white/5 hover:border-acid-green/30 transition-colors"
          >
            <div className="flex items-center gap-2 mb-2">
              <span className="text-lg">📊</span>
              <span className="font-semibold text-sm">Distribuição</span>
            </div>

            <div className="h-32">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    cx="50%"
                    cy="50%"
                    innerRadius={30}
                    outerRadius={50}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {categoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: "#1a1a2e",
                      border: "1px solid rgba(255,255,255,0.1)",
                      borderRadius: "8px",
                    }}
                    formatter={(value: number, name: string) => [`${value} vídeos`, name]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="flex flex-wrap gap-1 mt-2">
              {categoryData.slice(0, 4).map((cat, index) => (
                <span
                  key={cat.name}
                  className="text-[10px] px-1.5 py-0.5 rounded-full"
                  style={{ backgroundColor: `${cat.color}20`, color: cat.color }}
                >
                  {cat.name.split(" ")[0]}
                </span>
              ))}
              <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-white/5 text-white/40">
                +{categoryData.length - 4}
              </span>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
