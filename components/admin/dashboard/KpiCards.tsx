"use client";

import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";
import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Users, Package, type LucideIcon } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatCompact, formatPercent } from "@/lib/utils";
import { analyticsOverview } from "@/lib/data";

interface KpiCardsProps {
  locale: Locale;
}

function AnimatedNumber({ value, formatter }: { value: number; formatter: (v: number) => string }) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-50px" });

  useEffect(() => {
    if (!inView) return;
    const duration = 1200;
    const steps = 50;
    const stepTime = duration / steps;
    const increment = value / steps;
    let step = 0;
    const timer = setInterval(() => {
      step++;
      setDisplay(Math.min(increment * step, value));
      if (step >= steps) {
        clearInterval(timer);
        setDisplay(value);
      }
    }, stepTime);
    return () => clearInterval(timer);
  }, [inView, value]);

  return <span ref={ref}>{formatter(display)}</span>;
}

export default function KpiCards({ locale }: KpiCardsProps) {
  const isFa = locale === "fa";

  const kpis: Array<{
    id: string; icon: LucideIcon; labelFa: string; labelEn: string;
    value: number; change: number; color: string;
  }> = [
    { id: "revenue", icon: DollarSign, labelFa: "درآمد کل", labelEn: "Total Revenue", value: analyticsOverview.totalRevenue, change: analyticsOverview.revenueChange, color: "#22C55E" },
    { id: "orders", icon: ShoppingCart, labelFa: "سفارشات", labelEn: "Total Orders", value: analyticsOverview.totalOrders, change: analyticsOverview.ordersChange, color: "#EF4056" },
    { id: "users", icon: Users, labelFa: "کاربران", labelEn: "Total Users", value: analyticsOverview.totalUsers, change: analyticsOverview.usersChange, color: "#00BFFF" },
    { id: "products", icon: Package, labelFa: "محصولات", labelEn: "Products", value: analyticsOverview.totalProducts, change: analyticsOverview.productsChange, color: "#8B5CF6" },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
      {kpis.map((kpi, i) => {
        const Icon = kpi.icon;
        const isUp = kpi.change >= 0;
        const hasChange = kpi.change !== 0;
        return (
          <motion.div
            key={kpi.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06, duration: 0.4 }}
            whileHover={{ y: -3 }}
            className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 relative overflow-hidden"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${kpi.color}15` }}>
                <Icon size={18} style={{ color: kpi.color }} />
              </div>
              {hasChange && (
                <div className={`flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${isUp ? "bg-[#22C55E]/10 text-[#22C55E]" : "bg-[#EF4444]/10 text-[#EF4444]"}`}>
                  {isUp ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
                  {formatPercent(kpi.change, locale)}
                </div>
              )}
            </div>
            <div className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-1.5 tabular-nums">
              {kpi.id === "revenue" ? (
                <>
                  <AnimatedNumber value={kpi.value} formatter={(v) => formatCompact(v, locale)} />
                  <span className="text-[11px] text-[#A1A3A8] font-normal mr-1"> {isFa ? "تومان" : "T"}</span>
                </>
              ) : (
                <AnimatedNumber value={kpi.value} formatter={(v) => isFa ? Math.round(v).toLocaleString("fa-IR") : Math.round(v).toLocaleString("en-US")} />
              )}
            </div>
            <div className="text-[11px] text-[#A1A3A8]">{isFa ? kpi.labelFa : kpi.labelEn}</div>
          </motion.div>
        );
      })}
    </div>
  );
}
