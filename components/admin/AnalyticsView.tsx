"use client";

import { useState } from "react";
import { Download, RefreshCw } from "lucide-react";
import type { Locale, DateRangePreset } from "@/lib/types";
import {
  DateRangePicker,
  AnalyticsStats,
  MultiLineChart,
  StackedBarChart,
  ActivityHeatmap,
  FunnelChart,
  GoalsCard,
} from "./analytics";

interface AnalyticsViewProps {
  locale: Locale;
}

export default function AnalyticsView({ locale }: AnalyticsViewProps) {
  const isFa = locale === "fa";
  const [preset, setPreset] = useState<DateRangePreset>("last30days");

  return (
    <div className="space-y-4 md:space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {isFa ? "آنالیتیکس" : "Analytics"}
          </h1>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {isFa
              ? "تحلیل دقیق عملکرد فروشگاه"
              : "In-depth analysis of store performance"}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <DateRangePicker locale={locale} value={preset} onChange={setPreset} />
          <button className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-1.5 text-[12px]">
            <RefreshCw size={14} />
            <span className="hidden md:inline">{isFa ? "به‌روزرسانی" : "Refresh"}</span>
          </button>
          <button className="h-10 px-3 rounded-lg bg-[#EF4056] text-white hover:bg-[#d63850] transition-colors flex items-center gap-1.5 text-[12px] font-medium">
            <Download size={14} />
            <span className="hidden md:inline">{isFa ? "دانلود" : "Export"}</span>
          </button>
        </div>
      </div>

      {/* Stats */}
      <AnalyticsStats locale={locale} />

      {/* Multi Line + Stacked */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <MultiLineChart locale={locale} />
        <StackedBarChart locale={locale} />
      </div>

      {/* Heatmap */}
      <ActivityHeatmap locale={locale} />

      {/* Funnel + Goals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <FunnelChart locale={locale} />
        <GoalsCard locale={locale} />
      </div>
    </div>
  );
}
