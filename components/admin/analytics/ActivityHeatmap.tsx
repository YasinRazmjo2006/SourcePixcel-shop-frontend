"use client";

import { motion } from "framer-motion";
import { Grid3x3 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { hourlyActivity } from "@/lib/data";
import ChartCard from "../charts/ChartCard";

interface ActivityHeatmapProps {
  locale: Locale;
}

const DAYS_FA = ["شنبه", "یک", "دو", "سه", "چهار", "جمعه", "پنج"];
const DAYS_EN = ["Sat", "Sun", "Mon", "Tue", "Wed", "Fri", "Thu"];

export default function ActivityHeatmap({ locale }: ActivityHeatmapProps) {
  const isFa = locale === "fa";
  const days = isFa ? DAYS_FA : DAYS_EN;

  // Generate 7x24 grid from hourlyActivity
  const grid = days.map((_, dayIdx) =>
    hourlyActivity.map((h) => ({
      hour: h.hour,
      value: h.activity * (0.7 + (dayIdx / 10)),
    }))
  );

  const maxValue = Math.max(...grid.flat().map((c) => c.value));

  const getColor = (value: number) => {
    const intensity = value / maxValue;
    if (intensity < 0.15) return "#F5F5F5";
    if (intensity < 0.3) return "#FFD4DB";
    if (intensity < 0.5) return "#FFA7B5";
    if (intensity < 0.7) return "#FF7188";
    if (intensity < 0.85) return "#EF4056";
    return "#C62F44";
  };

  return (
    <ChartCard
      titleFa="نقشه حرارتی فعالیت"
      titleEn="Activity Heatmap"
      subtitleFa="فعالیت ساعتی در طول هفته"
      subtitleEn="Hourly activity throughout the week"
      icon={Grid3x3}
      delay={0.2}
    >
      <div className="overflow-x-auto -mx-2 px-2">
        <div className="min-w-[600px]">
          {/* Hour labels */}
          <div className="flex items-center gap-1 mb-2 mr-12">
            {Array.from({ length: 24 }, (_, h) => (
              <div
                key={h}
                className="flex-1 text-center text-[9px] text-[#A1A3A8]"
              >
                {h % 3 === 0 ? (isFa ? h.toLocaleString("fa-IR") : h) : ""}
              </div>
            ))}
          </div>

          {/* Grid */}
          <div className="space-y-1">
            {grid.map((row, dayIdx) => (
              <div key={dayIdx} className="flex items-center gap-1">
                <div className="w-10 text-[10px] text-[#A1A3A8] shrink-0">
                  {days[dayIdx]}
                </div>
                <div className="flex-1 flex gap-1">
                  {row.map((cell, h) => (
                    <motion.div
                      key={h}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: dayIdx * 0.02 + h * 0.002 }}
                      className="flex-1 aspect-square rounded-sm hover:scale-125 transition-transform cursor-pointer"
                      style={{ backgroundColor: getColor(cell.value) }}
                      title={`${days[dayIdx]} ${h}:00 — ${Math.round(cell.value)}`}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center justify-end gap-2 mt-4">
            <span className="text-[10px] text-[#A1A3A8]">
              {isFa ? "کم" : "Less"}
            </span>
            {["#F5F5F5", "#FFD4DB", "#FFA7B5", "#FF7188", "#EF4056", "#C62F44"].map(
              (color, i) => (
                <div
                  key={i}
                  className="w-3 h-3 rounded-sm"
                  style={{ backgroundColor: color }}
                />
              )
            )}
            <span className="text-[10px] text-[#A1A3A8]">
              {isFa ? "زیاد" : "More"}
            </span>
          </div>
        </div>
      </div>
    </ChartCard>
  );
}
