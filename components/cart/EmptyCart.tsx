import Link from "next/link";
import { ShoppingBag } from "lucide-react";
import type { Locale } from "@/lib/types";

interface EmptyCartProps {
  locale: Locale;
}

export default function EmptyCart({ locale }: EmptyCartProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] py-16 px-4 flex flex-col items-center text-center">
      <div className="w-24 h-24 rounded-full bg-[#F5F5F5] flex items-center justify-center mb-5">
        <ShoppingBag size={44} className="text-[#A1A3A8]" />
      </div>
      <h2 className="text-[18px] font-bold text-[#3F4064] mb-2">
        {isFa ? "سبد خرید شما خالی است" : "Your cart is empty"}
      </h2>
      <p className="text-[13px] text-[#62666D] mb-6 max-w-md">
        {isFa
          ? "می‌توانید از دسته‌بندی‌های مختلف، محصولات مورد نظر خود را اضافه کنید."
          : "You can add products from various categories to your cart."}
      </p>
      <Link
        href={`/${locale}`}
        className="bg-[#EF4056] text-white text-[13px] font-medium px-6 py-2.5 rounded-lg hover:bg-[#d63850] transition-colors"
      >
        {isFa ? "شروع خرید" : "Start shopping"}
      </Link>
    </div>
  );
}
