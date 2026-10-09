"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Flame, ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { getDiscountedProducts } from "@/lib/data";
import ProductCard from "@/components/product/ProductCard";

interface AmazingOfferProps {
  locale: Locale;
}

export default function AmazingOffer({ locale }: AmazingOfferProps) {
  const isFa = locale === "fa";
  const [timeLeft, setTimeLeft] = useState({
    hours: 12,
    minutes: 34,
    seconds: 56,
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        let { hours, minutes, seconds } = prev;
        seconds--;
        if (seconds < 0) {
          seconds = 59;
          minutes--;
          if (minutes < 0) {
            minutes = 59;
            hours--;
            if (hours < 0) hours = 23;
          }
        }
        return { hours, minutes, seconds };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const products = getDiscountedProducts().slice(0, 5);

  const fmt = (n: number) => {
    const s = String(n).padStart(2, "0");
    return isFa ? s.replace(/\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]) : s;
  };

  return (
    <div className="rounded-xl overflow-hidden bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E]">
      <div className="flex flex-col lg:flex-row">
        {/* Left panel */}
        <div
          className="lg:w-60 p-5 md:p-6 flex lg:flex-col items-center lg:items-start justify-between lg:justify-center gap-4 text-white shrink-0"
          style={{
            background: "linear-gradient(180deg, #EF4056 0%, #d63850 100%)",
          }}
        >
          <div className="flex flex-col items-center lg:items-start gap-2">
            <div className="flex items-center gap-2">
              <div className="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center">
                <Flame size={20} className="text-white" />
              </div>
              <div>
                <h2 className="text-[15px] md:text-[17px] font-bold leading-tight">
                  {isFa ? "پیشنهاد شگفت‌انگیز" : "Amazing Offer"}
                </h2>
                <p className="text-[10px] md:text-[11px] text-white/80">
                  {isFa ? "فرصت محدود" : "Limited time"}
                </p>
              </div>
            </div>

            {/* Countdown */}
            <div className="flex items-center gap-1.5 mt-2">
              <div className="bg-white text-[#EF4056] rounded-lg px-2 py-1.5 text-[15px] font-bold tabular-nums min-w-[36px] text-center shadow-lg">
                {fmt(timeLeft.seconds)}
              </div>
              <span className="text-white/70 text-[14px] font-bold">:</span>
              <div className="bg-white text-[#EF4056] rounded-lg px-2 py-1.5 text-[15px] font-bold tabular-nums min-w-[36px] text-center shadow-lg">
                {fmt(timeLeft.minutes)}
              </div>
              <span className="text-white/70 text-[14px] font-bold">:</span>
              <div className="bg-white text-[#EF4056] rounded-lg px-2 py-1.5 text-[15px] font-bold tabular-nums min-w-[36px] text-center shadow-lg">
                {fmt(timeLeft.hours)}
              </div>
            </div>
          </div>

          <Link
            href={`/${locale}/search?discount=1`}
            className="text-[11px] md:text-[12px] text-white font-medium bg-white/20 backdrop-blur px-3 py-1.5 rounded-full hover:bg-white/30 transition-colors flex items-center gap-1 whitespace-nowrap"
          >
            {isFa ? "مشاهده همه" : "See all"}
            {isFa ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
          </Link>
        </div>

        {/* Products */}
        <div className="flex-1 p-3 md:p-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-2 md:gap-3">
            {products.map((product, index) => (
              <ProductCard
                key={product.id}
                product={product}
                locale={locale}
                variant="compact"
                priority={index === 0}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
