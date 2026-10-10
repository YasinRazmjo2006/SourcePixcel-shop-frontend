# 32_loading_empty.py
# Loading و Empty states حرفه‌ای با illustration
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/common/EmptyState.tsx (upgraded with illustrations)
# ============================================================
files.append(("components/common/EmptyState.tsx", """"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { Locale } from "@/lib/types";
import { RippleButton } from "@/components/ui";

type IllustrationType =
  | "search"
  | "cart"
  | "wishlist"
  | "orders"
  | "compare"
  | "error"
  | "offline"
  | "404"
  | "empty-box"
  | "no-results";

interface EmptyStateProps {
  locale: Locale;
  type?: IllustrationType;
  titleFa?: string;
  titleEn?: string;
  messageFa?: string;
  messageEn?: string;
  actionLabelFa?: string;
  actionLabelEn?: string;
  actionHref?: string;
  onAction?: () => void;
}

const ILLUSTRATIONS: Record<
  IllustrationType,
  { emoji: string; color: string; bg: string }
> = {
  search: { emoji: "🔍", color: "#00BFFF", bg: "#00BFFF" },
  cart: { emoji: "🛒", color: "#EF4056", bg: "#EF4056" },
  wishlist: { emoji: "💝", color: "#EC4899", bg: "#EC4899" },
  orders: { emoji: "📦", color: "#8B5CF6", bg: "#8B5CF6" },
  compare: { emoji: "⚖️", color: "#F59E0B", bg: "#F59E0B" },
  error: { emoji: "⚠️", color: "#EF4444", bg: "#EF4444" },
  offline: { emoji: "📡", color: "#6B7280", bg: "#6B7280" },
  "404": { emoji: "🗺️", color: "#EF4056", bg: "#EF4056" },
  "empty-box": { emoji: "📭", color: "#A1A3A8", bg: "#A1A3A8" },
  "no-results": { emoji: "🔎", color: "#00BFFF", bg: "#00BFFF" },
};

export default function EmptyState({
  locale,
  type = "empty-box",
  titleFa,
  titleEn,
  messageFa,
  messageEn,
  actionLabelFa,
  actionLabelEn,
  actionHref,
  onAction,
}: EmptyStateProps) {
  const isFa = locale === "fa";
  const illustration = ILLUSTRATIONS[type];

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      {/* Illustration container with animated circles */}
      <div className="relative mb-6">
        {/* Outer pulse ring */}
        <motion.div
          animate={{ scale: [1, 1.15, 1], opacity: [0.15, 0.05, 0.15] }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute inset-0 rounded-full"
          style={{
            backgroundColor: illustration.color,
            width: 120,
            height: 120,
          }}
        />

        {/* Middle ring */}
        <motion.div
          animate={{ scale: [1, 1.08, 1], opacity: [0.1, 0.2, 0.1] }}
          transition={{
            duration: 2.5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 0.3,
          }}
          className="absolute inset-0 rounded-full"
          style={{
            backgroundColor: illustration.color,
            width: 120,
            height: 120,
          }}
        />

        {/* Emoji circle */}
        <motion.div
          initial={{ scale: 0, rotate: -10 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 20,
          }}
          className="relative w-[120px] h-[120px] rounded-full flex items-center justify-center"
          style={{ backgroundColor: `${illustration.bg}15` }}
        >
          <motion.span
            animate={{ y: [0, -6, 0] }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="text-[52px] select-none"
          >
            {illustration.emoji}
          </motion.span>
        </motion.div>

        {/* Decorative dots */}
        <motion.div
          animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
          className="absolute w-2 h-2 rounded-full"
          style={{
            backgroundColor: illustration.color,
            top: 10,
            right: 10,
          }}
        />
        <motion.div
          animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, delay: 0.8 }}
          className="absolute w-1.5 h-1.5 rounded-full"
          style={{
            backgroundColor: illustration.color,
            bottom: 15,
            left: 8,
          }}
        />
      </div>

      {/* Title */}
      <motion.h3
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15, duration: 0.3 }}
        className="text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2"
      >
        {isFa ? titleFa : titleEn}
      </motion.h3>

      {/* Message */}
      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.3 }}
        className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md leading-6"
      >
        {isFa ? messageFa : messageEn}
      </motion.p>

      {/* Action */}
      {(actionHref || onAction) && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25, duration: 0.3 }}
        >
          {actionHref ? (
            <Link href={actionHref}>
              <RippleButton size="md">
                {isFa ? actionLabelFa : actionLabelEn}
              </RippleButton>
            </Link>
          ) : (
            <RippleButton onClick={onAction} size="md">
              {isFa ? actionLabelFa : actionLabelEn}
            </RippleButton>
          )}
        </motion.div>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/common/LoadingScreen.tsx — صفحه لودینگ کامل
# ============================================================
files.append(("components/common/LoadingScreen.tsx", """"use client";

import { motion } from "framer-motion";

interface LoadingScreenProps {
  label?: string;
}

export default function LoadingScreen({ label = "Loading..." }: LoadingScreenProps) {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-4">
      {/* Animated logo */}
      <div className="relative mb-6">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-20 h-20 rounded-full border-4 border-[#EF4056]/20 border-t-[#EF4056]"
        />
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          className="absolute inset-0 flex items-center justify-center"
        >
          <div className="w-10 h-10 rounded-xl bg-[#EF4056] flex items-center justify-center text-white text-[18px] font-bold shadow-lg">
            S
          </div>
        </motion.div>
      </div>

      {/* Dots */}
      <div className="flex items-center gap-2 mb-3">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            animate={{ y: [0, -6, 0], opacity: [0.4, 1, 0.4] }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              delay: i * 0.15,
              ease: "easeInOut",
            }}
            className="w-2 h-2 rounded-full bg-[#EF4056]"
          />
        ))}
      </div>

      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="text-[12px] text-[#A1A3A8]"
      >
        {label}
      </motion.p>
    </div>
  );
}
"""))

# ============================================================
# components/common/ProgressBar.tsx — نوار پیشرفت
# ============================================================
files.append(("components/common/ProgressBar.tsx", """"use client";

