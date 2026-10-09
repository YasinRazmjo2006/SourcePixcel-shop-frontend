import Link from "next/link";
import { Eye } from "lucide-react";
import { mockOrders } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface OrdersViewProps {
  locale: string;
}

const STATUS_STYLES: Record<string, { bg: string; text: string; labelFa: string; labelEn: string }> = {
  pending: { bg: "#F59E0B", text: "#F59E0B", labelFa: "در انتظار", labelEn: "Pending" },
  processing: { bg: "#00BFFF", text: "#00BFFF", labelFa: "در حال پردازش", labelEn: "Processing" },
  shipped: { bg: "#8B5CF6", text: "#8B5CF6", labelFa: "ارسال شده", labelEn: "Shipped" },
  delivered: { bg: "#22C55E", text: "#22C55E", labelFa: "تحویل شده", labelEn: "Delivered" },
  cancelled: { bg: "#EF4444", text: "#EF4444", labelFa: "لغو شده", labelEn: "Cancelled" },
};

export default function OrdersView({ locale }: OrdersViewProps) {
  const isFa = locale === "fa";

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {isFa ? "مدیریت سفارشات" : "Orders Management"}
        </h1>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? `${mockOrders.length} سفارش`
            : `${mockOrders.length} orders`}
        </p>
      </div>

      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[11px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-right p-3 font-medium">{isFa ? "شماره" : "ID"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "تاریخ" : "Date"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "مشتری" : "Customer"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "مبلغ" : "Amount"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "وضعیت" : "Status"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "عملیات" : "Actions"}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {mockOrders.map((order) => {
                const status = STATUS_STYLES[order.status];
                return (
                  <tr
                    key={order.id}
                    className="hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors"
                  >
                    <td className="p-3 text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                      {order.id}
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {order.date}
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {order.shippingAddress.split("،")[0]}
                    </td>
                    <td className="p-3 text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                      {formatPrice(order.total, isFa ? "fa" : "en")}
                    </td>
                    <td className="p-3">
                      <span
                        className="text-[10px] px-2 py-1 rounded-full font-medium"
                        style={{
                          backgroundColor: `${status.bg}15`,
                          color: status.text,
                        }}
                      >
                        {isFa ? status.labelFa : status.labelEn}
                      </span>
                    </td>
                    <td className="p-3">
                      <Link
                        href={`/${locale}/account/orders/${order.id}`}
                        className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
                      >
                        <Eye size={14} />
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
