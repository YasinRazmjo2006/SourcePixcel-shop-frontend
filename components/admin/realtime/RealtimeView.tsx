"use client";

import { motion } from "framer-motion";
import {
  Activity,
  Users,
  Zap,
  Radio,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { useRealtime } from "@/lib/hooks";
import { useLiveActivityStore, useAdminOrdersStore } from "@/lib/stores";
import { OnlineUsersCard, LiveActivityFeed, LiveOrdersCard, LiveIndicator } from ".";

interface RealtimeViewProps {
  locale: Locale;
}

export default function RealtimeView({ locale }: RealtimeViewProps) {
  const isFa = locale === "fa";
  useRealtime(true, 6000);

  const activities = useLiveActivityStore((s) => s.activities);
  const onlineUsers = useLiveActivityStore((s) => s.onlineUsers);
  const orders = useAdminOrdersStore((s) => s.orders);
  const todayOrders = orders.filter(
    (o) =>
      new Date(o.createdAt).toDateString() === new Date().toDateString()
  ).length;

  const t = {
    title: isFa ? "پایش زنده" : "Live Monitoring",
    subtitle: isFa
      ? "رویدادهای لحظه‌ای فروشگاه"
      : "Real-time store events",
  };

  const stats = [
    {
      id: "online",
      icon: Users,
      labelFa: "کاربران آنلاین",
      labelEn: "Users Online",
      value: onlineUsers,
      color: "#00BFFF",
    },
    {
      id: "activities",
      icon: Activity,
      labelFa: "رویدادهای امروز",
      labelEn: "Today's Events",
      value: activities.length,
      color: "#EF4056",
    },
    {
      id: "orders",
      icon: Zap,
      labelFa: "سفارشات امروز",
      labelEn: "Today's Orders",
      value: todayOrders,
      color: "#22C55E",
    },
  ];

  return (
    <div className="space-y-4 md:space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
              {t.title}
            </h1>
            <LiveIndicator locale={locale} />
          </div>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.subtitle}
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 relative overflow-hidden"
            >
              <div className="absolute -top-6 -right-6 w-16 h-16 rounded-full" style={{ backgroundColor: `${stat.color}10` }} />
              <div className="relative flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                  style={{ backgroundColor: `${stat.color}15` }}
                >
                  <Icon size={18} style={{ color: stat.color }} />
                </div>
                <div>
                  <div className="text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none tabular-nums">
                    {stat.value.toLocaleString(isFa ? "fa-IR" : "en-US")}
                  </div>
                  <div className="text-[11px] text-[#A1A3A8] mt-1">
                    {isFa ? stat.labelFa : stat.labelEn}
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Live Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <LiveActivityFeed locale={locale} />
        </div>
        <div className="lg:col-span-1 space-y-4">
          <OnlineUsersCard locale={locale} />
          <LiveOrdersCard locale={locale} />
        </div>
      </div>
    </div>
  );
}
