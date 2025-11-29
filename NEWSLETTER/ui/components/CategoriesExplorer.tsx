"use client";

import { useState, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import { ChevronRight, Play, Eye, Clock, ArrowUpRight } from "lucide-react";
import { REAL_EDITION, getAllRealVideos } from "@/lib/real-data";
import { Category, Video } from "@/lib/types";
import PeriodFilter, { PeriodOption, filterVideosByPeriod, countVideosByPeriod } from "./PeriodFilter";

export default function CategoriesExplorer() {
  const [activeCategory, setActiveCategory] = useState<string>(REAL_EDITION.categories[0]?.id || "");
  const [hoveredVideo, setHoveredVideo] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<PeriodOption>("all");

  // Contagem total de vídeos por período
  const allVideos = useMemo(() => getAllRealVideos(), []);
  const periodCounts = useMemo(() => countVideosByPeriod(allVideos), [allVideos]);

  // Filtrar categorias e vídeos pelo período selecionado
  const filteredCategories = useMemo(() => {
    return REAL_EDITION.categories.map((category) => {
      const filteredVideos = filterVideosByPeriod(category.videos, selectedPeriod);
      return {
        ...category,
        videos: filteredVideos,
        videoCount: filteredVideos.length,
      };
    }).filter((category) => category.videoCount > 0);
  }, [selectedPeriod]);

  const activeData = filteredCategories.find((c) => c.id === activeCategory) || filteredCategories[0];
  
  // Total de vídeos filtrados
  const totalFilteredVideos = filteredCategories.reduce((sum, c) => sum + c.videoCount, 0);

  return (
    <section className="py-16 relative">
      {/* Background Accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-electric-purple/5 to-transparent pointer-events-none" />

      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-2">Explore por Categoria</h2>
            <p className="text-white/50">
              {filteredCategories.length} categorias • {totalFilteredVideos} vídeos
              {selectedPeriod !== "all" && (
                <span className="text-acid-green/70"> (filtrado)</span>
              )}
            </p>
          </div>
          
          {/* Period Filter */}
          <PeriodFilter
            selected={selectedPeriod}
            onChange={setSelectedPeriod}
            videoCounts={periodCounts}
          />
        </div>

        {/* Category Pills */}
        <div className="flex flex-wrap gap-2 mb-10">
          {filteredCategories.map((category) => (
            <motion.button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                activeData?.id === category.id
                  ? "bg-gradient-to-r from-neon-orange to-electric-orange text-white shadow-lg shadow-neon-orange/20"
                  : "bg-white/5 text-white/60 hover:bg-white/10 hover:text-white"
              }`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span className="mr-2">{category.emoji}</span>
              {category.name}
              <span className="ml-2 opacity-60">({category.videoCount})</span>
            </motion.button>
          ))}
        </div>

        {/* Empty State */}
        {filteredCategories.length === 0 && (
          <div className="text-center py-16">
            <p className="text-white/50 text-lg">Nenhum vídeo encontrado para este período.</p>
            <button
              onClick={() => setSelectedPeriod("all")}
              className="mt-4 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white/70 hover:text-white transition-colors"
            >
              Ver todos os vídeos
            </button>
          </div>
        )}

        {/* Active Category Content */}
        <AnimatePresence mode="wait">
          {activeData && (
            <motion.div
              key={activeData.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              {/* Category Header Card */}
              <div className="glass-card rounded-3xl p-6 mb-8 border border-white/5">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-neon-orange/20 to-electric-purple/20 flex items-center justify-center text-4xl">
                      {activeData.emoji}
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold mb-1">{activeData.name}</h3>
                      <p className="text-white/50">{activeData.description}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-neon-orange">{activeData.videoCount}</div>
                    <div className="text-sm text-white/50">vídeos</div>
                  </div>
                </div>
              </div>

              {/* Videos Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {activeData.videos.slice(0, 8).map((video, index) => (
                  <VideoCard
                    key={video.video_id}
                    video={video}
                    index={index}
                    isHovered={hoveredVideo === video.video_id}
                    onHover={setHoveredVideo}
                  />
                ))}
              </div>

              {/* View All Button */}
              {activeData.videos.length > 8 && (
                <div className="text-center mt-8">
                  <button className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 hover:bg-white/10 text-white/80 hover:text-white transition-colors group">
                    Ver todos os {activeData.videoCount} vídeos
                    <ArrowUpRight size={18} className="group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                  </button>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </section>
  );
}

function VideoCard({
  video,
  index,
  isHovered,
  onHover,
}: {
  video: Video;
  index: number;
  isHovered: boolean;
  onHover: (id: string | null) => void;
}) {
  return (
    <motion.a
      href={video.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group relative"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      onMouseEnter={() => onHover(video.video_id)}
      onMouseLeave={() => onHover(null)}
    >
      <div className="relative rounded-2xl overflow-hidden glass-card border border-white/5 hover:border-neon-orange/30 transition-all duration-300 hover:shadow-lg hover:shadow-neon-orange/10">
        {/* Thumbnail */}
        <div className="relative aspect-video overflow-hidden">
          <Image
            src={`https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`}
            alt={video.title}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />

          {/* Play Button */}
          <motion.div
            className="absolute inset-0 flex items-center justify-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: isHovered ? 1 : 0 }}
            transition={{ duration: 0.2 }}
          >
            <div className="w-14 h-14 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/30">
              <Play size={24} className="text-white ml-1" fill="white" />
            </div>
          </motion.div>

          {/* Duration Badge */}
          <div className="absolute bottom-2 right-2 px-2 py-1 rounded-lg bg-black/70 backdrop-blur-sm text-xs flex items-center gap-1">
            <Clock size={10} />
            {Math.round(parseFloat(video.duration))} min
          </div>
        </div>

        {/* Content */}
        <div className="p-4">
          <h4 className="font-medium line-clamp-2 mb-2 group-hover:text-neon-orange transition-colors">
            {video.title}
          </h4>

          {/* Summary */}
          <p className="text-xs text-white/50 line-clamp-2 mb-3">{video.summary}</p>

          {/* Meta */}
          <div className="flex items-center justify-between text-xs text-white/40">
            <span className="truncate max-w-[60%]">{video.channel}</span>
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-1">
                <Eye size={10} />
                {video.views}
              </span>
            </div>
          </div>
        </div>
      </div>
    </motion.a>
  );
}
