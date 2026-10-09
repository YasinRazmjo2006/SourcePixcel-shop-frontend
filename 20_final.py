# 20_final.py
# بهینه‌سازی نهایی - سیستم Toast، Loading، Error Boundary
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/toast.ts
# ============================================================
files.append(("lib/stores/toast.ts", """"use client";

import { create } from "zustand";

export type ToastType = "success" | "error" | "info" | "warning";

export interface Toast {
  id: string;
  type: ToastType;
  titleFa: string;
  titleEn: string;
  messageFa?: string;
  messageEn?: string;
  duration?: number;
}

interface ToastState {
  toasts: Toast[];
  push: (toast: Omit<Toast, "id">) => void;
  remove: (id: string) => void;
  clear: () => void;
}

export const useToastStore = create<ToastState>((set) => ({
  toasts: [],

  push: (toast) => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    const newToast: Toast = { ...toast, id };
    set((state) => ({ toasts: [...state.toasts, newToast] }));

    // Auto-remove after duration
    const duration = toast.duration ?? 3500;
    if (duration > 0 && typeof window !== "undefined") {
      setTimeout(() => {
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id),
        }));
      }, duration);
    }
  },

  remove: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((t) => t.id !== id),
    }));
  },

  clear: () => set({ toasts: [] }),
}));
"""))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", """// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
"""))

# ============================================================
# components/common/ToastContainer.tsx
# ============================================================
files.append(("components/common/ToastContainer.tsx", """"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, XCircle, Info, AlertTriangle, X } from "lucide-react";
import { useToastStore, type ToastType } from "@/lib/stores";

const ICONS = {
  success: CheckCircle2,
  error: XCircle,
  info: Info,
  warning: AlertTriangle,
};

const COLORS: Record<ToastType, string> = {
  success: "bg-[#22C55E] text-white",
  error: "bg-[#EF4444] text-white",
  info: "bg-[#00BFFF] text-white",
  warning: "bg-[#F59E0B] text-white",
};

export default function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);
  const remove = useToastStore((s) => s.remove);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[200] flex flex-col gap-2 pointer-events-none w-full max-w-sm px-4">
      {toasts.map((toast) => {
        const Icon = ICONS[toast.type];
        return (
          <div
            key={toast.id}
            className={`${COLORS[toast.type]} rounded-lg shadow-lg p-3 flex items-start gap-3 pointer-events-auto animate-in fade-in slide-in-from-top-2 duration-200`}
          >
            <Icon size={18} className="shrink-0 mt-0.5" />
            <div className="flex-1 text-[13px]">
              <div className="font-bold">{toast.titleFa}</div>
              {toast.messageFa && (
                <div className="text-[12px] opacity-90 mt-0.5">
                  {toast.messageFa}
                </div>
              )}
            </div>
            <button
              onClick={() => remove(toast.id)}
              aria-label="Close"
              className="shrink-0 opacity-70 hover:opacity-100 transition-opacity"
            >
              <X size={16} />
            </button>
          </div>
        );
      })}
    </div>
  );
}
"""))

# ============================================================
# components/common/Skeleton.tsx
# ============================================================
files.append(("components/common/Skeleton.tsx", """interface SkeletonProps {
  className?: string;
  variant?: "text" | "circle" | "rect";
  width?: string | number;
  height?: string | number;
}

export default function Skeleton({
  className = "",
  variant = "rect",
  width,
  height,
}: SkeletonProps) {
  const base = "bg-[#E0E0E2] dark:bg-[#2A2A2E] animate-pulse";
  const shape =
    variant === "circle"
      ? "rounded-full"
      : variant === "text"
      ? "rounded"
      : "rounded-lg";

  return (
    <div
      className={`${base} ${shape} ${className}`}
      style={{ width, height }}
    />
  );
}
"""))

# ============================================================
# components/common/ProductCardSkeleton.tsx
# ============================================================
files.append(("components/common/ProductCardSkeleton.tsx", """import Skeleton from "./Skeleton";

export default function ProductCardSkeleton() {
  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] p-3">
      <Skeleton variant="rect" className="w-full aspect-square mb-3" />
      <Skeleton variant="text" className="w-full h-4 mb-2" />
      <Skeleton variant="text" className="w-2/3 h-4 mb-3" />
      <Skeleton variant="text" className="w-1/2 h-3" />
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
"""))

# ============================================================
# components/common/ErrorBoundary.tsx
# ============================================================
files.append(("components/common/ErrorBoundary.tsx", """"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

