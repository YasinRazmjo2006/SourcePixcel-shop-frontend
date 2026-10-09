import Link from "next/link";
import { mockOrders } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface RecentOrdersProps {
  locale: string;
}

const STATUS_STYLES: Record<string, { bg: string; text: string; labelFa: string; labelEn: string }> = {
  pending: { bg: "#F59E0B", text: "#F59E0B", labelFa: "در انتظار", labelEn: "Pending" },
  processing: { bg: "#00BFFF", text: "#00BFFF", labelFa: "در حال پردازش", labelEn: "Processing" },
  shipped: { bg: "#8B5CF6", text: "#8B5CF6", labelFa: "ارسال شده", labelEn: "Shipped" },
  delivered: { bg: "#22C55E", text: "#22C55E", labelFa: "تحویل شده", labelEn: "Delivered" },
  cancelled: { bg: "#EF4444", text: "#EF4444", labelFa: "لغو شده", labelEn: "Cancelled" },
};

export default function RecentOrders({ locale }: RecentOrdersProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "سفارشات اخیر" : "Recent Orders"}
        </h3>
        <Link
          href={`/${locale}/admin/orders`}
          className="text-[11px] text-[#00BFFF] hover:text-[#EF4056]"
        >
          {isFa ? "مشاهده همه" : "See all"}
        </Link>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[500px]">
          <thead>
            <tr className="text-[10px] text-[#A1A3A8] uppercase">
              <th className="text-right pb-2 font-medium">
                {isFa ? "شماره" : "ID"}
              </th>
              <th className="text-right pb-2 font-medium">
                {isFa ? "مشتری" : "Customer"}
              </th>
              <th className="text-right pb-2 font-medium">
                {isFa ? "مبلغ" : "Amount"}
              </th>
              <th className="text-right pb-2 font-medium">
                {isFa ? "وضعیت" : "Status"}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
            {mockOrders.map((order) => {
              const status = STATUS_STYLES[order.status];
              return (
                <tr key={order.id} className="text-[12px]">
                  <td className="py-3 text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                    {order.id}
                  </td>
                  <td className="py-3 text-[#62666D] dark:text-[#A1A3A8]">
                    {order.shippingAddress.split("،")[0]}
                  </td>
                  <td className="py-3 font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                    {formatPrice(order.total, isFa ? "fa" : "en")}
                  </td>
                  <td className="py-3">
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
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
