"use client";

import { useState } from "react";
import ShaderBackground from "@/components/ShaderBackground";
import Header from "@/components/Header";
import NewsTicker from "@/components/NewsTicker";
import Tabs, { TabType } from "@/components/Tabs";
import VideoCard from "@/components/VideoCard";
import CategoryCard from "@/components/CategoryCard";
import Footer from "@/components/Footer";
import { motion } from "framer-motion";
import { REAL_EDITION } from "@/lib/real-data";

export default function Home() {
  return (
    <main className="relative min-h-screen">
      {/* Shader Background */}
      <ShaderBackground />

      {/* Header */}
      <Header />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-32">
        <div className="container mx-auto max-w-6xl">
          {/* Badge no topo esquerda */}
          <motion.div
            className="absolute top-32 left-8 inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card neon-border"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <span className="w-2 h-2 rounded-full bg-acid-green animate-pulse" />
            <span className="mono-text text-xs">Edição Atual • 27/11/2025</span>
          </motion.div>

          <motion.div
            className="text-center space-y-6"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Main Heading - Maior e mais alto */}
            <motion.h1
              className="heading-xl gradient-text pt-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              Curadoria de IA
              <br />
              <span className="text-white text-5xl md:text-7xl">Feita por IA</span>
            </motion.h1>

            {/* Subtitle - Uma linha só */}
            <motion.p
              className="body-lg max-w-3xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
            >
              Sua newsletter semanal de Inteligência Artificial, organizada por temas relevantes
            </motion.p>

            {/* News Ticker - Carrossel de notícias */}
            <motion.div
              className="pt-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
            >
              <NewsTicker />
            </motion.div>

            {/* Stats - Abaixo do ticker */}
            <motion.div
              className="grid grid-cols-3 gap-8 max-w-3xl mx-auto pt-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.7 }}
            >
              <div className="text-center">
                <div className="heading-md gradient-text">473</div>
                <div className="body-sm">Vídeos Curados</div>
              </div>
              <div className="text-center">
                <div className="heading-md gradient-text">101</div>
                <div className="body-sm">Canais Especializados</div>
              </div>
              <div className="text-center">
                <div className="heading-md gradient-text">11</div>
                <div className="body-sm">Categorias</div>
              </div>
            </motion.div>

            {/* CTA Buttons - Abaixo dos stats */}
            <motion.div
              className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-8"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
            >
              <motion.button
                className="btn-primary px-8 py-4 text-base"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Ver Edição Atual
              </motion.button>

              <motion.button
                className="btn-secondary px-8 py-4 text-base"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Explorar Categorias
              </motion.button>
            </motion.div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.8,
            delay: 0.8,
            repeat: Infinity,
            repeatType: "reverse",
          }}
        >
          <div className="w-6 h-10 rounded-full border-2 border-white/20 flex items-start justify-center p-2">
            <motion.div
              className="w-1.5 h-1.5 rounded-full bg-electric-blue"
              animate={{ y: [0, 12, 0] }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            />
          </div>
        </motion.div>
      </section>

      {/* Content Section with Tabs */}
      <ContentSection />

      {/* Footer */}
      <Footer />
    </main>
  );
}

// Content Section Component
function ContentSection() {
  const [activeTab, setActiveTab] = useState<TabType>("current");

  return (
    <section className="relative py-12">
      {/* Tabs */}
      <Tabs activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Tab Content */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {activeTab === "current" && <CurrentEditionTab />}
        {activeTab === "categories" && <CategoriesTab />}
        {activeTab === "archive" && <ArchiveTab />}
      </div>
    </section>
  );
}

// Current Edition Tab
function CurrentEditionTab() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-16"
    >
      {REAL_EDITION.categories.map((category, index) => (
        <div key={category.id} className="space-y-6">
          {/* Category Header */}
          <div className="flex items-center gap-4">
            <span className="text-4xl">{category.emoji}</span>
            <div>
              <h2 className="heading-md">{category.name}</h2>
              <p className="body-sm">{category.description}</p>
            </div>
            <div className="ml-auto px-4 py-2 rounded-full glass-card">
              <span className="mono-text">{category.videoCount} vídeos</span>
            </div>
          </div>

          {/* Videos Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {category.videos.map((video, videoIndex) => (
              <VideoCard key={video.video_id} video={video} index={videoIndex} />
            ))}
          </div>
        </div>
      ))}
    </motion.div>
  );
}

// Categories Tab (Bento Grid)
function CategoriesTab() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {REAL_EDITION.categories.map((category, index) => (
          <CategoryCard
            key={category.id}
            category={category}
            index={index}
            onClick={() => console.log("Category clicked:", category.id)}
          />
        ))}
      </div>
    </motion.div>
  );
}

// Archive Tab (Placeholder)
function ArchiveTab() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="text-center py-20"
    >
      <h2 className="heading-lg mb-4">Arquivo de Edições</h2>
      <p className="body-lg text-white/60 mb-8">
        Edições anteriores estarão disponíveis em breve
      </p>
      <div className="inline-flex items-center gap-2 px-6 py-3 rounded-xl glass-card">
        <span className="mono-text">🚧 Em construção</span>
      </div>
    </motion.div>
  );
}
