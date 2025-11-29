"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Check, 
  X, 
  Search, 
  Filter, 
  Eye, 
  Download, 
  Mail,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Clock,
  ThumbsUp,
  MessageSquare
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { REAL_EDITION, getAllRealVideos } from "@/lib/real-data";
import { Video, Category } from "@/lib/types";

type SelectedVideo = Video & { order: number };

export default function NewsletterEditor() {
  const [selectedVideos, setSelectedVideos] = useState<Map<string, SelectedVideo>>(new Map());
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"views" | "date" | "likes">("views");
  const [showPreview, setShowPreview] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState<Set<string>>(new Set(["novos-modelos"]));

  // Filtrar e ordenar vídeos
  const filteredVideos = useMemo(() => {
    let videos = getAllRealVideos();

    // Filtrar por busca
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      videos = videos.filter(
        (v) =>
          v.title.toLowerCase().includes(query) ||
          v.channel.toLowerCase().includes(query) ||
          v.summary?.toLowerCase().includes(query)
      );
    }

    // Ordenar
    videos.sort((a, b) => {
      switch (sortBy) {
        case "views":
          return b.viewCount - a.viewCount;
        case "likes":
          return (b.likeCount || 0) - (a.likeCount || 0);
        case "date":
          return new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime();
        default:
          return 0;
      }
    });

    return videos;
  }, [searchQuery, sortBy]);

  // Vídeos por categoria
  const videosByCategory = useMemo(() => {
    const map = new Map<string, Video[]>();
    
    if (selectedCategory === "all") {
      REAL_EDITION.categories.forEach((cat) => {
        const catVideos = filteredVideos.filter((v) => 
          cat.videos.some((cv) => cv.video_id === v.video_id)
        );
        if (catVideos.length > 0) {
          map.set(cat.id, catVideos);
        }
      });
    } else {
      const cat = REAL_EDITION.categories.find((c) => c.id === selectedCategory);
      if (cat) {
        const catVideos = filteredVideos.filter((v) =>
          cat.videos.some((cv) => cv.video_id === v.video_id)
        );
        map.set(cat.id, catVideos);
      }
    }

    return map;
  }, [filteredVideos, selectedCategory]);

  // Toggle seleção de vídeo
  const toggleVideo = (video: Video) => {
    setSelectedVideos((prev) => {
      const newMap = new Map(prev);
      if (newMap.has(video.video_id)) {
        newMap.delete(video.video_id);
        // Reordenar
        let order = 1;
        newMap.forEach((v, k) => {
          newMap.set(k, { ...v, order: order++ });
        });
      } else {
        newMap.set(video.video_id, { ...video, order: newMap.size + 1 });
      }
      return newMap;
    });
  };

  // Toggle categoria expandida
  const toggleCategory = (catId: string) => {
    setExpandedCategories((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(catId)) {
        newSet.delete(catId);
      } else {
        newSet.add(catId);
      }
      return newSet;
    });
  };

  // Selecionar todos de uma categoria
  const selectAllInCategory = (catId: string) => {
    const cat = REAL_EDITION.categories.find((c) => c.id === catId);
    if (!cat) return;

    setSelectedVideos((prev) => {
      const newMap = new Map(prev);
      cat.videos.forEach((video) => {
        if (!newMap.has(video.video_id)) {
          newMap.set(video.video_id, { ...video, order: newMap.size + 1 });
        }
      });
      return newMap;
    });
  };

  // Limpar seleção
  const clearSelection = () => {
    setSelectedVideos(new Map());
  };

  // Obter categoria info
  const getCategoryInfo = (catId: string): Category | undefined => {
    return REAL_EDITION.categories.find((c) => c.id === catId);
  };

  return (
    <div className="min-h-screen bg-void">
      {/* Header */}
      <header className="sticky top-0 z-50 glass-card border-b border-white/10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="text-white/60 hover:text-white transition-colors">
                ← Voltar
              </Link>
              <h1 className="text-xl font-bold">Editor de Newsletter</h1>
            </div>

            <div className="flex items-center gap-4">
              <div className="px-4 py-2 rounded-lg glass-card">
                <span className="text-electric-blue font-bold">{selectedVideos.size}</span>
                <span className="text-white/60 ml-2">vídeos selecionados</span>
              </div>

              <button
                onClick={() => setShowPreview(true)}
                disabled={selectedVideos.size === 0}
                className="btn-secondary px-4 py-2 flex items-center gap-2 disabled:opacity-50"
              >
                <Eye size={18} />
                Preview
              </button>

              <button
                onClick={clearSelection}
                disabled={selectedVideos.size === 0}
                className="px-4 py-2 rounded-lg border border-white/20 hover:border-red-500/50 text-white/60 hover:text-red-400 transition-colors disabled:opacity-50"
              >
                Limpar
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Filters */}
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-wrap items-center gap-4 mb-6">
          {/* Search */}
          <div className="relative flex-1 min-w-[300px]">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40" size={18} />
            <input
              type="text"
              placeholder="Buscar vídeos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-xl glass-card border border-white/10 focus:border-electric-blue/50 outline-none transition-colors"
            />
          </div>

          {/* Category Filter */}
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-3 rounded-xl glass-card border border-white/10 focus:border-electric-blue/50 outline-none transition-colors bg-transparent"
          >
            <option value="all">Todas as Categorias</option>
            {REAL_EDITION.categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.emoji} {cat.name} ({cat.videoCount})
              </option>
            ))}
          </select>

          {/* Sort */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as "views" | "date" | "likes")}
            className="px-4 py-3 rounded-xl glass-card border border-white/10 focus:border-electric-blue/50 outline-none transition-colors bg-transparent"
          >
            <option value="views">Mais Vistos</option>
            <option value="likes">Mais Curtidos</option>
            <option value="date">Mais Recentes</option>
          </select>
        </div>

        {/* Categories with Videos */}
        <div className="space-y-6">
          {Array.from(videosByCategory.entries()).map(([catId, videos]) => {
            const catInfo = getCategoryInfo(catId);
            const isExpanded = expandedCategories.has(catId);
            const selectedInCategory = videos.filter((v) => selectedVideos.has(v.video_id)).length;

            return (
              <div key={catId} className="glass-card rounded-2xl overflow-hidden">
                {/* Category Header */}
                <div
                  className="flex items-center justify-between p-4 cursor-pointer hover:bg-white/5 transition-colors"
                  onClick={() => toggleCategory(catId)}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{catInfo?.emoji}</span>
                    <div>
                      <h2 className="font-bold">{catInfo?.name}</h2>
                      <p className="text-sm text-white/60">
                        {videos.length} vídeos • {selectedInCategory} selecionados
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        selectAllInCategory(catId);
                      }}
                      className="px-3 py-1 text-sm rounded-lg border border-white/20 hover:border-electric-blue/50 hover:text-electric-blue transition-colors"
                    >
                      Selecionar Todos
                    </button>
                    {isExpanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                  </div>
                </div>

                {/* Videos Grid */}
                <AnimatePresence>
                  {isExpanded && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="overflow-hidden"
                    >
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 p-4 pt-0">
                        {videos.map((video) => {
                          const isSelected = selectedVideos.has(video.video_id);
                          const selectedVideo = selectedVideos.get(video.video_id);

                          return (
                            <motion.div
                              key={video.video_id}
                              className={`relative rounded-xl overflow-hidden cursor-pointer transition-all ${
                                isSelected
                                  ? "ring-2 ring-electric-blue shadow-lg shadow-electric-blue/20"
                                  : "hover:ring-1 hover:ring-white/20"
                              }`}
                              onClick={() => toggleVideo(video)}
                              whileHover={{ scale: 1.02 }}
                              whileTap={{ scale: 0.98 }}
                            >
                              {/* Thumbnail */}
                              <div className="relative aspect-video">
                                <Image
                                  src={`https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`}
                                  alt={video.title}
                                  fill
                                  className="object-cover"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />

                                {/* Selection Badge */}
                                {isSelected && (
                                  <div className="absolute top-2 right-2 w-8 h-8 rounded-full bg-electric-blue flex items-center justify-center font-bold">
                                    {selectedVideo?.order}
                                  </div>
                                )}

                                {/* Duration */}
                                <div className="absolute bottom-2 right-2 px-2 py-1 rounded bg-black/70 text-xs flex items-center gap-1">
                                  <Clock size={12} />
                                  {Math.round(parseFloat(video.duration))} min
                                </div>
                              </div>

                              {/* Info */}
                              <div className="p-3 bg-void-light">
                                <h3 className="font-medium text-sm line-clamp-2 mb-2">{video.title}</h3>
                                <div className="flex items-center justify-between text-xs text-white/60">
                                  <span>{video.channel}</span>
                                  <div className="flex items-center gap-3">
                                    <span className="flex items-center gap-1">
                                      <Eye size={12} />
                                      {video.views}
                                    </span>
                                    <span className="flex items-center gap-1">
                                      <ThumbsUp size={12} />
                                      {video.likeCount}
                                    </span>
                                  </div>
                                </div>
                              </div>

                              {/* Selection Overlay */}
                              {isSelected && (
                                <div className="absolute inset-0 bg-electric-blue/10 pointer-events-none" />
                              )}
                            </motion.div>
                          );
                        })}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>

      {/* Preview Modal */}
      <AnimatePresence>
        {showPreview && (
          <NewsletterPreview
            selectedVideos={Array.from(selectedVideos.values()).sort((a, b) => a.order - b.order)}
            onClose={() => setShowPreview(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

// Newsletter Preview Component
function NewsletterPreview({
  selectedVideos,
  onClose,
}: {
  selectedVideos: SelectedVideo[];
  onClose: () => void;
}) {
  const [format, setFormat] = useState<"html" | "markdown">("html");

  // Agrupar vídeos por categoria
  const videosByCategory = useMemo(() => {
    const map = new Map<string, SelectedVideo[]>();

    selectedVideos.forEach((video) => {
      // Encontrar categoria do vídeo
      const category = REAL_EDITION.categories.find((cat) =>
        cat.videos.some((v) => v.video_id === video.video_id)
      );
      const catId = category?.id || "outros";

      if (!map.has(catId)) {
        map.set(catId, []);
      }
      map.get(catId)!.push(video);
    });

    return map;
  }, [selectedVideos]);

  // Gerar HTML da newsletter
  const generateHTML = () => {
    let html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>IANIA IA NEWS - Newsletter</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background: #0a0a0f; color: #fff; }
    h1 { color: #00d4ff; }
    h2 { color: #a855f7; border-bottom: 1px solid #333; padding-bottom: 10px; }
    .video { margin: 20px 0; padding: 15px; background: #1a1a2e; border-radius: 12px; }
    .video img { width: 100%; border-radius: 8px; }
    .video h3 { margin: 10px 0 5px; }
    .video p { color: #888; font-size: 14px; }
    .video a { color: #00d4ff; text-decoration: none; }
    .stats { display: flex; gap: 15px; font-size: 12px; color: #666; margin-top: 10px; }
  </style>
</head>
<body>
  <h1>🤖 IANIA IA NEWS</h1>
  <p>Sua curadoria semanal de Inteligência Artificial</p>
`;

    videosByCategory.forEach((videos, catId) => {
      const cat = REAL_EDITION.categories.find((c) => c.id === catId);
      html += `\n  <h2>${cat?.emoji || "📁"} ${cat?.name || catId}</h2>\n`;

      videos.forEach((video) => {
        html += `
  <div class="video">
    <img src="https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg" alt="${video.title}">
    <h3><a href="https://www.youtube.com/watch?v=${video.video_id}" target="_blank">${video.title}</a></h3>
    <p>${video.summary}</p>
    <div class="stats">
      <span>📺 ${video.channel}</span>
      <span>👁 ${video.views}</span>
      <span>👍 ${video.likeCount}</span>
    </div>
  </div>
`;
      });
    });

    html += `
  <hr style="border-color: #333; margin: 30px 0;">
  <p style="text-align: center; color: #666;">
    Curado com IA ✨ | <a href="https://iania.ai" style="color: #00d4ff;">iania.ai</a>
  </p>
</body>
</html>`;

    return html;
  };

  // Gerar Markdown
  const generateMarkdown = () => {
    let md = `# 🤖 IANIA IA NEWS\n\n*Sua curadoria semanal de Inteligência Artificial*\n\n---\n\n`;

    videosByCategory.forEach((videos, catId) => {
      const cat = REAL_EDITION.categories.find((c) => c.id === catId);
      md += `## ${cat?.emoji || "📁"} ${cat?.name || catId}\n\n`;

      videos.forEach((video) => {
        md += `### [${video.title}](https://www.youtube.com/watch?v=${video.video_id})\n\n`;
        md += `![${video.title}](https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg)\n\n`;
        md += `${video.summary}\n\n`;
        md += `📺 ${video.channel} | 👁 ${video.views} | 👍 ${video.likeCount}\n\n`;
        md += `---\n\n`;
      });
    });

    md += `\n*Curado com IA ✨ | [iania.ai](https://iania.ai)*`;

    return md;
  };

  // Download
  const handleDownload = () => {
    const content = format === "html" ? generateHTML() : generateMarkdown();
    const blob = new Blob([content], { type: format === "html" ? "text/html" : "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `newsletter-${new Date().toISOString().split("T")[0]}.${format === "html" ? "html" : "md"}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Copiar para clipboard
  const handleCopy = async () => {
    const content = format === "html" ? generateHTML() : generateMarkdown();
    await navigator.clipboard.writeText(content);
    alert("Copiado para a área de transferência!");
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="w-full max-w-4xl max-h-[90vh] overflow-hidden rounded-2xl glass-card"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-white/10">
          <h2 className="text-xl font-bold">Preview da Newsletter</h2>
          <div className="flex items-center gap-4">
            {/* Format Toggle */}
            <div className="flex rounded-lg overflow-hidden border border-white/20">
              <button
                onClick={() => setFormat("html")}
                className={`px-4 py-2 text-sm ${
                  format === "html" ? "bg-electric-blue text-white" : "text-white/60 hover:text-white"
                }`}
              >
                HTML
              </button>
              <button
                onClick={() => setFormat("markdown")}
                className={`px-4 py-2 text-sm ${
                  format === "markdown" ? "bg-electric-blue text-white" : "text-white/60 hover:text-white"
                }`}
              >
                Markdown
              </button>
            </div>

            <button
              onClick={handleCopy}
              className="px-4 py-2 rounded-lg border border-white/20 hover:border-electric-blue/50 text-white/60 hover:text-electric-blue transition-colors"
            >
              Copiar
            </button>

            <button onClick={handleDownload} className="btn-primary px-4 py-2 flex items-center gap-2">
              <Download size={18} />
              Download
            </button>

            <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-lg transition-colors">
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Preview Content */}
        <div className="p-4 overflow-y-auto max-h-[calc(90vh-80px)]">
          <div className="rounded-xl overflow-hidden bg-void-light p-6">
            {/* Newsletter Header */}
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold gradient-text mb-2">🤖 IANIA IA NEWS</h1>
              <p className="text-white/60">Sua curadoria semanal de Inteligência Artificial</p>
              <p className="text-sm text-white/40 mt-2">
                {selectedVideos.length} vídeos selecionados • {new Date().toLocaleDateString("pt-BR")}
              </p>
            </div>

            {/* Categories */}
            {Array.from(videosByCategory.entries()).map(([catId, videos]) => {
              const cat = REAL_EDITION.categories.find((c) => c.id === catId);

              return (
                <div key={catId} className="mb-8">
                  <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
                    <span>{cat?.emoji || "📁"}</span>
                    <span>{cat?.name || catId}</span>
                    <span className="text-sm font-normal text-white/40">({videos.length})</span>
                  </h2>

                  <div className="space-y-4">
                    {videos.map((video) => (
                      <div
                        key={video.video_id}
                        className="flex gap-4 p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors"
                      >
                        <div className="relative w-40 aspect-video flex-shrink-0 rounded-lg overflow-hidden">
                          <Image
                            src={`https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`}
                            alt={video.title}
                            fill
                            className="object-cover"
                          />
                        </div>

                        <div className="flex-1 min-w-0">
                          <h3 className="font-medium mb-1 line-clamp-2">{video.title}</h3>
                          <p className="text-sm text-white/60 line-clamp-2 mb-2">{video.summary}</p>
                          <div className="flex items-center gap-4 text-xs text-white/40">
                            <span>📺 {video.channel}</span>
                            <span>👁 {video.views}</span>
                            <span>👍 {video.likeCount}</span>
                          </div>
                        </div>

                        <a
                          href={`https://www.youtube.com/watch?v=${video.video_id}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex-shrink-0 p-2 hover:bg-white/10 rounded-lg transition-colors"
                        >
                          <ExternalLink size={18} className="text-white/40" />
                        </a>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}

            {/* Footer */}
            <div className="text-center pt-6 border-t border-white/10 mt-8">
              <p className="text-white/40 text-sm">Curado com IA ✨ | iania.ai</p>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
