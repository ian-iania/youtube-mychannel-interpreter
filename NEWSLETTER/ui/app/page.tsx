"use client";

import ShaderBackground from "@/components/ShaderBackground";
import Header from "@/components/Header";
import { motion } from "framer-motion";

export default function Home() {
  return (
    <main className="relative min-h-screen">
      {/* Shader Background */}
      <ShaderBackground />

      {/* Header */}
      <Header />

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-6xl">
          <motion.div
            className="text-center space-y-8"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            {/* Badge */}
            <motion.div
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card neon-border"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <span className="w-2 h-2 rounded-full bg-acid-green animate-pulse" />
              <span className="mono-text">Edição Atual • Semana de 27/11/2025</span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              className="heading-xl gradient-text"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              Curadoria de IA
              <br />
              <span className="text-white">Feita por IA</span>
            </motion.h1>

            {/* Subtitle */}
            <motion.p
              className="body-lg max-w-2xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
            >
              Sua newsletter semanal de Inteligência Artificial, organizada por temas relevantes.
              <br />
              <span className="text-electric-cyan">473 vídeos</span> curados de{" "}
              <span className="text-electric-purple">101 canais</span> especializados.
            </motion.p>

            {/* CTA Buttons */}
            <motion.div
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
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

            {/* Stats */}
            <motion.div
              className="grid grid-cols-3 gap-8 max-w-3xl mx-auto pt-12"
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

      {/* Placeholder para próximas seções */}
      <section className="relative min-h-screen flex items-center justify-center px-4">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="heading-lg mb-6">Próximas Seções</h2>
          <p className="body-lg text-white/60">
            Tabs, Categorias, Vídeos, Bento Grid...
          </p>
        </div>
      </section>
    </main>
  );
}
