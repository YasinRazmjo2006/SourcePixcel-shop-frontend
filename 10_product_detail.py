# 10_product_detail.py
# ساخت صفحه جزئیات محصول
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/product/ProductGallery.tsx
# ============================================================
files.append(("components/product/ProductGallery.tsx", """"use client";

import { useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface ProductGalleryProps {
  images: string[];
  alt: string;
}

export default function ProductGallery({ images, alt }: ProductGalleryProps) {
  const [active, setActive] = useState(0);

  const next = () => setActive((p) => (p + 1) % images.length);
  const prev = () => setActive((p) => (p - 1 + images.length) % images.length);

  return (
    <div className="flex flex-col-reverse md:flex-row gap-3">
      {/* Thumbnails */}
      <div className="flex md:flex-col gap-2 overflow-x-auto md:overflow-visible">
        {images.map((img, i) => (
          <button
            key={i}
            onClick={() => setActive(i)}
            className={`w-14 h-14 md:w-16 md:h-16 shrink-0 rounded-lg border-2 overflow-hidden transition-colors ${
              i === active
                ? "border-[#EF4056]"
                : "border-[#E0E0E2] hover:border-[#A1A3A8]"
            }`}
            aria-label={`Image ${i + 1}`}
          >
            <Image
              src={img}
              alt={`${alt} thumbnail ${i + 1}`}
              width={64}
              height={64}
              className="w-full h-full object-cover"
            />
          </button>
        ))}
      </div>

      {/* Main image */}
      <div className="flex-1 relative group">
        <div className="aspect-square bg-white rounded-lg border border-[#E0E0E2] overflow-hidden relative">
          <Image
            src={images[active]}
            alt={alt}
            fill
            sizes="(max-width: 768px) 100vw, 50vw"
            className="object-contain p-4"
            priority
          />
        </div>

        {images.length > 1 && (
          <>
            <button
              onClick={prev}
              aria-label="Previous image"
              className="absolute top-1/2 -translate-y-1/2 right-2 w-9 h-9 rounded-full bg-white/90 backdrop-blur flex items-center justify-center text-[#3F4064] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronRight size={18} />
            </button>
            <button
              onClick={next}
              aria-label="Next image"
              className="absolute top-1/2 -translate-y-1/2 left-2 w-9 h-9 rounded-full bg-white/90 backdrop-blur flex items-center justify-center text-[#3F4064] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronLeft size={18} />
            </button>
          </>
        )}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/product/QuantitySelector.tsx
# ============================================================
files.append(("components/product/QuantitySelector.tsx", """"use client";

import { Minus, Plus } from "lucide-react";
import type { Locale } from "@/lib/types";

interface QuantitySelectorProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  locale: Locale;
}

export default function QuantitySelector({
  value,
  onChange,
  min = 1,
  max = 10,
  locale,
}: QuantitySelectorProps) {
  const isFa = locale === "fa";

  const dec = () => onChange(Math.max(min, value - 1));
  const inc = () => onChange(Math.min(max, value + 1));

  return (
    <div className="flex items-center gap-3">
      <span className="text-[12px] text-[#62666D]">
        {isFa ? "تعداد:" : "Quantity:"}
      </span>
      <div className="flex items-center gap-2 border border-[#E0E0E2] rounded-lg">
        <button
          onClick={inc}
          disabled={value >= max}
          aria-label="Increase quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] rounded-r-lg transition-colors"
        >
          <Plus size={16} />
        </button>
        <span className="w-8 text-center text-[14px] font-bold text-[#3F4064] tabular-nums">
          {isFa ? value.toLocaleString("fa-IR") : value}
        </span>
        <button
          onClick={dec}
          disabled={value <= min}
          aria-label="Decrease quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] rounded-l-lg transition-colors"
        >
          <Minus size={16} />
        </button>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/product/ProductTabs.tsx
# ============================================================
files.append(("components/product/ProductTabs.tsx", """"use client";

import { useState } from "react";
import { Star } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import RatingStars from "./RatingStars";

interface ProductTabsProps {
  product: Product;
  locale: Locale;
}

interface Review {
  id: number;
  name: string;
  rating: number;
  date: string;
  comment: string;
}

const MOCK_REVIEWS: Review[] = [
  {
    id: 1,
    name: "علی محمدی",
    rating: 5,
    date: "۱۴۰۳/۰۵/۱۲",
    comment: "کیفیت ساخت فوق‌العاده، دقیقاً همون چیزی که انتظار داشتم. ارسال هم سریع بود.",
  },
  {
    id: 2,
    name: "سارا احمدی",
    rating: 4,
    date: "۱۴۰۳/۰۵/۰۸",
    comment: "به طور کلی راضی هستم. فقط قیمت کمی بالاست ولی ارزشش رو داره.",
  },
  {
    id: 3,
    name: "رضا کریمی",
    rating: 5,
    date: "۱۴۰۳/۰۴/۲۵",
    comment: "پیشنهاد می‌کنم. بسته‌بندی عالی و محصول اورجینال بود.",
  },
];

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

  // Rating breakdown
  const breakdown = [
    { stars: 5, count: Math.round(product.reviewCount * 0.7) },
    { stars: 4, count: Math.round(product.reviewCount * 0.18) },
    { stars: 3, count: Math.round(product.reviewCount * 0.07) },
    { stars: 2, count: Math.round(product.reviewCount * 0.03) },
    { stars: 1, count: Math.round(product.reviewCount * 0.02) },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2]">
      {/* Tab headers */}
      <div className="flex border-b border-[#E0E0E2] overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-5 py-3 text-[13px] font-medium whitespace-nowrap transition-colors border-b-2 ${
              activeTab === tab.id
                ? "text-[#EF4056] border-[#EF4056]"
                : "text-[#62666D] border-transparent hover:text-[#3F4064]"
            }`}
          >
            {isFa ? tab.fa : tab.en}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-5">
        {activeTab === "specs" && (
          <div className="space-y-0">
            {specs.map((spec, i) => (
              <div
                key={i}
                className={`flex items-start py-3 gap-4 ${
                  i % 2 === 0 ? "bg-[#FAFAFA]" : "bg-white"
                } rounded px-3`}
              >
                <span className="text-[12px] text-[#A1A3A8] w-32 shrink-0">
                  {isFa ? spec.labelFa : spec.labelEn}
                </span>
                <span className="text-[13px] text-[#3F4064] flex-1">
                  {isFa ? spec.valueFa : spec.valueEn}
                </span>
              </div>
            ))}
          </div>
        )}

        {activeTab === "description" && (
          <p className="text-[13px] text-[#62666D] leading-7 whitespace-pre-line">
            {description}
          </p>
        )}

        {activeTab === "reviews" && (
          <div className="space-y-5">
            {/* Rating summary */}
            <div className="flex flex-col md:flex-row gap-6 pb-5 border-b border-[#E0E0E2]">
              <div className="text-center md:text-right">
                <div className="text-[42px] font-bold text-[#3F4064] leading-none mb-2">
                  {product.rating.toFixed(1)}
                </div>
                <RatingStars rating={product.rating} size={16} />
                <div className="text-[11px] text-[#A1A3A8] mt-2">
                  {isFa
                    ? `از ${product.reviewCount.toLocaleString("fa-IR")} نظر`
                    : `from ${product.reviewCount.toLocaleString("en-US")} reviews`}
                </div>
              </div>

              <div className="flex-1 space-y-2">
                {breakdown.map((row) => {
                  const percent = product.reviewCount
                    ? (row.count / product.reviewCount) * 100
                    : 0;
                  return (
                    <div key={row.stars} className="flex items-center gap-2">
                      <span className="text-[11px] text-[#62666D] w-12 flex items-center gap-1">
                        {isFa ? row.stars.toLocaleString("fa-IR") : row.stars}
                        <Star size={10} className="fill-[#F9A825] text-[#F9A825]" />
                      </span>
                      <div className="flex-1 h-2 bg-[#F5F5F5] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-[#F9A825] rounded-full transition-all"
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                      <span className="text-[11px] text-[#A1A3A8] w-10 text-left">
                        {percent.toFixed(0)}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Reviews list */}
            <div className="space-y-4">
              {MOCK_REVIEWS.map((review) => (
                <div
                  key={review.id}
                  className="pb-4 border-b border-[#F5F5F5] last:border-0"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-full bg-[#F5F5F5] flex items-center justify-center text-[12px] font-bold text-[#62666D]">
                        {review.name[0]}
                      </div>
                      <div>
                        <div className="text-[13px] font-medium text-[#3F4064]">
                          {review.name}
                        </div>
                        <div className="flex items-center gap-2 mt-1">
                          <RatingStars rating={review.rating} size={10} />
                          <span className="text-[10px] text-[#A1A3A8]">
                            {review.date}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <p className="text-[12px] text-[#62666D] leading-6 mt-2 pr-12">
                    {review.comment}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/product/ProductDetail.tsx
# ============================================================
files.append(("components/product/ProductDetail.tsx", """"use client";

import { useState } from "react";
import Link from "next/link";
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
    `https://picsum.photos/seed/sp${product.id}a/600/600`,
    `https://picsum.photos/seed/sp${product.id}b/600/600`,
    `https://picsum.photos/seed/sp${product.id}c/600/600`,
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
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 md:p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
        {/* Gallery */}
        <ProductGallery images={images} alt={title} />

        {/* Info */}
        <div className="flex flex-col">
          {/* Breadcrumb-ish brand line */}
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

          {/* Title */}
          <h1 className="text-[18px] md:text-[20px] font-bold text-[#3F4064] leading-7 mb-3">
            {title}
          </h1>

          {/* Rating */}
          <div className="flex items-center gap-2 mb-4">
            <RatingStars rating={product.rating} size={14} />
            <span className="text-[12px] text-[#A1A3A8]">
              ({product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
              {isFa ? "نظر" : "reviews"})
            </span>
          </div>

          {/* Tags */}
          {product.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {product.tags.map((tag, i) => (
                <span
                  key={i}
                  className="text-[11px] bg-[#F5F5F5] text-[#62666D] px-2 py-1 rounded"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Divider */}
          <div className="border-t border-[#E0E0E2] my-4" />

          {/* Price */}
          <div className="mb-4">
            <PriceTag
              price={product.price}
              finalPrice={product.finalPrice}
              discountPercent={product.discountPercent}
              locale={locale}
              size="lg"
            />
          </div>

          {/* Stock status */}
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

          {/* Quantity + Actions */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mb-5">
            <QuantitySelector
              value={quantity}
              onChange={setQuantity}
              max={10}
              locale={locale}
            />
          </div>

          <div className="flex items-center gap-3 mb-6">
            <button
              onClick={handleAddToCart}
              disabled={!product.inStock}
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
            </button>

            <button
              onClick={() => toggleWishlist(product.id)}
              aria-label={isFa ? "علاقه‌مندی" : "Wishlist"}
              className={`w-11 h-11 rounded-lg border flex items-center justify-center transition-colors ${
                isInWishlist
                  ? "border-[#EF4056] bg-[#EF4056]/5"
                  : "border-[#E0E0E2] hover:border-[#EF4056]"
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
            </button>

            <button
              aria-label={isFa ? "اشتراک‌گذاری" : "Share"}
              className="w-11 h-11 rounded-lg border border-[#E0E0E2] flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
            >
              <Share2 size={18} />
            </button>
          </div>

          {/* Features */}
          <div className="bg-[#FAFAFA] rounded-lg p-3 space-y-2">
            {features.map((f, i) => {
              const Icon = f.icon;
              return (
                <div
                  key={i}
                  className="flex items-center gap-2 text-[12px] text-[#62666D]"
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
  );
}
"""))

# ============================================================
# components/product/RelatedProducts.tsx
# ============================================================
files.append(("components/product/RelatedProducts.tsx", """import type { Locale, Product } from "@/lib/types";
import ProductCard from "./ProductCard";

interface RelatedProductsProps {
  products: Product[];
  locale: Locale;
}

export default function RelatedProducts({
  products,
  locale,
}: RelatedProductsProps) {
  const isFa = locale === "fa";

  if (products.length === 0) return null;

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-4">
        {isFa ? "محصولات مرتبط" : "Related Products"}
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
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
# components/product/index.ts (updated)
# ============================================================
files.append(("components/product/index.ts", """// components/product/index.ts
export { default as ProductCard } from "./ProductCard";
export { default as RatingStars } from "./RatingStars";
export { default as PriceTag } from "./PriceTag";
export { default as ProductFilters } from "./ProductFilters";
export { default as ProductSort } from "./ProductSort";
export { default as ProductGallery } from "./ProductGallery";
export { default as ProductDetail } from "./ProductDetail";
export { default as ProductTabs } from "./ProductTabs";
export { default as QuantitySelector } from "./QuantitySelector";
export { default as RelatedProducts } from "./RelatedProducts";
export type { FilterValues } from "./ProductFilters";
"""))

# ============================================================
# app/[locale]/product/[slug]/page.tsx
# ============================================================
files.append(("app/[locale]/product/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Locale } from "@/lib/types";
import {
  products,
  getProductBySlug,
  getProductsByCategory,
  getCategoryById,
} from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";
import {
  ProductDetail,
  ProductTabs,
  RelatedProducts,
} from "@/components/product";

interface PageProps {
  params: Promise<{ locale: string; slug: string }>;
}

export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    products.map((p) => ({ locale, slug: p.slug }))
  );
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const product = getProductBySlug(slug);
  if (!product) return { title: "Product not found" };
  return {
    title: `${product.titleEn} — SourcePixcel`,
    description: product.titleEn,
  };
}

export default async function ProductPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const product = getProductBySlug(slug);
  if (!product) notFound();

  const category = getCategoryById(product.category);
  const isFa = typedLocale === "fa";

  const related = getProductsByCategory(product.category)
    .filter((p) => p.id !== product.id)
    .slice(0, 5);

  const breadcrumbItems = [
    {
      labelFa: "دسته‌بندی‌ها",
      labelEn: "Categories",
      href: `/${typedLocale}/categories`,
    },
  ];

  if (category) {
    breadcrumbItems.push({
      labelFa: category.nameFa,
      labelEn: category.nameEn,
      href: `/${typedLocale}/category/${category.slug}`,
    });
  }

  breadcrumbItems.push({
    labelFa: product.titleFa,
    labelEn: product.titleEn,
  });

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
      <Breadcrumb locale={typedLocale} items={breadcrumbItems} />

      <ProductDetail product={product} locale={typedLocale} />

      <ProductTabs product={product} locale={typedLocale} />

      <RelatedProducts products={related} locale={typedLocale} />
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 10: Product Detail")
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
        print("Open: http://localhost:3000/fa/product/samsung-galaxy-s24-ultra")
        print("\nNext: run 11_cart.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()