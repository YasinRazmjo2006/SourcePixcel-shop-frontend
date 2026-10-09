# 17_compare.py
# ساخت سیستم مقایسه محصولات
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/compare.ts
# ============================================================
files.append(("lib/stores/compare.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

const MAX_COMPARE = 4;

interface CompareState {
  ids: number[];
  toggle: (productId: number) => void;
  has: (productId: number) => boolean;
  remove: (productId: number) => void;
  clear: () => void;
  isFull: () => boolean;
}

export const useCompareStore = create<CompareState>()(
  persist(
    (set, get) => ({
      ids: [],

      toggle: (productId) => {
        set((state) => {
          if (state.ids.includes(productId)) {
            return { ids: state.ids.filter((id) => id !== productId) };
          }
          if (state.ids.length >= MAX_COMPARE) {
            return state;
          }
          return { ids: [...state.ids, productId] };
        });
      },

      has: (productId) => get().ids.includes(productId),

      remove: (productId) => {
        set((state) => ({
          ids: state.ids.filter((id) => id !== productId),
        }));
      },

      clear: () => set({ ids: [] }),

      isFull: () => get().ids.length >= MAX_COMPARE,
    }),
    { name: "sourcepixcel-compare" }
  )
);

export const COMPARE_MAX = MAX_COMPARE;
"""))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", """// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export type { AuthUser } from "./auth";
"""))

# ============================================================
# components/product/CompareButton.tsx
# ============================================================
files.append(("components/product/CompareButton.tsx", """"use client";

import { GitCompareArrows } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useCompareStore, COMPARE_MAX } from "@/lib/stores";

interface CompareButtonProps {
  productId: number;
  locale: Locale;
  size?: "sm" | "md";
  variant?: "icon" | "full";
}

export default function CompareButton({
  productId,
  locale,
  size = "md",
  variant = "icon",
}: CompareButtonProps) {
  const isFa = locale === "fa";
  const toggle = useCompareStore((s) => s.toggle);
  const isInCompare = useCompareStore((s) => s.ids.includes(productId));
  const isFull = useCompareStore((s) => s.ids.length >= COMPARE_MAX && !isInCompare);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isFull) return;
    toggle(productId);
  };

  const iconSize = size === "sm" ? 14 : 16;

  if (variant === "full") {
    return (
      <button
        onClick={handleClick}
        disabled={isFull}
        className={`h-10 px-4 rounded-lg border text-[12px] font-medium flex items-center justify-center gap-2 transition-colors ${
          isInCompare
            ? "bg-[#EF4056]/5 border-[#EF4056] text-[#EF4056]"
            : isFull
            ? "bg-[#F5F5F5] border-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
            : "bg-white border-[#E0E0E2] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056]"
        }`}
      >
        <GitCompareArrows size={iconSize} />
        {isInCompare
          ? isFa
            ? "در مقایسه"
            : "In compare"
          : isFa
          ? "افزودن به مقایسه"
          : "Compare"}
      </button>
    );
  }

  return (
    <button
      onClick={handleClick}
      disabled={isFull}
      aria-label={isFa ? "افزودن به مقایسه" : "Add to compare"}
      title={
        isFull
          ? isFa
            ? `حداکثر ${COMPARE_MAX} محصول`
            : `Max ${COMPARE_MAX} products`
          : isFa
          ? "افزودن به مقایسه"
          : "Add to compare"
      }
      className={`w-7 h-7 rounded-full flex items-center justify-center transition-all ${
        isInCompare
          ? "bg-[#EF4056] text-white"
          : isFull
          ? "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
          : "bg-white/90 backdrop-blur text-[#62666D] hover:text-[#EF4056]"
      }`}
    >
      <GitCompareArrows size={iconSize} />
    </button>
  );
}
"""))

# ============================================================
# components/product/ProductCard.tsx (updated to add compare button)
# ============================================================
files.append(("components/product/ProductCard.tsx", """"use client";

