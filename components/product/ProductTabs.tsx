"use client";

import { useState } from "react";
import type { Locale, Product } from "@/lib/types";
import ReviewsSection from "./ReviewsSection";

interface ProductTabsProps {
  product: Product;
  locale: Locale;
}

export default function ProductTabs({ product, locale }: ProductTabsProps) {
  const isFa = locale === "fa";
  const [activeTab, setActiveTab] = useState<"specs" | "description" | "reviews">(
    "specs"
  );

  const tabs = [
    { id: "specs", fa: "مشخصات", en: "Specifications" },
    { id: "description", fa: "توضیحات", en: "Description" },
    { id: "reviews", fa: "نظرات", en: "Reviews" },
  ] as const;

  const specs = [
    { labelFa: "برند", labelEn: "Brand", valueFa: product.brand, valueEn: product.brand },
    { labelFa: "دسته‌بندی", labelEn: "Category", valueFa: product.category, valueEn: product.category },
    { labelFa: "امتیاز", labelEn: "Rating", valueFa: product.rating.toFixed(1), valueEn: product.rating.toFixed(1) },
    { labelFa: "تعداد نظرات", labelEn: "Review count", valueFa: product.reviewCount.toLocaleString("fa-IR"), valueEn: product.reviewCount.toLocaleString("en-US") },
    { labelFa: "وضعیت", labelEn: "Status", valueFa: product.inStock ? "موجود" : "ناموجود", valueEn: product.inStock ? "In stock" : "Out of stock" },
    { labelFa: "کد محصول", labelEn: "SKU", valueFa: `SP-${product.id.toString().padStart(5, "0")}`, valueEn: `SP-${product.id.toString().padStart(5, "0")}` },
  ];

  const description = isFa
    ? `${product.titleFa} یکی از بهترین محصولات موجود در دسته ${product.category} است. این محصول با کیفیت ساخت بالا و طراحی مدرن، تجربه‌ای بی‌نظیر را برای شما فراهم می‌کند. تمامی محصولات SourcePixcel دارای ضمانت اصالت و ۷ روز مهلت بازگشت هستند.`
    : `${product.titleEn} is one of the best products in the ${product.category} category. With high build quality and modern design, it provides an unparalleled experience. All SourcePixcel products come with authenticity guarantee and 7-day return policy.`;

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
      {/* Tab headers */}
      <div className="flex border-b border-[#E0E0E2] dark:border-[#2A2A2E] overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-5 py-3 text-[13px] font-medium whitespace-nowrap transition-colors border-b-2 ${
              activeTab === tab.id
                ? "text-[#EF4056] border-[#EF4056]"
                : "text-[#62666D] dark:text-[#A1A3A8] border-transparent hover:text-[#3F4064] dark:hover:text-[#E5E5EA]"
            }`}
          >
            {isFa ? tab.fa : tab.en}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-4 md:p-5">
        {activeTab === "specs" && (
          <div className="space-y-0">
            {specs.map((spec, i) => (
              <div
                key={i}
                className={`flex items-start py-3 gap-4 ${
                  i % 2 === 0
                    ? "bg-[#FAFAFA] dark:bg-[#0F0F12]"
                    : "bg-white dark:bg-[#1A1A1E]"
                } rounded px-3`}
              >
                <span className="text-[12px] text-[#A1A3A8] w-32 shrink-0">
                  {isFa ? spec.labelFa : spec.labelEn}
                </span>
                <span className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] flex-1">
                  {isFa ? spec.valueFa : spec.valueEn}
                </span>
              </div>
            ))}
          </div>
        )}

        {activeTab === "description" && (
          <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] leading-7 whitespace-pre-line">
            {description}
          </p>
        )}

        {activeTab === "reviews" && (
          <ReviewsSection productId={product.id} locale={locale} />
        )}
      </div>
    </div>
  );
}
