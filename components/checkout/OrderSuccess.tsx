import Link from "next/link";
import { CheckCircle2, Package, ArrowLeft } from "lucide-react";
import type { Locale } from "@/lib/types";

interface OrderSuccessProps {
  locale: Locale;
  orderNumber: string;
}

export default function OrderSuccess({
  locale,
  orderNumber,
}: OrderSuccessProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-8 md:p-12 text-center max-w-2xl mx-auto">
      <div className="w-20 h-20 rounded-full bg-[#22C55E]/10 flex items-center justify-center mx-auto mb-5">
        <CheckCircle2 size={48} className="text-[#22C55E]" />
      </div>

      <h1 className="text-[22px] font-bold text-[#3F4064] mb-3">
        {isFa ? "سفارش شما ثبت شد!" : "Order placed successfully!"}
      </h1>

      <p className="text-[13px] text-[#62666D] mb-6 leading-6">
        {isFa
          ? "از خرید شما سپاسگزاریم. کد پیگیری سفارش برای شما پیامک خواهد شد."
          : "Thank you for your purchase. Your order tracking code will be sent via SMS."}
      </p>

      <div className="bg-[#FAFAFA] rounded-lg p-4 mb-6 inline-block">
        <div className="text-[11px] text-[#A1A3A8] mb-1">
          {isFa ? "شماره سفارش" : "Order Number"}
        </div>
        <div className="text-[16px] font-bold text-[#3F4064]" dir="ltr">
          {orderNumber}
        </div>
      </div>

      <div className="flex items-center justify-center gap-3 flex-wrap">
        <Link
          href={`/${locale}/account/orders`}
          className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-2"
        >
          <Package size={16} />
          {isFa ? "پیگیری سفارش" : "Track Order"}
        </Link>
        <Link
          href={`/${locale}`}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <ArrowLeft size={16} />
          {isFa ? "بازگشت به فروشگاه" : "Back to Store"}
        </Link>
      </div>
    </div>
  );
}
