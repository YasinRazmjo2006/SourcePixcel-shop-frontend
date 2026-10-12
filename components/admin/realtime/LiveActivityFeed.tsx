"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  Activity,
  Package,
  Users,
  Star,
  CreditCard,
  AlertTriangle,
  type LucideIcon,
} from "lucide-react";
import type { Locale, ActivityType } from "@/lib/types";
import { useLiveActivityStore } from "@/lib/stores";
import { formatRelativeTime, formatPrice } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import LiveIndicator from "./LiveIndicator";

interface LiveActivityFeedProps {
  locale: Locale;
}

const CONFIG: Record<ActivityType, { icon: LucideIcon; color: string }> = {
  order: { icon: Package, color: "#22C55E" },
  user: { icon: Users, color: "#00BFFF" },
  review: { icon: Star, color: "#F59E0B" },
  payment: { icon: CreditCard, color: "#8B5CF6" },
  product: { icon: AlertTriangle, color: "#EF4056" },
  system: { icon: Activity, color: "#94A3B8" },
};

export default function LiveActivityFeed({ locale }: LiveActivityFeedProps) {
  const isFa = locale === "fa";
  const activities = useLiveActivityStore((s) => s.activities);
  const isConnected = useLiveActivityStore((s) => s.isConnected);

  return (
    <ChartCard
      titleFa="فعالیت زنده"
      titleEn="Live Activity"
      subtitleFa="رویدادهای لحظه‌ای"
      subtitleEn="Real-time events"
      icon={Activity}
      delay={0.1}
      action={<LiveIndicator locale={locale} />}
    >
      <div className="max-h-[400px] overflow-y-auto -mx-2 px-2">
        {activities.length === 0 ? (
          <div className="py-12 text-center">
            <div className="w-12 h-12 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
              <motion.div
                animate={{ scale: [1, 1.2, 1], opacity: [0.6, 1, 0.6] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <Activity size={20} className="text-[#A1A3A8]" />
              </motion.div>
            </div>
            <div className="text-[12px] text-[#A1A3A8]">
              {isFa
                ? isConnected
                  ? "در حال انتظار برای رویدادها..."
                  : "اتصال قطع است"
                : isConnected
                ? "Waiting for events..."
                : "Connection lost"}
            </div>
          </div>
        ) : (
          <div className="space-y-1">
            <AnimatePresence initial={false} mode="popLayout">
              {activities.map((activity) => {
                const config = CONFIG[activity.type];
                const Icon = config.icon;
                return (
                  <motion.div
                    key={activity.id}
                    layout
                    initial={{ opacity: 0, x: -20, height: 0 }}
                    animate={{ opacity: 1, x: 0, height: "auto" }}
                    exit={{ opacity: 0, x: 20, height: 0 }}
                    transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
                    className="flex gap-3 p-2.5 rounded-lg hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors"
                  >
                    <div
                      className="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
                      style={{ backgroundColor: `${config.color}20` }}
                    >
                      <Icon size={14} style={{ color: config.color }} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                          {isFa ? activity.titleFa : activity.titleEn}
                        </div>
                        <span className="text-[9px] text-[#A1A3A8] shrink-0 whitespace-nowrap">
                          {formatRelativeTime(activity.timestamp, locale)}
                        </span>
                      </div>
                      <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] leading-5 mt-0.5">
                        {isFa ? activity.descriptionFa : activity.descriptionEn}
                      </p>
                      {activity.amount && (
                        <div className="text-[10px] font-bold text-[#EF4056] mt-1 tabular-nums">
                          {formatPrice(activity.amount, locale)}{" "}
                          {isFa ? "تومان" : "Toman"}
                        </div>
                      )}
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        )}
      </div>
    </ChartCard>
  );
}
