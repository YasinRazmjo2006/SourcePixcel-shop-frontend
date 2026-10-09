import { PackageOpen } from "lucide-react";
import Link from "next/link";
import type { Locale } from "@/lib/types";

interface EmptyStateProps {
  locale: Locale;
  titleFa?: string;
  titleEn?: string;
  messageFa?: string;
  messageEn?: string;
}

export default function EmptyState({
  locale,
  titleFa = "محصولی یافت نشد",
  titleEn = "No products found",
  messageFa = "متأسفانه محصولی با فیلترهای انتخابی شما پیدا نشد.",
  messageEn = "Unfortunately, no products match your selected filters.",
}: EmptyStateProps) {
  const isFa = locale === "fa";

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="w-20 h-20 rounded-full bg-[#F5F5F5] flex items-center justify-center mb-4">
        <PackageOpen size={36} className="text-[#A1A3A8]" />
      </div>
      <h3 className="text-[16px] font-bold text-[#3F4064] mb-2">
        {isFa ? titleFa : titleEn}
      </h3>
      <p className="text-[13px] text-[#62666D] mb-4 max-w-md">
        {isFa ? messageFa : messageEn}
      </p>
      <Link
        href={`/${locale}`}
        className="text-[13px] text-[#EF4056] hover:underline"
      >
        {isFa ? "بازگشت به خانه" : "Back to home"}
      </Link>
    </div>
  );
}
