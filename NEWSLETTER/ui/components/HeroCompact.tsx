"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Calendar } from "lucide-react";
import { REAL_EDITION, getAllRealVideos } from "@/lib/real-data";

// Logo SVG component baseado no design fornecido
function IaniaLogo({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 200 60" className={className} fill="currentColor">
      <text
        x="0"
        y="48"
        fontFamily="'Pacifico', 'Dancing Script', cursive"
        fontSize="52"
        fontWeight="400"
        fill="white"
      >
        iania
      </text>
    </svg>
  );
}

export default function HeroCompact() {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 60000);
    return () => clearInterval(timer);
  }, []);

  // Breaking news ticker items - título + canal
  const breakingNews = getAllRealVideos()
    .sort((a, b) => b.viewCount - a.viewCount)
    .slice(0, 8)
    .map((v) => ({ title: v.title, channel: v.channel }));

  // Horário da última atualização
  const lastUpdate = new Date(REAL_EDITION.collectedAt);
  const lastUpdateFormatted = lastUpdate.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <section className="relative pt-24 pb-6 overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-neon-orange/5 via-transparent to-transparent pointer-events-none" />

      <div className="container mx-auto px-4">
        {/* Main Title - Centralizado */}
        <motion.div
          className="text-center mb-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          {/* Logo + Title */}
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-3" style={{ fontFamily: "'Pacifico', 'Dancing Script', cursive" }}>
            <span className="text-white">iania</span>
            <span className="text-white/60 font-sans text-3xl md:text-4xl lg:text-5xl ml-3 font-light">AI News</span>
          </h1>
          
          {/* Subtitle em uma linha */}
          <p className="text-base md:text-lg text-white/50 flex items-center justify-center gap-3 flex-wrap">
            <span>Vídeos analisados e organizados por categoria</span>
            <span className="text-white/30">•</span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-acid-green animate-pulse" />
              Atualizado: {lastUpdateFormatted}
            </span>
          </p>
        </motion.div>

        {/* Breaking News Ticker */}
        <motion.div
          className="relative overflow-hidden rounded-full glass-card border border-white/5"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div className="absolute left-0 top-0 bottom-0 w-24 bg-gradient-to-r from-void to-transparent z-10" />
          <div className="absolute right-0 top-0 bottom-0 w-24 bg-gradient-to-l from-void to-transparent z-10" />
          
          <div className="flex items-center py-2.5 px-4">
            <div className="flex-shrink-0 flex items-center gap-2 pr-4 border-r border-white/10 mr-4">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-neon-orange opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-neon-orange" />
              </span>
              <span className="text-xs font-medium text-neon-orange uppercase tracking-wider">Em Alta</span>
            </div>
            
            <div className="overflow-hidden flex-1">
              <motion.div
                className="flex gap-8 whitespace-nowrap"
                animate={{ x: [0, -2000] }}
                transition={{
                  x: {
                    repeat: Infinity,
                    repeatType: "loop",
                    duration: 60,
                    ease: "linear",
                  },
                }}
              >
                {[...breakingNews, ...breakingNews].map((item, index) => (
                  <span key={index} className="text-sm text-white/70">
                    {item.title}
                    <span className="text-electric-cyan/70 ml-2">— {item.channel}</span>
                    <span className="mx-4 text-white/30">•</span>
                  </span>
                ))}
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
