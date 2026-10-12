# 46_admin_realtime.py
# Step 9: Real-time + Live Notifications
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# lib/stores/live-activity.ts
# ============================================================
files.append(("lib/stores/live-activity.ts", '''"use client";

import { create } from "zustand";
import type { AdminActivity } from "@/lib/types";

interface LiveActivityState {
  activities: AdminActivity[];
  onlineUsers: number;
  isConnected: boolean;
  addActivity: (activity: AdminActivity) => void;
  setOnlineUsers: (count: number) => void;
  setConnected: (connected: boolean) => void;
  clear: () => void;
}

export const useLiveActivityStore = create<LiveActivityState>((set) => ({
  activities: [],
  onlineUsers: 0,
  isConnected: false,

  addActivity: (activity) =>
    set((state) => ({
      activities: [activity, ...state.activities].slice(0, 50),
    })),

  setOnlineUsers: (count) => set({ onlineUsers: count }),
  setConnected: (connected) => set({ isConnected: connected }),
  clear: () => set({ activities: [] }),
}));
'''))

# ============================================================
# lib/hooks/use-realtime.ts — mock WebSocket
# ============================================================
files.append(("lib/hooks/use-realtime.ts", '''"use client";

import { useEffect, useRef } from "react";
import { useLiveActivityStore } from "@/lib/stores";
import type { AdminActivity, ActivityType } from "@/lib/types";
import {
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
  intBetween,
} from "@/lib/data";

const ACTIVITY_TEMPLATES: Array<{
  type: ActivityType;
  titleFa: string;
  titleEn: string;
  descFa: (name: string, amount?: number) => string;
  descEn: (name: string, amount?: number) => string;
  withAmount?: boolean;
}> = [
  {
    type: "order",
    titleFa: "سفارش جدید",
    titleEn: "New order",
    descFa: (n, a) => `${n} سفارش جدید به مبلغ ${a?.toLocaleString("fa-IR")} تومان ثبت کرد`,
    descEn: (n, a) => `${n} placed an order for ${a?.toLocaleString("en-US")} Toman`,
    withAmount: true,
  },
  {
    type: "user",
    titleFa: "کاربر جدید",
    titleEn: "New user",
    descFa: (n) => `${n} عضو جدید فروشگاه شد`,
    descEn: (n) => `${n} just joined the store`,
  },
  {
    type: "review",
    titleFa: "نظر جدید",
    titleEn: "New review",
    descFa: (n) => `${n} یک نظر جدید ثبت کرد`,
    descEn: (n) => `${n} submitted a new review`,
  },
  {
    type: "payment",
    titleFa: "پرداخت موفق",
    titleEn: "Payment received",
    descFa: (n, a) => `پرداخت ${a?.toLocaleString("fa-IR")} تومان از ${n} دریافت شد`,
    descEn: (n, a) => `Payment of ${a?.toLocaleString("en-US")} Toman received from ${n}`,
    withAmount: true,
  },
  {
    type: "product",
    titleFa: "موجودی کم",
    titleEn: "Low stock",
    descFa: () => `موجودی یکی از محصولات کمتر از ۵ عدد شد`,
    descEn: () => `A product's stock dropped below 5`,
  },
];

function generateRandomActivity(): AdminActivity {
  const template =
    ACTIVITY_TEMPLATES[Math.floor(Math.random() * ACTIVITY_TEMPLATES.length)];
  const firstName =
    PERSIAN_FIRST_NAMES[Math.floor(Math.random() * PERSIAN_FIRST_NAMES.length)];
  const lastName =
    PERSIAN_LAST_NAMES[Math.floor(Math.random() * PERSIAN_LAST_NAMES.length)];
  const fullName = `${firstName} ${lastName}`;
  const amount = template.withAmount
    ? intBetween(200_000, 50_000_000, Math.random)
    : undefined;

  return {
    id: `live-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    type: template.type,
    titleFa: template.titleFa,
    titleEn: template.titleEn,
    descriptionFa: template.descFa(fullName, amount),
    descriptionEn: template.descEn(fullName, amount),
    timestamp: Date.now(),
    user: { name: fullName },
    amount,
  };
}

/**
 * Simulated WebSocket connection that generates live activities.
 * In production, replace with actual WebSocket / Socket.io.
 */
export function useRealtime(enabled = true, intervalMs = 8000) {
  const addActivity = useLiveActivityStore((s) => s.addActivity);
  const setOnlineUsers = useLiveActivityStore((s) => s.setOnlineUsers);
  const setConnected = useLiveActivityStore((s) => s.setConnected);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const onlineIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!enabled) return;

    // Simulate connection
    setConnected(true);
    setOnlineUsers(intBetween(120, 350, Math.random));

    // First activity after 3 seconds
    const firstTimeout = setTimeout(() => {
      addActivity(generateRandomActivity());
    }, 3000);

    // Then regular intervals
    intervalRef.current = setInterval(() => {
      addActivity(generateRandomActivity());
    }, intervalMs);

    // Update online users every 5 seconds
    onlineIntervalRef.current = setInterval(() => {
      setOnlineUsers(intBetween(120, 350, Math.random));
    }, 5000);

    return () => {
      clearTimeout(firstTimeout);
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (onlineIntervalRef.current) clearInterval(onlineIntervalRef.current);
      setConnected(false);
    };
  }, [enabled, intervalMs, addActivity, setOnlineUsers, setConnected]);
}
'''))

