import Link from "next/link";
import { ShoppingCart, ArrowLeft, ArrowRight } from "lucide-react";
import type { Locale, AdminOrderStatus } from "@/lib/types";
import { adminOrders } from "@/lib/data";
import { formatPrice, formatRelativeTime } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";

interface RecentOrdersTableProps { locale: Locale; }

const STATUS: Record<AdminOrderStatus, { bg: string; fa: string; en: string }> = {
  pending: { bg: "#F59E0B", fa: "در انتظار", en: "Pending" },
  processing: { bg: "#00BFFF", fa: "در حال پردازش", en: "Processing" },
  shipped: { bg: "#8B5CF6", fa: "ارسال شده", en: "Shipped" },
  delivered: { bg: "#22C55E", fa: "تحویل شده", en: "Delivered" },
  cancelled: { bg: "#EF4444", fa: "لغو شده", en: "Cancelled" },
  refunded: { bg: "#94A3B8", fa: "مرجوع", en: "Refunded" },
};

export default function RecentOrdersTable({ locale }: RecentOrdersTableProps) {
  const isFa = locale === "fa";
  const recent = adminOrders.slice(0, 6);

  return (
    <ChartCard
      titleFa="سفارشات اخیر"
      titleEn="Recent Orders"
      subtitleFa="۶ سفارش آخر"
      subtitleEn="Last 6 orders"
      icon={ShoppingCart}
      delay={0.35}
      action={
        <Link href={`/${locale}/admin/orders`} className="text-[11px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors shrink-0">
          {isFa ? "همه" : "All"}
          {isFa ? <ArrowLeft size={12} /> : <ArrowRight size={12} />}
        </Link>
      }
    >
      <div className="overflow-x-auto -mx-4 md:-mx-5 px-4 md:px-5">
        <table className="w-full min-w-[500px]">
          <thead>
            <tr className="text-[10px] text-[#A1A3A8] uppercase border-b border-[#F5F5F5] dark:border-[#2A2A2E]">
              <th className="text-start pb-2 font-medium">{isFa ? "شماره" : "ID"}</th>
              <th className="text-start pb-2 font-medium">{isFa ? "مشتری" : "Customer"}</th>
              <th className="text-start pb-2 font-medium">{isFa ? "مبلغ" : "Total"}</th>
              <th className="text-start pb-2 font-medium">{isFa ? "وضعیت" : "Status"}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
            {recent.map((order) => {
              const s = STATUS[order.status];
              return (
                <tr key={order.id} className="hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors">
                  <td className="py-2.5">
                    <div className="text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">{order.id}</div>
                    <div className="text-[9px] text-[#A1A3A8]">{formatRelativeTime(new Date(order.createdAt).getTime(), locale)}</div>
                  </td>
                  <td className="py-2.5"><div className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] truncate max-w-[120px]">{order.customerName}</div></td>
                  <td className="py-2.5 text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">{formatPrice(order.total, locale)}</td>
                  <td className="py-2.5">
                    <span className="text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap" style={{ backgroundColor: `${s.bg}15`, color: s.bg }}>
                      {isFa ? s.fa : s.en}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </ChartCard>
  );
}
