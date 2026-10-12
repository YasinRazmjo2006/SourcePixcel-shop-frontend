"use client";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { Layers } from "lucide-react";
import type { Locale } from "@/lib/types";
import { monthlySales } from "@/lib/data";
import { formatCompact } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import ChartTooltip from "../charts/ChartTooltip";

interface StackedBarChartProps {
  locale: Locale;
}

export default function StackedBarChart({ locale }: StackedBarChartProps) {
  const isFa = locale === "fa";
  const data = monthlySales.map((item) => ({
    label: isFa ? item.monthFa : item.month,
    desktop: Math.round(item.visitors * 0.5),
    mobile: Math.round(item.visitors * 0.38),
    tablet: Math.round(item.visitors * 0.12),
  }));

  return (
    <ChartCard
      titleFa="بازدید بر اساس دستگاه"
      titleEn="Visitors by Device"
      subtitleFa="توزیع دسکتاپ، موبایل و تبلت"
      subtitleEn="Desktop, mobile and tablet distribution"
      icon={Layers}
      delay={0.15}
    >
      <div className="h-[320px] -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E2" opacity={0.4} vertical={false} />
            <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} tickFormatter={(v) => formatCompact(v, locale)} width={50} orientation={isFa ? "right" : "left"} />
            <Tooltip content={<ChartTooltip />} cursor={{ fill: "#EF4056", opacity: 0.05 }} />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} iconType="circle" iconSize={8} />
            <Bar dataKey="desktop" name={isFa ? "دسکتاپ" : "Desktop"} stackId="a" fill="#EF4056" radius={[0, 0, 0, 0]} />
            <Bar dataKey="mobile" name={isFa ? "موبایل" : "Mobile"} stackId="a" fill="#00BFFF" />
            <Bar dataKey="tablet" name={isFa ? "تبلت" : "Tablet"} stackId="a" fill="#8B5CF6" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
