"use client";

import type { Locale } from "@/lib/types";
import { useAdminStore } from "@/lib/stores";
import {
  KpiCards,
  SalesChart,
  CategoryChart,
  SharePieChart,
  VisitorsChart,
  TopProductsTable,
  RecentOrdersTable,
  ActivityTimeline,
  QuickActions,
} from "./dashboard";
import RealtimeWidget from "./RealtimeWidget";

interface DashboardViewProps {
  locale: Locale;
}

export default function DashboardView({ locale }: DashboardViewProps) {
  const isFa = locale === "fa";
  const adminName = useAdminStore((s) => s.adminName);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return isFa ? "صبح بخیر" : "Good morning";
    if (hour < 17) return isFa ? "روز بخیر" : "Good afternoon";
    return isFa ? "شب بخیر" : "Good evening";
  };

  return (
    <div className="space-y-4 md:space-y-5">
      <div>
        <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {getGreeting()}، {adminName ?? "Admin"} 👋
        </h1>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? "خلاصه‌ای از عملکرد فروشگاه SourcePixcel"
            : "Overview of SourcePixcel store performance"}
        </p>
      </div>

      <QuickActions locale={locale} />
      <KpiCards locale={locale} />

      <RealtimeWidget locale={locale} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <SalesChart locale={locale} />
        </div>
        <div className="lg:col-span-1">
          <CategoryChart locale={locale} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <VisitorsChart locale={locale} />
        </div>
        <div className="lg:col-span-1">
          <SharePieChart locale={locale} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <TopProductsTable locale={locale} />
        <RecentOrdersTable locale={locale} />
      </div>

      <ActivityTimeline locale={locale} />
    </div>
  );
}