import { motion } from "framer-motion";

interface ProgressBarProps {
  value: number; // 0-100
  color?: string;
  height?: number;
  showLabel?: boolean;
}

export default function ProgressBar({
  value,
  color = "#EF4056",
  height = 4,
  showLabel = false,
}: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, value));

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between mb-1">
          <span className="text-[10px] text-[#A1A3A8]">{clamped}%</span>
        </div>
      )}
      <div
        className="w-full bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-full overflow-hidden"
        style={{ height }}
      >
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${clamped}%` }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="h-full rounded-full"
          style={{
            background: `linear-gradient(90deg, ${color} 0%, ${color}dd 100%)`,
          }}
        />
      </div>
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
export { default as LoadingScreen } from "./LoadingScreen";
export { default as ProgressBar } from "./ProgressBar";
"""))

# ============================================================
# app/[locale]/loading.tsx (upgraded)
# ============================================================
files.append(("app/[locale]/loading.tsx", """"use client";

import { motion } from "framer-motion";
import { ProductCardSkeleton, Skeleton } from "@/components/common";

export default function Loading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
      {/* Hero skeleton */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Skeleton variant="rect" className="w-full h-[200px] md:h-[300px] rounded-xl" />
      </motion.div>

      {/* Service badges skeleton */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex flex-col items-center gap-2"
            >
              <Skeleton variant="circle" width={48} height={48} />
              <Skeleton variant="text" width={60} height={12} />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Category circles skeleton */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <Skeleton variant="text" width={100} height={20} className="mb-4" />
        <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-3">
          {Array.from({ length: 12 }).map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.03 }}
              className="flex flex-col items-center gap-2"
            >
              <Skeleton variant="circle" width={64} height={64} />
              <Skeleton variant="text" width={50} height={10} />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Product grid skeleton */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <Skeleton variant="text" width={120} height={20} className="mb-4" />
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
            >
              <ProductCardSkeleton />
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/cart/loading.tsx
# ============================================================
files.append(("app/[locale]/cart/loading.tsx", """"use client";

import { motion } from "framer-motion";
import { Skeleton } from "@/components/common";

export default function CartLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Skeleton variant="text" width={120} height={20} className="mb-4" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-3">
          {[1, 2, 3].map((i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 flex gap-4"
            >
              <Skeleton variant="rect" width={100} height={100} className="shrink-0" />
              <div className="flex-1 space-y-3">
                <Skeleton variant="text" width="80%" height={16} />
                <Skeleton variant="text" width="40%" height={12} />
                <div className="flex items-center justify-between pt-2">
                  <Skeleton variant="rect" width={90} height={32} />
                  <Skeleton variant="text" width={80} height={16} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 space-y-3">
            <Skeleton variant="text" width={120} height={20} className="mb-4" />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="rect" width="100%" height={44} className="mt-4" />
          </div>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/product/[slug]/loading.tsx
# ============================================================
files.append(("app/[locale]/product/[slug]/loading.tsx", """"use client";

import { motion } from "framer-motion";
import { Skeleton } from "@/components/common";

export default function ProductLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Skeleton variant="text" width={200} height={16} className="mb-4" />

      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Gallery skeleton */}
          <div className="flex flex-col-reverse md:flex-row gap-3">
            <div className="flex md:flex-col gap-2">
              {[1, 2, 3, 4].map((i) => (
                <Skeleton
                  key={i}
                  variant="rect"
                  width={64}
                  height={64}
                  className="shrink-0"
                />
              ))}
            </div>
            <Skeleton
              variant="rect"
              className="flex-1 aspect-square rounded-xl"
            />
          </div>

          {/* Info skeleton */}
          <div className="space-y-4">
            <Skeleton variant="text" width="40%" height={14} />
            <Skeleton variant="text" width="100%" height={24} />
            <Skeleton variant="text" width="60%" height={18} />
            <Skeleton variant="rect" width="100%" height={1} />
            <Skeleton variant="text" width="50%" height={32} />
            <Skeleton variant="rect" width={120} height={32} />
            <Skeleton variant="rect" width="100%" height={44} />
            <div className="space-y-2 pt-3">
              <Skeleton variant="text" width="100%" height={14} />
              <Skeleton variant="text" width="100%" height={14} />
              <Skeleton variant="text" width="80%" height={14} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/blog/loading.tsx
# ============================================================
files.append(("app/[locale]/blog/loading.tsx", """"use client";

import { motion } from "framer-motion";
import { Skeleton } from "@/components/common";

export default function BlogLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Skeleton variant="text" width={150} height={20} className="mb-6" />

      {/* Featured */}
      <div className="mb-8">
        <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
          <Skeleton variant="rect" className="w-full aspect-[16/7]" />
          <div className="p-4 space-y-3">
            <Skeleton variant="text" width="30%" height={14} />
            <Skeleton variant="text" width="80%" height={24} />
            <Skeleton variant="text" width="100%" height={14} />
            <Skeleton variant="text" width="60%" height={14} />
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden"
          >
            <Skeleton variant="rect" className="w-full aspect-video" />
            <div className="p-4 space-y-3">
              <Skeleton variant="text" width="30%" height={12} />
              <Skeleton variant="text" width="100%" height={18} />
              <Skeleton variant="text" width="100%" height={14} />
              <Skeleton variant="text" width="80%" height={14} />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/account/loading.tsx
# ============================================================
files.append(("app/[locale]/account/loading.tsx", """"use client";

import { Skeleton } from "@/components/common";

export default function AccountLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 space-y-3">
            <div className="flex items-center gap-3 pb-3 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <Skeleton variant="circle" width={48} height={48} />
              <div className="flex-1 space-y-2">
                <Skeleton variant="text" width="80%" height={14} />
                <Skeleton variant="text" width="60%" height={12} />
              </div>
            </div>
            {[1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} variant="text" width="100%" height={36} />
            ))}
          </div>
        </div>

        <div className="lg:col-span-3 space-y-4">
          <Skeleton variant="rect" width="100%" height={100} className="rounded-xl" />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} variant="rect" width="100%" height={100} className="rounded-xl" />
            ))}
          </div>
          <Skeleton variant="rect" width="100%" height={200} className="rounded-xl" />
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/search/page.tsx (updated with new EmptyState)
# ============================================================
files.append(("app/[locale]/search/page.tsx", """import { Suspense } from "react";
import type { Locale } from "@/lib/types";
import { SearchPage } from "@/components/search";
import LoadingScreen from "@/components/common/LoadingScreen";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SearchRoute({ params }: PageProps) {
  const { locale } = await params;
  return (
    <Suspense
      fallback={
        <LoadingScreen label={locale === "fa" ? "در حال جستجو..." : "Searching..."} />
      }
    >
      <SearchPage locale={locale as Locale} />
    </Suspense>
  );
}
"""))

# ============================================================
# components/search/SearchPage.tsx (updated with new EmptyState)
# ============================================================
files.append(("components/search/SearchPage.tsx", """"use client";

import { useState, useMemo, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { Search as SearchIcon, X, Sparkles } from "lucide-react";
import type { Locale, Product, SortOption } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import ProductCard from "@/components/product/ProductCard";
import ProductSort from "@/components/product/ProductSort";
import Pagination from "@/components/common/Pagination";
import EmptyState from "@/components/common/EmptyState";
import { Breadcrumb } from "@/components/common";

interface SearchPageProps {
  locale: Locale;
}

const PER_PAGE = 12;

const POPULAR_SEARCHES = [
  { fa: "گوشی سامسونگ", en: "Samsung phone" },
  { fa: "لپ‌تاپ ایسوس", en: "Asus laptop" },
  { fa: "هدفون سونی", en: "Sony headphones" },
  { fa: "ساعت اپل", en: "Apple watch" },
  { fa: "کفش نایک", en: "Nike shoes" },
  { fa: "دوربین کانن", en: "Canon camera" },
];

export default function SearchPage({ locale }: SearchPageProps) {
  const isFa = locale === "fa";
  const params = useSearchParams();

  const initialQuery = params.get("q") ?? "";
  const [query, setQuery] = useState(initialQuery);
  const [inputValue, setInputValue] = useState(initialQuery);
  const [sort, setSort] = useState<SortOption>("popular");
  const [page, setPage] = useState(1);

  useEffect(() => {
    setInputValue(query);
  }, [query]);

  const results = useMemo(() => {
    if (!query.trim()) return [];
    const q = query.toLowerCase().trim();
    let result = allProducts.filter((p) => {
      const titleFa = p.titleFa.toLowerCase();
      const titleEn = p.titleEn.toLowerCase();
      const brand = p.brand.toLowerCase();
      const tags = p.tags.join(" ").toLowerCase();
      return (
        titleFa.includes(q) ||
        titleEn.includes(q) ||
        brand.includes(q) ||
        tags.includes(q)
      );
    });

    switch (sort) {
      case "newest":
        result.sort((a, b) => b.id - a.id);
        break;
      case "price-asc":
        result.sort((a, b) => a.finalPrice - b.finalPrice);
        break;
      case "price-desc":
        result.sort((a, b) => b.finalPrice - a.finalPrice);
        break;
      case "rating":
        result.sort((a, b) => b.rating - a.rating);
        break;
      default:
        result.sort((a, b) => b.reviewCount - a.reviewCount);
    }

    return result;
  }, [query, sort]);

  useEffect(() => {
    setPage(1);
  }, [query, sort]);

  const totalPages = Math.ceil(results.length / PER_PAGE);
  const paginated = results.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setQuery(inputValue.trim());
  };

  const clearSearch = () => {
    setInputValue("");
    setQuery("");
  };

  const t = {
    title: isFa ? "جستجو" : "Search",
    placeholder: isFa ? "جستجو در SourcePixcel" : "Search in SourcePixcel",
    hint: isFa
      ? "نام محصول، برند یا دسته‌بندی خود را وارد کنید."
      : "Enter a product name, brand, or category.",
    resultsFor: isFa ? "نتایج برای" : "Results for",
    clear: isFa ? "پاک کردن" : "Clear",
    popular: isFa ? "جستجوهای محبوب" : "Popular searches",
    startSearching: isFa ? "شروع جستجو" : "Start searching",
  };

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "جستجو", labelEn: "Search" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
        {t.title}
      </h1>

      {/* Search input */}
      <form onSubmit={handleSubmit} className="mb-5">
        <div className="relative max-w-2xl">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={t.placeholder}
            autoFocus
            className="w-full h-12 rounded-xl bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[14px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] focus:ring-2 focus:ring-[#EF4056]/10 transition-all"
            style={{
              paddingRight: isFa ? 100 : 16,
              paddingLeft: isFa ? 16 : 100,
            }}
          />
          <div
            className="absolute top-1/2 -translate-y-1/2 flex items-center gap-1"
            style={{ [isFa ? "left" : "right"]: 8 } as React.CSSProperties}
          >
            {inputValue && (
              <motion.button
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                type="button"
                onClick={clearSearch}
                aria-label={t.clear}
                className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              >
                <X size={16} />
              </motion.button>
            )}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              className="h-9 px-4 rounded-lg bg-[#EF4056] text-white flex items-center justify-center hover:bg-[#d63850] transition-colors"
            >
              <SearchIcon size={16} />
            </motion.button>
          </div>
        </div>
      </form>

      {/* Empty - no query */}
      {!query && (
        <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8">
          <div className="flex flex-col items-center text-center mb-8">
            <motion.div
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-16 h-16 rounded-full bg-[#00BFFF]/10 flex items-center justify-center mb-4"
            >
              <SearchIcon size={28} className="text-[#00BFFF]" />
            </motion.div>
            <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] max-w-md leading-6">
              {t.hint}
            </p>
          </div>

          {/* Popular searches */}
          <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] pt-6">
            <div className="flex items-center gap-2 mb-4 justify-center">
              <Sparkles size={16} className="text-[#F59E0B]" />
              <h2 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.popular}
              </h2>
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              {POPULAR_SEARCHES.map((item, i) => (
                <motion.button
                  key={i}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    const q = isFa ? item.fa : item.en;
                    setInputValue(q);
                    setQuery(q);
                  }}
                  className="text-[12px] bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] px-3 py-1.5 rounded-full hover:bg-[#EF4056] hover:text-white transition-colors"
                >
                  {isFa ? item.fa : item.en}
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {query && (
        <>
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <h2 className="text-[14px] text-[#62666D] dark:text-[#A1A3A8]">
              {t.resultsFor}{" "}
              <span className="font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                "{query}"
              </span>
            </h2>
          </div>

          {paginated.length === 0 ? (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
              <EmptyState
                locale={locale}
                type="no-results"
                titleFa="نتیجه‌ای یافت نشد"
                titleEn="No results found"
                messageFa="متأسفانه محصولی با این عبارت پیدا نشد. عبارت دیگری را امتحان کنید یا از جستجوهای محبوب استفاده کنید."
                messageEn="No products matched your search. Try another keyword or explore popular searches."
                actionLabelFa="مشاهده همه محصولات"
                actionLabelEn="Browse all products"
                actionHref={`/${locale}/categories`}
              />
            </div>
          ) : (
            <>
              <ProductSort
                value={sort}
                onChange={setSort}
                locale={locale}
                resultCount={results.length}
              />

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mt-3">
                {paginated.map((product, i) => (
                  <motion.div
                    key={product.id}
                    initial={{ opacity: 0, y: 12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.03 }}
                  >
                    <ProductCard product={product} locale={locale} />
                  </motion.div>
                ))}
              </div>

              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
                locale={locale}
              />
            </>
          )}
        </>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/cart/EmptyCart.tsx (updated with new EmptyState)
# ============================================================
files.append(("components/cart/EmptyCart.tsx", """import type { Locale } from "@/lib/types";
import { EmptyState } from "@/components/common";

interface EmptyCartProps {
  locale: Locale;
}

export default function EmptyCart({ locale }: EmptyCartProps) {
  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
      <EmptyState
        locale={locale}
        type="cart"
        titleFa="سبد خرید شما خالی است"
        titleEn="Your cart is empty"
        messageFa="می‌توانید از دسته‌بندی‌های مختلف، محصولات مورد نظر خود را اضافه کنید و از تخفیف‌های ویژه بهره‌مند شوید."
        messageEn="You can browse various categories, add products to your cart, and enjoy special discounts."
        actionLabelFa="شروع خرید"
        actionLabelEn="Start shopping"
        actionHref={`/${locale}`}
      />
    </div>
  );
}
"""))

# ============================================================
# components/account/WishlistView.tsx (updated with new EmptyState)
# ============================================================
files.append(("components/account/WishlistView.tsx", """"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useWishlistStore } from "@/lib/stores";
import ProductCard from "@/components/product/ProductCard";
import { EmptyState } from "@/components/common";

interface WishlistViewProps {
  locale: Locale;
}

export default function WishlistView({ locale }: WishlistViewProps) {
  const isFa = locale === "fa";
  const ids = useWishlistStore((s) => s.ids);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const items: Product[] = ids
    .map((id) => allProducts.find((p) => p.id === id))
    .filter((p): p is Product => p !== undefined);

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="space-y-3">
        <h1 className="text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "علاقه‌مندی‌ها" : "Wishlist"}
        </h1>
        <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
          <EmptyState
            locale={locale}
            type="wishlist"
            titleFa="لیست علاقه‌مندی‌ها خالی است"
            titleEn="Your wishlist is empty"
            messageFa="محصولات مورد علاقه خود را با کلیک روی آیکون قلب اضافه کنید و بعداً به راحتی به سبد خرید اضافه کنید."
            messageEn="Add products to your wishlist by clicking the heart icon, and easily add them to your cart later."
            actionLabelFa="مشاهده محصولات"
            actionLabelEn="Browse products"
            actionHref={`/${locale}`}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "علاقه‌مندی‌ها" : "Wishlist"}
        </h1>
        <span className="text-[12px] text-[#A1A3A8]">
          {isFa
            ? `${items.length.toLocaleString("fa-IR")} کالا`
            : `${items.length} items`}
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {items.map((product, i) => (
          <motion.div
            key={product.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
          >
            <ProductCard product={product} locale={locale} />
          </motion.div>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/compare/CompareEmpty.tsx (updated)
# ============================================================
files.append(("components/compare/CompareEmpty.tsx", """import type { Locale } from "@/lib/types";
import { EmptyState } from "@/components/common";

interface CompareEmptyProps {
  locale: Locale;
}

export default function CompareEmpty({ locale }: CompareEmptyProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
      <EmptyState
        locale={locale}
        type="compare"
        titleFa="لیست مقایسه خالی است"
        titleEn="Compare list is empty"
        messageFa="برای مقایسه، روی آیکون مقایسه در کارت محصولات کلیک کنید. می‌توانید تا ۴ محصول را همزمان مقایسه کنید."
        messageEn="Click the compare icon on product cards to add them. You can compare up to 4 products at once."
        actionLabelFa="مشاهده محصولات"
        actionLabelEn="Browse products"
        actionHref={`/${locale}`}
      />
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/error.tsx (upgraded)
# ============================================================
files.append(("app/[locale]/error.tsx", """"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { RefreshCw, Home, AlertTriangle } from "lucide-react";
import Link from "next/link";
import { RippleButton } from "@/components/ui";

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
      <div className="relative mb-6 inline-block">
        <motion.div
          animate={{ scale: [1, 1.15, 1], opacity: [0.15, 0.05, 0.15] }}
          transition={{ duration: 3, repeat: Infinity }}
          className="absolute inset-0 rounded-full bg-[#EF4444]"
          style={{ width: 120, height: 120 }}
        />
        <motion.div
          initial={{ scale: 0, rotate: -10 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
          className="relative w-[120px] h-[120px] rounded-full bg-[#EF4444]/10 flex items-center justify-center"
        >
          <motion.div
            animate={{ rotate: [0, -5, 5, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <AlertTriangle size={52} className="text-[#EF4444]" />
          </motion.div>
        </motion.div>
      </div>

      <motion.h1
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2"
      >
        خطایی رخ داد
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md mx-auto leading-6"
      >
        متأسفانه در بارگذاری این صفحه مشکلی پیش آمد. لطفاً دوباره تلاش کنید یا به
        صفحه اصلی بازگردید.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        className="flex items-center justify-center gap-3 flex-wrap"
      >
        <RippleButton onClick={reset} variant="primary" size="md">
          <RefreshCw size={16} />
          تلاش مجدد
        </RippleButton>

        <Link href="/fa">
          <RippleButton variant="ghost" size="md">
            <Home size={16} />
            بازگشت به خانه
          </RippleButton>
        </Link>
      </motion.div>
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 32: Loading & Empty States")
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
        print("  3) Test these URLs:")
        print("     http://localhost:3000/fa/search")
        print("     http://localhost:3000/fa/cart (empty)")
        print("     http://localhost:3000/fa/account/wishlist (empty)")
        print("     http://localhost:3000/fa/compare (empty)")
        print("     http://localhost:3000/fa/some-missing-page")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()