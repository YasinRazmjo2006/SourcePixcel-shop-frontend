"use client";

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from "recharts";
import { PieChart as PieIcon } from "lucide-react";
import { motion } from "framer-motion";
import type { Locale } from "@/lib/types";
import { categorySales } from "@/lib/data";
import { formatPercent, formatCompact } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import ChartTooltip from "../charts/ChartTooltip";

interface SharePieChartProps { locale: Locale; }

export default function SharePieChart({ locale }: SharePieChartProps) {
  const isFa = locale === "fa";
  const top = categorySales.slice(0, 5);
  const others = categorySales.slice(5);
  const othersTotal = others.reduce((sum, c) => sum + c.sales, 0);

  const data = [
    ...top.map((c) => ({ name: isFa ? c.nameFa : c.nameEn, value: c.sales, color: c.color })),
    ...(othersTotal > 0 ? [{ name: isFa ? "سایر" : "Others", value: othersTotal, color: "#94A3B8" }] : []),
  ];

  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <ChartCard
      titleFa="سهم دسته‌بندی‌ها"
      titleEn="Category Share"
      subtitleFa="سهم از کل فروش"
      subtitleEn="Share of total sales"
      icon={PieIcon}
      delay={0.2}
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
        <div className="h-[220px] relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={data} dataKey="value" nameKey="name" innerRadius={55} outerRadius={85} paddingAngle={2} stroke="none">
                {data.map((entry, i) => (<Cell key={i} fill={entry.color} />))}
              </Pie>
              <Tooltip content={<ChartTooltip formatter={(v) => formatCompact(Number(v), locale)} />} />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center">
              <div className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums leading-none">{formatCompact(total, locale)}</div>
              <div className="text-[9px] text-[#A1A3A8] mt-1">{isFa ? "کل فروش" : "Total"}</div>
            </div>
          </div>
        </div>
        <div className="space-y-2">
          {data.map((item, i) => {
            const percent = (item.value / total) * 100;
            return (
              <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 + i * 0.05 }} className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm shrink-0" style={{ backgroundColor: item.color }} />
                <span className="flex-1 text-[11px] text-[#62666D] dark:text-[#A1A3A8] truncate">{item.name}</span>
                <span className="text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">{formatPercent(percent, locale)}</span>
              </motion.div>
            );
          })}
        </div>
      </div>
    </ChartCard>
  );
}
