"use client";

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from "recharts";
import { TrendingUp } from "lucide-react";
import type { Locale } from "@/lib/types";
import { monthlySales } from "@/lib/data";
import { formatCompact, formatPrice } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import ChartTooltip from "../charts/ChartTooltip";

interface SalesChartProps { locale: Locale; }

export default function SalesChart({ locale }: SalesChartProps) {
  const isFa = locale === "fa";
  const data = monthlySales.map((item) => ({ ...item, label: isFa ? item.monthFa : item.month }));

  return (
    <ChartCard
      titleFa="نمودار فروش سالانه"
      titleEn="Annual Sales"
      subtitleFa="فروش ۱۲ ماه گذشته"
      subtitleEn="Last 12 months"
      icon={TrendingUp}
      delay={0.1}
    >
      <div className="h-[280px] -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="salesGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#EF4056" stopOpacity={0.3} />
                <stop offset="100%" stopColor="#EF4056" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E2" opacity={0.4} vertical={false} />
            <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} interval={0} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} tickFormatter={(v) => formatCompact(v, locale)} width={55} orientation={isFa ? "right" : "left"} />
            <Tooltip content={<ChartTooltip formatter={(v) => `${formatPrice(Number(v), locale)} ${isFa ? "تومان" : "T"}`} />} />
            <Area type="monotone" dataKey="sales" name={isFa ? "فروش" : "Sales"} stroke="#EF4056" strokeWidth={2.5} fill="url(#salesGradient)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
