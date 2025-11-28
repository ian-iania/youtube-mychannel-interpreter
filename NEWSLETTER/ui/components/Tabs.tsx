"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export type TabType = "current" | "categories" | "archive";

interface Tab {
  id: TabType;
  label: string;
  icon?: string;
}

const TABS: Tab[] = [
  { id: "current", label: "Edição Atual", icon: "📰" },
  { id: "categories", label: "Por Categoria", icon: "🗂️" },
  { id: "archive", label: "Arquivo", icon: "📚" },
];

interface TabsProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

export default function Tabs({ activeTab, onTabChange }: TabsProps) {
  return (
    <div className="w-full py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        {/* Tabs Container */}
        <div className="flex items-center justify-center">
          <div className="inline-flex items-center gap-2 p-2 rounded-2xl glass-card">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => onTabChange(tab.id)}
                className={cn(
                  "relative px-6 py-3 rounded-xl font-heading font-bold text-sm tracking-tight transition-all duration-300",
                  activeTab === tab.id
                    ? "text-white"
                    : "text-white/50 hover:text-white/80"
                )}
              >
                {/* Active background */}
                {activeTab === tab.id && (
                  <motion.div
                    layoutId="activeTab"
                    className="absolute inset-0 bg-gradient-to-r from-electric-blue to-electric-purple rounded-xl"
                    transition={{
                      type: "spring",
                      stiffness: 500,
                      damping: 30,
                    }}
                  />
                )}

                {/* Content */}
                <span className="relative z-10 flex items-center gap-2">
                  {tab.icon && <span>{tab.icon}</span>}
                  {tab.label}
                </span>

                {/* Glow effect when active */}
                {activeTab === tab.id && (
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-electric-blue to-electric-purple rounded-xl blur-xl opacity-50"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 0.5 }}
                    exit={{ opacity: 0 }}
                  />
                )}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
