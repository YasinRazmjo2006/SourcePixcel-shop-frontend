"use client";

import { useState } from "react";
import { Truck, Zap, Package } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

export interface ShippingOption {
  id: string;
  nameFa: string;
  nameEn: string;
  descFa: string;
  descEn: string;
  price: number;
  icon: "truck" | "zap" | "package";
}

interface ShippingMethodProps {
  locale: Locale;
  selected: string | null;
  onSelect: (id: string) => void;
  onNext: () => void;
  onBack: () => void;
  subtotal: number;
}

export default function ShippingMethod({
  locale,
  selected,
  onSelect,
  onNext,
  onBack,
  subtotal,
}: ShippingMethodProps) {
  const isFa = locale === "fa";

  const FREE_THRESHOLD = 5_000_000;

  const options: ShippingOption[] = [
    {
      id: "post",
      nameFa: "پست پیشتاز",
      nameEn: "Express Post",
      descFa: "۳ تا ۵ روز کاری",
      descEn: "3 to 5 business days",
      price: subtotal >= FREE_THRESHOLD ? 0 : 45_000,
      icon: "truck",
    },
    {
      id: "tipax",
      nameFa: "تیپاکس",
      nameEn: "Tipax",
      descFa: "۱ تا ۲ روز کاری",
      descEn: "1 to 2 business days",
      price: subtotal >= FREE_THRESHOLD ? 0 : 85_000,
      icon: "zap",
    },
    {
      id: "pickup",
      nameFa: "تحویل حضوری",
      nameEn: "Store Pickup",
      descFa: "دریافت از فروشگاه",
      descEn: "Pick up from store",
      price: 0,
      icon: "package",
    },
  ];

  const IconMap = { truck: Truck, zap: Zap, package: Package };

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-5">
        {isFa ? "روش ارسال" : "Shipping Method"}
      </h2>

      {subtotal >= FREE_THRESHOLD && (
        <div className="bg-[#22C55E]/5 border border-[#22C55E]/20 rounded-lg p-3 mb-4 text-[12px] text-[#22C55E]">
          {isFa
            ? "🎉 ارسال شما رایگان است (خرید بالای ۵ میلیون تومان)"
            : "🎉 You have free shipping (orders above 5M Toman)"}
        </div>
      )}

      <div className="space-y-3">
        {options.map((opt) => {
          const Icon = IconMap[opt.icon];
          const isSelected = selected === opt.id;
          return (
            <button
              key={opt.id}
              type="button"
              onClick={() => onSelect(opt.id)}
              className={`w-full flex items-center gap-4 p-4 rounded-lg border-2 text-right transition-colors ${
                isSelected
                  ? "border-[#EF4056] bg-[#EF4056]/5"
                  : "border-[#E0E0E2] hover:border-[#A1A3A8]"
              }`}
            >
              <div
                className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                  isSelected
                    ? "bg-[#EF4056] text-white"
                    : "bg-[#F5F5F5] text-[#62666D]"
                }`}
              >
                <Icon size={20} />
              </div>

              <div className="flex-1 text-right">
                <div className="text-[13px] font-bold text-[#3F4064]">
                  {isFa ? opt.nameFa : opt.nameEn}
                </div>
                <div className="text-[11px] text-[#A1A3A8] mt-0.5">
                  {isFa ? opt.descFa : opt.descEn}
                </div>
              </div>

              <div className="text-left shrink-0">
                <div
                  className={`text-[13px] font-bold ${
                    opt.price === 0 ? "text-[#22C55E]" : "text-[#3F4064]"
                  }`}
                >
                  {opt.price === 0
                    ? isFa
                      ? "رایگان"
                      : "Free"
                    : `${formatPrice(opt.price, locale)} ${
                        isFa ? "تومان" : "T"
                      }`}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      <div className="flex justify-between mt-6">
        <button
          type="button"
          onClick={onBack}
          className="h-10 px-6 rounded-lg border border-[#E0E0E2] text-[13px] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
        >
          {isFa ? "بازگشت" : "Back"}
        </button>
        <button
          type="button"
          onClick={onNext}
          disabled={!selected}
          className="h-10 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isFa ? "ادامه" : "Continue"}
        </button>
      </div>
    </div>
  );
}
