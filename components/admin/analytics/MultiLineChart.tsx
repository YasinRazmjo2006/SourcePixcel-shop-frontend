"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { Activity } from "lucide-react";
import type { Locale } from "@/lib/types";
import { monthlySales } from "@/lib/data";
import { formatCompact } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import ChartTooltip from "../charts/ChartTooltip";

interface MultiLineChartProps {
  locale: Locale;
}

export default function MultiLineChart({ locale }: MultiLineChartProps) {
  const isFa = locale === "fa";
  const data = monthlySales.map((item) => ({
    ...item,
    label: isFa ? item.monthFa : item.month,
    conversion: Number(((item.orders / item.visitors) * 100).toFixed(2)),
  }));

  return (
    <ChartCard
      titleFa="مقایسه شاخص‌ها"
      titleEn="Metrics Comparison"
      subtitleFa="سفارشات، بازدیدکنندگان و نرخ تبدیل"
      subtitleEn="Orders, visitors and conversion rate"
      icon={Activity}
      delay={0.1}
    >
      <div className="h-[320px] -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E2" opacity={0.4} vertical={false} />
            <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} />
            <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} tickFormatter={(v) => formatCompact(v, locale)} width={50} orientation={isFa ? "right" : "left"} />
            <YAxis yAxisId="right" orientation={isFa ? "left" : "right"} axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} tickFormatter={(v) => `${v}%`} width={40} />
            <Tooltip content={<ChartTooltip />} />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} iconType="circle" iconSize={8} />
            <Line yAxisId="left" type="monotone" dataKey="orders" name={isFa ? "سفارشات" : "Orders"} stroke="#EF4056" strokeWidth={2.5} dot={{ r: 3 }} />
            <Line yAxisId="left" type="monotone" dataKey="visitors" name={isFa ? "بازدیدکننده" : "Visitors"} stroke="#00BFFF" strokeWidth={2.5} dot={{ r: 3 }} />
            <Line yAxisId="right" type="monotone" dataKey="conversion" name={isFa ? "نرخ تبدیل" : "Conversion"} stroke="#22C55E" strokeWidth={2.5} strokeDasharray="5 5" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