interface ErrorBoundaryProps {
  locale?: string;
  children: React.ReactNode;
}

export default function ErrorBoundary({
  locale = "fa",
  children,
}: ErrorBoundaryProps) {
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const isFa = locale === "fa";

  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      setHasError(true);
      setErrorMessage(event.error?.message ?? "Unknown error");
    };
    window.addEventListener("error", handleError);
    return () => window.removeEventListener("error", handleError);
  }, []);

  if (hasError) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center px-4 text-center">
        <div className="w-20 h-20 rounded-full bg-[#EF4444]/10 flex items-center justify-center mb-4">
          <AlertTriangle size={40} className="text-[#EF4444]" />
        </div>
        <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
          {isFa ? "مشکلی پیش آمد" : "Something went wrong"}
        </h1>
        <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md">
          {isFa
            ? "متأسفانه خطایی رخ داد. لطفاً صفحه را دوباره بارگذاری کنید."
            : "An unexpected error occurred. Please reload the page."}
        </p>
        <div className="flex items-center gap-3">
          <button
            onClick={() => window.location.reload()}
            className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] flex items-center gap-2"
          >
            <RefreshCw size={16} />
            {isFa ? "بارگذاری مجدد" : "Reload"}
          </button>
          <Link
            href={`/${locale}`}
            className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] flex items-center gap-2"
          >
            <Home size={16} />
            {isFa ? "بازگشت به خانه" : "Home"}
          </Link>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
"""))

# ============================================================
# components/common/index.ts (final update)
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
"""))

