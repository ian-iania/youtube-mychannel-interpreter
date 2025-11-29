"use client";

import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import Image from "next/image";
import { Clock, Eye, ThumbsUp, Play, ExternalLink, ChevronRight } from "lucide-react";
import { getAllRealVideos } from "@/lib/real-data";
import { Video } from "@/lib/types";

export default function TopStoriesGrid() {
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  // Pegar os vídeos mais populares
  const topVideos = useMemo(() => {
    const allVideos = getAllRealVideos();
    return [...allVideos].sort((a, b) => b.viewCount - a.viewCount).slice(0, 7);
  }, []);

  const [featured, ...secondary] = topVideos;

  return (
    <section className="py-12">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-1 h-8 bg-gradient-to-b from-neon-orange to-electric-orange rounded-full" />
            <h2 className="text-2xl font-bold">Top Stories</h2>
          </div>
          <button className="flex items-center gap-1 text-sm text-white/60 hover:text-neon-orange transition-colors group">
            Ver todas
            <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </button>
        </div>

        {/* Bento Grid Layout */}
        <div className="grid grid-cols-12 gap-4">
          {/* Featured Story - Large */}
          <motion.a
            href={featured.url}
            target="_blank"
            rel="noopener noreferrer"
            className="col-span-12 lg:col-span-8 row-span-2 relative group rounded-3xl overflow-hidden cursor-pointer"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            onMouseEnter={() => setHoveredId(featured.video_id)}
            onMouseLeave={() => setHoveredId(null)}
          >
            {/* Background Image */}
            <div className="absolute inset-0">
              <Image
                src={`https://i.ytimg.com/vi/${featured.video_id}/maxresdefault.jpg`}
                alt={featured.title}
                fill
                className="object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black via-black/50 to-transparent" />
            </div>

            {/* Content */}
            <div className="relative h-full min-h-[400px] lg:min-h-[500px] flex flex-col justify-end p-6 lg:p-10">
              {/* Category Badge */}
              <div className="mb-4">
                <span className="px-3 py-1 rounded-full text-xs font-medium bg-neon-orange/20 text-neon-orange border border-neon-orange/30">
                  🔥 Em Alta
                </span>
              </div>

              {/* Title */}
              <h3 className="text-2xl lg:text-4xl font-bold mb-4 leading-tight group-hover:text-neon-orange transition-colors">
                {featured.title}
              </h3>

              {/* Summary */}
              <p className="text-white/70 text-lg mb-6 line-clamp-2 max-w-2xl">{featured.summary}</p>

              {/* Meta */}
              <div className="flex items-center gap-6 text-sm text-white/60">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
                    {featured.channel.charAt(0)}
                  </div>
                  <span>{featured.channel}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Eye size={14} />
                  {featured.views}
                </div>
                <div className="flex items-center gap-1">
                  <ThumbsUp size={14} />
                  {featured.likeCount?.toLocaleString()}
                </div>
                <div className="flex items-center gap-1">
                  <Clock size={14} />
                  {Math.round(parseFloat(featured.duration))} min
                </div>
              </div>

              {/* Play Button */}
              <motion.div
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{
                  scale: hoveredId === featured.video_id ? 1 : 0.8,
                  opacity: hoveredId === featured.video_id ? 1 : 0,
                }}
                transition={{ duration: 0.3 }}
              >
                <div className="w-20 h-20 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border border-white/30">
                  <Play size={32} className="text-white ml-1" fill="white" />
                </div>
              </motion.div>
            </div>
          </motion.a>

          {/* Secondary Stories - Right Column */}
          <div className="col-span-12 lg:col-span-4 grid gap-4">
            {secondary.slice(0, 2).map((video, index) => (
              <SecondaryCard key={video.video_id} video={video} index={index} />
            ))}
          </div>

          {/* Bottom Row - Small Cards */}
          {secondary.slice(2, 6).map((video, index) => (
            <motion.a
              key={video.video_id}
              href={video.url}
              target="_blank"
              rel="noopener noreferrer"
              className="col-span-6 lg:col-span-3 group"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 + index * 0.1 }}
            >
              <div className="relative aspect-video rounded-2xl overflow-hidden mb-3">
                <Image
                  src={`https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`}
                  alt={video.title}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute bottom-2 right-2 px-2 py-1 rounded bg-black/70 text-xs flex items-center gap-1">
                  <Clock size={10} />
                  {Math.round(parseFloat(video.duration))} min
                </div>
              </div>
              <h4 className="font-medium text-sm line-clamp-2 group-hover:text-neon-orange transition-colors">
                {video.title}
              </h4>
              <div className="flex items-center gap-2 mt-2 text-xs text-white/50">
                <span>{video.channel}</span>
                <span>•</span>
                <span>{video.views}</span>
              </div>
            </motion.a>
          ))}
        </div>
      </div>
    </section>
  );
}

// Secondary Card Component
function SecondaryCard({ video, index }: { video: Video; index: number }) {
  return (
    <motion.a
      href={video.url}
      target="_blank"
      rel="noopener noreferrer"
      className="relative group rounded-2xl overflow-hidden glass-card border border-white/5 hover:border-neon-orange/30 transition-all"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
    >
      <div className="flex gap-4 p-4">
        {/* Thumbnail */}
        <div className="relative w-32 h-20 flex-shrink-0 rounded-xl overflow-hidden">
          <Image
            src={`https://i.ytimg.com/vi/${video.video_id}/hqdefault.jpg`}
            alt={video.title}
            fill
            className="object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-colors" />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-sm line-clamp-2 mb-2 group-hover:text-neon-orange transition-colors">
            {video.title}
          </h4>
          <div className="flex items-center gap-3 text-xs text-white/50">
            <span>{video.channel}</span>
            <span className="flex items-center gap-1">
              <Eye size={10} />
              {video.views}
            </span>
          </div>
        </div>
      </div>
    </motion.a>
  );
}
