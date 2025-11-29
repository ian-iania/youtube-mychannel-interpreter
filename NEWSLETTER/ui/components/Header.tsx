"use client";

import { useState, useEffect } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { Menu, X, PenSquare, Trophy, Clock } from "lucide-react";
import { REAL_EDITION } from "@/lib/real-data";
import { cn } from "@/lib/utils";
import Link from "next/link";
import Image from "next/image";
export default function Header() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { scrollY } = useScroll();

  // Horário da última atualização
  const lastUpdate = new Date(REAL_EDITION.collectedAt);
  const lastUpdateFormatted = lastUpdate.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });

  // Transform para blur no scroll
  const headerBlur = useTransform(scrollY, [0, 100], [0, 20]);
  const headerOpacity = useTransform(scrollY, [0, 100], [0.8, 0.95]);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navItems = [
    { label: "Edição Atual", href: "#current" },
    { label: "Categorias", href: "#categories" },
    { label: "Benchmarks", href: "/benchmarks" },
    { label: "Sobre", href: "#about" },
  ];

  return (
    <motion.header
      className={cn(
        "fixed top-0 left-0 right-0 z-40 transition-all duration-300",
        isScrolled ? "py-4" : "py-6"
      )}
      style={{
        backdropFilter: `blur(${headerBlur}px)`,
        backgroundColor: `rgba(3, 3, 5, ${headerOpacity})`,
      }}
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.a
            href="/"
            className="flex items-center gap-2 group"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            {/* Ícone IA */}
            <Image 
              src="/logo-icon.png" 
              alt="IANIA" 
              width={40} 
              height={40}
              className="h-10 w-auto invert"
            />
            
            {/* Atualizado - após o logo */}
            <span className="hidden md:flex items-center gap-1.5 ml-4 pl-4 border-l border-white/10 text-xs text-white/40">
              <Clock size={12} className="text-acid-green" />
              Atualizado em {lastUpdateFormatted}
            </span>
          </motion.a>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            {navItems.map((item, index) => (
              <motion.a
                key={item.href}
                href={item.href}
                className="font-heading font-medium text-sm text-white/70 hover:text-white transition-colors relative group"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                {item.label}
                
                {/* Underline effect */}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-gradient-to-r from-electric-blue to-electric-purple group-hover:w-full transition-all duration-300" />
              </motion.a>
            ))}
          </nav>

          {/* CTA Buttons */}
          <div className="hidden md:flex items-center gap-3">
            <Link href="/benchmarks">
              <motion.button
                className="btn-secondary flex items-center gap-2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.25 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Trophy size={16} />
                Benchmarks
              </motion.button>
            </Link>
            <Link href="/editor">
              <motion.button
                className="btn-secondary flex items-center gap-2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.3 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <PenSquare size={16} />
                Editor
              </motion.button>
            </Link>
            <motion.button
              className="btn-primary"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Assinar Newsletter
            </motion.button>
          </div>

          {/* Mobile Menu Button */}
          <motion.button
            className="md:hidden p-2 rounded-lg glass-card neon-border"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            whileTap={{ scale: 0.95 }}
          >
            {isMobileMenuOpen ? (
              <X className="w-5 h-5" />
            ) : (
              <Menu className="w-5 h-5" />
            )}
          </motion.button>
        </div>

        {/* Mobile Menu */}
        <motion.div
          className="md:hidden overflow-hidden"
          initial={false}
          animate={{
            height: isMobileMenuOpen ? "auto" : 0,
            opacity: isMobileMenuOpen ? 1 : 0,
          }}
          transition={{ duration: 0.3 }}
        >
          <nav className="flex flex-col gap-4 pt-6 pb-4">
            {navItems.map((item, index) => (
              <motion.a
                key={item.href}
                href={item.href}
                className="font-heading font-medium text-sm text-white/70 hover:text-white transition-colors py-2 px-4 rounded-lg hover:bg-glass-white"
                initial={{ opacity: 0, x: -20 }}
                animate={{
                  opacity: isMobileMenuOpen ? 1 : 0,
                  x: isMobileMenuOpen ? 0 : -20,
                }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                {item.label}
              </motion.a>
            ))}
            
            <motion.button
              className="btn-primary mt-2"
              initial={{ opacity: 0, y: 10 }}
              animate={{
                opacity: isMobileMenuOpen ? 1 : 0,
                y: isMobileMenuOpen ? 0 : 10,
              }}
              transition={{ duration: 0.3, delay: 0.2 }}
            >
              Assinar Newsletter
            </motion.button>
          </nav>
        </motion.div>
      </div>
    </motion.header>
  );
}