# ============================================================
# app/[locale]/error.tsx
# ============================================================
files.append(("app/[locale]/error.tsx", """"use client";

import { useEffect } from "react";
import Link from "next/link";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Page error:", error);
  }, [error]);

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-16 text-center">
      <div className="w-20 h-20 rounded-full bg-[#EF4444]/10 flex items-center justify-center mx-auto mb-4">
        <AlertTriangle size={40} className="text-[#EF4444]" />
      </div>
      <h1 className="text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
        خطایی رخ داد
      </h1>
      <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md mx-auto">
        متأسفانه در بارگذاری این صفحه مشکلی پیش آمد. لطفاً دوباره تلاش کنید.
      </p>
      <div className="flex items-center justify-center gap-3 flex-wrap">
        <button
          onClick={reset}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] flex items-center gap-2"
        >
          <RefreshCw size={16} />
          تلاش مجدد
        </button>
        <Link
          href="/fa"
          className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] flex items-center gap-2"
        >
          <Home size={16} />
          بازگشت به خانه
        </Link>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/loading.tsx
# ============================================================
files.append(("app/[locale]/loading.tsx", """import { ProductCardSkeleton, Skeleton } from "@/components/common";

export default function Loading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
      <Skeleton variant="rect" className="w-full h-[200px] md:h-[300px]" />
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <ProductCardSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/not-found.tsx (improved 404)
# ============================================================
files.append(("app/[locale]/not-found.tsx", """import Link from "next/link";
import { Home, Search, ArrowRight, ArrowLeft } from "lucide-react";

export default async function LocaleNotFound({
  params,
}: {
  params?: Promise<{ locale: string }>;
}) {
  const locale = params ? (await params).locale : "fa";
  const isFa = locale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-16 md:py-24 text-center">
      <h1 className="text-[100px] md:text-[140px] font-bold text-[#EF4056] leading-none mb-4 select-none">
        404
      </h1>
      <h2 className="text-[22px] md:text-[26px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
        {isFa ? "صفحه‌ای که دنبالش هستید پیدا نشد" : "Page not found"}
      </h2>
      <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-8 max-w-md mx-auto leading-7">
        {isFa
          ? "ممکن است آدرس اشتباه باشد یا صفحه حذف شده باشد. می‌توانید از جستجو استفاده کنید یا به خانه برگردید."
          : "The address might be incorrect, or the page may have been removed. Try searching or go back to home."}
      </p>
      <div className="flex items-center justify-center gap-3 flex-wrap">
        <Link
          href={`/${locale}`}
          className="h-11 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors inline-flex items-center gap-2"
        >
          {isFa ? <ArrowRight size={16} /> : <ArrowLeft size={16} />}
          {isFa ? "بازگشت به خانه" : "Back to Home"}
        </Link>
        <Link
          href={`/${locale}/search`}
          className="h-11 px-6 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] font-medium text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors inline-flex items-center gap-2"
        >
          <Search size={16} />
          {isFa ? "جستجو در فروشگاه" : "Search"}
        </Link>
      </div>

      <div className="mt-12 text-[12px] text-[#A1A3A8]">
        {isFa
          ? "اگر فکر می‌کنید این یک خطاست، با پشتیبانی تماس بگیرید."
          : "If you think this is an error, please contact support."}
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/not-found.tsx (global 404)
# ============================================================
files.append(("app/not-found.tsx", """import Link from "next/link";
import { Home, ArrowLeft } from "lucide-react";

export default function GlobalNotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center bg-[#F5F5F5]">
      <h1 className="text-[100px] font-bold text-[#EF4056] leading-none mb-4">
        404
      </h1>
      <h2 className="text-[22px] font-bold text-[#3F4064] mb-3">
        Page not found
      </h2>
      <p className="text-[13px] text-[#62666D] mb-8 max-w-md">
        The page you are looking for was not found.
      </p>
      <Link
        href="/fa"
        className="h-11 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] inline-flex items-center gap-2"
      >
        <Home size={16} />
        Back to Home
      </Link>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/layout.tsx (with ToastContainer)
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import ToastContainer from "@/components/common/ToastContainer";
import type { Locale } from "@/lib/types";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div
      dir={locale === "fa" ? "rtl" : "ltr"}
      lang={locale}
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      <Header locale={locale as Locale} />
      <main style={{ flex: 1 }}>{children}</main>
      <Footer locale={locale as Locale} />
      <ToastContainer />
    </div>
  );
}
"""))

# ============================================================
# components/product/ProductCard.tsx (updated with toast)
# ============================================================
files.append(("components/product/ProductCard.tsx", """"use client";

import Link from "next/link";
import Image from "next/image";
import { Heart, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore, useToastStore } from "@/lib/stores";
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
    <div className="group relative bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-lg transition-all duration-200 overflow-hidden">
      <div
        className={`absolute top-2 z-20 flex flex-col gap-1.5 ${
          isFa ? "left-2" : "right-2"
        }`}
      >
        <button
          onClick={handleToggleWishlist}
          aria-label={isFa ? "افزودن به علاقه‌مندی" : "Add to wishlist"}
          className={`w-7 h-7 rounded-full bg-white/90 backdrop-blur flex items-center justify-center transition-all ${
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
          <Image
            src={product.image}
            alt={title}
            fill
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 20vw"
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            priority={priority}
          />
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
        <button
          onClick={handleAddToCart}
          disabled={!product.inStock}
          aria-label={isFa ? "افزودن به سبد خرید" : "Add to cart"}
          className={`absolute bottom-3 w-8 h-8 rounded-full flex items-center justify-center transition-all ${
            isFa ? "left-3" : "right-3"
          } ${
            product.inStock
              ? "bg-[#EF4056] text-white hover:bg-[#d63850]"
              : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
          }`}
        >
          <ShoppingCart size={15} />
        </button>
      )}
    </div>
  );
}
"""))

# ============================================================
# README.md (final)
# ============================================================
files.append(("README.md", """# SourcePixcel

Bilingual (Persian / English) e-commerce frontend built with Next.js 15.

## Stack

- Next.js 15.5.9 (App Router)
- React 19.2.0
- TypeScript 5
- Tailwind CSS 3.4
- Zustand 5 (state management)
- lucide-react (icons)

## Features

- Bilingual support (Persian RTL / English LTR)
- 68 mock products, 12 categories, 30 brands
- Product listing with filters + sort + pagination
- Product detail with gallery, tabs, reviews
- Cart with localStorage persistence
- Multi-step checkout (simulated Zarinpal gateway)
- Auth pages (login, register, forgot password)
- User dashboard (orders, wishlist, addresses, profile)
- Product comparison (up to 4 products)
- Blog with list + detail
- Search with live filter
- Dark mode with localStorage
- Toast notifications
- Skeleton loaders
- Error boundaries
- SEO: sitemap, robots, JSON-LD, Open Graph
- PWA manifest

## Installation

    npm install --registry=https://mirror-npm.runflare.com

## Development

    npm run dev

## Build

    npm run build

## URLs

### Persian
- Home: http://localhost:3000/fa
- Categories: http://localhost:3000/fa/categories
- Category: http://localhost:3000/fa/category/mobile
- Product: http://localhost:3000/fa/product/samsung-galaxy-s24-ultra
- Cart: http://localhost:3000/fa/cart
- Checkout: http://localhost:3000/fa/checkout
- Login: http://localhost:3000/fa/auth/login
- Register: http://localhost:3000/fa/auth/register
- Account: http://localhost:3000/fa/account
- Compare: http://localhost:3000/fa/compare
- Blog: http://localhost:3000/fa/blog
- Search: http://localhost:3000/fa/search
- About: http://localhost:3000/fa/about
- Contact: http://localhost:3000/fa/contact
- FAQ: http://localhost:3000/fa/faq
- Terms: http://localhost:3000/fa/terms
- Privacy: http://localhost:3000/fa/privacy

### English
Replace `/fa/` with `/en/` in all URLs above.

## SEO URLs

- Sitemap: http://localhost:3000/sitemap.xml
- Robots: http://localhost:3000/robots.txt
- Manifest: http://localhost:3000/manifest.webmanifest

## Demo Credentials

Login accepts any valid Iranian mobile (`09XXXXXXXXX`) with any password of 6+ characters.

Coupon code: `SOURCE10` (10% off)

## Project Structure

    app/
      layout.tsx              Root layout
      page.tsx                Redirect to /fa
      not-found.tsx           Global 404
      sitemap.ts              Auto-generated sitemap
      robots.ts               robots.txt
      manifest.ts             PWA manifest
      globals.css
      [locale]/
        layout.tsx            Locale wrapper with Header/Footer/Toasts
        page.tsx              Home
        loading.tsx           Loading skeleton
        error.tsx             Error boundary
        not-found.tsx         Locale 404
        categories/           All categories
        category/[slug]/      Category products
        product/[slug]/       Product detail
        cart/                 Cart
        checkout/             Multi-step checkout
        compare/              Compare products
        search/               Search results
        blog/                 Blog list + detail
        account/              User dashboard
        auth/                 Login, Register, Forgot
        about/                About
        contact/              Contact
        faq/                  FAQ
        terms/                Terms
        privacy/              Privacy
    components/
      layout/                 Header, Footer
      home/                   HeroSlider, CategoryCircles, AmazingOffer, ...
      product/                ProductCard, ProductGallery, ProductTabs, ...
      cart/                   CartLine, CartSummary, ...
      checkout/               ShippingForm, PaymentStep, ...
      account/                AccountSidebar, DashboardView, ...
      auth/                   LoginForm, RegisterForm, ...
      blog/                   BlogCard, BlogList, BlogPostDetail
      compare/                CompareTable, ComparePage
      search/                 SearchPage
      common/                 Breadcrumb, Pagination, Skeleton, Toast, ...
    lib/
      data/                   Mock data (products, categories, brands, ...)
      stores/                 Zustand stores (cart, wishlist, auth, ...)
      types/                  TypeScript types
      utils/                  Helpers (format, validators, seo)

## License

Demo project. All rights reserved.
"""))

# ============================================================
# SELF-CHECK SCRIPT
# ============================================================
files.append(("check_project.py", """# check_project.py
# Self-check script — verifies all critical files exist
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CRITICAL_FILES = [
    # Config
    "package.json",
    "next.config.js",
    "tsconfig.json",
    "tailwind.config.ts",
    "postcss.config.js",

    # Root app
    "app/layout.tsx",
    "app/page.tsx",
    "app/globals.css",
    "app/not-found.tsx",
    "app/sitemap.ts",
    "app/robots.ts",
    "app/manifest.ts",

    # Locale
    "app/[locale]/layout.tsx",
    "app/[locale]/page.tsx",
    "app/[locale]/loading.tsx",
    "app/[locale]/error.tsx",
    "app/[locale]/not-found.tsx",

    # Types
    "lib/types/product.ts",
    "lib/types/blog.ts",
    "lib/types/index.ts",

    # Data
    "lib/data/products.ts",
    "lib/data/mock-orders.ts",
    "lib/data/mock-blog.ts",
    "lib/data/iran-provinces.ts",
    "lib/data/index.ts",

    # Stores
    "lib/stores/cart.ts",
    "lib/stores/wishlist.ts",
    "lib/stores/auth.ts",
    "lib/stores/compare.ts",
    "lib/stores/theme.ts",
    "lib/stores/toast.ts",
    "lib/stores/index.ts",

    # Utils
    "lib/utils/format.ts",
    "lib/utils/validators.ts",
    "lib/utils/seo.ts",
    "lib/utils/index.ts",

    # Layout
    "components/layout/Header.tsx",
    "components/layout/Footer.tsx",

    # Home
    "components/home/HeroSlider.tsx",
    "components/home/CategoryCircles.tsx",
    "components/home/AmazingOffer.tsx",
    "components/home/ProductSection.tsx",
    "components/home/BrandLogos.tsx",
    "components/home/ServiceBadges.tsx",
    "components/home/index.ts",

    # Product
    "components/product/ProductCard.tsx",
    "components/product/RatingStars.tsx",
    "components/product/PriceTag.tsx",
    "components/product/ProductFilters.tsx",
    "components/product/ProductSort.tsx",
    "components/product/ProductGallery.tsx",
    "components/product/ProductDetail.tsx",
    "components/product/ProductTabs.tsx",
    "components/product/QuantitySelector.tsx",
    "components/product/RelatedProducts.tsx",
    "components/product/CompareButton.tsx",
    "components/product/index.ts",

    # Cart
    "components/cart/CartPage.tsx",
    "components/cart/CartLine.tsx",
    "components/cart/CartSummary.tsx",
    "components/cart/EmptyCart.tsx",
    "components/cart/index.ts",

    # Checkout
    "components/checkout/CheckoutPage.tsx",
    "components/checkout/StepIndicator.tsx",
    "components/checkout/ShippingForm.tsx",
    "components/checkout/ShippingMethod.tsx",
    "components/checkout/PaymentStep.tsx",
    "components/checkout/OrderReview.tsx",
    "components/checkout/OrderSuccess.tsx",
    "components/checkout/index.ts",

    # Auth
    "components/auth/AuthCard.tsx",
    "components/auth/LoginForm.tsx",
    "components/auth/RegisterForm.tsx",
    "components/auth/ForgotPasswordForm.tsx",
    "components/auth/index.ts",

    # Account
    "components/account/AccountSidebar.tsx",
    "components/account/AccountGuard.tsx",
    "components/account/DashboardView.tsx",
    "components/account/OrdersView.tsx",
    "components/account/OrderDetailView.tsx",
    "components/account/WishlistView.tsx",
    "components/account/AddressesView.tsx",
    "components/account/ProfileView.tsx",
    "components/account/OrderStatusBadge.tsx",
    "components/account/index.ts",

    # Blog
    "components/blog/BlogCard.tsx",
    "components/blog/BlogList.tsx",
    "components/blog/BlogPostDetail.tsx",
    "components/blog/index.ts",

    # Compare
    "components/compare/ComparePage.tsx",
    "components/compare/CompareTable.tsx",
    "components/compare/CompareEmpty.tsx",
    "components/compare/index.ts",

    # Search
    "components/search/SearchPage.tsx",
    "components/search/index.ts",

    # Common
    "components/common/Breadcrumb.tsx",
    "components/common/Pagination.tsx",
    "components/common/EmptyState.tsx",
    "components/common/StaticPage.tsx",
    "components/common/ThemeProvider.tsx",
    "components/common/ThemeToggle.tsx",
    "components/common/JsonLd.tsx",
    "components/common/ToastContainer.tsx",
    "components/common/Skeleton.tsx",
    "components/common/ProductCardSkeleton.tsx",
    "components/common/ErrorBoundary.tsx",
    "components/common/index.ts",
]

print("=" * 60)
print("SourcePixcel — Self-Check")
print("=" * 60)
print(f"Base: {BASE}\\n")

missing = []
present = 0

for path in CRITICAL_FILES:
    full = os.path.join(BASE, *path.split("/"))
    if os.path.exists(full):
        present += 1
    else:
        missing.append(path)

print(f"Present: {present}/{len(CRITICAL_FILES)}")

if missing:
    print(f"\\nMissing ({len(missing)} files):")
    for path in missing:
        print(f"  ✗ {path}")
    print("\\n" + "=" * 60)
    print("INCOMPLETE")
    print("=" * 60)
else:
    print("\\n" + "=" * 60)
    print("✅ ALL FILES PRESENT!")
    print("=" * 60)
    print("\\nProject is complete. Run: npm run dev")
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 20: Final Touches")
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
        print("\n" + "=" * 60)
        print("🎉 ALL STEPS COMPLETE! 🎉")
        print("=" * 60)
        print("\nNext:")
        print("  1) npm run dev")
        print("  2) python check_project.py   (verify everything)")
        print("  3) Open http://localhost:3000/fa")
        print("\nCongratulations! Your project is complete.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()