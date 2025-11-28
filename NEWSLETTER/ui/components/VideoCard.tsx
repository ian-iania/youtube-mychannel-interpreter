"use client";

import { motion } from "framer-motion";
import { Play, Clock, Eye, ThumbsUp, ExternalLink } from "lucide-react";
import Image from "next/image";
import { Video } from "@/lib/types";
import { formatViews, formatDuration, getYouTubeThumbnail, extractYouTubeId } from "@/lib/utils";

interface VideoCardProps {
  video: Video;
  index?: number;
}

export default function VideoCard({ video, index = 0 }: VideoCardProps) {
  const videoId = extractYouTubeId(video.url);
  const thumbnail = videoId ? getYouTubeThumbnail(videoId, "high") : video.thumbnail;

  return (
    <motion.article
      className="group glass-card rounded-2xl overflow-hidden hover:shadow-glow-lg transition-all duration-300"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      whileHover={{ y: -8 }}
    >
      <a
        href={video.url}
        target="_blank"
        rel="noopener noreferrer"
        className="block"
      >
        {/* Thumbnail */}
        <div className="relative aspect-video bg-void-light overflow-hidden">
          {thumbnail && (
            <Image
              src={thumbnail}
              alt={video.title}
              fill
              className="object-cover transition-transform duration-300 group-hover:scale-110"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
          )}

          {/* Overlay on hover */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="absolute inset-0 flex items-center justify-center">
              <motion.div
                className="w-16 h-16 rounded-full bg-electric-blue/90 flex items-center justify-center"
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <Play className="w-8 h-8 text-white fill-white ml-1" />
              </motion.div>
            </div>
          </div>

          {/* Duration badge */}
          {video.duration && (
            <div className="absolute bottom-3 right-3 px-2 py-1 rounded-lg bg-black/80 backdrop-blur-sm">
              <span className="text-xs font-mono text-white flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {formatDuration(parseFloat(video.duration))}
              </span>
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-5 space-y-3">
          {/* Channel */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-electric-blue to-electric-purple flex items-center justify-center">
              <span className="text-xs font-bold">
                {video.channel.charAt(0).toUpperCase()}
              </span>
            </div>
            <span className="text-sm font-medium text-white/70">{video.channel}</span>
          </div>

          {/* Title */}
          <h3 className="font-heading font-bold text-lg text-white line-clamp-2 group-hover:text-electric-blue transition-colors">
            {video.title}
          </h3>

          {/* Summary */}
          {video.summary && (
            <p className="body-sm line-clamp-2">{video.summary}</p>
          )}

          {/* Key Points */}
          {video.keyPoints && video.keyPoints.length > 0 && (
            <div className="space-y-1">
              <p className="text-xs font-mono text-electric-cyan">Principais pontos:</p>
              <ul className="space-y-1">
                {video.keyPoints.slice(0, 2).map((point, i) => (
                  <li key={i} className="text-xs text-white/60 flex items-start gap-2">
                    <span className="text-electric-purple mt-0.5">•</span>
                    <span className="line-clamp-1">{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Stats */}
          <div className="flex items-center gap-4 pt-2 border-t border-white/10">
            {video.viewCount !== undefined && (
              <div className="flex items-center gap-1 text-white/50">
                <Eye className="w-4 h-4" />
                <span className="text-xs font-mono">{formatViews(video.viewCount)}</span>
              </div>
            )}

            {video.likeCount !== undefined && video.likeCount > 0 && (
              <div className="flex items-center gap-1 text-white/50">
                <ThumbsUp className="w-4 h-4" />
                <span className="text-xs font-mono">{formatViews(video.likeCount)}</span>
              </div>
            )}

            <div className="ml-auto">
              <ExternalLink className="w-4 h-4 text-white/50 group-hover:text-electric-blue transition-colors" />
            </div>
          </div>
        </div>
      </a>

      {/* Neon border on hover */}
      <div className="absolute inset-0 rounded-2xl border border-electric-blue/0 group-hover:border-electric-blue/50 transition-colors duration-300 pointer-events-none" />
    </motion.article>
  );
}

// Compact version for lists
export function VideoCardCompact({ video, index = 0 }: VideoCardProps) {
  const videoId = extractYouTubeId(video.url);
  const thumbnail = videoId ? getYouTubeThumbnail(videoId, "medium") : video.thumbnail;

  return (
    <motion.article
      className="group glass-card rounded-xl overflow-hidden hover:shadow-glow transition-all duration-300"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      whileHover={{ x: 4 }}
    >
      <a
        href={video.url}
        target="_blank"
        rel="noopener noreferrer"
        className="flex gap-3 p-3"
      >
        {/* Thumbnail */}
        <div className="relative w-32 h-20 flex-shrink-0 rounded-lg overflow-hidden bg-void-light">
          {thumbnail && (
            <Image
              src={thumbnail}
              alt={video.title}
              fill
              className="object-cover"
              sizes="128px"
            />
          )}

          {/* Play overlay */}
          <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <Play className="w-6 h-6 text-white fill-white" />
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0 space-y-1">
          <h4 className="font-heading font-bold text-sm text-white line-clamp-2 group-hover:text-electric-blue transition-colors">
            {video.title}
          </h4>

          <p className="text-xs text-white/50">{video.channel}</p>

          <div className="flex items-center gap-3 text-xs text-white/40">
            {video.viewCount !== undefined && (
              <span className="flex items-center gap-1">
                <Eye className="w-3 h-3" />
                {formatViews(video.viewCount)}
              </span>
            )}
            {video.duration && (
              <span className="flex items-center gap-1">
                <Clock className="w-3 h-3" />
                {formatDuration(parseFloat(video.duration))}
              </span>
            )}
          </div>
        </div>
      </a>
    </motion.article>
  );
}
