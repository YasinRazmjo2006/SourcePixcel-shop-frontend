"use client";

import { useState } from "react";
import { Tag, Check, X } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

interface CartSummaryProps {
  locale: Locale;
  subtotal: number;
  totalDiscount: number;
  shipping: number;
  total: number;
  onCheckout: () => void;
}

export default function CartSummary({
  locale,
  subtotal,
  totalDiscount,
  shipping,
  total,
  onCheckout,
}: CartSummaryProps) {
  const isFa = locale === "fa";
  const [coupon, setCoupon] = useState("");
  const [couponStatus, setCouponStatus] = useState<"idle" | "ok" | "error">(
    "idle"
  );

  const t = {
    summary: isFa ? "خلاصه سفارش" : "Order Summary",
    subtotal: isFa ? "جمع کل کالاها" : "Subtotal",
    discount: isFa ? "تخفیف" : "Discount",
    shipping: isFa ? "هزینه ارسال" : "Shipping",
    total: isFa ? "مبلغ قابل پرداخت" : "Total",
    free: isFa ? "رایگان" : "Free",
    couponPlaceholder: isFa ? "کد تخفیف" : "Coupon code",
    apply: isFa ? "اعمال" : "Apply",
    checkout: isFa ? "ادامه فرآیند خرید" : "Proceed to Checkout",
    couponOk: isFa ? "کد تخفیف معتبر است" : "Coupon applied",
    couponError: isFa ? "کد تخفیف نامعتبر است" : "Invalid coupon",
  };

  const handleApplyCoupon = () => {
    if (coupon.trim().toUpperCase() === "SOURCE10") {
      setCouponStatus("ok");
    } else {
      setCouponStatus("error");
    }
  };

  const removeCoupon = () => {
    setCoupon("");
    setCouponStatus("idle");
  };

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 sticky top-24">
      <h2 className="text-[15px] font-bold text-[#3F4064] mb-4">
        {t.summary}
      </h2>

      {/* Coupon */}
      <div className="mb-4">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Tag
              size={14}
              className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
              style={{ [isFa ? "right" : "left"]: 10 } as React.CSSProperties}
            />
            <input
              type="text"
              value={coupon}
              onChange={(e) => {
                setCoupon(e.target.value);
                setCouponStatus("idle");
              }}
              placeholder={t.couponPlaceholder}
              className="w-full h-9 rounded-lg border border-[#E0E0E2] text-[12px] focus:outline-none focus:border-[#EF4056]"
              style={{
                paddingRight: isFa ? 32 : 12,
                paddingLeft: isFa ? 12 : 32,
              }}
            />
          </div>
          {couponStatus === "ok" ? (
            <button
              onClick={removeCoupon}
              className="h-9 px-3 rounded-lg bg-[#22C55E]/10 text-[#22C55E] text-[12px] font-medium flex items-center gap-1"
            >
              <Check size={14} />
            </button>
          ) : (
            <button
              onClick={handleApplyCoupon}
              disabled={!coupon.trim()}
              className="h-9 px-3 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {t.apply}
            </button>
          )}
        </div>
        {couponStatus === "ok" && (
          <p className="text-[11px] text-[#22C55E] mt-2 flex items-center gap-1">
            <Check size={12} /> {t.couponOk}
          </p>
        )}
        {couponStatus === "error" && (
          <p className="text-[11px] text-[#EF4444] mt-2 flex items-center gap-1">
            <X size={12} /> {t.couponError}
          </p>
        )}
      </div>

      {/* Divider */}
      <div className="border-t border-[#E0E0E2] pt-4 space-y-3">
        <div className="flex items-center justify-between text-[13px]">
          <span className="text-[#62666D]">{t.subtotal}</span>
          <span className="text-[#3F4064] font-medium">
            {formatPrice(subtotal, locale)}{" "}
            <span className="text-[10px] text-[#A1A3A8]">
              {isFa ? "تومان" : "T"}
            </span>
          </span>
        </div>

        {totalDiscount > 0 && (
          <div className="flex items-center justify-between text-[13px]">
            <span className="text-[#62666D]">{t.discount}</span>
            <span className="text-[#EF4056] font-medium">
              -{formatPrice(totalDiscount, locale)}{" "}
              <span className="text-[10px]">
                {isFa ? "تومان" : "T"}
              </span>
            </span>
          </div>
        )}

        <div className="flex items-center justify-between text-[13px]">
          <span className="text-[#62666D]">{t.shipping}</span>
          <span
            className={
              shipping === 0
                ? "text-[#22C55E] font-medium"
                : "text-[#3F4064] font-medium"
            }
          >
            {shipping === 0
              ? t.free
              : `${formatPrice(shipping, locale)} ${
                  isFa ? "تومان" : "T"
                }`}
          </span>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-[#E0E0E2] my-4" />

      {/* Total */}
      <div className="flex items-center justify-between mb-4">
        <span className="text-[14px] font-bold text-[#3F4064]">{t.total}</span>
        <div className="flex items-center gap-1">
          <span className="text-[18px] font-bold text-[#EF4056]">
            {formatPrice(total, locale)}
          </span>
          <span className="text-[11px] text-[#62666D]">
            {isFa ? "تومان" : "Toman"}
          </span>
        </div>
      </div>

      {/* Checkout button */}
      <button
        onClick={onCheckout}
        className="w-full h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors"
      >
        {t.checkout}
      </button>

      {/* Hint */}
      <p className="text-[11px] text-[#A1A3A8] text-center mt-3">
        {isFa
          ? "با کد SOURCE10 از ۱۰٪ تخفیف بهره‌مند شوید"
          : "Use code SOURCE10 for 10% off"}
      </p>
    </div>
  );
}
