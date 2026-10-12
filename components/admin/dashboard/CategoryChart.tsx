"use client";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from "recharts";
import { BarChart3 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { categorySales } from "@/lib/data";
import { formatCompact, formatPrice } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import ChartTooltip from "../charts/ChartTooltip";

interface CategoryChartProps { locale: Locale; }

export default function CategoryChart({ locale }: CategoryChartProps) {
  const isFa = locale === "fa";
  const data = categorySales.slice(0, 8).map((item) => ({ ...item, label: isFa ? item.nameFa : item.nameEn }));

  return (
    <ChartCard
      titleFa="فروش بر اساس دسته‌بندی"
      titleEn="Sales by Category"
      subtitleFa="۸ دسته‌بندی برتر"
      subtitleEn="Top 8 categories"
      icon={BarChart3}
      delay={0.15}
    >
      <div className="h-[280px] -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E2" opacity={0.4} vertical={false} />
            <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: "#A1A3A8" }} interval={0} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} tickFormatter={(v) => formatCompact(v, locale)} width={55} orientation={isFa ? "right" : "left"} />
            <Tooltip content={<ChartTooltip formatter={(v) => `${formatPrice(Number(v), locale)}`} />} />
            <Bar dataKey="sales" name={isFa ? "فروش" : "Sales"} radius={[6, 6, 0, 0]}>
              {data.map((entry, i) => (<Cell key={i} fill={entry.color} />))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
