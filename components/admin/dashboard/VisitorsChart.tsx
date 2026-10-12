"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";
import { Users } from "lucide-react";
import type { Locale } from "@/lib/types";
import { dailyVisitors } from "@/lib/data";
import { formatCompact } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import ChartTooltip from "../charts/ChartTooltip";

interface VisitorsChartProps { locale: Locale; }

export default function VisitorsChart({ locale }: VisitorsChartProps) {
  const isFa = locale === "fa";
  const data = dailyVisitors.map((item) => {
    const d = new Date(item.date);
    return { ...item, label: d.toLocaleDateString(isFa ? "fa-IR" : "en-US", { month: "short", day: "numeric" }) };
  });

  return (
    <ChartCard
      titleFa="بازدیدکنندگان روزانه"
      titleEn="Daily Visitors"
      subtitleFa="۳۰ روز گذشته"
      subtitleEn="Last 30 days"
      icon={Users}
      delay={0.25}
    >
      <div className="h-[280px] -mx-2">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E0E0E2" opacity={0.4} vertical={false} />
            <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} interval={4} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: "#A1A3A8" }} tickFormatter={(v) => formatCompact(v, locale)} width={45} orientation={isFa ? "right" : "left"} />
            <Tooltip content={<ChartTooltip />} />
            <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} iconType="circle" iconSize={8} />
            <Line type="monotone" dataKey="visitors" name={isFa ? "بازدیدکننده" : "Visitors"} stroke="#00BFFF" strokeWidth={2.5} dot={false} />
            <Line type="monotone" dataKey="newUsers" name={isFa ? "کاربر جدید" : "New Users"} stroke="#8B5CF6" strokeWidth={2.5} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