import Link from "next/link";
import Image from "next/image";
import { Heart, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore } from "@/lib/stores";
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

  const title = isFa ? product.titleFa : product.titleEn;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!product.inStock) return;
    addToCart(product.id, 1);
  };

  const handleToggleWishlist = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleWishlist(product.id);
  };

  return (
    <div className="group relative bg-white rounded-lg border border-[#E0E0E2] hover:shadow-lg transition-all duration-200 overflow-hidden">
      {/* Action icons (top corner) */}
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

      {/* Discount badge */}
      {product.discountPercent > 0 && (
        <div
          className={`absolute top-2 z-10 bg-[#EF4056] text-white text-[11px] font-bold rounded px-1.5 py-0.5 ${
            isFa ? "right-2" : "left-2"
          }`}
        >
          {product.discountPercent.toLocaleString(isFa ? "fa-IR" : "en-US")}٪
        </div>
      )}

      {/* Out of stock overlay */}
      {!product.inStock && (
        <div className="absolute inset-0 bg-white/70 z-20 flex items-center justify-center">
          <span className="text-[#62666D] text-[13px] font-medium bg-white px-3 py-1 rounded">
            {isFa ? "ناموجود" : "Out of stock"}
          </span>
        </div>
      )}

      <Link href={`/${locale}/product/${product.slug}`} className="block">
        <div className="aspect-square bg-[#F5F5F5] relative overflow-hidden">
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
            className="text-[13px] text-[#3F4064] leading-5 mb-2 line-clamp-2 min-h-[40px]"
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
# components/compare/CompareEmpty.tsx
# ============================================================
files.append(("components/compare/CompareEmpty.tsx", """import Link from "next/link";
import { GitCompareArrows } from "lucide-react";
import type { Locale } from "@/lib/types";

interface CompareEmptyProps {
  locale: Locale;
}

export default function CompareEmpty({ locale }: CompareEmptyProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] py-16 px-4 flex flex-col items-center text-center">
      <div className="w-24 h-24 rounded-full bg-[#F5F5F5] flex items-center justify-center mb-5">
        <GitCompareArrows size={44} className="text-[#A1A3A8]" />
      </div>
      <h2 className="text-[18px] font-bold text-[#3F4064] mb-2">
        {isFa ? "لیست مقایسه خالی است" : "Compare list is empty"}
      </h2>
      <p className="text-[13px] text-[#62666D] mb-6 max-w-md">
        {isFa
          ? "برای مقایسه، روی آیکون مقایسه در کارت محصولات کلیک کنید. می‌توانید تا ۴ محصول را همزمان مقایسه کنید."
          : "Click the compare icon on product cards to add them. You can compare up to 4 products at once."}
      </p>
      <Link
        href={`/${locale}`}
        className="bg-[#EF4056] text-white text-[13px] font-medium px-6 py-2.5 rounded-lg hover:bg-[#d63850] transition-colors"
      >
        {isFa ? "مشاهده محصولات" : "Browse products"}
      </Link>
    </div>
  );
}
"""))

# ============================================================
# components/compare/CompareTable.tsx
# ============================================================
files.append(("components/compare/CompareTable.tsx", """"use client";

import Link from "next/link";
import Image from "next/image";
import { X, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useCompareStore } from "@/lib/stores";
import { formatPrice, formatRating } from "@/lib/utils";
import { getBrandById, getCategoryById } from "@/lib/data";
import RatingStars from "@/components/product/RatingStars";

interface CompareTableProps {
  locale: Locale;
  products: Product[];
}

export default function CompareTable({ locale, products }: CompareTableProps) {
  const isFa = locale === "fa";
  const remove = useCompareStore((s) => s.remove);
  const clearAll = useCompareStore((s) => s.clear);
  const addToCart = useCartStore((s) => s.addItem);

  const rows = [
    {
      key: "price",
      labelFa: "قیمت",
      labelEn: "Price",
      render: (p: Product) => (
        <div>
          {p.discountPercent > 0 && (
            <div className="text-[11px] text-[#A1A3A8] line-through">
              {formatPrice(p.price, locale)}
            </div>
          )}
          <div className="text-[13px] font-bold text-[#3F4064]">
            {formatPrice(p.finalPrice, locale)}{" "}
            <span className="text-[10px] text-[#A1A3A8] font-normal">
              {isFa ? "تومان" : "T"}
            </span>
          </div>
        </div>
      ),
    },
    {
      key: "brand",
      labelFa: "برند",
      labelEn: "Brand",
      render: (p: Product) => {
        const brand = getBrandById(p.brand);
        return (
          <span className="text-[12px] text-[#3F4064]">
            {brand ? (isFa ? brand.nameFa : brand.nameEn) : p.brand}
          </span>
        );
      },
    },
    {
      key: "category",
      labelFa: "دسته‌بندی",
      labelEn: "Category",
      render: (p: Product) => {
        const cat = getCategoryById(p.category);
        return (
          <span className="text-[12px] text-[#3F4064]">
            {cat ? (isFa ? cat.nameFa : cat.nameEn) : p.category}
          </span>
        );
      },
    },
    {
      key: "rating",
      labelFa: "امتیاز",
      labelEn: "Rating",
      render: (p: Product) => (
        <div className="flex items-center gap-2">
          <RatingStars rating={p.rating} size={12} />
          <span className="text-[11px] text-[#62666D]">
            {formatRating(p.rating, locale)} (
            {p.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")})
          </span>
        </div>
      ),
    },
    {
      key: "stock",
      labelFa: "وضعیت",
      labelEn: "Status",
      render: (p: Product) => (
        <span
          className={`text-[12px] font-medium ${
            p.inStock ? "text-[#22C55E]" : "text-[#EF4444]"
          }`}
        >
          {p.inStock
            ? isFa
              ? "موجود"
              : "In stock"
            : isFa
            ? "ناموجود"
            : "Out of stock"}
        </span>
      ),
    },
    {
      key: "discount",
      labelFa: "تخفیف",
      labelEn: "Discount",
      render: (p: Product) => (
        <span
          className={`text-[12px] font-medium ${
            p.discountPercent > 0 ? "text-[#EF4056]" : "text-[#A1A3A8]"
          }`}
        >
          {p.discountPercent > 0
            ? `${p.discountPercent.toLocaleString(
                isFa ? "fa-IR" : "en-US"
              )}٪`
            : "—"}
        </span>
      ),
    },
    {
      key: "sku",
      labelFa: "کد محصول",
      labelEn: "SKU",
      render: (p: Product) => (
        <span className="text-[11px] text-[#62666D]" dir="ltr">
          SP-{p.id.toString().padStart(5, "0")}
        </span>
      ),
    },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2]">
        <h2 className="text-[14px] font-bold text-[#3F4064]">
          {isFa
            ? `مقایسه ${products.length} محصول`
            : `Comparing ${products.length} products`}
        </h2>
        <button
          onClick={clearAll}
          className="text-[12px] text-[#EF4056] hover:underline"
        >
          {isFa ? "پاک کردن همه" : "Clear all"}
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[700px]">
          {/* Header: product cards */}
          <thead>
            <tr>
              <th className="w-32 bg-[#FAFAFA] border-b border-[#E0E0E2]"></th>
              {products.map((p) => (
                <th
                  key={p.id}
                  className="p-4 bg-white border-b border-[#E0E0E2] border-l border-[#F5F5F5] align-top"
                >
                  <div className="relative">
                    <button
                      onClick={() => remove(p.id)}
                      aria-label={isFa ? "حذف" : "Remove"}
                      className={`absolute top-0 w-6 h-6 rounded-full bg-white border border-[#E0E0E2] flex items-center justify-center text-[#62666D] hover:text-[#EF4444] hover:border-[#EF4444] transition-colors z-10 ${
                        isFa ? "right-0" : "left-0"
                      }`}
                    >
                      <X size={12} />
                    </button>

                    <Link
                      href={`/${locale}/product/${p.slug}`}
                      className="block"
                    >
                      <div className="w-full aspect-square bg-[#F5F5F5] rounded-lg overflow-hidden relative mb-3">
                        <Image
                          src={p.image}
                          alt={isFa ? p.titleFa : p.titleEn}
                          fill
                          sizes="200px"
                          className="object-cover"
                        />
                      </div>
                      <div className="text-[12px] text-[#3F4064] line-clamp-2 min-h-[40px] hover:text-[#EF4056] transition-colors">
                        {isFa ? p.titleFa : p.titleEn}
                      </div>
                    </Link>

                    <button
                      onClick={() => p.inStock && addToCart(p.id, 1)}
                      disabled={!p.inStock}
                      className={`w-full mt-3 h-8 rounded-lg text-[11px] font-medium flex items-center justify-center gap-1 transition-colors ${
                        p.inStock
                          ? "bg-[#EF4056] text-white hover:bg-[#d63850]"
                          : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
                      }`}
                    >
                      <ShoppingCart size={12} />
                      {isFa ? "افزودن به سبد" : "Add"}
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          {/* Body: comparison rows */}
          <tbody>
            {rows.map((row, rowIdx) => (
              <tr
                key={row.key}
                className={rowIdx % 2 === 0 ? "bg-white" : "bg-[#FAFAFA]"}
              >
                <td className="p-3 text-[12px] text-[#62666D] font-medium border-b border-[#F5F5F5] align-middle">
                  {isFa ? row.labelFa : row.labelEn}
                </td>
                {products.map((p) => (
                  <td
                    key={p.id}
                    className="p-3 border-b border-[#F5F5F5] border-l border-white align-middle"
                  >
                    {row.render(p)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/compare/ComparePage.tsx
# ============================================================
files.append(("components/compare/ComparePage.tsx", """"use client";

import { useState, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCompareStore } from "@/lib/stores";
import { Breadcrumb } from "@/components/common";
import CompareEmpty from "./CompareEmpty";
import CompareTable from "./CompareTable";

interface ComparePageProps {
  locale: Locale;
}

export default function ComparePage({ locale }: ComparePageProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const ids = useCompareStore((s) => s.ids);

  useEffect(() => {
    setMounted(true);
  }, []);

  const items: Product[] = ids
    .map((id) => allProducts.find((p) => p.id === id))
    .filter((p): p is Product => p !== undefined);

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "مقایسه محصولات", labelEn: "Compare" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">
        {isFa ? "مقایسه محصولات" : "Compare Products"}
      </h1>

      {items.length === 0 ? (
        <CompareEmpty locale={locale} />
      ) : (
        <CompareTable locale={locale} products={items} />
      )}
    </div>
  );
}
"""))

# ============================================================
# components/compare/index.ts
# ============================================================
files.append(("components/compare/index.ts", """// components/compare/index.ts
export { default as ComparePage } from "./ComparePage";
export { default as CompareTable } from "./CompareTable";
export { default as CompareEmpty } from "./CompareEmpty";
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
export { default as CompareButton } from "./CompareButton";
export type { FilterValues } from "./ProductFilters";
"""))

# ============================================================
# app/[locale]/compare/page.tsx
# ============================================================
files.append(("app/[locale]/compare/page.tsx", """import type { Locale } from "@/lib/types";
import { ComparePage } from "@/components/compare";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export const metadata = {
  title: "Compare — SourcePixcel",
  description: "Compare products side by side.",
};

export default async function CompareRoute({ params }: PageProps) {
  const { locale } = await params;
  return <ComparePage locale={locale as Locale} />;
}
"""))

# ============================================================
# components/layout/Header.tsx (add compare icon to top bar)
# ============================================================
files.append(("components/layout/Header.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Search,
  ShoppingCart,
  Heart,
  User,
  Menu,
  X,
  ChevronDown,
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
  GitCompareArrows,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { useWishlistStore } from "@/lib/stores";
import { useCompareStore } from "@/lib/stores";

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

interface HeaderProps {
  locale: Locale;
}

export default function Header({ locale }: HeaderProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openCategory, setOpenCategory] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  const totalItems = useCartStore((s) => s.items.reduce((sum, i) => sum + i.quantity, 0));
  const wishlistCount = useWishlistStore((s) => s.ids.length);
  const compareCount = useCompareStore((s) => s.ids.length);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
    setOpenCategory(null);
  }, [pathname]);

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    searchPlaceholder: isFa ? "جستجو در SourcePixcel" : "Search in SourcePixcel",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    wishlist: isFa ? "علاقه‌مندی‌ها" : "Wishlist",
    compare: isFa ? "مقایسه" : "Compare",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
  };

  const swapLocale = (newLocale: Locale) => {
    const rest = pathname.replace(/^\\/(fa|en)/, "");
    return `/${newLocale}${rest}`;
  };

  return (
    <>
      {/* Top thin bar */}
      <div className="bg-white border-b border-[#E0E0E2]">
        <div className="max-w-[1400px] mx-auto px-4 h-10 flex items-center justify-between text-[12px]">
          <div className="flex items-center gap-4">
            <Link
              href={swapLocale(isFa ? "en" : "fa")}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors"
            >
              {isFa ? "English" : "فارسی"}
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href={`/${locale}/auth/login`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors"
            >
              {t.login}
            </Link>
            <span className="text-[#E0E0E2]">|</span>
            <Link
              href={`/${locale}/compare`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <GitCompareArrows size={14} />
              {mounted && compareCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {compareCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/account/wishlist`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <Heart size={14} />
              {mounted && wishlistCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {wishlistCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/cart`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <ShoppingCart size={14} />
              {mounted && totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* Main header row */}
      <div className="bg-white border-b border-[#E0E0E2] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          <button
            className="lg:hidden text-[#3F4064]"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>

          <Link
            href={`/${locale}`}
            className="text-[#EF4056] font-bold text-xl shrink-0"
          >
            SourcePixcel
          </Link>

          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <div className="relative">
              <input
                type="text"
                placeholder={t.searchPlaceholder}
                className="w-full h-10 pr-10 pl-4 rounded-lg bg-[#F5F5F5] border border-[#E0E0E2] text-sm text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] transition-colors"
                style={{ paddingRight: isFa ? 40 : 16, paddingLeft: isFa ? 16 : 40 }}
              />
              <Search
                size={18}
                className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
                style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
              />
            </div>
          </div>

          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} />
            <span>{t.account}</span>
          </Link>

          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2]" />

          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] text-sm hover:text-[#EF4056] transition-colors relative"
          >
            <ShoppingCart size={20} />
            <span>{t.cart}</span>
            {mounted && totalItems > 0 && (
              <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* Mega menu */}
        <div className="hidden lg:block border-t border-[#E0E0E2]">
          <div className="max-w-[1400px] mx-auto px-4">
            <nav className="flex items-center gap-1 h-12">
              {categories.map((cat) => {
                const Icon = ICON_MAP[cat.icon] ?? Cable;
                const isOpen = openCategory === cat.id;
                return (
                  <div
                    key={cat.id}
                    className="relative"
                    onMouseEnter={() => setOpenCategory(cat.id)}
                    onMouseLeave={() => setOpenCategory(null)}
                  >
                    <Link
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                    >
                      <Icon size={16} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      <ChevronDown size={12} className="opacity-50" />
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white border border-[#E0E0E2] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        {cat.subcategories.map((sub) => (
                          <Link
                            key={sub.id}
                            href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                            className="block px-4 py-2 text-[13px] text-[#62666D] hover:bg-[#F5F5F5] hover:text-[#EF4056] transition-colors"
                          >
                            {isFa ? sub.nameFa : sub.nameEn}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-[100] lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
          />
          <div
            className="absolute top-0 bottom-0 bg-white w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button onClick={() => setMobileOpen(false)} aria-label="Close menu">
                <X size={24} className="text-[#3F4064]" />
              </button>
            </div>

            <div className="p-4">
              <div className="relative mb-4">
                <input
                  type="text"
                  placeholder={t.searchPlaceholder}
                  className="w-full h-10 px-4 rounded-lg bg-[#F5F5F5] border border-[#E0E0E2] text-sm"
                />
              </div>

              <div className="mb-4">
                <Link
                  href={`/${locale}/auth/login`}
                  className="block text-center bg-[#EF4056] text-white rounded-lg py-2 text-sm font-medium"
                >
                  {t.login}
                </Link>
              </div>

              <div className="border-t border-[#E0E0E2] pt-4">
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                {categories.map((cat) => {
                  const Icon = ICON_MAP[cat.icon] ?? Cable;
                  return (
                    <Link
                      key={cat.id}
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-3 py-2 text-sm text-[#3F4064] hover:text-[#EF4056]"
                    >
                      <Icon size={18} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 17: Compare")
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
        print("Test:")
        print("  1) Go to /fa, hover a product, click compare icon")
        print("  2) Add 2-4 products")
        print("  3) Go to http://localhost:3000/fa/compare")
        print("\nNext: run 18_dark_mode.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()