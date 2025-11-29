"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import {
  Trophy,
  Brain,
  Code,
  Calculator,
  MessageSquare,
  Wrench,
  Image,
  Globe,
  ExternalLink,
  TrendingUp,
  TrendingDown,
  Filter,
  Search,
} from "lucide-react";

// Tipos de tarefas para classificação
type TaskType =
  | "all"
  | "reasoning"
  | "coding"
  | "math"
  | "chat"
  | "tool-use"
  | "multimodal"
  | "multilingual"
  | "qa";

interface Benchmark {
  id: string;
  name: string;
  shortName: string;
  description: string;
  taskType: TaskType;
  url: string;
  source: string;
  topModels: {
    model: string;
    organization: string;
    score: number;
    trend?: "up" | "down" | "stable";
  }[];
  lastUpdated: string;
  featured?: boolean;
}

// Dados dos benchmarks organizados por tipo de tarefa
const BENCHMARKS: Benchmark[] = [
  // Chatbot / Arena - DADOS REAIS de https://lmarena.ai/leaderboard (29/11/2025)
  {
    id: "chatbot-arena",
    name: "Chatbot Arena (LMArena)",
    shortName: "Arena",
    description: "Avaliação crowdsourced com sistema ELO baseado em preferência humana",
    taskType: "chat",
    url: "https://lmarena.ai/leaderboard",
    source: "LMArena",
    topModels: [
      { model: "Gemini 3 Pro", organization: "Google", score: 1492, trend: "up" },
      { model: "Grok 4.1 Thinking", organization: "xAI", score: 1482, trend: "up" },
      { model: "Claude Opus 4.5", organization: "Anthropic", score: 1466, trend: "stable" },
      { model: "Grok 4.1", organization: "xAI", score: 1464, trend: "stable" },
      { model: "GPT-5.1 High", organization: "OpenAI", score: 1461, trend: "stable" },
    ],
    lastUpdated: "2025-11-29",
    featured: true,
  },
  // Reasoning
  {
    id: "gpqa",
    name: "GPQA (Graduate-Level Problems)",
    shortName: "GPQA",
    description: "Problemas de nível de pós-graduação em física e matemática",
    taskType: "reasoning",
    url: "https://paperswithcode.com/dataset/gpqa",
    source: "Papers With Code",
    topModels: [
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 59.4 },
      { model: "GPT-4o", organization: "OpenAI", score: 53.6 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 51.2 },
    ],
    lastUpdated: "2024-11-25",
    featured: true,
  },
  {
    id: "hellaswag",
    name: "HellaSwag",
    shortName: "HellaSwag",
    description: "Mede inferência de senso comum em completar frases",
    taskType: "reasoning",
    url: "https://rowanzellers.com/hellaswag/",
    source: "Allen AI",
    topModels: [
      { model: "GPT-4", organization: "OpenAI", score: 95.3 },
      { model: "Claude 3 Opus", organization: "Anthropic", score: 94.8 },
      { model: "Mixtral 8x7B", organization: "Mistral", score: 84.4 },
    ],
    lastUpdated: "2024-11-20",
  },
  {
    id: "arc",
    name: "ARC (Abstract Reasoning Corpus)",
    shortName: "ARC",
    description: "Mede inteligência fluida geral similar a humanos",
    taskType: "reasoning",
    url: "https://github.com/fchollet/ARC",
    source: "François Chollet",
    topModels: [
      { model: "GPT-4o", organization: "OpenAI", score: 91.2 },
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 89.7 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 88.3 },
    ],
    lastUpdated: "2024-11-22",
  },
  // QA & Knowledge
  {
    id: "mmlu",
    name: "MMLU (Massive Multitask Language Understanding)",
    shortName: "MMLU",
    description: "Testa conhecimento em 57 assuntos de nível elementar a profissional",
    taskType: "qa",
    url: "https://paperswithcode.com/dataset/mmlu",
    source: "Papers With Code",
    topModels: [
      { model: "GPT-4o", organization: "OpenAI", score: 88.7 },
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 88.3 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 85.9 },
      { model: "Llama 3.1 405B", organization: "Meta", score: 85.2 },
    ],
    lastUpdated: "2024-11-27",
    featured: true,
  },
  {
    id: "truthfulqa",
    name: "TruthfulQA",
    shortName: "TruthfulQA",
    description: "Mede se o modelo gera respostas verdadeiras em 817 questões",
    taskType: "qa",
    url: "https://github.com/sylinrl/TruthfulQA",
    source: "OpenAI",
    topModels: [
      { model: "GPT-4", organization: "OpenAI", score: 78.5 },
      { model: "Claude 3 Opus", organization: "Anthropic", score: 76.2 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 74.8 },
    ],
    lastUpdated: "2024-11-18",
  },
  // Math
  {
    id: "math",
    name: "MATH Benchmark",
    shortName: "MATH",
    description: "12.500 problemas desafiadores de competições de matemática",
    taskType: "math",
    url: "https://github.com/hendrycks/math",
    source: "Hendrycks et al.",
    topModels: [
      { model: "GPT-4o", organization: "OpenAI", score: 76.6 },
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 71.1 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 67.7 },
    ],
    lastUpdated: "2024-11-26",
    featured: true,
  },
  {
    id: "gsm8k",
    name: "GSM8K",
    shortName: "GSM8K",
    description: "8.500 problemas de matemática de nível escolar",
    taskType: "math",
    url: "https://github.com/openai/grade-school-math",
    source: "OpenAI",
    topModels: [
      { model: "GPT-4o", organization: "OpenAI", score: 95.3 },
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 96.4 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 94.4 },
    ],
    lastUpdated: "2024-11-24",
  },
  // Coding
  {
    id: "humaneval",
    name: "HumanEval",
    shortName: "HumanEval",
    description: "164 problemas de programação para avaliar geração de código",
    taskType: "coding",
    url: "https://github.com/openai/human-eval",
    source: "OpenAI",
    topModels: [
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 92.0 },
      { model: "GPT-4o", organization: "OpenAI", score: 90.2 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 84.1 },
    ],
    lastUpdated: "2024-11-27",
    featured: true,
  },
  {
    id: "mbpp",
    name: "MBPP (Mostly Basic Python Problems)",
    shortName: "MBPP",
    description: "1.000 problemas Python de nível iniciante",
    taskType: "coding",
    url: "https://github.com/google-research/google-research/tree/master/mbpp",
    source: "Google Research",
    topModels: [
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 89.4 },
      { model: "GPT-4o", organization: "OpenAI", score: 87.8 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 83.2 },
    ],
    lastUpdated: "2024-11-23",
  },
  // Tool Use
  {
    id: "bfcl",
    name: "Berkeley Function Calling Leaderboard",
    shortName: "BFCL",
    description: "Avalia capacidade de chamar funções/APIs corretamente",
    taskType: "tool-use",
    url: "https://gorilla.cs.berkeley.edu/leaderboard.html",
    source: "UC Berkeley",
    topModels: [
      { model: "GPT-4o", organization: "OpenAI", score: 88.5 },
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 86.2 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 82.7 },
    ],
    lastUpdated: "2024-11-25",
    featured: true,
  },
  {
    id: "metatool",
    name: "MetaTool Benchmark",
    shortName: "MetaTool",
    description: "Avalia consciência de uso de ferramentas e seleção correta",
    taskType: "tool-use",
    url: "https://github.com/HowieHwong/MetaTool",
    source: "MetaTool Team",
    topModels: [
      { model: "GPT-4", organization: "OpenAI", score: 76.3 },
      { model: "Claude 3 Opus", organization: "Anthropic", score: 72.1 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 68.9 },
    ],
    lastUpdated: "2024-11-20",
  },
  // Multimodal
  {
    id: "mmmu",
    name: "MMMU (Massive Multimodal Multidiscipline Understanding)",
    shortName: "MMMU",
    description: "11.500 questões multimodais de nível universitário",
    taskType: "multimodal",
    url: "https://mmmu-benchmark.github.io/",
    source: "MMMU Team",
    topModels: [
      { model: "GPT-4V", organization: "OpenAI", score: 56.8 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 58.5 },
      { model: "Claude 3 Opus", organization: "Anthropic", score: 54.9 },
    ],
    lastUpdated: "2024-11-26",
    featured: true,
  },
  // Multilingual
  {
    id: "mgsm",
    name: "MGSM (Multilingual GSM)",
    shortName: "MGSM",
    description: "GSM8K traduzido para 10 idiomas para avaliar raciocínio multilíngue",
    taskType: "multilingual",
    url: "https://github.com/google-research/url-nlp/tree/main/mgsm",
    source: "Google Research",
    topModels: [
      { model: "GPT-4o", organization: "OpenAI", score: 91.2 },
      { model: "Claude 3.5 Sonnet", organization: "Anthropic", score: 89.7 },
      { model: "Gemini 1.5 Pro", organization: "Google", score: 88.1 },
    ],
    lastUpdated: "2024-11-22",
  },
];

