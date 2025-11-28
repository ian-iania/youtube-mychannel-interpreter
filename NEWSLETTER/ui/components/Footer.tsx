"use client";

import { motion } from "framer-motion";
import { Sparkles, Github, Twitter, Linkedin, Mail, ArrowUp } from "lucide-react";

export default function Footer() {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <footer className="relative mt-32 border-t border-white/10">
      {/* Marquee Section */}
      <div className="relative overflow-hidden py-8 bg-gradient-to-r from-electric-blue/5 via-electric-purple/5 to-electric-blue/5">
        <Marquee />
      </div>

      {/* Main Footer Content */}
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-electric-blue to-electric-purple flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-heading font-extrabold text-lg gradient-text">
                  IANIA IA NEWS
                </h3>
                <p className="font-mono text-[10px] text-white/40 tracking-wider">
                  AI CURATED
                </p>
              </div>
            </div>
            <p className="body-sm max-w-xs">
              Sua curadoria semanal de Inteligência Artificial, organizada por temas relevantes.
            </p>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h4 className="font-heading font-bold text-sm text-white">Navegação</h4>
            <ul className="space-y-2">
              {["Edição Atual", "Por Categoria", "Arquivo", "Sobre"].map((link) => (
                <li key={link}>
                  <a
                    href={`#${link.toLowerCase().replace(/\s+/g, "-")}`}
                    className="body-sm hover:text-electric-blue transition-colors"
                  >
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Categories */}
          <div className="space-y-4">
            <h4 className="font-heading font-bold text-sm text-white">Categorias</h4>
            <ul className="space-y-2">
              {[
                "🚀 Novos Modelos",
                "🏢 Produtos",
                "💻 IDEs",
                "🎓 Cursos",
              ].map((category) => (
                <li key={category}>
                  <a
                    href="#categories"
                    className="body-sm hover:text-electric-purple transition-colors"
                  >
                    {category}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Newsletter Signup */}
          <div className="space-y-4">
            <h4 className="font-heading font-bold text-sm text-white">
              Assine a Newsletter
            </h4>
            <p className="body-sm">
              Receba as melhores notícias de IA toda semana.
            </p>
            <div className="flex gap-2">
              <input
                type="email"
                placeholder="seu@email.com"
                className="flex-1 px-4 py-2 rounded-lg glass-card border border-white/10 text-sm focus:border-electric-blue focus:outline-none transition-colors"
              />
              <motion.button
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-electric-blue to-electric-purple font-heading font-bold text-sm"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                →
              </motion.button>
            </div>
          </div>
        </div>

        {/* Social Links & Copyright */}
        <div className="mt-16 pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-6">
          {/* Social Icons */}
          <div className="flex items-center gap-4">
            {[
              { icon: Github, href: "https://github.com" },
              { icon: Twitter, href: "https://twitter.com" },
              { icon: Linkedin, href: "https://linkedin.com" },
              { icon: Mail, href: "mailto:contato@iania.ai" },
            ].map(({ icon: Icon, href }, index) => (
              <motion.a
                key={index}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="w-10 h-10 rounded-lg glass-card flex items-center justify-center hover:bg-white/10 transition-colors"
                whileHover={{ scale: 1.1, rotate: 5 }}
                whileTap={{ scale: 0.95 }}
              >
                <Icon className="w-4 h-4 text-white/70" />
              </motion.a>
            ))}
          </div>

          {/* Copyright */}
          <p className="text-xs text-white/40 font-mono">
            © 2025 IANIA IA NEWS. Curated with AI ✨
          </p>

          {/* Back to Top */}
          <motion.button
            onClick={scrollToTop}
            className="w-10 h-10 rounded-lg glass-card flex items-center justify-center hover:bg-white/10 transition-colors"
            whileHover={{ scale: 1.1, y: -2 }}
            whileTap={{ scale: 0.95 }}
          >
            <ArrowUp className="w-4 h-4 text-white/70" />
          </motion.button>
        </div>
      </div>
    </footer>
  );
}

// Marquee Component
function Marquee() {
  const phrases = [
    "LET'S BUILD THE AI FUTURE",
    "CURATED BY AI FOR HUMANS",
    "473 VIDEOS ANALYZED",
    "101 CHANNELS MONITORED",
    "WEEKLY UPDATES",
    "AI-FIRST DESIGN",
  ];

  return (
    <div className="flex gap-8">
      {/* First marquee */}
      <motion.div
        className="flex gap-8 whitespace-nowrap"
        animate={{
          x: [0, -100 + "%"],
        }}
        transition={{
          x: {
            repeat: Infinity,
            repeatType: "loop",
            duration: 25,
            ease: "linear",
          },
        }}
      >
        {[...phrases, ...phrases].map((phrase, index) => (
          <div key={index} className="flex items-center gap-8">
            <span className="font-heading font-bold text-2xl md:text-3xl gradient-text tracking-tighter">
              {phrase}
            </span>
            <span className="text-electric-blue text-2xl">✦</span>
          </div>
        ))}
      </motion.div>

      {/* Second marquee (for seamless loop) */}
      <motion.div
        className="flex gap-8 whitespace-nowrap"
        animate={{
          x: [0, -100 + "%"],
        }}
        transition={{
          x: {
            repeat: Infinity,
            repeatType: "loop",
            duration: 25,
            ease: "linear",
          },
        }}
      >
        {[...phrases, ...phrases].map((phrase, index) => (
          <div key={`dup-${index}`} className="flex items-center gap-8">
            <span className="font-heading font-bold text-2xl md:text-3xl gradient-text tracking-tighter">
              {phrase}
            </span>
            <span className="text-electric-blue text-2xl">✦</span>
          </div>
        ))}
      </motion.div>
    </div>
  );
}
