"use client";

import { motion } from "framer-motion";
import { ArrowRight, Sparkles } from "lucide-react";
import { Category } from "@/lib/types";
import { cn } from "@/lib/utils";

interface CategoryCardProps {
  category: Category;
  index?: number;
  onClick?: () => void;
}

export default function CategoryCard({ category, index = 0, onClick }: CategoryCardProps) {
  return (
    <motion.article
      className={cn(
        "group relative glass-card rounded-2xl overflow-hidden cursor-pointer",
        "hover:shadow-glow-purple-lg transition-all duration-300"
      )}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ scale: 1.02, rotateY: 2, rotateX: -2 }}
      style={{ transformStyle: "preserve-3d" }}
      onClick={onClick}
    >
      {/* Background gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-electric-blue/5 via-electric-purple/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      {/* AI-generated image placeholder */}
      {category.imageUrl && (
        <div className="absolute inset-0 opacity-10 group-hover:opacity-20 transition-opacity duration-300">
          <div
            className="w-full h-full bg-cover bg-center"
            style={{ backgroundImage: `url(${category.imageUrl})` }}
          />
        </div>
      )}

      {/* Content */}
      <div className="relative p-6 space-y-4 z-10">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            {/* Emoji icon */}
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-electric-blue/20 to-electric-purple/20 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform duration-300">
              {category.emoji}
            </div>

            {/* Video count badge */}
            <div className="px-3 py-1 rounded-full bg-electric-blue/10 border border-electric-blue/20">
              <span className="text-xs font-mono text-electric-cyan">
                {category.videoCount} vídeos
              </span>
            </div>
          </div>

          {/* Arrow icon */}
          <motion.div
            className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center opacity-0 group-hover:opacity-100"
            whileHover={{ x: 4 }}
            transition={{ duration: 0.2 }}
          >
            <ArrowRight className="w-4 h-4 text-electric-blue" />
          </motion.div>
        </div>

        {/* Title */}
        <h3 className="font-heading font-bold text-xl text-white group-hover:text-electric-blue transition-colors">
          {category.name}
        </h3>

        {/* Description */}
        <p className="body-sm line-clamp-2">{category.description}</p>

        {/* AI prompt indicator (for development) */}
        {category.imagePrompt && (
          <div className="flex items-center gap-2 text-xs text-white/30">
            <Sparkles className="w-3 h-3" />
            <span className="font-mono">AI-ready</span>
          </div>
        )}
      </div>

      {/* Neon border on hover */}
      <div className="absolute inset-0 rounded-2xl border border-electric-purple/0 group-hover:border-electric-purple/50 transition-colors duration-300 pointer-events-none" />

      {/* Glow effect */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-electric-blue/0 via-electric-purple/0 to-electric-blue/0 group-hover:from-electric-blue/5 group-hover:via-electric-purple/5 group-hover:to-electric-blue/5 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10" />
    </motion.article>
  );
}

// Compact version for sidebar/lists
export function CategoryCardCompact({ category, onClick }: CategoryCardProps) {
  return (
    <motion.button
      className="w-full group glass-card rounded-xl p-4 text-left hover:shadow-glow transition-all duration-300"
      whileHover={{ x: 4 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
    >
      <div className="flex items-center gap-3">
        {/* Emoji */}
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-electric-blue/20 to-electric-purple/20 flex items-center justify-center text-xl flex-shrink-0">
          {category.emoji}
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h4 className="font-heading font-bold text-sm text-white group-hover:text-electric-blue transition-colors truncate">
            {category.name}
          </h4>
          <p className="text-xs text-white/50">{category.videoCount} vídeos</p>
        </div>

        {/* Arrow */}
        <ArrowRight className="w-4 h-4 text-white/30 group-hover:text-electric-blue transition-colors flex-shrink-0" />
      </div>
    </motion.button>
  );
}
