"use client";

import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, Clock, MousePointerClick, Users, ShoppingBag } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatCompact, formatPercent } from "@/lib/utils";

interface AnalyticsStatsProps {
  locale: Locale;
}

interface Stat {
  id: string;
  icon: typeof Clock;
  labelFa: string;
  labelEn: string;
  value: number;
  formatted: string;
  change: number;
  color: string;
}

export default function AnalyticsStats({ locale }: AnalyticsStatsProps) {
  const isFa = locale === "fa";

  const stats: Stat[] = [
    {
      id: "session",
      icon: Clock,
      labelFa: "میانگین زمان سشن",
      labelEn: "Avg Session Duration",
      value: 285,
      formatted: isFa ? "۴ دقیقه ۴۵ ثانیه" : "4m 45s",
      change: 8.5,
      color: "#8B5CF6",
    },
    {
      id: "rate",
      icon: MousePointerClick,
      labelFa: "نرخ پرش",
      labelEn: "Bounce Rate",
      value: 32.4,
      formatted: isFa ? "۳۲.۴٪" : "32.4%",
      change: -5.2,
      color: "#F59E0B",
    },
    {
      id: "conversion",
      icon: ShoppingBag,
      labelFa: "نرخ تبدیل",
      labelEn: "Conversion Rate",
      value: 3.42,
      formatted: isFa ? "۳.۴۲٪" : "3.42%",
      change: 12.3,
      color: "#22C55E",
    },
    {
      id: "newusers",
      icon: Users,
      labelFa: "کاربران جدید",
      labelEn: "New Users",
      value: 342,
      formatted: isFa ? "۳۴۲" : "342",
      change: 15.8,
      color: "#00BFFF",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
      {stats.map((stat, i) => {
        const Icon = stat.icon;
        const isUp = stat.change >= 0;
        return (
          <motion.div
            key={stat.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06, duration: 0.4 }}
            className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4"
          >
            <div className="flex items-center justify-between mb-3">
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: `${stat.color}15` }}
              >
                <Icon size={18} style={{ color: stat.color }} />
              </div>
              <div
                className={`flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                  isUp
                    ? "bg-[#22C55E]/10 text-[#22C55E]"
                    : "bg-[#EF4444]/10 text-[#EF4444]"
                }`}
              >
                {isUp ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
                {formatPercent(stat.change, locale)}
              </div>
            </div>
            <div className="text-[18px] md:text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-1.5">
              {stat.formatted}
            </div>
            <div className="text-[11px] text-[#A1A3A8]">
              {isFa ? stat.labelFa : stat.labelEn}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
