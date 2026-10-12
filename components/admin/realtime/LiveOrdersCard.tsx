"use client";

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