# ============================================================
# lib/hooks/index.ts (updated)
# ============================================================
files.append(("lib/hooks/index.ts", '''// lib/hooks/index.ts
export { useDebounce } from "./useDebounce";
export { useIntersectionObserver } from "./useIntersectionObserver";
export {
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  usePrefersReducedMotion,
} from "./useMediaQuery";
export { useVirtualRows } from "./use-virtual-rows";
export { useRealtime } from "./use-realtime";
'''))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", '''// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export { useAdminStore } from "./admin";
export { useAdminUIStore } from "./admin-ui";
export { useAdminProductsStore } from "./admin-products";
export { useAdminOrdersStore } from "./admin-orders";
export { useAdminReportsStore } from "./admin-reports";
export { useLiveActivityStore } from "./live-activity";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
export type { SavedReport, ReportType, ReportFormat } from "./admin-reports";
'''))

# ============================================================
# components/admin/realtime/LiveIndicator.tsx
# ============================================================
files.append(("components/admin/realtime/LiveIndicator.tsx", '''"use client";

import { motion } from "framer-motion";
import { Wifi, WifiOff } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useLiveActivityStore } from "@/lib/stores";

interface LiveIndicatorProps {
  locale: Locale;
}

export default function LiveIndicator({ locale }: LiveIndicatorProps) {
  const isFa = locale === "fa";
  const isConnected = useLiveActivityStore((s) => s.isConnected);

  return (
    <div
      className={`inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full text-[10px] font-bold transition-colors ${
        isConnected
          ? "bg-[#22C55E]/10 text-[#22C55E]"
          : "bg-[#EF4444]/10 text-[#EF4444]"
      }`}
    >
      {isConnected ? (
        <>
          <motion.span
            animate={{ scale: [1, 1.3, 1], opacity: [1, 0.5, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="w-1.5 h-1.5 rounded-full bg-[#22C55E]"
          />
          <Wifi size={11} />
          <span>{isFa ? "زنده" : "LIVE"}</span>
        </>
      ) : (
        <>
          <WifiOff size={11} />
          <span>{isFa ? "قطع" : "OFFLINE"}</span>
        </>
      )}
    </div>
  );
}
'''))

# ============================================================
# components/admin/realtime/OnlineUsersCard.tsx
# ============================================================
files.append(("components/admin/realtime/OnlineUsersCard.tsx", '''"use client";

import { motion } from "framer-motion";
import { Users, TrendingUp } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useLiveActivityStore } from "@/lib/stores";

interface OnlineUsersCardProps {
  locale: Locale;
}

export default function OnlineUsersCard({ locale }: OnlineUsersCardProps) {
  const isFa = locale === "fa";
  const onlineUsers = useLiveActivityStore((s) => s.onlineUsers);
  const isConnected = useLiveActivityStore((s) => s.isConnected);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-[#00BFFF] to-[#0284C7] rounded-xl p-4 text-white relative overflow-hidden"
    >
      {/* Decorative circles */}
      <div className="absolute -top-8 -right-8 w-24 h-24 rounded-full bg-white/10" />
      <div className="absolute -bottom-6 -left-6 w-20 h-20 rounded-full bg-white/5" />

      <div className="relative">
        <div className="flex items-center justify-between mb-3">
          <div className="w-9 h-9 rounded-lg bg-white/15 backdrop-blur flex items-center justify-center">
            <Users size={16} />
          </div>
          {isConnected && (
            <motion.div
              animate={{ opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-[10px] font-bold bg-white/15 backdrop-blur px-2 py-0.5 rounded-full flex items-center gap-1"
            >
              <TrendingUp size={10} />
              {isFa ? "زنده" : "LIVE"}
            </motion.div>
          )}
        </div>

        <div className="text-[28px] font-bold leading-none tabular-nums mb-1">
          {onlineUsers.toLocaleString(isFa ? "fa-IR" : "en-US")}
        </div>
        <div className="text-[11px] text-white/80">
          {isFa ? "کاربر آنلاین" : "Users Online"}
        </div>
      </div>
    </motion.div>
  );
}
'''))

# ============================================================
# components/admin/realtime/LiveActivityFeed.tsx
# ============================================================
files.append(("components/admin/realtime/LiveActivityFeed.tsx", '''"use client";

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
'''))

# ============================================================
# components/admin/realtime/LiveOrdersCard.tsx
# ============================================================
files.append(("components/admin/realtime/LiveOrdersCard.tsx", '''"use client";

import { motion } from "framer-motion";
import { ShoppingCart, ArrowLeft, ArrowRight } from "lucide-react";
import Link from "next/link";
import type { Locale } from "@/lib/types";
import { useAdminOrdersStore } from "@/lib/stores";
import { formatPrice, formatRelativeTime } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";
import OrderStatusBadge from "../orders/OrderStatusBadge";

interface LiveOrdersCardProps {
  locale: Locale;
}

export default function LiveOrdersCard({ locale }: LiveOrdersCardProps) {
  const isFa = locale === "fa";
  const orders = useAdminOrdersStore((s) => s.orders);
  const recent = orders.slice(0, 5);

  return (
    <ChartCard
      titleFa="آخرین سفارشات"
      titleEn="Latest Orders"
      subtitleFa="به‌روزرسانی خودکار"
      subtitleEn="Auto-updating"
      icon={ShoppingCart}
      delay={0.15}
      action={
        <Link
          href={`/${locale}/admin/orders`}
          className="text-[11px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors shrink-0"
        >
          {isFa ? "همه" : "All"}
          {isFa ? <ArrowLeft size={12} /> : <ArrowRight size={12} />}
        </Link>
      }
    >
      <div className="space-y-2">
        {recent.map((order, i) => (
          <motion.div
            key={order.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors"
          >
            <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center shrink-0">
              <ShoppingCart size={14} className="text-[#EF4056]" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2 mb-0.5">
                <div className="text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                  {order.id}
                </div>
                <OrderStatusBadge status={order.status} locale={locale} />
              </div>
              <div className="flex items-center justify-between gap-2">
                <span className="text-[10px] text-[#A1A3A8] truncate">
                  {order.customerName}
                </span>
                <span className="text-[11px] font-bold text-[#EF4056] tabular-nums shrink-0">
                  {formatPrice(order.total, locale)}
                </span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </ChartCard>
  );
}
'''))

# ============================================================
# components/admin/realtime/index.ts
# ============================================================
files.append(("components/admin/realtime/index.ts", '''// components/admin/realtime/index.ts
export { default as LiveIndicator } from "./LiveIndicator";
export { default as OnlineUsersCard } from "./OnlineUsersCard";
export { default as LiveActivityFeed } from "./LiveActivityFeed";
export { default as LiveOrdersCard } from "./LiveOrdersCard";
'''))

# ============================================================
# components/admin/RealtimeWidget.tsx — to add to dashboard
# ============================================================
files.append(("components/admin/RealtimeWidget.tsx", '''"use client";

import type { Locale } from "@/lib/types";
import { useRealtime } from "@/lib/hooks";
import { OnlineUsersCard, LiveActivityFeed, LiveOrdersCard } from "./realtime";

interface RealtimeWidgetProps {
  locale: Locale;
  enabled?: boolean;
}

export default function RealtimeWidget({
  locale,
  enabled = true,
}: RealtimeWidgetProps) {
  useRealtime(enabled);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="lg:col-span-1 space-y-4">
        <OnlineUsersCard locale={locale} />
      </div>
      <div className="lg:col-span-2">
        <LiveActivityFeed locale={locale} />
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/realtime/RealtimeView.tsx — full page
# ============================================================
files.append(("components/admin/realtime/RealtimeView.tsx", '''"use client";

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
'''))

# ============================================================
# app/[locale]/admin/realtime/page.tsx
# ============================================================
files.append(("app/[locale]/admin/realtime/page.tsx", '''import RealtimeView from "@/components/admin/realtime/RealtimeView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminRealtimePage({ params }: PageProps) {
  const { locale } = await params;
  return <RealtimeView locale={locale as "fa" | "en"} />;
}
'''))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", '''// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as DashboardView } from "./DashboardView";
export { default as AnalyticsView } from "./AnalyticsView";
export { default as UsersView } from "./UsersView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as ReportsView } from "./ReportsView";
export { default as AdminLoginForm } from "./AdminLoginForm";
export { default as RealtimeWidget } from "./RealtimeWidget";

// Layout
export * from "./layout";

// Dashboard
export * from "./dashboard";

// Analytics
export * from "./analytics";

// Users
export * from "./users";

// Products
export * from "./products";

// Orders
export * from "./orders";

// Reports
export * from "./reports";

// Realtime
export * from "./realtime";

// Charts
export * from "./charts";
'''))

# ============================================================
# lib/admin-nav.ts (updated) — add realtime link
# ============================================================
files.append(("lib/admin-nav.ts", '''// lib/admin-nav.ts
import {
  LayoutDashboard,
  BarChart3,
  Package,
  ShoppingCart,
  Users,
  Tag,
  Star,
  FileText,
  Settings,
  Layers,
  Radio,
  type LucideIcon,
} from "lucide-react";

export interface AdminNavItem {
  id: string;
  href: string;
  labelFa: string;
  labelEn: string;
  icon: LucideIcon;
  badge?: number | "dynamic";
  children?: AdminNavItem[];
  exact?: boolean;
}

export const ADMIN_NAV: AdminNavItem[] = [
  {
    id: "dashboard",
    href: "/admin",
    labelFa: "داشبورد",
    labelEn: "Dashboard",
    icon: LayoutDashboard,
    exact: true,
  },
  {
    id: "realtime",
    href: "/admin/realtime",
    labelFa: "پایش زنده",
    labelEn: "Real-time",
    icon: Radio,
    badge: "dynamic",
  },
  {
    id: "analytics",
    href: "/admin/analytics",
    labelFa: "آنالیتیکس",
    labelEn: "Analytics",
    icon: BarChart3,
  },
  {
    id: "products",
    href: "/admin/products",
    labelFa: "محصولات",
    labelEn: "Products",
    icon: Package,
    children: [
      {
        id: "products-list",
        href: "/admin/products",
        labelFa: "لیست محصولات",
        labelEn: "Products List",
        icon: Package,
        exact: true,
      },
      {
        id: "categories",
        href: "/admin/categories",
        labelFa: "دسته‌بندی‌ها",
        labelEn: "Categories",
        icon: Layers,
      },
    ],
  },
  {
    id: "orders",
    href: "/admin/orders",
    labelFa: "سفارشات",
    labelEn: "Orders",
    icon: ShoppingCart,
    badge: 4,
  },
  {
    id: "users",
    href: "/admin/users",
    labelFa: "کاربران",
    labelEn: "Users",
    icon: Users,
  },
  {
    id: "discounts",
    href: "/admin/discounts",
    labelFa: "تخفیف‌ها",
    labelEn: "Discounts",
    icon: Tag,
  },
  {
    id: "reviews",
    href: "/admin/reviews",
    labelFa: "نظرات",
    labelEn: "Reviews",
    icon: Star,
  },
  {
    id: "reports",
    href: "/admin/reports",
    labelFa: "گزارشات",
    labelEn: "Reports",
    icon: FileText,
  },
  {
    id: "settings",
    href: "/admin/settings",
    labelFa: "تنظیمات",
    labelEn: "Settings",
    icon: Settings,
  },
];

export interface FlatNavItem {
  id: string;
  href: string;
  labelFa: string;
  labelEn: string;
  icon: LucideIcon;
}

export const FLAT_ADMIN_NAV: FlatNavItem[] = ADMIN_NAV.flatMap((item) => {
  const self = {
    id: item.id,
    href: item.href,
    labelFa: item.labelFa,
    labelEn: item.labelEn,
    icon: item.icon,
  };
  const children = (item.children ?? []).map((child) => ({
    id: child.id,
    href: child.href,
    labelFa: child.labelFa,
    labelEn: child.labelEn,
    icon: child.icon,
  }));
  return [self, ...children];
});
'''))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 9: Real-time")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")
    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/realtime")

if __name__ == "__main__":
    main()