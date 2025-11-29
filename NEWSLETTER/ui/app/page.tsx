"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Header from "@/components/Header";
import HeroCompact from "@/components/HeroCompact";
import AIPulseDashboard from "@/components/AIPulseDashboard";
import TopStoriesGrid from "@/components/TopStoriesGrid";
import CategoriesExplorer from "@/components/CategoriesExplorer";
import Footer from "@/components/Footer";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-void text-white overflow-x-hidden">
      {/* Header */}
      <Header />

      {/* Hero Compacto */}
      <HeroCompact />

      {/* AI Pulse Dashboard - Indicadores */}
      <AIPulseDashboard />

      {/* Divisor visual */}
      <div className="container mx-auto px-4">
        <div className="h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>

      {/* Top Stories Grid */}
      <TopStoriesGrid />

      {/* Divisor visual */}
      <div className="container mx-auto px-4">
        <div className="h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />
      </div>

      {/* Categories Explorer */}
      <CategoriesExplorer />

      {/* Footer */}
      <Footer />
    </main>
  );
}
