"use client";

import { motion } from "framer-motion";
import { Calendar, Clock } from "lucide-react";

export type PeriodOption = "all" | "today" | "2days" | "week";

interface PeriodFilterProps {
  selected: PeriodOption;
  onChange: (period: PeriodOption) => void;
  videoCounts: Record<PeriodOption, number>;
}

const PERIOD_OPTIONS: { id: PeriodOption; label: string; icon?: React.ReactNode }[] = [
  { id: "all", label: "Todos" },
  { id: "today", label: "Hoje" },
  { id: "2days", label: "Últimos 2 dias" },
  { id: "week", label: "Última semana" },
];

export function filterVideosByPeriod<T extends { publishedAt: string }>(
  videos: T[],
  period: PeriodOption
): T[] {
  if (period === "all") return videos;

  const now = new Date();
  const cutoffDate = new Date();

  switch (period) {
    case "today":
      cutoffDate.setHours(0, 0, 0, 0);
      break;
    case "2days":
      cutoffDate.setDate(now.getDate() - 2);
      cutoffDate.setHours(0, 0, 0, 0);
      break;
    case "week":
      cutoffDate.setDate(now.getDate() - 7);
      cutoffDate.setHours(0, 0, 0, 0);
      break;
  }

  return videos.filter((video) => {
    const publishedDate = new Date(video.publishedAt);
    return publishedDate >= cutoffDate;
  });
}

export function countVideosByPeriod<T extends { publishedAt: string }>(
  videos: T[]
): Record<PeriodOption, number> {
  return {
    all: videos.length,
    today: filterVideosByPeriod(videos, "today").length,
    "2days": filterVideosByPeriod(videos, "2days").length,
    week: filterVideosByPeriod(videos, "week").length,
  };
}

export default function PeriodFilter({ selected, onChange, videoCounts }: PeriodFilterProps) {
  return (
    <div className="flex items-center gap-2 flex-wrap">
      <span className="text-sm text-white/40 flex items-center gap-1.5 mr-2">
        <Calendar size={14} />
        Período:
      </span>
      {PERIOD_OPTIONS.map((option) => {
        const count = videoCounts[option.id];
        const isSelected = selected === option.id;
        const isDisabled = count === 0 && option.id !== "all";

        return (
          <motion.button
            key={option.id}
            onClick={() => !isDisabled && onChange(option.id)}
            disabled={isDisabled}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              isSelected
                ? "bg-acid-green/20 text-acid-green border border-acid-green/30"
                : isDisabled
                ? "bg-white/5 text-white/20 cursor-not-allowed"
                : "bg-white/5 text-white/60 hover:bg-white/10 hover:text-white border border-transparent"
            }`}
            whileHover={!isDisabled ? { scale: 1.02 } : {}}
            whileTap={!isDisabled ? { scale: 0.98 } : {}}
          >
            {option.label}
            <span className={`ml-1.5 ${isSelected ? "text-acid-green/70" : "opacity-50"}`}>
              ({count})
            </span>
          </motion.button>
        );
      })}
    </div>
  );
}
