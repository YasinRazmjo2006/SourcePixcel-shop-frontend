# 21_home_upgrade.py
# ارتقای صفحه اصلی با بخش‌های جدید و طراحی زیباتر
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/home/HeroSlider.tsx (improved)
# ============================================================
files.append(("components/home/HeroSlider.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight, ArrowLeft, ArrowRight } from "lucide-react";
import type { Locale } from "@/lib/types";

interface Slide {
  id: number;
  bgFrom: string;
  bgTo: string;
  emoji: string;
  titleFa: string;
  titleEn: string;
  subtitleFa: string;
  subtitleEn: string;
  ctaFa: string;
  ctaEn: string;
  href: string;
}

const SLIDES: Slide[] = [
  {
    id: 1,
    bgFrom: "#EF4056",
    bgTo: "#FF7B8A",
    emoji: "📱",
    titleFa: "جشنواره موبایل",
    titleEn: "Mobile Festival",
    subtitleFa: "تا ۴۰٪ تخفیف روی گوشی‌های پرچمدار",
    subtitleEn: "Up to 40% off on flagship phones",
    ctaFa: "مشاهده تخفیف‌ها",
    ctaEn: "See Discounts",
    href: "/category/mobile",
  },
  {
    id: 2,
    bgFrom: "#00BFFF",
    bgTo: "#4DD0FF",
    emoji: "💻",
    titleFa: "لپ‌تاپ‌های حرفه‌ای",
    titleEn: "Pro Laptops",
    subtitleFa: "جدیدترین مدل‌های ایسوس، اپل و لنوو",
    subtitleEn: "Latest Asus, Apple, and Lenovo models",
    ctaFa: "خرید کنید",
    ctaEn: "Shop Now",
    href: "/category/laptop",
  },
  {
    id: 3,
    bgFrom: "#8B5CF6",
    bgTo: "#A78BFA",
    emoji: "🎧",
    titleFa: "صدای بی‌نظیر",
    titleEn: "Ultimate Sound",
    subtitleFa: "هدفون‌های بی‌سیم با نویز کنسلینگ",
    subtitleEn: "Wireless headphones with noise cancelling",
    ctaFa: "مشاهده محصولات",
    ctaEn: "View Products",
    href: "/category/audio",
  },
];

interface HeroSliderProps {
  locale: Locale;
}

export default function HeroSlider({ locale }: HeroSliderProps) {
  const isFa = locale === "fa";
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrent((prev) => (prev + 1) % SLIDES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const goTo = (i: number) => setCurrent(i);
  const next = () => setCurrent((prev) => (prev + 1) % SLIDES.length);
  const prev = () =>
    setCurrent((prev) => (prev - 1 + SLIDES.length) % SLIDES.length);

  const slide = SLIDES[current];

  return (
    <div className="relative w-full h-[180px] md:h-[280px] lg:h-[350px] rounded-xl overflow-hidden group">
      {/* Background gradient */}
      <div
        className="absolute inset-0 transition-all duration-700"
        style={{
          background: `linear-gradient(135deg, ${slide.bgFrom} 0%, ${slide.bgTo} 100%)`,
        }}
      />

      {/* Decorative circles */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-20 -right-20 w-80 h-80 rounded-full bg-white/10" />
        <div className="absolute -bottom-24 -left-24 w-96 h-96 rounded-full bg-white/5" />
        <div className="absolute top-1/2 left-1/3 w-40 h-40 rounded-full bg-white/5" />
      </div>

      {/* Content */}
      <div className="relative h-full flex items-center justify-between px-6 md:px-12 lg:px-16">
        {/* Text side */}
        <div className="flex-1 text-white z-10 max-w-lg">
          <h2 className="text-[22px] md:text-[34px] lg:text-[42px] font-bold mb-2 md:mb-3 drop-shadow-lg">
            {isFa ? slide.titleFa : slide.titleEn}
          </h2>
          <p className="text-[12px] md:text-[15px] lg:text-[17px] text-white/90 mb-4 md:mb-6 drop-shadow">
            {isFa ? slide.subtitleFa : slide.subtitleEn}
          </p>
          <Link
            href={`/${locale}${slide.href}`}
            className="inline-flex items-center gap-2 bg-white text-[#3F4064] font-bold text-[12px] md:text-[14px] px-5 md:px-6 py-2.5 md:py-3 rounded-lg hover:bg-white/90 hover:scale-105 transition-all shadow-lg"
          >
            {isFa ? slide.ctaFa : slide.ctaEn}
            {isFa ? <ArrowLeft size={16} /> : <ArrowRight size={16} />}
          </Link>
        </div>

        {/* Icon side */}
        <div className="hidden md:flex items-center justify-center shrink-0">
          <div className="text-[140px] lg:text-[200px] drop-shadow-2xl transform group-hover:scale-110 transition-transform duration-500 select-none">
            {slide.emoji}
          </div>
        </div>
      </div>

      {/* Arrows */}
      <button
        onClick={prev}
        aria-label="Previous slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 md:w-11 md:h-11 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white hover:bg-white/30 opacity-0 group-hover:opacity-100 transition-opacity z-20 ${
          isFa ? "right-3" : "left-3"
        }`}
      >
        {isFa ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>
      <button
        onClick={next}
        aria-label="Next slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 md:w-11 md:h-11 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white hover:bg-white/30 opacity-0 group-hover:opacity-100 transition-opacity z-20 ${
          isFa ? "left-3" : "right-3"
        }`}
      >
        {isFa ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>

      {/* Dots */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-20">
        {SLIDES.map((_, i) => (
          <button
            key={i}
            onClick={() => goTo(i)}
            aria-label={`Slide ${i + 1}`}
            className={`h-1.5 rounded-full transition-all ${
              i === current ? "bg-white w-8" : "bg-white/50 w-2 hover:bg-white/70"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/ServiceBadges.tsx (improved)
# ============================================================
files.append(("components/home/ServiceBadges.tsx", """import {
  Truck,
  ShieldCheck,
  RotateCcw,
  Headphones,
  Award,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface ServiceBadgesProps {
  locale: Locale;
}

export default function ServiceBadges({ locale }: ServiceBadgesProps) {
  const isFa = locale === "fa";

  const badges = [
    {
      icon: Truck,
      fa: "ارسال سریع",
      en: "Fast Shipping",
      color: "#EF4056",
      bg: "#EF4056",
    },
    {
      icon: ShieldCheck,
      fa: "پرداخت امن",
      en: "Secure Payment",
      color: "#22C55E",
      bg: "#22C55E",
    },
    {
      icon: RotateCcw,
      fa: "۷ روز بازگشت",
      en: "7-Day Return",
      color: "#00BFFF",
      bg: "#00BFFF",
    },
    {
      icon: Headphones,
      fa: "پشتیبانی ۲۴/۷",
      en: "24/7 Support",
      color: "#F59E0B",
      bg: "#F59E0B",
    },
    {
      icon: Award,
      fa: "ضمانت اصالت",
      en: "Authentic",
      color: "#8B5CF6",
      bg: "#8B5CF6",
    },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
      <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
        {badges.map((b, i) => {
          const Icon = b.icon;
          return (
            <div
              key={i}
              className="flex flex-col items-center gap-2 text-center group cursor-pointer"
            >
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center transition-transform group-hover:scale-110"
                style={{ backgroundColor: `${b.bg}15` }}
              >
                <Icon size={22} style={{ color: b.color }} />
              </div>
              <span className="text-[11px] md:text-[12px] text-[#62666D] dark:text-[#A1A3A8] font-medium">
                {isFa ? b.fa : b.en}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/CategoryCircles.tsx (improved)
# ============================================================
files.append(("components/home/CategoryCircles.tsx", """import Link from "next/link";
import {
  Smartphone,
  Laptop,
  Tablet,
  Headphones,
  Camera,
  Watch,
  Gamepad2,
  Cable,
  Shirt,
  Footprints,
  Home,
  BookOpen,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string; style?: React.CSSProperties }>> = {
  Smartphone, Laptop, Tablet, Headphones, Camera, Watch,
  Gamepad2, Cable, Shirt, Footprints, Home, BookOpen,
};

const CATEGORY_COLORS: Record<string, string> = {
  mobile: "#EF4056",
  laptop: "#00BFFF",
  tablet: "#8B5CF6",
  audio: "#F59E0B",
  camera: "#22C55E",
  smartwatch: "#EC4899",
  gaming: "#06B6D4",
  accessories: "#6B7280",
  clothing: "#F97316",
  shoes: "#10B981",
  home: "#6366F1",
  books: "#84CC16",
};

interface CategoryCirclesProps {
  locale: Locale;
}

export default function CategoryCircles({ locale }: CategoryCirclesProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[15px] md:text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "دسته‌بندی‌ها" : "Shop by Category"}
        </h2>
      </div>

      <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-3">
        {categories.map((cat) => {
          const Icon = ICON_MAP[cat.icon] ?? Cable;
          const color = CATEGORY_COLORS[cat.id] ?? "#EF4056";
          return (
            <Link
              key={cat.id}
              href={`/${locale}/category/${cat.slug}`}
              className="flex flex-col items-center gap-2 group"
            >
              <div
                className="w-14 h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center transition-all group-hover:scale-110 group-hover:shadow-lg"
                style={{ backgroundColor: `${color}15` }}
              >
                <Icon
                  size={26}
                  style={{ color }}
                  className="transition-transform"
                />
              </div>
              <span className="text-[10px] md:text-[11px] text-[#62666D] dark:text-[#A1A3A8] text-center leading-tight font-medium group-hover:text-[#EF4056] transition-colors">
                {isFa ? cat.nameFa : cat.nameEn}
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/AmazingOffer.tsx (improved)
# ============================================================
files.append(("components/home/AmazingOffer.tsx", """"use client";

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
    return isFa ? s.replace(/\\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]) : s;
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
"""))

# ============================================================
# components/home/Testimonials.tsx (new)
# ============================================================
files.append(("components/home/Testimonials.tsx", """import { Star, Quote } from "lucide-react";
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
"""))

# ============================================================
# components/home/BlogPreview.tsx (new)
# ============================================================
files.append(("components/home/BlogPreview.tsx", """import Link from "next/link";
import Image from "next/image";
import { Calendar, Clock, ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { blogPosts } from "@/lib/data";

interface BlogPreviewProps {
  locale: Locale;
}

export default function BlogPreview({ locale }: BlogPreviewProps) {
  const isFa = locale === "fa";
  const posts = blogPosts.slice(0, 3);

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[16px] md:text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "آخرین مطالب وبلاگ" : "Latest from the Blog"}
        </h2>
        <Link
          href={`/${locale}/blog`}
          className="text-[12px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors"
        >
          {isFa ? "مشاهده همه" : "See all"}
          {isFa ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {posts.map((post) => (
          <Link
            key={post.id}
            href={`/${locale}/blog/${post.slug}`}
            className="group bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div className="relative aspect-video overflow-hidden bg-[#F5F5F5]">
              <Image
                src={post.cover}
                alt={isFa ? post.titleFa : post.titleEn}
                fill
                sizes="(max-width: 768px) 100vw, 33vw"
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <span
                className="absolute top-3 bg-[#EF4056] text-white text-[10px] font-medium px-2 py-1 rounded"
                style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
              >
                {isFa ? post.categoryFa : post.categoryEn}
              </span>
            </div>

            <div className="p-4">
              <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-5 line-clamp-2 mb-2 group-hover:text-[#EF4056] transition-colors min-h-[40px]">
                {isFa ? post.titleFa : post.titleEn}
              </h3>

              <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] line-clamp-2 mb-3 min-h-[32px]">
                {isFa ? post.excerptFa : post.excerptEn}
              </p>

              <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8] pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
                <span className="flex items-center gap-1">
                  <Calendar size={11} />
                  {isFa ? post.dateFa : post.dateEn}
                </span>
                <span className="flex items-center gap-1">
                  <Clock size={11} />
                  {isFa ? post.readTimeFa : post.readTimeEn}
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/Newsletter.tsx (new)
# ============================================================
files.append(("components/home/Newsletter.tsx", """"use client";

import { useState } from "react";
import { Mail, Send, CheckCircle2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { isValidEmail } from "@/lib/utils";

interface NewsletterProps {
  locale: Locale;
}

export default function Newsletter({ locale }: NewsletterProps) {
  const isFa = locale === "fa";
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const t = {
    title: isFa ? "عضویت در خبرنامه" : "Join Our Newsletter",
    subtitle: isFa
      ? "از تخفیف‌های ویژه و محصولات جدید باخبر شوید"
      : "Get notified about special offers and new arrivals",
    placeholder: isFa ? "ایمیل خود را وارد کنید" : "Enter your email",
    submit: isFa ? "عضویت" : "Subscribe",
    success: isFa
      ? "با موفقیت عضو خبرنامه شدید!"
      : "You've successfully subscribed!",
    error: isFa ? "ایمیل نامعتبر است" : "Invalid email address",
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValidEmail(email)) {
      setStatus("error");
      return;
    }
    setStatus("success");
    setEmail("");
    setTimeout(() => setStatus("idle"), 3500);
  };

  return (
    <div
      className="rounded-xl overflow-hidden p-6 md:p-8"
      style={{
        background: "linear-gradient(135deg, #3F4064 0%, #2A2A3E 100%)",
      }}
    >
      <div className="flex flex-col md:flex-row items-center gap-6">
        <div className="flex-1 text-center md:text-start">
          <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center mb-3 mx-auto md:mx-0">
            <Mail size={22} className="text-white" />
          </div>
          <h2 className="text-[18px] md:text-[20px] font-bold text-white mb-2">
            {t.title}
          </h2>
          <p className="text-[12px] md:text-[13px] text-white/70">
            {t.subtitle}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex-1 w-full max-w-md">
          <div className="flex gap-2">
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setStatus("idle");
              }}
              placeholder={t.placeholder}
              dir="ltr"
              className="flex-1 h-12 px-4 rounded-lg bg-white/10 backdrop-blur border border-white/20 text-white placeholder:text-white/50 text-[13px] focus:outline-none focus:border-white/50 transition-colors"
            />
            <button
              type="submit"
              className="h-12 px-5 rounded-lg bg-[#EF4056] text-white font-bold text-[13px] hover:bg-[#d63850] transition-colors flex items-center gap-2 whitespace-nowrap"
            >
              <Send size={16} />
              {t.submit}
            </button>
          </div>

          {status === "success" && (
            <div className="flex items-center gap-2 mt-2 text-[#22C55E] text-[12px]">
              <CheckCircle2 size={14} />
              {t.success}
            </div>
          )}
          {status === "error" && (
            <div className="mt-2 text-[#EF4444] text-[12px]">{t.error}</div>
          )}
        </form>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/index.ts (updated)
# ============================================================
files.append(("components/home/index.ts", """// components/home/index.ts
export { default as HeroSlider } from "./HeroSlider";
export { default as ServiceBadges } from "./ServiceBadges";
export { default as CategoryCircles } from "./CategoryCircles";
export { default as AmazingOffer } from "./AmazingOffer";
export { default as ProductSection } from "./ProductSection";
export { default as BrandLogos } from "./BrandLogos";
export { default as Testimonials } from "./Testimonials";
export { default as BlogPreview } from "./BlogPreview";
export { default as Newsletter } from "./Newsletter";
"""))

# ============================================================
# app/[locale]/page.tsx (updated with new sections)
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
  Testimonials,
  BlogPreview,
  Newsletter,
} from "@/components/home";
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

        {/* 9. Testimonials */}
        <Testimonials locale={typedLocale} />

        {/* 10. Blog */}
        <BlogPreview locale={typedLocale} />

        {/* 11. Newsletter */}
        <Newsletter locale={typedLocale} />
      </div>
    </>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 21: Home Upgrade")
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
        print("Now run:")
        print("  Remove-Item -Recurse -Force .next")
        print("  npm run dev")
        print("\nOpen: http://localhost:3000/fa")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()