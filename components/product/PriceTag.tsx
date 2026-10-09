import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

interface PriceTagProps {
  price: number;
  finalPrice: number;
  discountPercent: number;
  locale: Locale;
  size?: "sm" | "md" | "lg";
}

export default function PriceTag({
  price,
  finalPrice,
  discountPercent,
  locale,
  size = "md",
}: PriceTagProps) {
  const isFa = locale === "fa";
  const hasDiscount = discountPercent > 0;

  const sizeClasses = {
    sm: { price: "text-[13px]", old: "text-[10px]", badge: "text-[10px] px-1" },
    md: { price: "text-[15px]", old: "text-[11px]", badge: "text-[11px] px-1.5" },
    lg: { price: "text-[20px]", old: "text-[13px]", badge: "text-[12px] px-2" },
  }[size];

  return (
    <div className="flex flex-col items-start gap-1">
      {hasDiscount && (
        <div className="flex items-center gap-2">
          <span
            className={`${sizeClasses.badge} bg-[#EF4056] text-white rounded font-bold`}
          >
            {discountPercent.toLocaleString(isFa ? "fa-IR" : "en-US")}٪
          </span>
          <span
            className={`${sizeClasses.old} text-[#A1A3A8] line-through`}
          >
            {formatPrice(price, locale)}
          </span>
        </div>
      )}
      <div className="flex items-center gap-1">
        <span className={`${sizeClasses.price} font-bold text-[#3F4064]`}>
          {formatPrice(finalPrice, locale)}
        </span>
        <span className="text-[11px] text-[#62666D]">
          {isFa ? "تومان" : "Toman"}
        </span>
      </div>
    </div>
  );
}
