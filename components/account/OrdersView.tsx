import Link from "next/link";
import { Package, ChevronLeft } from "lucide-react";
import type { Locale } from "@/lib/types";
import { mockOrders } from "@/lib/data";
import { formatPrice } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";
import { EmptyState } from "@/components/common";

interface OrdersViewProps {
  locale: Locale;
}

export default function OrdersView({ locale }: OrdersViewProps) {
  const isFa = locale === "fa";

  if (mockOrders.length === 0) {
    return (
      <EmptyState
        locale={locale}
        titleFa="سفارشی یافت نشد"
        titleEn="No orders found"
        messageFa="شما هنوز سفارشی ثبت نکرده‌اید."
        messageEn="You haven't placed any orders yet."
      />
    );
  }

  return (
    <div className="space-y-3">
      <h1 className="text-[18px] font-bold text-[#3F4064] mb-2">
        {isFa ? "سفارشات من" : "My Orders"}
      </h1>

      {mockOrders.map((order) => (
        <Link
          key={order.id}
          href={`/${locale}/account/orders/${order.id}`}
          className="block bg-white rounded-lg border border-[#E0E0E2] p-4 hover:border-[#EF4056] transition-colors"
        >
          <div className="flex items-center justify-between gap-4 mb-3">
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-10 h-10 rounded-lg bg-[#F5F5F5] flex items-center justify-center shrink-0">
                <Package size={18} className="text-[#62666D]" />
              </div>
              <div className="min-w-0">
                <div className="text-[13px] font-bold text-[#3F4064]" dir="ltr">
                  {order.id}
                </div>
                <div className="text-[11px] text-[#A1A3A8]">{order.date}</div>
              </div>
            </div>
            <OrderStatusBadge status={order.status} locale={locale} />
          </div>

          <div className="flex items-center justify-between gap-4 pt-3 border-t border-[#F5F5F5]">
            <div className="text-[11px] text-[#62666D] truncate flex-1">
              {order.shippingAddress}
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <div className="text-[13px] font-bold text-[#3F4064]">
                {formatPrice(order.total, locale)}{" "}
                <span className="text-[10px] text-[#A1A3A8] font-normal">
                  {isFa ? "تومان" : "T"}
                </span>
              </div>
              <ChevronLeft
                size={16}
                className={`text-[#A1A3A8] ${isFa ? "" : "rotate-180"}`}
              />
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
