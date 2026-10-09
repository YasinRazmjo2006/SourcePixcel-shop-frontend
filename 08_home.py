# 08_home.py
# ساخت صفحه اصلی کامل
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/home/HeroSlider.tsx
# ============================================================
files.append(("components/home/HeroSlider.tsx", """"use client";

import { useState, useEffect } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";

interface Slide {
  id: number;
  image: string;
  titleFa: string;
  titleEn: string;
  ctaFa: string;
  ctaEn: string;
  href: string;
}

const SLIDES: Slide[] = [
  {
    id: 1,
    image: "https://picsum.photos/seed/hero1/1400/500",
    titleFa: "جشنواره فروش ویژه",
    titleEn: "Special Sale Festival",
    ctaFa: "مشاهده تخفیف‌ها",
    ctaEn: "See Discounts",
    href: "/category/mobile",
  },
  {
    id: 2,
    image: "https://picsum.photos/seed/hero2/1400/500",
    titleFa: "جدیدترین لپ‌تاپ‌ها",
    titleEn: "Latest Laptops",
    ctaFa: "خرید کنید",
    ctaEn: "Shop Now",
    href: "/category/laptop",
  },
  {
    id: 3,
    image: "https://picsum.photos/seed/hero3/1400/500",
    titleFa: "هدفون‌های حرفه‌ای",
    titleEn: "Pro Headphones",
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
    <div className="relative w-full h-[180px] md:h-[280px] lg:h-[350px] rounded-lg overflow-hidden bg-[#F5F5F5] group">
      {/* Image */}
      <img
        src={slide.image}
        alt={isFa ? slide.titleFa : slide.titleEn}
        className="absolute inset-0 w-full h-full object-cover transition-opacity duration-500"
      />

      {/* Overlay */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent" />

      {/* Content */}
      <div
        className={`absolute bottom-6 z-10 ${
          isFa ? "right-6 md:right-10" : "left-6 md:left-10"
        }`}
      >
        <h2 className="text-white text-xl md:text-3xl font-bold mb-2">
          {isFa ? slide.titleFa : slide.titleEn}
        </h2>
        <a
          href={`/${locale}${slide.href}`}
          className="inline-block bg-[#EF4056] text-white text-[12px] md:text-[14px] font-medium px-4 py-2 rounded-lg hover:bg-[#d63850] transition-colors"
        >
          {isFa ? slide.ctaFa : slide.ctaEn}
        </a>
      </div>

      {/* Arrows */}
      <button
        onClick={prev}
        aria-label="Previous slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-[#3F4064] opacity-0 group-hover:opacity-100 transition-opacity ${
          isFa ? "right-3" : "left-3"
        }`}
      >
        {isFa ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
      </button>
      <button
        onClick={next}
        aria-label="Next slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-white/80 backdrop-blur flex items-center justify-center text-[#3F4064] opacity-0 group-hover:opacity-100 transition-opacity ${
          isFa ? "left-3" : "right-3"
        }`}
      >
        {isFa ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
      </button>

      {/* Dots */}
      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2 z-10">
        {SLIDES.map((_, i) => (
          <button
            key={i}
            onClick={() => goTo(i)}
            aria-label={`Slide ${i + 1}`}
            className={`h-2 rounded-full transition-all ${
              i === current ? "bg-white w-6" : "bg-white/50 w-2"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/ServiceBadges.tsx
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
    { icon: Truck, fa: "ارسال سریع", en: "Fast Shipping" },
    { icon: ShieldCheck, fa: "پرداخت امن", en: "Secure Payment" },
    { icon: RotateCcw, fa: "۷ روز بازگشت", en: "7-Day Return" },
    { icon: Headphones, fa: "پشتیبانی ۲۴/۷", en: "24/7 Support" },
    { icon: Award, fa: "ضمانت اصالت", en: "Authentic" },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
        {badges.map((b, i) => {
          const Icon = b.icon;
          return (
            <div
              key={i}
              className="flex flex-col items-center gap-2 text-center"
            >
              <div className="w-10 h-10 rounded-full bg-[#F5F5F5] flex items-center justify-center">
                <Icon size={20} className="text-[#62666D]" />
              </div>
              <span className="text-[11px] text-[#62666D]">
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
# components/home/CategoryCircles.tsx
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

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
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
};

interface CategoryCirclesProps {
  locale: Locale;
}

export default function CategoryCircles({ locale }: CategoryCirclesProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-4">
        {isFa ? "دسته‌بندی‌ها" : "Categories"}
      </h2>
      <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-3">
        {categories.map((cat) => {
          const Icon = ICON_MAP[cat.icon] ?? Cable;
          return (
            <Link
              key={cat.id}
              href={`/${locale}/category/${cat.slug}`}
              className="flex flex-col items-center gap-2 group"
            >
              <div className="w-14 h-14 md:w-16 md:h-16 rounded-full bg-[#F5F5F5] flex items-center justify-center group-hover:bg-[#EF4056]/10 transition-colors">
                <Icon
                  size={24}
                  className="text-[#62666D] group-hover:text-[#EF4056] transition-colors"
                />
              </div>
              <span className="text-[11px] text-[#62666D] text-center leading-tight group-hover:text-[#EF4056] transition-colors">
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
# components/home/AmazingOffer.tsx
# ============================================================
files.append(("components/home/AmazingOffer.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Flame, ChevronLeft } from "lucide-react";
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

  const products = getDiscountedProducts().slice(0, 8);

  const fmt = (n: number) => {
    const s = String(n).padStart(2, "0");
    return isFa ? s.replace(/\\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]) : s;
  };

  return (
    <div className="bg-gradient-to-l from-[#EF4056] to-[#d63850] rounded-lg overflow-hidden">
      <div className="flex flex-col lg:flex-row">
        {/* Left panel (RTL: right) */}
        <div className="lg:w-64 p-4 md:p-6 flex lg:flex-col items-center justify-between lg:justify-center gap-4 text-white shrink-0">
          <div className="flex items-center gap-2">
            <Flame size={24} />
            <h2 className="text-[16px] md:text-[18px] font-bold">
              {isFa ? "پیشنهاد شگفت‌انگیز" : "Amazing Offer"}
            </h2>
          </div>

          <div className="flex items-center gap-1">
            <div className="bg-white text-[#EF4056] rounded px-2 py-1 text-[14px] font-bold tabular-nums">
              {fmt(timeLeft.seconds)}
            </div>
            <span className="text-white">:</span>
            <div className="bg-white text-[#EF4056] rounded px-2 py-1 text-[14px] font-bold tabular-nums">
              {fmt(timeLeft.minutes)}
            </div>
            <span className="text-white">:</span>
            <div className="bg-white text-[#EF4056] rounded px-2 py-1 text-[14px] font-bold tabular-nums">
              {fmt(timeLeft.hours)}
            </div>
          </div>

          <Link
            href={`/${locale}/search?discount=1`}
            className="text-[12px] text-white/90 hover:text-white flex items-center gap-1 transition-colors"
          >
            {isFa ? "مشاهده همه" : "See all"}
            <ChevronLeft size={14} />
          </Link>
        </div>

        {/* Products */}
        <div className="flex-1 bg-white p-3">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                locale={locale}
                variant="compact"
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
# components/home/ProductSection.tsx
# ============================================================
files.append(("components/home/ProductSection.tsx", """import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import ProductCard from "@/components/product/ProductCard";

interface ProductSectionProps {
  titleFa: string;
  titleEn: string;
  products: Product[];
  locale: Locale;
  seeAllHref?: string;
}

export default function ProductSection({
  titleFa,
  titleEn,
  products,
  locale,
  seeAllHref,
}: ProductSectionProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[16px] font-bold text-[#3F4064]">
          {isFa ? titleFa : titleEn}
        </h2>
        {seeAllHref && (
          <Link
            href={`/${locale}${seeAllHref}`}
            className="text-[12px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors"
          >
            {isFa ? "مشاهده همه" : "See all"}
            <ChevronLeft size={14} />
          </Link>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            locale={locale}
          />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/BrandLogos.tsx
# ============================================================
files.append(("components/home/BrandLogos.tsx", """import type { Locale } from "@/lib/types";
import { brands } from "@/lib/data";

interface BrandLogosProps {
  locale: Locale;
}

export default function BrandLogos({ locale }: BrandLogosProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-4">
        {isFa ? "برندهای محبوب" : "Popular Brands"}
      </h2>
      <div className="grid grid-cols-3 md:grid-cols-5 lg:grid-cols-8 gap-3">
        {brands.slice(0, 16).map((brand) => (
          <div
            key={brand.id}
            className="aspect-square rounded-lg bg-[#F5F5F5] flex items-center justify-center p-2 hover:bg-[#EF4056]/5 transition-colors cursor-pointer"
          >
            <span className="text-[11px] md:text-[12px] text-[#62666D] font-medium text-center">
              {isFa ? brand.nameFa : brand.nameEn}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/home/index.ts
# ============================================================
files.append(("components/home/index.ts", """// components/home/index.ts
export { default as HeroSlider } from "./HeroSlider";
export { default as ServiceBadges } from "./ServiceBadges";
export { default as CategoryCircles } from "./CategoryCircles";
export { default as AmazingOffer } from "./AmazingOffer";
export { default as ProductSection } from "./ProductSection";
export { default as BrandLogos } from "./BrandLogos";
"""))

# ============================================================
# app/[locale]/page.tsx (full home page)
# ============================================================
files.append(("app/[locale]/page.tsx", """import type { Locale } from "@/lib/types";
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
} from "@/components/home";

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  const featured = getFeaturedProducts();
  const newProducts = getNewProducts();
  const discounted = getDiscountedProducts();

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
      {/* Hero Slider */}
      <HeroSlider locale={typedLocale} />

      {/* Service Badges */}
      <ServiceBadges locale={typedLocale} />

      {/* Category Circles */}
      <CategoryCircles locale={typedLocale} />

      {/* Amazing Offer */}
      <AmazingOffer locale={typedLocale} />

      {/* Featured Products */}
      {featured.length > 0 && (
        <ProductSection
          titleFa="پیشنهاد ویژه"
          titleEn="Featured Products"
          products={featured}
          locale={typedLocale}
          seeAllHref="/search?featured=1"
        />
      )}

      {/* New Arrivals */}
      {newProducts.length > 0 && (
        <ProductSection
          titleFa="جدیدترین‌ها"
          titleEn="New Arrivals"
          products={newProducts}
          locale={typedLocale}
          seeAllHref="/search?new=1"
        />
      )}

      {/* Discounted Products */}
      {discounted.length > 4 && (
        <ProductSection
          titleFa="تخفیف‌دارها"
          titleEn="Discounted"
          products={discounted.slice(0, 10)}
          locale={typedLocale}
          seeAllHref="/search?discount=1"
        />
      )}

      {/* Brand Logos */}
      <BrandLogos locale={typedLocale} />
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 08: Home Page")
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
        print("Now run: npm run dev")
        print("Open: http://localhost:3000/fa")
        print("\nNext: run 09_category.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()