// Ícones por tipo de tarefa
const TASK_ICONS: Record<TaskType, React.ReactNode> = {
  all: <Filter size={16} />,
  reasoning: <Brain size={16} />,
  coding: <Code size={16} />,
  math: <Calculator size={16} />,
  chat: <MessageSquare size={16} />,
  "tool-use": <Wrench size={16} />,
  multimodal: <Image size={16} />,
  multilingual: <Globe size={16} />,
  qa: <Trophy size={16} />,
};

// Labels por tipo de tarefa
const TASK_LABELS: Record<TaskType, string> = {
  all: "Todos",
  reasoning: "Raciocínio",
  coding: "Código",
  math: "Matemática",
  chat: "Chatbot",
  "tool-use": "Tool Use",
  multimodal: "Multimodal",
  multilingual: "Multilíngue",
  qa: "QA & Conhecimento",
};

export default function BenchmarksPage() {
  const [selectedTask, setSelectedTask] = useState<TaskType>("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Filtrar benchmarks
  const filteredBenchmarks = BENCHMARKS.filter((b) => {
    const matchesTask = selectedTask === "all" || b.taskType === selectedTask;
    const matchesSearch =
      searchQuery === "" ||
      b.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      b.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesTask && matchesSearch;
  });

  // Benchmarks em destaque
  const featuredBenchmarks = BENCHMARKS.filter((b) => b.featured);

  return (
    <main className="min-h-screen bg-void text-white">
      <Header />

      <div className="pt-24 pb-16">
        <div className="container mx-auto px-4">
          {/* Page Header */}
          <motion.div
            className="max-w-3xl mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="gradient-text">Benchmarks</span> & Leaderboards
            </h1>
            <p className="text-lg text-white/60">
              Acompanhe os principais benchmarks de avaliação de modelos de IA, organizados por tipo de tarefa.
              Dados atualizados regularmente das fontes oficiais.
            </p>
          </motion.div>

          {/* Featured Benchmarks */}
          <motion.section
            className="mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Trophy className="text-electric-amber" size={20} />
              Principais Benchmarks
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {featuredBenchmarks.map((benchmark, index) => (
                <BenchmarkCard key={benchmark.id} benchmark={benchmark} index={index} featured />
              ))}
            </div>
          </motion.section>

          {/* Filters */}
          <motion.div
            className="flex flex-col md:flex-row gap-4 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40" />
              <input
                type="text"
                placeholder="Buscar benchmarks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 focus:border-neon-orange/50 focus:outline-none text-sm"
              />
            </div>

            {/* Task Filter Pills */}
            <div className="flex flex-wrap gap-2">
              {(Object.keys(TASK_LABELS) as TaskType[]).map((task) => (
                <button
                  key={task}
                  onClick={() => setSelectedTask(task)}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm transition-all ${
                    selectedTask === task
                      ? "bg-neon-orange text-white"
                      : "bg-white/5 text-white/60 hover:bg-white/10 hover:text-white"
                  }`}
                >
                  {TASK_ICONS[task]}
                  {TASK_LABELS[task]}
                </button>
              ))}
            </div>
          </motion.div>

          {/* All Benchmarks Grid */}
          <motion.section
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="text-xl font-bold mb-6">
              {selectedTask === "all" ? "Todos os Benchmarks" : `Benchmarks de ${TASK_LABELS[selectedTask]}`}
              <span className="text-white/40 font-normal ml-2">({filteredBenchmarks.length})</span>
            </h2>

            <AnimatePresence mode="wait">
              <motion.div
                key={selectedTask + searchQuery}
                className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                {filteredBenchmarks.map((benchmark, index) => (
                  <BenchmarkCard key={benchmark.id} benchmark={benchmark} index={index} />
                ))}
              </motion.div>
            </AnimatePresence>

            {filteredBenchmarks.length === 0 && (
              <div className="text-center py-12 text-white/40">
                Nenhum benchmark encontrado para os filtros selecionados.
              </div>
            )}
          </motion.section>
        </div>
      </div>

      <Footer />
    </main>
  );
}

// Benchmark Card Component
function BenchmarkCard({
  benchmark,
  index,
  featured = false,
}: {
  benchmark: Benchmark;
  index: number;
  featured?: boolean;
}) {
  return (
    <motion.a
      href={benchmark.url}
      target="_blank"
      rel="noopener noreferrer"
      className={`group glass-card rounded-2xl p-5 border transition-all hover:shadow-lg ${
        featured
          ? "border-electric-amber/20 hover:border-electric-amber/50 hover:shadow-electric-amber/10"
          : "border-white/5 hover:border-neon-orange/30 hover:shadow-neon-orange/10"
      }`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-white/60">{TASK_ICONS[benchmark.taskType]}</span>
          <span className="text-xs text-white/40 uppercase tracking-wider">
            {TASK_LABELS[benchmark.taskType]}
          </span>
        </div>
        <ExternalLink size={14} className="text-white/20 group-hover:text-white/60 transition-colors" />
      </div>

      {/* Title */}
      <h3 className="font-bold text-lg mb-2 group-hover:text-neon-orange transition-colors">
        {benchmark.shortName}
      </h3>
      <p className="text-sm text-white/50 mb-4 line-clamp-2">{benchmark.description}</p>

      {/* Top Models */}
      <div className="space-y-2">
        {benchmark.topModels.slice(0, 3).map((model, i) => (
          <div key={model.model} className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2">
              <span
                className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${
                  i === 0
                    ? "bg-electric-amber/20 text-electric-amber"
                    : i === 1
                    ? "bg-white/10 text-white/60"
                    : "bg-white/5 text-white/40"
                }`}
              >
                {i + 1}
              </span>
              <span className="text-white/80 truncate max-w-[120px]">{model.model}</span>
            </div>
            <div className="flex items-center gap-1">
              <span className="font-mono text-white/60">{model.score}</span>
              {model.trend === "up" && <TrendingUp size={12} className="text-acid-green" />}
              {model.trend === "down" && <TrendingDown size={12} className="text-red-400" />}
            </div>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="mt-4 pt-3 border-t border-white/5 flex items-center justify-between text-xs text-white/30">
        <span>{benchmark.source}</span>
        <span>Atualizado: {new Date(benchmark.lastUpdated).toLocaleDateString("pt-BR")}</span>
      </div>
    </motion.a>
  );
}
