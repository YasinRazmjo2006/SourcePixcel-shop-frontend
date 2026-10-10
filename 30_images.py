# 30_images.py
# بهبود تجربه تصاویر: blur placeholder، تصاویر زیباتر، بارگذاری نرم
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/utils/blur.ts — تولید blur placeholder
# ============================================================
files.append(("lib/utils/blur.ts", """// lib/utils/blur.ts

/**
 * Generate a tiny base64 SVG placeholder for next/image blur effect.
 * Uses category color for a beautiful gradient shimmer.
 */
export function generateBlurPlaceholder(
  color: string = "#EF4056",
  width: number = 16,
  height: number = 16
): string {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="${color}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="${color}" stop-opacity="0.1"/>
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#g)"/>
</svg>`;
  const base64 = Buffer.from(svg).toString("base64");
  return `data:image/svg+xml;base64,${base64}`;
}

/**
 * Map a product category to its color for consistent placeholders.
 */
export const CATEGORY_COLORS: Record<string, string> = {
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

export function getCategoryColor(category: string): string {
  return CATEGORY_COLORS[category] ?? "#EF4056";
}

export function getProductBlur(category: string): string {
  return generateBlurPlaceholder(getCategoryColor(category));
}
"""))

# ============================================================
# lib/utils/index.ts (updated)
# ============================================================
files.append(("lib/utils/index.ts", """// lib/utils/index.ts
export {
  formatPrice,
  formatPriceWithCurrency,
  calcFinalPrice,
  formatDiscount,
  formatRating,
  formatReviewCount,
  truncate,
  getProductTitle,
  getCategoryName,
  getBrandName,
  formatDate,
  localePath,
  cn,
  getStockLabel,
  scrollToTop,
} from "./format";

export {
  isValidIranianMobile,
  normalizeMobile,
  formatMobileDisplay,
  isValidEmail,
  isValidIranianNationalId,
  isValidIranianPostalCode,
  getPasswordStrength,
  isValidPassword,
} from "./validators";

export {
  buildMetadata,
  buildProductSchema,
  buildOrganizationSchema,
  buildWebSiteSchema,
  buildBreadcrumbSchema,
  SITE_NAME_EXPORT,
  SITE_URL_EXPORT,
} from "./seo";

export {
  generateBlurPlaceholder,
  getCategoryColor,
  getProductBlur,
  CATEGORY_COLORS,
} from "./blur";
"""))

# ============================================================
# components/common/SmartImage.tsx — تصویر با blur placeholder
# ============================================================
files.append(("components/common/SmartImage.tsx", """"use client";

import Image, { type ImageProps } from "next/image";
import { useState } from "react";
import { getCategoryColor } from "@/lib/utils";

interface SmartImageProps extends Omit<ImageProps, "onLoad" | "onError"> {
  /** Optional category to pick color for placeholder */
  category?: string;
  /** Optional wrapper className */
  wrapperClassName?: string;
}

/**
 * SmartImage — next/image with automatic blur placeholder
 * and smooth fade-in on load.
 */
export default function SmartImage({
  category,
  wrapperClassName,
  className,
  alt,
  ...props
}: SmartImageProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  const color = category ? getCategoryColor(category) : "#EF4056";
  const blurDataURL = `data:image/svg+xml;base64,${Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="${color}" stop-opacity="0.3"/><stop offset="100%" stop-color="${color}" stop-opacity="0.1"/></linearGradient></defs><rect width="16" height="16" fill="url(#g)"/></svg>`
  ).toString("base64")}`;

  return (
    <div className={`relative w-full h-full ${wrapperClassName ?? ""}`}>
      {/* Colored placeholder while loading */}
      {!isLoaded && !hasError && (
        <div
          className="absolute inset-0 animate-pulse"
          style={{
            background: `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`,
          }}
        />
      )}

      {/* Error fallback */}
      {hasError && (
        <div
          className="absolute inset-0 flex items-center justify-center"
          style={{ backgroundColor: `${color}10` }}
        >
          <span className="text-[10px] text-[#A1A3A8]">⚠</span>
        </div>
      )}

      {/* Image */}
      <Image
        {...props}
        alt={alt}
        placeholder="blur"
        blurDataURL={blurDataURL}
        onLoad={() => setIsLoaded(true)}
        onError={() => setHasError(true)}
        className={`${className ?? ""} transition-opacity duration-500 ${
          isLoaded ? "opacity-100" : "opacity-0"
        }`}
      />
    </div>
  );
}
"""))

