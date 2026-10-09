import type { Locale } from "@/lib/types";
import type { MockOrder } from "@/lib/data";

interface OrderStatusBadgeProps {
  status: MockOrder["status"];
  locale: Locale;
}

export default function OrderStatusBadge({
  status,
  locale,
}: OrderStatusBadgeProps) {
  const isFa = locale === "fa";

  const map: Record<
    MockOrder["status"],
    { fa: string; en: string; className: string }
  > = {
    pending: {
      fa: "در انتظار پرداخت",
      en: "Pending",
      className: "bg-[#F59E0B]/10 text-[#F59E0B]",
    },
    processing: {
      fa: "در حال پردازش",
      en: "Processing",
      className: "bg-[#00BFFF]/10 text-[#00BFFF]",
    },
    shipped: {
      fa: "ارسال شده",
      en: "Shipped",
      className: "bg-[#8B5CF6]/10 text-[#8B5CF6]",
    },
    delivered: {
      fa: "تحویل داده شده",
      en: "Delivered",
      className: "bg-[#22C55E]/10 text-[#22C55E]",
    },
    cancelled: {
      fa: "لغو شده",
      en: "Cancelled",
      className: "bg-[#EF4444]/10 text-[#EF4444]",
    },
  };

  const item = map[status];

  return (
    <span
      className={`inline-block text-[11px] font-medium px-2 py-1 rounded-full ${item.className}`}
    >
      {isFa ? item.fa : item.en}
    </span>
  );
}
