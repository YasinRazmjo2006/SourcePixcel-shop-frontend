"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Star, Quote, ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";

interface TestimonialsProps {
  locale: Locale;
}

const TESTIMONIALS = [
  {
    id: 1,
    nameFa: "علی محمدی",
    nameEn: "Ali Mohammadi",
    roleFa: "مشتری وفادار",
    roleEn: "Loyal Customer",
    textFa:
      "کیفیت محصولات فوق‌العاده بود و ارسال خیلی سریع انجام شد. سه بار از SourcePixcel خرید کردم و هر بار راضی بودم. پشتیبانی‌شون واقعاً حرفه‌ای است.",
    textEn:
      "Product quality was excellent and shipping was very fast. I've ordered three times and was satisfied each time. Their support is truly professional.",
    rating: 5,
    color: "#EF4056",
    initial: "ع",
  },
  {
    id: 2,
    nameFa: "سارا احمدی",
    nameEn: "Sara Ahmadi",
    roleFa: "طراح گرافیک",
    roleEn: "Graphic Designer",
    textFa:
      "قیمت‌ها واقعاً مناسب بود و پشتیبانی ۲۴ ساعته‌شون خیلی کمکم کرد. بسته‌بندی هم خیلی حرفه‌ای بود. حتماً به دوستانم معرفی می‌کنم.",
    textEn:
      "Prices were really reasonable and their 24/7 support helped me a lot. Packaging was very professional. I'll definitely recommend it.",
    rating: 5,
    color: "#00BFFF",
    initial: "س",
  },
  {
    id: 3,
    nameFa: "رضا کریمی",
    nameEn: "Reza Karimi",
    roleFa: "برنامه‌نویس",
    roleEn: "Developer",
    textFa:
      "بسته‌بندی خیلی حرفه‌ای بود و کالا کاملاً سالم رسید. تجربه خرید عالی داشتم. فقط ای کاش تنوع محصولات بیشتری داشت.",
    textEn:
      "Packaging was very professional and the product arrived in perfect condition. Great shopping experience. I just wish there were more product variety.",
    rating: 4,
    color: "#8B5CF6",
    initial: "ر",
  },
  {
    id: 4,
    nameFa: "مریم رضایی",
    nameEn: "Maryam Rezaei",
    roleFa: "پزشک",
    roleEn: "Doctor",
    textFa:
      "از خریدم کاملاً راضی هستم. محصول اورجینال بود و قیمت مناسب. فرآیند بازگشت هم آسان بود (البته نیازی نشد).",
    textEn:
      "I'm completely satisfied with my purchase. The product was original with a good price. The return process is also easy (though I didn't need it).",
    rating: 5,
    color: "#EC4899",
    initial: "م",
  },
];

export default function Testimonials({ locale }: TestimonialsProps) {
  const isFa = locale === "fa";
  const [current, setCurrent] = useState(0);
  const [autoPlay, setAutoPlay] = useState(true);

  useEffect(() => {
    if (!autoPlay) return;
    const timer = setInterval(() => {
      setCurrent((p) => (p + 1) % TESTIMONIALS.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [autoPlay]);

  const next = () => {
    setAutoPlay(false);
    setCurrent((p) => (p + 1) % TESTIMONIALS.length);
  };

  const prev = () => {
    setAutoPlay(false);
    setCurrent((p) => (p - 1 + TESTIMONIALS.length) % TESTIMONIALS.length);
  };

  const t = TESTIMONIALS[current];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
      {/* Header */}
      <div className="p-5 border-b border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-between">
        <div>
          <h2 className="text-[16px] md:text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {isFa ? "نظرات مشتریان" : "Customer Reviews"}
          </h2>
          <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
            {isFa
              ? "بیش از ۱۲۵٬۰۰۰ مشتری راضی از SourcePixcel"
              : "Over 125,000 happy customers at SourcePixcel"}
          </p>
        </div>
        <div className="hidden md:flex items-center gap-1">
          <button
            onClick={prev}
            aria-label="Previous"
            className="w-9 h-9 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
          >
            {isFa ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
          </button>
          <button
            onClick={next}
            aria-label="Next"
            className="w-9 h-9 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
          >
            {isFa ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-5 md:p-8">
        <AnimatePresence mode="wait">
          <motion.div
            key={current}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            transition={{ duration: 0.3 }}
          >
            {/* Quote icon */}
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center mb-4"
              style={{ backgroundColor: `${t.color}15` }}
            >
              <Quote size={18} style={{ color: t.color }} />
            </div>

            {/* Rating */}
            <div className="flex items-center gap-1 mb-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <Star
                  key={i}
                  size={16}
                  className={
                    i < t.rating
                      ? "fill-[#F9A825] text-[#F9A825]"
                      : "text-[#E0E0E2] dark:text-[#3A3A40]"
                  }
                />
              ))}
            </div>

            {/* Text */}
            <p className="text-[13px] md:text-[15px] text-[#3F4064] dark:text-[#E5E5EA] leading-7 md:leading-8 mb-6 min-h-[100px] md:min-h-[80px]">
              "{isFa ? t.textFa : t.textEn}"
            </p>

            {/* Author */}
            <div className="flex items-center gap-3">
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-[16px] shrink-0"
                style={{ backgroundColor: t.color }}
              >
                {t.initial}
              </div>
              <div>
                <div className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                  {isFa ? t.nameFa : t.nameEn}
                </div>
                <div className="text-[11px] text-[#A1A3A8]">
                  {isFa ? t.roleFa : t.roleEn}
                </div>
              </div>
            </div>
          </motion.div>
        </AnimatePresence>

        {/* Dots */}
        <div className="flex items-center justify-center gap-2 mt-6">
          {TESTIMONIALS.map((_, i) => (
            <button
              key={i}
              onClick={() => {
                setAutoPlay(false);
                setCurrent(i);
              }}
              aria-label={`Slide ${i + 1}`}
              className={`h-1.5 rounded-full transition-all ${
                i === current
                  ? "bg-[#EF4056] w-6"
                  : "bg-[#E0E0E2] dark:bg-[#3A3A40] w-1.5"
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