# ============================================================
# components/common/index.ts (updated)
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
export { default as StaticPage } from "./StaticPage";
export { default as ThemeProvider } from "./ThemeProvider";
export { default as ThemeToggle } from "./ThemeToggle";
export { default as JsonLd } from "./JsonLd";
export { default as ToastContainer } from "./ToastContainer";
export { default as Skeleton } from "./Skeleton";
export { default as ProductCardSkeleton } from "./ProductCardSkeleton";
export { default as ErrorBoundary } from "./ErrorBoundary";
export { default as KeyboardShortcuts } from "./KeyboardShortcuts";
export { default as OfflineBanner } from "./OfflineBanner";
export { default as FontLoader } from "./FontLoader";
export { default as SmartImage } from "./SmartImage";
"""))

# ============================================================
# components/product/ProductCard.tsx (updated with SmartImage)
# ============================================================
files.append(("components/product/ProductCard.tsx", """"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Heart, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore, useToastStore } from "@/lib/stores";
import { SmartImage } from "@/components/common";
import RatingStars from "./RatingStars";
import PriceTag from "./PriceTag";
import CompareButton from "./CompareButton";

interface ProductCardProps {
  product: Product;
  locale: Locale;
  variant?: "default" | "compact";
  priority?: boolean;
}

export default function ProductCard({
  product,
  locale,
  variant = "default",
  priority = false,
}: ProductCardProps) {
  const isFa = locale === "fa";
  const addToCart = useCartStore((s) => s.addItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);
  const isInWishlist = useWishlistStore((s) => s.ids.includes(product.id));
  const pushToast = useToastStore((s) => s.push);

  const title = isFa ? product.titleFa : product.titleEn;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!product.inStock) return;
    addToCart(product.id, 1);
    pushToast({
      type: "success",
      titleFa: "به سبد خرید اضافه شد",
      titleEn: "Added to cart",
      messageFa: title,
      messageEn: title,
    });
  };

  const handleToggleWishlist = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleWishlist(product.id);
    pushToast({
      type: isInWishlist ? "info" : "success",
      titleFa: isInWishlist ? "از علاقه‌مندی‌ها حذف شد" : "به علاقه‌مندی‌ها اضافه شد",
      titleEn: isInWishlist ? "Removed from wishlist" : "Added to wishlist",
      messageFa: title,
      messageEn: title,
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      whileHover={{ y: -4 }}
      className="group relative bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-lg transition-shadow duration-300 overflow-hidden"
    >
      <div
        className={`absolute top-2 z-20 flex flex-col gap-1.5 ${
          isFa ? "left-2" : "right-2"
        }`}
      >
        <button
          onClick={handleToggleWishlist}
          aria-label={isFa ? "افزودن به علاقه‌مندی" : "Add to wishlist"}
          className={`w-7 h-7 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center transition-all ${
            isInWishlist ? "opacity-100" : "opacity-0 group-hover:opacity-100"
          }`}
        >
          <Heart
            size={14}
            className={
              isInWishlist
                ? "fill-[#EF4056] text-[#EF4056]"
                : "text-[#62666D]"
            }
          />
        </button>
        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
          <CompareButton productId={product.id} locale={locale} size="sm" />
        </div>
      </div>

      {product.discountPercent > 0 && (
        <div
          className={`absolute top-2 z-10 bg-[#EF4056] text-white text-[11px] font-bold rounded px-1.5 py-0.5 ${
            isFa ? "right-2" : "left-2"
          }`}
        >
          {product.discountPercent.toLocaleString(isFa ? "fa-IR" : "en-US")}٪
        </div>
      )}

      {!product.inStock && (
        <div className="absolute inset-0 bg-white/70 dark:bg-[#1A1A1E]/70 z-20 flex items-center justify-center">
          <span className="text-[#62666D] dark:text-[#A1A3A8] text-[13px] font-medium bg-white dark:bg-[#1A1A1E] px-3 py-1 rounded">
            {isFa ? "ناموجود" : "Out of stock"}
          </span>
        </div>
      )}

      <Link href={`/${locale}/product/${product.slug}`} className="block">
        <div className="aspect-square bg-[#F5F5F5] dark:bg-[#2A2A2E] relative overflow-hidden">
          <motion.div
            className="absolute inset-0"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          >
            <SmartImage
              src={product.image}
              alt={title}
              fill
              sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 20vw"
              className="object-cover"
              priority={priority}
              category={product.category}
            />
          </motion.div>
        </div>

        <div className={`p-3 ${variant === "compact" ? "pb-2" : ""}`}>
          <h3
            className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] leading-5 mb-2 line-clamp-2 min-h-[40px]"
            title={title}
          >
            {title}
          </h3>

          <div className="flex items-center gap-1 mb-3">
            <RatingStars rating={product.rating} size={11} />
            <span className="text-[10px] text-[#A1A3A8]">
              ({product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")})
            </span>
          </div>

          <PriceTag
            price={product.price}
            finalPrice={product.finalPrice}
            discountPercent={product.discountPercent}
            locale={locale}
            size="sm"
          />
        </div>
      </Link>

      {variant === "default" && (
        <motion.button
          onClick={handleAddToCart}
          disabled={!product.inStock}
          aria-label={isFa ? "افزودن به سبد خرید" : "Add to cart"}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className={`absolute bottom-3 w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
            isFa ? "left-3" : "right-3"
          } ${
            product.inStock
              ? "bg-[#EF4056] text-white hover:bg-[#d63850]"
              : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
          }`}
        >
          <ShoppingCart size={15} />
        </motion.button>
      )}
    </motion.div>
  );
}
"""))

# ============================================================
# components/product/ProductGallery.tsx (updated with SmartImage)
# ============================================================
files.append(("components/product/ProductGallery.tsx", """"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, ZoomIn } from "lucide-react";
import { SmartImage } from "@/components/common";

interface ProductGalleryProps {
  images: string[];
  alt: string;
  category?: string;
}

export default function ProductGallery({
  images,
  alt,
  category,
}: ProductGalleryProps) {
  const [active, setActive] = useState(0);
  const [isZoomed, setIsZoomed] = useState(false);

  const next = () => setActive((p) => (p + 1) % images.length);
  const prev = () => setActive((p) => (p - 1 + images.length) % images.length);

  return (
    <div className="flex flex-col-reverse md:flex-row gap-3">
      {/* Thumbnails */}
      <div className="flex md:flex-col gap-2 overflow-x-auto md:overflow-visible pb-1 md:pb-0">
        {images.map((img, i) => (
          <motion.button
            key={i}
            onClick={() => setActive(i)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`w-14 h-14 md:w-16 md:h-16 shrink-0 rounded-lg border-2 overflow-hidden transition-colors relative ${
              i === active
                ? "border-[#EF4056]"
                : "border-[#E0E0E2] dark:border-[#2A2A2E] hover:border-[#A1A3A8]"
            }`}
            aria-label={`Image ${i + 1}`}
          >
            <SmartImage
              src={img}
              alt={`${alt} thumbnail ${i + 1}`}
              fill
              sizes="64px"
              className="object-cover"
              category={category}
            />
          </motion.button>
        ))}
      </div>

      {/* Main image */}
      <div className="flex-1 relative group">
        <div className="aspect-square bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={active}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
              className="absolute inset-0"
            >
              <SmartImage
                src={images[active]}
                alt={alt}
                fill
                sizes="(max-width: 768px) 100vw, 50vw"
                className="object-contain p-4"
                priority
                category={category}
              />
            </motion.div>
          </AnimatePresence>
        </div>

        {images.length > 1 && (
          <>
            <button
              onClick={prev}
              aria-label="Previous image"
              className="absolute top-1/2 -translate-y-1/2 right-2 w-9 h-9 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] opacity-0 group-hover:opacity-100 transition-opacity shadow-md hover:bg-white"
            >
              <ChevronRight size={18} />
            </button>
            <button
              onClick={next}
              aria-label="Next image"
              className="absolute top-1/2 -translate-y-1/2 left-2 w-9 h-9 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] opacity-0 group-hover:opacity-100 transition-opacity shadow-md hover:bg-white"
            >
              <ChevronLeft size={18} />
            </button>
          </>
        )}

        {/* Zoom hint */}
        <div className="absolute top-3 opacity-0 group-hover:opacity-100 transition-opacity"
          style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
        >
          <div className="w-8 h-8 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#62666D] shadow-md">
            <ZoomIn size={14} />
          </div>
        </div>
      </div>
    </div>
  );
}

const isFa = true;
"""))

# ============================================================
# components/product/ProductDetail.tsx (updated gallery usage)
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
  );
}
"""))

