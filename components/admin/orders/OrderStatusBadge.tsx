"use client";

import type { Locale, AdminOrderStatus } from "@/lib/types";

interface OrderStatusBadgeProps {
  status: AdminOrderStatus;
  locale: Locale;
}

const CONFIG: Record<
  AdminOrderStatus,
  { bg: string; fa: string; en: string }
> = {
  pending: { bg: "#F59E0B", fa: "در انتظار", en: "Pending" },
  processing: { bg: "#00BFFF", fa: "در حال پردازش", en: "Processing" },
  shipped: { bg: "#8B5CF6", fa: "ارسال شده", en: "Shipped" },
  delivered: { bg: "#22C55E", fa: "تحویل شده", en: "Delivered" },
  cancelled: { bg: "#EF4444", fa: "لغو شده", en: "Cancelled" },
  refunded: { bg: "#94A3B8", fa: "مرجوع", en: "Refunded" },
};

export default function OrderStatusBadge({
  status,
  locale,
}: OrderStatusBadgeProps) {
  const isFa = locale === "fa";
  const c = CONFIG[status];

  return (
    <span
      className="text-[10px] px-2 py-1 rounded-full font-medium whitespace-nowrap inline-block"
      style={{ backgroundColor: `${c.bg}15`, color: c.bg }}
    >
      {isFa ? c.fa : c.en}
    </span>
  );
}
