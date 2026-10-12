"use client";

import { motion } from "framer-motion";
import { Filter } from "lucide-react";
import type { Locale } from "@/lib/types";
import { salesFunnel } from "@/lib/data";
import ChartCard from "../charts/ChartCard";

interface FunnelChartProps {
  locale: Locale;
}

const COLORS = ["#EF4056", "#FF7188", "#F59E0B", "#00BFFF", "#22C55E"];

export default function FunnelChart({ locale }: FunnelChartProps) {
  const isFa = locale === "fa";

  return (
    <ChartCard
      titleFa="قیف فروش"
      titleEn="Sales Funnel"
      subtitleFa="مسیر کاربر از بازدید تا خرید"
      subtitleEn="User journey from visit to purchase"
      icon={Filter}
      delay={0.25}
    >
      <div className="space-y-2">
        {salesFunnel.map((step, i) => {
          const widthPercent = step.percentage;
          const dropped = i > 0 ? salesFunnel[i - 1].percentage - step.percentage : 0;

          return (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, x: isFa ? 30 : -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1, duration: 0.4 }}
              className="relative"
            >
              <div className="flex items-center gap-3">
                <div className="w-24 md:w-32 shrink-0 text-end">
                  <div className="text-[11px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
                    {isFa ? step.stepFa : step.step}
                  </div>
                  <div className="text-[10px] text-[#A1A3A8]">
                    {step.value.toLocaleString(isFa ? "fa-IR" : "en-US")}
                  </div>
                </div>

                <div className="flex-1 relative">
                  <div className="h-10 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${widthPercent}%` }}
                      transition={{ delay: 0.3 + i * 0.1, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                      className="h-full rounded-lg relative flex items-center justify-end px-3"
                      style={{
                        background: `linear-gradient(90deg, ${COLORS[i]}, ${COLORS[i]}dd)`,
                        minWidth: "50px",
                      }}
                    >
                      <span className="text-[11px] font-bold text-white tabular-nums">
                        {step.percentage.toFixed(1)}%
                      </span>
                    </motion.div>
                  </div>

                  {dropped > 0 && (
                    <div className="absolute -bottom-2 right-2 text-[9px] text-[#EF4444] font-medium bg-white dark:bg-[#1A1A1E] px-1 rounded">
                      −{dropped.toFixed(1)}%
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </ChartCard>
  );
}
