import { Star, Quote } from "lucide-react";
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
      "کیفیت محصولات فوق‌العاده بود و ارسال خیلی سریع انجام شد. حتماً دوباره خرید می‌کنم.",
    textEn:
      "Product quality was excellent and shipping was very fast. I will definitely buy again.",
    rating: 5,
    color: "#EF4056",
  },
  {
    id: 2,
    nameFa: "سارا احمدی",
    nameEn: "Sara Ahmadi",
    roleFa: "طراح گرافیک",
    roleEn: "Graphic Designer",
    textFa:
      "قیمت‌ها واقعاً مناسب بود و پشتیبانی ۲۴ ساعته‌شون خیلی کمکم کرد. ممنون SourcePixcel!",
    textEn:
      "Prices were really reasonable and their 24/7 support helped me a lot. Thanks SourcePixcel!",
    rating: 5,
    color: "#00BFFF",
  },
  {
    id: 3,
    nameFa: "رضا کریمی",
    nameEn: "Reza Karimi",
    roleFa: "برنامه‌نویس",
    roleEn: "Developer",
    textFa:
      "بسته‌بندی خیلی حرفه‌ای بود و کالا کاملاً سالم رسید. تجربه خرید عالی داشتم.",
    textEn:
      "Packaging was very professional and the product arrived in perfect condition. Great shopping experience.",
    rating: 4,
    color: "#8B5CF6",
  },
];

export default function Testimonials({ locale }: TestimonialsProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="mb-5">
        <h2 className="text-[16px] md:text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {isFa ? "نظرات مشتریان" : "Customer Reviews"}
        </h2>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? "بیش از ۱۰٬۰۰۰ مشتری راضی از SourcePixcel"
            : "Over 10,000 happy customers at SourcePixcel"}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {TESTIMONIALS.map((t) => (
          <div
            key={t.id}
            className="relative bg-[#FAFAFA] dark:bg-[#2A2A2E] rounded-xl p-5 hover:shadow-lg transition-shadow"
          >
            {/* Quote icon */}
            <div
              className="absolute top-4 w-8 h-8 rounded-full flex items-center justify-center"
              style={{
                backgroundColor: `${t.color}15`,
                [isFa ? "left" : "right"]: 16,
              } as React.CSSProperties}
            >
              <Quote size={14} style={{ color: t.color }} />
            </div>

            {/* Rating */}
            <div className="flex items-center gap-1 mb-3">
              {Array.from({ length: 5 }).map((_, i) => (
                <Star
                  key={i}
                  size={14}
                  className={
                    i < t.rating
                      ? "fill-[#F9A825] text-[#F9A825]"
                      : "text-[#E0E0E2]"
                  }
                />
              ))}
            </div>

            {/* Text */}
            <p className="text-[12px] md:text-[13px] text-[#62666D] dark:text-[#A1A3A8] leading-6 mb-4 min-h-[80px]">
              "{isFa ? t.textFa : t.textEn}"
            </p>

            {/* Author */}
            <div className="flex items-center gap-3 pt-3 border-t border-[#E0E0E2] dark:border-[#3A3A40]">
              <div
                className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-[14px] shrink-0"
                style={{ backgroundColor: t.color }}
              >
                {(isFa ? t.nameFa : t.nameEn)[0]}
              </div>
              <div>
                <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                  {isFa ? t.nameFa : t.nameEn}
                </div>
                <div className="text-[10px] text-[#A1A3A8]">
                  {isFa ? t.roleFa : t.roleEn}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
