# 33_trust.py
# Trust Signals: badges، counters، testimonials، guarantees
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/trust/StatsCounter.tsx
# ============================================================
files.append(("components/trust/StatsCounter.tsx", """"use client";

import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";
import { Users, Package, Star, Truck } from "lucide-react";
import type { Locale } from "@/lib/types";

interface StatsCounterProps {
  locale: Locale;
}

interface StatItem {
  icon: React.ComponentType<{ size?: number; className?: string }>;
  value: number;
  suffix: string;
  labelFa: string;
  labelEn: string;
  color: string;
}

const STATS: StatItem[] = [
  {
    icon: Users,
    value: 125000,
    suffix: "+",
    labelFa: "مشتری راضی",
    labelEn: "Happy Customers",
    color: "#EF4056",
  },
  {
    icon: Package,
    value: 480000,
    suffix: "+",
    labelFa: "سفارش موفق",
    labelEn: "Successful Orders",
    color: "#22C55E",
  },
  {
    icon: Star,
    value: 4.9,
    suffix: "/5",
    labelFa: "امتیاز کاربران",
    labelEn: "User Rating",
    color: "#F59E0B",
  },
  {
    icon: Truck,
    value: 24,
    suffix: "h",
    labelFa: "میانگین ارسال",
    labelEn: "Avg Delivery",
    color: "#00BFFF",
  },
];

function AnimatedNumber({
  value,
  suffix,
  decimals = 0,
}: {
  value: number;
  suffix: string;
  decimals?: number;
}) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-50px" });

  useEffect(() => {
    if (!inView) return;

    const duration = 1500;
    const steps = 60;
    const stepTime = duration / steps;
    const increment = value / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = Math.min(increment * step, value);
      setDisplay(current);

      if (step >= steps) {
        clearInterval(timer);
        setDisplay(value);
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [inView, value]);

  const formatted =
    decimals > 0
      ? display.toFixed(decimals)
      : Math.floor(display).toLocaleString("en-US");

  return (
    <span ref={ref} className="tabular-nums">
      {formatted}
      {suffix}
    </span>
  );
}

export default function StatsCounter({ locale }: StatsCounterProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-gradient-to-l from-[#EF4056] to-[#d63850] rounded-xl overflow-hidden">
      <div className="max-w-[1400px] mx-auto px-4 py-6 md:py-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {STATS.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1, duration: 0.4 }}
                className="flex flex-col items-center text-center text-white"
              >
                <div className="w-12 h-12 rounded-full bg-white/15 backdrop-blur flex items-center justify-center mb-3">
                  <Icon size={22} />
                </div>
                <div className="text-[20px] md:text-[26px] font-bold mb-1">
                  <AnimatedNumber
                    value={stat.value}
                    suffix={stat.suffix}
                    decimals={stat.value < 10 ? 1 : 0}
                  />
                </div>
                <div className="text-[11px] md:text-[12px] text-white/80">
                  {isFa ? stat.labelFa : stat.labelEn}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/trust/TrustBadges.tsx
# ============================================================
files.append(("components/trust/TrustBadges.tsx", """"use client";

import { motion } from "framer-motion";
import {
  ShieldCheck,
  Award,
  Lock,
  BadgeCheck,
  FileCheck,
  Building2,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface TrustBadgesProps {
  locale: Locale;
  variant?: "default" | "compact";
}

const BADGES = [
  {
    icon: ShieldCheck,
    labelFa: "نماد اعتماد الکترونیکی",
    labelEn: "E-Trust Seal",
    color: "#22C55E",
  },
  {
    icon: BadgeCheck,
    labelFa: "ساماندهی رسانه‌های دیجیتال",
    labelEn: "Digital Media Regulation",
    color: "#00BFFF",
  },
  {
    icon: Building2,
    labelFa: "اتحادیه کشوری کسب‌وکار",
    labelEn: "National Business Union",
    color: "#8B5CF6",
  },
  {
    icon: Lock,
    labelFa: "پرداخت امن SSL",
    labelEn: "SSL Secure Payment",
    color: "#F59E0B",
  },
  {
    icon: Award,
    labelFa: "برترین فروشگاه آنلاین",
    labelEn: "Top Online Store",
    color: "#EF4056",
  },
  {
    icon: FileCheck,
    labelFa: "ضمانت بازگشت ۷ روزه",
    labelEn: "7-Day Return Guarantee",
    color: "#10B981",
  },
];

export default function TrustBadges({
  locale,
  variant = "default",
}: TrustBadgesProps) {
  const isFa = locale === "fa";

  if (variant === "compact") {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <h3 className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
          <ShieldCheck size={14} className="text-[#22C55E]" />
          {isFa ? "نشان‌های اعتماد" : "Trust Badges"}
        </h3>
        <div className="grid grid-cols-3 gap-2">
          {BADGES.slice(0, 6).map((badge, i) => {
            const Icon = badge.icon;
            return (
              <motion.div
                key={i}
                whileHover={{ scale: 1.05, y: -2 }}
                className="aspect-square rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex flex-col items-center justify-center gap-1 p-2 cursor-pointer hover:shadow-sm transition-shadow"
                style={{ backgroundColor: `${badge.color}08` }}
              >
                <Icon
                  size={20}
                  style={{ color: badge.color }}
                />
                <span className="text-[8px] text-center text-[#62666D] dark:text-[#A1A3A8] leading-tight">
                  {isFa ? badge.labelFa : badge.labelEn}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center gap-2 mb-4">
        <ShieldCheck size={18} className="text-[#22C55E]" />
        <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "چرا SourcePixcel؟" : "Why SourcePixcel?"}
        </h2>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {BADGES.map((badge, i) => {
          const Icon = badge.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              whileHover={{ scale: 1.03, y: -3 }}
              className="flex flex-col items-center gap-2 p-3 rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] cursor-pointer hover:shadow-md transition-all"
              style={{ backgroundColor: `${badge.color}08` }}
            >
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center"
                style={{ backgroundColor: `${badge.color}15` }}
              >
                <Icon size={22} style={{ color: badge.color }} />
              </div>
              <span className="text-[10px] md:text-[11px] text-center text-[#3F4064] dark:text-[#E5E5EA] font-medium leading-tight">
                {isFa ? badge.labelFa : badge.labelEn}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/trust/Guarantees.tsx
# ============================================================
files.append(("components/trust/Guarantees.tsx", """"use client";

import { motion } from "framer-motion";
import {
  Truck,
  RefreshCw,
  Headphones,
  Award,
  CreditCard,
  Package,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface GuaranteesProps {
  locale: Locale;
}

const GUARANTEES = [
  {
    icon: Truck,
    titleFa: "ارسال سریع",
    titleEn: "Fast Shipping",
    descFa: "ارسال به سراسر ایران در ۲۴ ساعت",
    descEn: "Delivery across Iran within 24 hours",
    color: "#EF4056",
  },
  {
    icon: RefreshCw,
    titleFa: "بازگشت ۷ روزه",
    titleEn: "7-Day Return",
    descFa: "بازگشت آسان بدون قید و شرط",
    descEn: "Easy return without any conditions",
    color: "#22C55E",
  },
  {
    icon: Award,
    titleFa: "ضمانت اصالت",
    titleEn: "Authenticity",
    descFa: "۱۰۰٪ اورجینال و با ضمانت",
    descEn: "100% original with warranty",
    color: "#8B5CF6",
  },
  {
    icon: CreditCard,
    titleFa: "پرداخت امن",
    titleEn: "Secure Payment",
    descFa: "پرداخت آنلاین با رمزنگاری SSL",
    descEn: "Online payment with SSL encryption",
    color: "#00BFFF",
  },
  {
    icon: Headphones,
    titleFa: "پشتیبانی ۲۴/۷",
    titleEn: "24/7 Support",
    descFa: "پاسخگویی در تمام ساعات شبانه‌روز",
    descEn: "Available at all hours",
    color: "#F59E0B",
  },
  {
    icon: Package,
    titleFa: "بسته‌بندی حرفه‌ای",
    titleEn: "Pro Packaging",
    descFa: "بسته‌بندی ایمن و استاندارد",
    descEn: "Safe and standard packaging",
    color: "#EC4899",
  },
];

export default function Guarantees({ locale }: GuaranteesProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-5">
        {isFa ? "تعهدات ما به شما" : "Our Promises to You"}
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {GUARANTEES.map((item, i) => {
          const Icon = item.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="flex items-start gap-3 group"
            >
              <motion.div
                whileHover={{ scale: 1.1, rotate: 5 }}
                className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0"
                style={{ backgroundColor: `${item.color}15` }}
              >
                <Icon size={20} style={{ color: item.color }} />
              </motion.div>
              <div className="min-w-0">
                <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1 group-hover:text-[#EF4056] transition-colors">
                  {isFa ? item.titleFa : item.titleEn}
                </div>
                <div className="text-[10px] text-[#62666D] dark:text-[#A1A3A8] leading-5">
                  {isFa ? item.descFa : item.descEn}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/trust/PaymentMethods.tsx
# ============================================================
files.append(("components/trust/PaymentMethods.tsx", """import type { Locale } from "@/lib/types";

interface PaymentMethodsProps {
  locale: Locale;
}

export default function PaymentMethods({ locale }: PaymentMethodsProps) {
  const isFa = locale === "fa";

  const methods = [
    { nameFa: "زرین‌پال", nameEn: "Zarinpal", color: "#F9A825", short: "Z" },
    { nameFa: "آی‌دی پی", nameEn: "IDPay", color: "#22C55E", short: "ID" },
    { nameFa: "پی‌پینگ", nameEn: "PayPing", color: "#00BFFF", short: "PP" },
    { nameFa: "نکست‌پی", nameEn: "NextPay", color: "#8B5CF6", short: "NP" },
    { nameFa: "شاپرک", nameEn: "Shaparak", color: "#EF4056", short: "SH" },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
        {isFa ? "درگاه‌های پرداخت معتبر" : "Trusted Payment Gateways"}
      </h3>

      <div className="flex items-center gap-2 flex-wrap">
        {methods.map((method, i) => (
          <div
            key={i}
            className="flex items-center gap-2 px-3 py-2 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-sm transition-shadow cursor-pointer"
          >
            <div
              className="w-6 h-6 rounded flex items-center justify-center text-white text-[10px] font-bold shrink-0"
              style={{ backgroundColor: method.color }}
            >
              {method.short}
            </div>
            <span className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] font-medium">
              {isFa ? method.nameFa : method.nameEn}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/trust/Testimonials.tsx (upgraded)
# ============================================================
files.append(("components/trust/Testimonials.tsx", """"use client";

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
"""))

# ============================================================
# components/trust/index.ts
# ============================================================
files.append(("components/trust/index.ts", """// components/trust/index.ts
export { default as StatsCounter } from "./StatsCounter";
export { default as TrustBadges } from "./TrustBadges";
export { default as Guarantees } from "./Guarantees";
export { default as PaymentMethods } from "./PaymentMethods";
export { default as Testimonials } from "./Testimonials";
"""))

# ============================================================
# app/[locale]/page.tsx (updated with trust sections)
# ============================================================
files.append(("app/[locale]/page.tsx", """import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import {
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
} from "@/lib/data";
import {
  HeroSlider,
  ServiceBadges,
  CategoryCircles,
  AmazingOffer,
  ProductSection,
  BrandLogos,
  BlogPreview,
  Newsletter,
} from "@/components/home";
import {
  StatsCounter,
  TrustBadges,
  Guarantees,
  PaymentMethods,
  Testimonials,
} from "@/components/trust";
import JsonLd from "@/components/common/JsonLd";
import {
  buildMetadata,
  buildOrganizationSchema,
  buildWebSiteSchema,
} from "@/lib/utils";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return buildMetadata({
    locale: typedLocale,
    titleFa: "SourcePixcel | فروشگاه آنلاین مدرن",
    titleEn: "SourcePixcel | Modern Online Store",
    descriptionFa:
      "فروشگاه اینترنتی SourcePixcel — خرید آنلاین موبایل، لپ‌تاپ، لوازم خانگی، پوشاک و لوازم جانبی با ارسال سریع و ضمانت اصالت.",
    descriptionEn:
      "SourcePixcel online store — shop mobile phones, laptops, home appliances, fashion, and accessories with fast shipping and authenticity guarantee.",
    path: "",
  });
}

const HOME_SECTION_SIZE = 5;

export default async function HomePage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  const featured = getFeaturedProducts().slice(0, HOME_SECTION_SIZE);
  const newProducts = getNewProducts().slice(0, HOME_SECTION_SIZE);
  const discounted = getDiscountedProducts().slice(0, HOME_SECTION_SIZE);

  return (
    <>
      <JsonLd data={[buildOrganizationSchema(), buildWebSiteSchema()]} />
      <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
        {/* 1. Hero Slider */}
        <HeroSlider locale={typedLocale} />

        {/* 2. Service Badges */}
        <ServiceBadges locale={typedLocale} />

        {/* 3. Categories */}
        <CategoryCircles locale={typedLocale} />

        {/* 4. Amazing Offer */}
        <AmazingOffer locale={typedLocale} />

        {/* 5. Featured */}
        {featured.length > 0 && (
          <ProductSection
            titleFa="پیشنهاد ویژه"
            titleEn="Featured Products"
            products={featured}
            locale={typedLocale}
            seeAllHref="/search?featured=1"
          />
        )}

        {/* 6. New Arrivals */}
        {newProducts.length > 0 && (
          <ProductSection
            titleFa="جدیدترین‌ها"
            titleEn="New Arrivals"
            products={newProducts}
            locale={typedLocale}
            seeAllHref="/search?new=1"
          />
        )}

        {/* 7. Brands */}
        <BrandLogos locale={typedLocale} />

        {/* 8. Discounted */}
        {discounted.length > 0 && (
          <ProductSection
            titleFa="تخفیف‌دارها"
            titleEn="Discounted"
            products={discounted}
            locale={typedLocale}
            seeAllHref="/search?discount=1"
          />
        )}

        {/* 9. Guarantees */}
        <Guarantees locale={typedLocale} />

        {/* 10. Stats Counter */}
        <StatsCounter locale={typedLocale} />

        {/* 11. Trust Badges */}
        <TrustBadges locale={typedLocale} />

        {/* 12. Payment Methods */}
        <PaymentMethods locale={typedLocale} />

        {/* 13. Testimonials */}
        <Testimonials locale={typedLocale} />

        {/* 14. Blog */}
        <BlogPreview locale={typedLocale} />

        {/* 15. Newsletter */}
        <Newsletter locale={typedLocale} />
      </div>
    </>
  );
}
"""))

# ============================================================
# components/home/index.ts (remove old Testimonials)
# ============================================================
files.append(("components/home/index.ts", """// components/home/index.ts
export { default as HeroSlider } from "./HeroSlider";
export { default as ServiceBadges } from "./ServiceBadges";
export { default as CategoryCircles } from "./CategoryCircles";
export { default as AmazingOffer } from "./AmazingOffer";
export { default as ProductSection } from "./ProductSection";
export { default as BrandLogos } from "./BrandLogos";
export { default as BlogPreview } from "./BlogPreview";
export { default as Newsletter } from "./Newsletter";
"""))

# ============================================================
# components/product/ProductDetail.tsx (updated with TrustBadges)
# ============================================================
files.append(("components/product/ProductDetail.tsx", """"use client";

import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Heart,
  ShoppingCart,
  Truck,
  ShieldCheck,
  RotateCcw,
  Share2,
  Check,
} from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore } from "@/lib/stores";
import { getBrandById } from "@/lib/data";
import { TrustBadges } from "@/components/trust";
import RatingStars from "./RatingStars";
import PriceTag from "./PriceTag";
import ProductGallery from "./ProductGallery";
import QuantitySelector from "./QuantitySelector";

interface ProductDetailProps {
  product: Product;
  locale: Locale;
}

export default function ProductDetail({ product, locale }: ProductDetailProps) {
  const isFa = locale === "fa";
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  const addToCart = useCartStore((s) => s.addItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);
  const isInWishlist = useWishlistStore((s) => s.ids.includes(product.id));

  const brand = getBrandById(product.brand);
  const title = isFa ? product.titleFa : product.titleEn;

  const images = [
    product.image,
    `/images/products/product-${product.id}.svg`,
    `/images/products/product-${product.id}.svg`,
    `/images/products/product-${product.id}.svg`,
  ];

  const handleAddToCart = () => {
    if (!product.inStock) return;
    addToCart(product.id, quantity);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const features = [
    { icon: Truck, fa: "ارسال سریع", en: "Fast Shipping" },
    { icon: ShieldCheck, fa: "ضمانت اصالت", en: "Authenticity" },
    { icon: RotateCcw, fa: "۷ روز بازگشت", en: "7-Day Return" },
  ];

  return (
    <div className="space-y-4">
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          <ProductGallery
            images={images}
            alt={title}
            category={product.category}
          />

          <div className="flex flex-col">
            {brand && (
              <div className="text-[12px] text-[#A1A3A8] mb-2">
                {isFa ? "برند:" : "Brand:"}{" "}
                <Link
                  href={`/${locale}/category/${product.category}`}
                  className="text-[#00BFFF] hover:underline"
                >
                  {isFa ? brand.nameFa : brand.nameEn}
                </Link>
              </div>
            )}

            <h1 className="text-[18px] md:text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-7 mb-3">
              {title}
            </h1>

            <div className="flex items-center gap-2 mb-4">
              <RatingStars rating={product.rating} size={14} />
              <span className="text-[12px] text-[#A1A3A8]">
                ({product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
                {isFa ? "نظر" : "reviews"})
              </span>
            </div>

            {product.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {product.tags.map((tag, i) => (
                  <span
                    key={i}
                    className="text-[11px] bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] px-2 py-1 rounded"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] my-4" />

            <div className="mb-4">
              <PriceTag
                price={product.price}
                finalPrice={product.finalPrice}
                discountPercent={product.discountPercent}
                locale={locale}
                size="lg"
              />
            </div>

            <div className="mb-4">
              <span
                className={`text-[13px] font-medium flex items-center gap-2 ${
                  product.inStock ? "text-[#22C55E]" : "text-[#EF4444]"
                }`}
              >
                {product.inStock ? (
                  <>
                    <Check size={16} />
                    {isFa ? "موجود در انبار" : "In stock"}
                  </>
                ) : (
                  <>
                    {isFa ? "ناموجود" : "Out of stock"}
                  </>
                )}
              </span>
            </div>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mb-5">
              <QuantitySelector
                value={quantity}
                onChange={setQuantity}
                max={10}
                locale={locale}
              />
            </div>

            <div className="flex items-center gap-3 mb-6">
              <motion.button
                onClick={handleAddToCart}
                disabled={!product.inStock}
                whileHover={{ scale: product.inStock ? 1.02 : 1 }}
                whileTap={{ scale: product.inStock ? 0.98 : 1 }}
                className={`flex-1 h-11 rounded-lg text-[14px] font-bold flex items-center justify-center gap-2 transition-colors ${
                  product.inStock
                    ? added
                      ? "bg-[#22C55E] text-white"
                      : "bg-[#EF4056] text-white hover:bg-[#d63850]"
                    : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
                }`}
              >
                <ShoppingCart size={18} />
                {added
                  ? isFa
                    ? "به سبد اضافه شد"
                    : "Added to cart"
                  : isFa
                  ? "افزودن به سبد خرید"
                  : "Add to cart"}
              </motion.button>

              <motion.button
                onClick={() => toggleWishlist(product.id)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                aria-label={isFa ? "علاقه‌مندی" : "Wishlist"}
                className={`w-11 h-11 rounded-lg border flex items-center justify-center transition-colors ${
                  isInWishlist
                    ? "border-[#EF4056] bg-[#EF4056]/5"
                    : "border-[#E0E0E2] dark:border-[#2A2A2E] hover:border-[#EF4056]"
                }`}
              >
                <Heart
                  size={18}
                  className={
                    isInWishlist
                      ? "fill-[#EF4056] text-[#EF4056]"
                      : "text-[#62666D]"
                  }
                />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                aria-label={isFa ? "اشتراک‌گذاری" : "Share"}
                className="w-11 h-11 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
              >
                <Share2 size={18} />
              </motion.button>
            </div>

            <div className="bg-[#FAFAFA] dark:bg-[#0F0F12] rounded-lg p-3 space-y-2">
              {features.map((f, i) => {
                const Icon = f.icon;
                return (
                  <div
                    key={i}
                    className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]"
                  >
                    <Icon size={14} className="text-[#A1A3A8]" />
                    <span>{isFa ? f.fa : f.en}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Trust badges section */}
      <TrustBadges locale={locale} variant="compact" />
    </div>
  );
}
"""))

# ============================================================
# components/checkout/CheckoutPage.tsx (updated with payment methods)
# ============================================================
files.append(("components/checkout/CheckoutPage.tsx", """"use client";

import { useState, useMemo, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { Breadcrumb, EmptyState } from "@/components/common";
import { PaymentMethods, TrustBadges } from "@/components/trust";
import StepIndicator from "./StepIndicator";
import ShippingForm, { type ShippingData } from "./ShippingForm";
import ShippingMethod from "./ShippingMethod";
import OrderReview from "./OrderReview";
import ZarinpalGateway from "@/components/payment/ZarinpalGateway";
import PaymentCallback from "@/components/payment/PaymentCallback";

interface CheckoutPageProps {
  locale: Locale;
}

const STEPS = [
  { fa: "اطلاعات ارسال", en: "Shipping" },
  { fa: "روش ارسال", en: "Method" },
  { fa: "پرداخت", en: "Payment" },
];

const EMPTY_SHIPPING: ShippingData = {
  fullName: "",
  mobile: "",
  province: "",
  city: "",
  postalCode: "",
  address: "",
};

export default function CheckoutPage({ locale }: CheckoutPageProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const [step, setStep] = useState(1);
  const [shipping, setShipping] = useState<ShippingData>(EMPTY_SHIPPING);
  const [shippingMethodId, setShippingMethodId] = useState<string | null>(null);
  const [showGateway, setShowGateway] = useState(false);
  const [paymentResult, setPaymentResult] = useState<{
    status: "success" | "failed" | "cancelled";
    authority: string;
  } | null>(null);

  const items = useCartStore((s) => s.items);
  const clearCart = useCartStore((s) => s.clear);

  useEffect(() => {
    setMounted(true);
  }, []);

  const lines = useMemo(() => {
    return items
      .map((line) => {
        const product = allProducts.find((p) => p.id === line.productId);
        return product ? { product, quantity: line.quantity } : null;
      })
      .filter((x): x is { product: Product; quantity: number } => x !== null);
  }, [items]);

  const totals = useMemo(() => {
    const subtotal = lines.reduce(
      (sum, l) => sum + l.product.price * l.quantity,
      0
    );
    const finalTotal = lines.reduce(
      (sum, l) => sum + l.product.finalPrice * l.quantity,
      0
    );
    const totalDiscount = subtotal - finalTotal;
    const FREE = 5_000_000;

    let shippingCost = 0;
    if (shippingMethodId === "post") {
      shippingCost = finalTotal >= FREE ? 0 : 45_000;
    } else if (shippingMethodId === "tipax") {
      shippingCost = finalTotal >= FREE ? 0 : 85_000;
    } else if (shippingMethodId === "pickup") {
      shippingCost = 0;
    }

    const total = finalTotal + shippingCost;
    return { subtotal, totalDiscount, shippingCost, total };
  }, [lines, shippingMethodId]);

  const [orderNumber] = useState(
    () => `SP-${Date.now().toString().slice(-8)}`
  );

  const handlePay = () => {
    setShowGateway(true);
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleGatewaySuccess = (refId: string) => {
    const authority = sessionStorage.getItem("sourcepixcel-txn-authority") || "";
    clearCart();
    setShowGateway(false);
    setPaymentResult({ status: "success", authority });
  };

  const handleGatewayCancel = () => {
    setShowGateway(false);
    setPaymentResult({ status: "cancelled", authority: "" });
  };

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  if (paymentResult) {
    return (
      <PaymentCallback
        locale={locale}
        authority={paymentResult.authority}
        status={paymentResult.status}
      />
    );
  }

  if (showGateway) {
    return (
      <ZarinpalGateway
        locale={locale}
        amount={totals.total}
        orderNumber={orderNumber}
        onSuccess={handleGatewaySuccess}
        onCancel={handleGatewayCancel}
      />
    );
  }

  if (lines.length === 0) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-4">
        <Breadcrumb
          locale={locale}
          items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
        />
        <EmptyState
          locale={locale}
          type="cart"
          titleFa="سبد خرید خالی است"
          titleEn="Your cart is empty"
          messageFa="برای تسویه حساب ابتدا محصولی به سبد خرید اضافه کنید."
          messageEn="Add a product to your cart before checking out."
          actionLabelFa="شروع خرید"
          actionLabelEn="Start shopping"
          actionHref={`/${locale}`}
        />
      </div>
    );
  }

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
        {isFa ? "تسویه حساب" : "Checkout"}
      </h1>

      <StepIndicator currentStep={step} steps={STEPS} locale={locale} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          {step === 1 && (
            <ShippingForm
              locale={locale}
              initialData={shipping}
              onSubmit={(data) => {
                setShipping(data);
                setStep(2);
              }}
            />
          )}

          {step === 2 && (
            <ShippingMethod
              locale={locale}
              selected={shippingMethodId}
              onSelect={setShippingMethodId}
              onNext={() => setStep(3)}
              onBack={() => setStep(1)}
              subtotal={totals.subtotal}
            />
          )}

          {step === 3 && (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
              <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-5">
                {isFa ? "پرداخت" : "Payment"}
              </h2>

              <div className="bg-[#FAFAFA] dark:bg-[#0F0F12] rounded-xl p-4 mb-4 border border-[#E0E0E2] dark:border-[#2A2A2E]">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    {isFa ? "مبلغ قابل پرداخت" : "Amount to Pay"}
                  </span>
                  <span className="text-[18px] font-bold text-[#EF4056]">
                    {totals.total.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
                    <span className="text-[11px] text-[#62666D] font-normal">
                      {isFa ? "تومان" : "T"}
                    </span>
                  </span>
                </div>
                <div className="text-[11px] text-[#A1A3A8] text-center">
                  {isFa
                    ? "پس از کلیک روی پرداخت، به درگاه زرین‌پال منتقل می‌شوید."
                    : "After clicking pay, you will be redirected to Zarinpal."}
                </div>
              </div>

              <div className="border-2 border-dashed border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl p-5 bg-[#F9A825]/5 mb-5">
                <div className="flex items-center justify-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#F9A825] to-[#FFB300] flex items-center justify-center text-white text-[22px] font-bold">
                    Z
                  </div>
                  <div className="text-center">
                    <div className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                      {isFa ? "درگاه پرداخت زرین‌پال" : "Zarinpal Payment Gateway"}
                    </div>
                    <div className="text-[11px] text-[#A1A3A8]">
                      {isFa ? "محیط آزمایشی (Sandbox)" : "Sandbox Environment"}
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep(2)}
                  className="h-11 px-5 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                >
                  {isFa ? "بازگشت" : "Back"}
                </button>
                <button
                  onClick={handlePay}
                  className="flex-1 h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors"
                >
                  {isFa ? "پرداخت و اتمام خرید" : "Pay & Complete Order"}
                </button>
              </div>
            </div>
          )}

          {/* Payment methods + Trust badges in checkout */}
          <PaymentMethods locale={locale} />
        </div>

        <div className="lg:col-span-1 space-y-4">
          {step >= 2 && shipping.fullName ? (
            <OrderReview
              locale={locale}
              lines={lines}
              shipping={shipping}
              shippingMethodId={shippingMethodId ?? "post"}
              subtotal={totals.subtotal}
              totalDiscount={totals.totalDiscount}
              shippingCost={totals.shippingCost}
              total={totals.total}
            />
          ) : (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5 text-[12px] text-[#A1A3A8] text-center">
              {isFa
                ? "اطلاعات سفارش پس از تکمیل فرم نمایش داده می‌شود."
                : "Order details will appear after completing the form."}
            </div>
          )}

          <TrustBadges locale={locale} variant="compact" />
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 33: Trust Signals")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa")
        print("\nYou should see on home page:")
        print("  ✓ Guarantees (6 items)")
        print("  ✓ Stats Counter (animated numbers)")
        print("  ✓ Trust Badges (6 items)")
        print("  ✓ Payment Methods")
        print("  ✓ Testimonials Carousel")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()