# ============================================================
# components/home/BlogPreview.tsx (updated with SmartImage)
# ============================================================
files.append(("components/home/BlogPreview.tsx", """import Link from "next/link";
import { Calendar, Clock, ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { blogPosts } from "@/lib/data";
import { SmartImage } from "@/components/common";

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
              <SmartImage
                src={post.cover}
                alt={isFa ? post.titleFa : post.titleEn}
                fill
                sizes="(max-width: 768px) 100vw, 33vw"
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <span
                className="absolute top-3 bg-[#EF4056] text-white text-[10px] font-medium px-2 py-1 rounded z-10"
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
# components/blog/BlogCard.tsx (updated with SmartImage)
# ============================================================
files.append(("components/blog/BlogCard.tsx", """import Link from "next/link";
import { Calendar, Clock, User } from "lucide-react";
import type { BlogPost, Locale } from "@/lib/types";
import { SmartImage } from "@/components/common";

interface BlogCardProps {
  post: BlogPost;
  locale: Locale;
  featured?: boolean;
}

export default function BlogCard({ post, locale, featured = false }: BlogCardProps) {
  const isFa = locale === "fa";

  const title = isFa ? post.titleFa : post.titleEn;
  const excerpt = isFa ? post.excerptFa : post.excerptEn;
  const category = isFa ? post.categoryFa : post.categoryEn;
  const author = isFa ? post.authorFa : post.authorEn;
  const date = isFa ? post.dateFa : post.dateEn;
  const readTime = isFa ? post.readTimeFa : post.readTimeEn;

  return (
    <Link
      href={`/${locale}/blog/${post.slug}`}
      className="group bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden hover:shadow-lg transition-shadow flex flex-col"
    >
      <div className={`relative ${featured ? "aspect-[16/7]" : "aspect-video"} overflow-hidden`}>
        <SmartImage
          src={post.cover}
          alt={title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <span className="absolute top-3 bg-[#EF4056] text-white text-[10px] font-medium px-2 py-1 rounded z-10"
          style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
        >
          {category}
        </span>
      </div>

      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-[14px] md:text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-6 mb-2 line-clamp-2 group-hover:text-[#EF4056] transition-colors">
          {title}
        </h3>

        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6 line-clamp-2 mb-3 flex-1">
          {excerpt}
        </p>

        <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8] pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex-wrap">
          <span className="flex items-center gap-1">
            <User size={11} />
            {author}
          </span>
          <span className="flex items-center gap-1">
            <Calendar size={11} />
            {date}
          </span>
          <span className="flex items-center gap-1">
            <Clock size={11} />
            {readTime}
          </span>
        </div>
      </div>
    </Link>
  );
}
"""))

# ============================================================
# components/blog/BlogPostDetail.tsx (updated with SmartImage)
# ============================================================
files.append(("components/blog/BlogPostDetail.tsx", """import Link from "next/link";
import { Calendar, Clock, User, Tag, ArrowRight, ArrowLeft } from "lucide-react";
import type { BlogPost, Locale } from "@/lib/types";
import { Breadcrumb, SmartImage } from "@/components/common";

interface BlogPostDetailProps {
  locale: Locale;
  post: BlogPost;
  related: BlogPost[];
}

export default function BlogPostDetail({
  locale,
  post,
  related,
}: BlogPostDetailProps) {
  const isFa = locale === "fa";

  const title = isFa ? post.titleFa : post.titleEn;
  const content = isFa ? post.contentFa : post.contentEn;
  const category = isFa ? post.categoryFa : post.categoryEn;
  const author = isFa ? post.authorFa : post.authorEn;
  const date = isFa ? post.dateFa : post.dateEn;
  const readTime = isFa ? post.readTimeFa : post.readTimeEn;

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[
          { labelFa: "وبلاگ", labelEn: "Blog", href: `/${locale}/blog` },
          { labelFa: post.titleFa, labelEn: post.titleEn },
        ]}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <article className="lg:col-span-2 bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
          <div className="relative aspect-video">
            <SmartImage
              src={post.cover}
              alt={title}
              fill
              sizes="(max-width: 1024px) 100vw, 66vw"
              className="object-cover"
              priority
            />
          </div>

          <div className="p-5 md:p-7">
            <div className="mb-3">
              <Link
                href={`/${locale}/blog`}
                className="inline-block bg-[#EF4056]/10 text-[#EF4056] text-[11px] font-medium px-2 py-1 rounded"
              >
                {category}
              </Link>
            </div>

            <h1 className="text-[22px] md:text-[26px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-9 mb-4">
              {title}
            </h1>

            <div className="flex items-center gap-4 text-[11px] text-[#A1A3A8] pb-4 mb-5 border-b border-[#E0E0E2] dark:border-[#2A2A2E] flex-wrap">
              <span className="flex items-center gap-1">
                <User size={12} />
                {author}
              </span>
              <span className="flex items-center gap-1">
                <Calendar size={12} />
                {date}
              </span>
              <span className="flex items-center gap-1">
                <Clock size={12} />
                {readTime}
              </span>
            </div>

            <div className="prose text-[13px] md:text-[14px] text-[#62666D] dark:text-[#A1A3A8] whitespace-pre-line">
              {content}
            </div>

            {post.tags.length > 0 && (
              <div className="flex items-center gap-2 mt-8 pt-5 border-t border-[#E0E0E2] dark:border-[#2A2A2E] flex-wrap">
                <Tag size={14} className="text-[#A1A3A8]" />
                {post.tags.map((tag, i) => (
                  <span
                    key={i}
                    className="text-[11px] bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] px-2 py-1 rounded"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="mt-6">
              <Link
                href={`/${locale}/blog`}
                className="inline-flex items-center gap-2 text-[12px] text-[#00BFFF] hover:text-[#EF4056] transition-colors"
              >
                {isFa ? <ArrowRight size={14} /> : <ArrowLeft size={14} />}
                {isFa ? "بازگشت به وبلاگ" : "Back to blog"}
              </Link>
            </div>
          </div>
        </article>

        <aside className="lg:col-span-1">
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 sticky top-24">
            <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {isFa ? "مطالب مرتبط" : "Related Posts"}
            </h2>
            <div className="space-y-3">
              {related.map((rp) => (
                <Link
                  key={rp.id}
                  href={`/${locale}/blog/${rp.slug}`}
                  className="flex gap-3 group"
                >
                  <div className="w-20 h-16 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
                    <SmartImage
                      src={rp.cover}
                      alt={isFa ? rp.titleFa : rp.titleEn}
                      fill
                      sizes="80px"
                      className="object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] leading-5 line-clamp-2 group-hover:text-[#EF4056] transition-colors">
                      {isFa ? rp.titleFa : rp.titleEn}
                    </h3>
                    <div className="text-[10px] text-[#A1A3A8] mt-1">
                      {isFa ? rp.dateFa : rp.dateEn}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </aside>
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
    print("SourcePixcel — Step 30: Image Experience")
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
        print("\nYou should see:")
        print("  ✓ Colored placeholder while images load")
        print("  ✓ Smooth fade-in on image load")
        print("  ✓ Gallery with animated transitions")
        print("  ✓ Error fallback for broken images")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()