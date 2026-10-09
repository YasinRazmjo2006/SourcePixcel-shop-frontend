# 09_category.py
# ساخت صفحه دسته‌بندی با فیلترها
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/common/Breadcrumb.tsx
# ============================================================
files.append(("components/common/Breadcrumb.tsx", """import Link from "next/link";
import { ChevronLeft, Home } from "lucide-react";
import type { Locale } from "@/lib/types";

interface BreadcrumbItem {
  labelFa: string;
  labelEn: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  locale: Locale;
}

export default function Breadcrumb({ items, locale }: BreadcrumbProps) {
  const isFa = locale === "fa";

  return (
    <nav
      aria-label="Breadcrumb"
      className="flex items-center gap-2 text-[12px] text-[#62666D] py-3 flex-wrap"
    >
      <Link
        href={`/${locale}`}
        className="flex items-center gap-1 hover:text-[#EF4056] transition-colors"
      >
        <Home size={14} />
        <span>{isFa ? "خانه" : "Home"}</span>
      </Link>

      {items.map((item, i) => (
        <div key={i} className="flex items-center gap-2">
          <ChevronLeft
            size={14}
            className={isFa ? "" : "rotate-180"}
          />
          {item.href ? (
            <Link
              href={item.href}
              className="hover:text-[#EF4056] transition-colors"
            >
              {isFa ? item.labelFa : item.labelEn}
            </Link>
          ) : (
            <span className="text-[#3F4064] font-medium">
              {isFa ? item.labelFa : item.labelEn}
            </span>
          )}
        </div>
      ))}
    </nav>
  );
}
"""))

# ============================================================
# components/common/Pagination.tsx
# ============================================================
files.append(("components/common/Pagination.tsx", """"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  locale: Locale;
}

export default function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  locale,
}: PaginationProps) {
  const isFa = locale === "fa";

  if (totalPages <= 1) return null;

  const pages: (number | "...")[] = [];
  const showEllipsis = totalPages > 7;

  if (!showEllipsis) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    pages.push(1);
    if (currentPage > 3) pages.push("...");
    const start = Math.max(2, currentPage - 1);
    const end = Math.min(totalPages - 1, currentPage + 1);
    for (let i = start; i <= end; i++) pages.push(i);
    if (currentPage < totalPages - 2) pages.push("...");
    pages.push(totalPages);
  }

  const fmt = (n: number) =>
    isFa ? n.toLocaleString("fa-IR") : n.toString();

  return (
    <div className="flex items-center justify-center gap-1 mt-6">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
        className="w-9 h-9 rounded-lg border border-[#E0E0E2] bg-white flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {isFa ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {pages.map((p, i) =>
        p === "..." ? (
          <span
            key={`ellipsis-${i}`}
            className="w-9 h-9 flex items-center justify-center text-[#A1A3A8]"
          >
            ...
          </span>
        ) : (
          <button
            key={p}
            onClick={() => onPageChange(p)}
            className={`w-9 h-9 rounded-lg border text-[13px] font-medium transition-colors ${
              p === currentPage
                ? "bg-[#EF4056] text-white border-[#EF4056]"
                : "bg-white text-[#3F4064] border-[#E0E0E2] hover:border-[#EF4056] hover:text-[#EF4056]"
            }`}
          >
            {fmt(p)}
          </button>
        )
      )}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Next page"
        className="w-9 h-9 rounded-lg border border-[#E0E0E2] bg-white flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {isFa ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
      </button>
    </div>
  );
}
"""))

# ============================================================
# components/common/EmptyState.tsx
# ============================================================
files.append(("components/common/EmptyState.tsx", """import { PackageOpen } from "lucide-react";
import Link from "next/link";
import type { Locale } from "@/lib/types";

interface EmptyStateProps {
  locale: Locale;
  titleFa?: string;
  titleEn?: string;
  messageFa?: string;
  messageEn?: string;
}

export default function EmptyState({
  locale,
  titleFa = "محصولی یافت نشد",
  titleEn = "No products found",
  messageFa = "متأسفانه محصولی با فیلترهای انتخابی شما پیدا نشد.",
  messageEn = "Unfortunately, no products match your selected filters.",
}: EmptyStateProps) {
  const isFa = locale === "fa";

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      <div className="w-20 h-20 rounded-full bg-[#F5F5F5] flex items-center justify-center mb-4">
        <PackageOpen size={36} className="text-[#A1A3A8]" />
      </div>
      <h3 className="text-[16px] font-bold text-[#3F4064] mb-2">
        {isFa ? titleFa : titleEn}
      </h3>
      <p className="text-[13px] text-[#62666D] mb-4 max-w-md">
        {isFa ? messageFa : messageEn}
      </p>
      <Link
        href={`/${locale}`}
        className="text-[13px] text-[#EF4056] hover:underline"
      >
        {isFa ? "بازگشت به خانه" : "Back to home"}
      </Link>
    </div>
  );
}
"""))

# ============================================================
# components/common/index.ts
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
"""))

# ============================================================
# components/product/ProductFilters.tsx
# ============================================================
files.append(("components/product/ProductFilters.tsx", """"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, X } from "lucide-react";
import type { Brand, Category, Locale } from "@/lib/types";

export interface FilterValues {
  categoryId: string | null;
  brandIds: string[];
  minPrice: number;
  maxPrice: number;
  inStockOnly: boolean;
  discountedOnly: boolean;
  minRating: number;
}

interface ProductFiltersProps {
  locale: Locale;
  categories: Category[];
  brands: Brand[];
  values: FilterValues;
  onChange: (values: FilterValues) => void;
  maxPriceLimit: number;
}

export default function ProductFilters({
  locale,
  categories,
  brands,
  values,
  onChange,
  maxPriceLimit,
}: ProductFiltersProps) {
  const isFa = locale === "fa";
  const [openSections, setOpenSections] = useState({
    categories: true,
    brands: true,
    price: true,
    availability: true,
    rating: true,
  });

  const toggle = (key: keyof typeof openSections) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const toggleBrand = (brandId: string) => {
    const newBrands = values.brandIds.includes(brandId)
      ? values.brandIds.filter((b) => b !== brandId)
      : [...values.brandIds, brandId];
    onChange({ ...values, brandIds: newBrands });
  };

  const clearAll = () => {
    onChange({
      categoryId: null,
      brandIds: [],
      minPrice: 0,
      maxPrice: maxPriceLimit,
      inStockOnly: false,
      discountedOnly: false,
      minRating: 0,
    });
  };

  const hasActiveFilters =
    values.categoryId !== null ||
    values.brandIds.length > 0 ||
    values.minPrice > 0 ||
    values.maxPrice < maxPriceLimit ||
    values.inStockOnly ||
    values.discountedOnly ||
    values.minRating > 0;

  const t = {
    filters: isFa ? "فیلترها" : "Filters",
    clear: isFa ? "پاک کردن همه" : "Clear all",
    categories: isFa ? "دسته‌بندی" : "Category",
    brands: isFa ? "برند" : "Brand",
    price: isFa ? "محدوده قیمت" : "Price range",
    availability: isFa ? "وضعیت" : "Availability",
    inStockOnly: isFa ? "فقط کالاهای موجود" : "In stock only",
    discountedOnly: isFa ? "فقط کالاهای تخفیف‌دار" : "Discounted only",
    rating: isFa ? "امتیاز" : "Rating",
    andUp: isFa ? "و بالاتر" : "and up",
    from: isFa ? "از" : "From",
    to: isFa ? "تا" : "To",
  };

  const SectionHeader = ({
    title,
    sectionKey,
  }: {
    title: string;
    sectionKey: keyof typeof openSections;
  }) => (
    <button
      onClick={() => toggle(sectionKey)}
      className="w-full flex items-center justify-between py-3 text-[13px] font-bold text-[#3F4064] border-b border-[#E0E0E2]"
    >
      <span>{title}</span>
      {openSections[sectionKey] ? (
        <ChevronUp size={16} />
      ) : (
        <ChevronDown size={16} />
      )}
    </button>
  );

  return (
    <aside className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-[14px] font-bold text-[#3F4064] flex items-center gap-2">
          {t.filters}
        </h2>
        {hasActiveFilters && (
          <button
            onClick={clearAll}
            className="text-[11px] text-[#EF4056] hover:underline flex items-center gap-1"
          >
            <X size={12} />
            {t.clear}
          </button>
        )}
      </div>

      {/* Categories */}
      <div>
        <SectionHeader title={t.categories} sectionKey="categories" />
        {openSections.categories && (
          <ul className="py-2 space-y-1">
            <li>
              <button
                onClick={() => onChange({ ...values, categoryId: null })}
                className={`text-[12px] py-1 transition-colors ${
                  values.categoryId === null
                    ? "text-[#EF4056] font-medium"
                    : "text-[#62666D] hover:text-[#EF4056]"
                }`}
              >
                {isFa ? "همه" : "All"}
              </button>
            </li>
            {categories.map((cat) => (
              <li key={cat.id}>
                <button
                  onClick={() =>
                    onChange({
                      ...values,
                      categoryId:
                        values.categoryId === cat.id ? null : cat.id,
                    })
                  }
                  className={`text-[12px] py-1 transition-colors ${
                    values.categoryId === cat.id
                      ? "text-[#EF4056] font-medium"
                      : "text-[#62666D] hover:text-[#EF4056]"
                  }`}
                >
                  {isFa ? cat.nameFa : cat.nameEn}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Brands */}
      <div>
        <SectionHeader title={t.brands} sectionKey="brands" />
        {openSections.brands && (
          <div className="py-2 space-y-1 max-h-60 overflow-y-auto">
            {brands.map((brand) => (
              <label
                key={brand.id}
                className="flex items-center gap-2 py-1 cursor-pointer group"
              >
                <input
                  type="checkbox"
                  checked={values.brandIds.includes(brand.id)}
                  onChange={() => toggleBrand(brand.id)}
                  className="w-4 h-4 accent-[#EF4056]"
                />
                <span className="text-[12px] text-[#62666D] group-hover:text-[#EF4056] transition-colors">
                  {isFa ? brand.nameFa : brand.nameEn}
                </span>
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Price */}
      <div>
        <SectionHeader title={t.price} sectionKey="price" />
        {openSections.price && (
          <div className="py-3 space-y-3">
            <div className="flex items-center gap-2">
              <div className="flex-1">
                <label className="text-[10px] text-[#A1A3A8] block mb-1">
                  {t.from}
                </label>
                <input
                  type="number"
                  value={values.minPrice}
                  onChange={(e) =>
                    onChange({
                      ...values,
                      minPrice: Number(e.target.value) || 0,
                    })
                  }
                  className="w-full h-8 px-2 rounded border border-[#E0E0E2] text-[12px] focus:outline-none focus:border-[#EF4056]"
                />
              </div>
              <div className="flex-1">
                <label className="text-[10px] text-[#A1A3A8] block mb-1">
                  {t.to}
                </label>
                <input
                  type="number"
                  value={values.maxPrice}
                  onChange={(e) =>
                    onChange({
                      ...values,
                      maxPrice: Number(e.target.value) || maxPriceLimit,
                    })
                  }
                  className="w-full h-8 px-2 rounded border border-[#E0E0E2] text-[12px] focus:outline-none focus:border-[#EF4056]"
                />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Availability */}
      <div>
        <SectionHeader title={t.availability} sectionKey="availability" />
        {openSections.availability && (
          <div className="py-2 space-y-2">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={values.inStockOnly}
                onChange={(e) =>
                  onChange({ ...values, inStockOnly: e.target.checked })
                }
                className="w-4 h-4 accent-[#EF4056]"
              />
              <span className="text-[12px] text-[#62666D]">
                {t.inStockOnly}
              </span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={values.discountedOnly}
                onChange={(e) =>
                  onChange({ ...values, discountedOnly: e.target.checked })
                }
                className="w-4 h-4 accent-[#EF4056]"
              />
              <span className="text-[12px] text-[#62666D]">
                {t.discountedOnly}
              </span>
            </label>
          </div>
        )}
      </div>

      {/* Rating */}
      <div>
        <SectionHeader title={t.rating} sectionKey="rating" />
        {openSections.rating && (
          <div className="py-2 space-y-1">
            {[4, 3, 2, 1].map((r) => (
              <label
                key={r}
                className="flex items-center gap-2 py-1 cursor-pointer"
              >
                <input
                  type="radio"
                  name="rating"
                  checked={values.minRating === r}
                  onChange={() => onChange({ ...values, minRating: r })}
                  className="w-4 h-4 accent-[#EF4056]"
                />
                <span className="text-[12px] text-[#62666D]">
                  {isFa ? r.toLocaleString("fa-IR") : r} ★ {t.andUp}
                </span>
              </label>
            ))}
            <label className="flex items-center gap-2 py-1 cursor-pointer">
              <input
                type="radio"
                name="rating"
                checked={values.minRating === 0}
                onChange={() => onChange({ ...values, minRating: 0 })}
                className="w-4 h-4 accent-[#EF4056]"
              />
              <span className="text-[12px] text-[#62666D]">
                {isFa ? "همه" : "All"}
              </span>
            </label>
          </div>
        )}
      </div>
    </aside>
  );
}
"""))

# ============================================================
# components/product/ProductSort.tsx
# ============================================================
files.append(("components/product/ProductSort.tsx", """import type { Locale, SortOption } from "@/lib/types";

interface ProductSortProps {
  value: SortOption;
  onChange: (value: SortOption) => void;
  locale: Locale;
  resultCount: number;
}

export default function ProductSort({
  value,
  onChange,
  locale,
  resultCount,
}: ProductSortProps) {
  const isFa = locale === "fa";

  const options: { value: SortOption; fa: string; en: string }[] = [
    { value: "popular", fa: "پرفروش‌ترین", en: "Most Popular" },
    { value: "newest", fa: "جدیدترین", en: "Newest" },
    { value: "price-asc", fa: "ارزان‌ترین", en: "Price: Low to High" },
    { value: "price-desc", fa: "گران‌ترین", en: "Price: High to Low" },
    { value: "rating", fa: "محبوب‌ترین", en: "Best Rating" },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-3 flex items-center justify-between gap-4 flex-wrap">
      <span className="text-[12px] text-[#62666D]">
        {isFa
          ? `${resultCount.toLocaleString("fa-IR")} کالا`
          : `${resultCount.toLocaleString("en-US")} products`}
      </span>

      <div className="flex items-center gap-2">
        <span className="text-[12px] text-[#A1A3A8] hidden md:inline">
          {isFa ? "مرتب‌سازی:" : "Sort by:"}
        </span>
        <select
          value={value}
          onChange={(e) => onChange(e.target.value as SortOption)}
          className="h-8 px-2 rounded border border-[#E0E0E2] text-[12px] text-[#3F4064] focus:outline-none focus:border-[#EF4056] bg-white"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {isFa ? opt.fa : opt.en}
            </option>
          ))}
        </select>
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
export type { FilterValues } from "./ProductFilters";
"""))

# ============================================================
# components/category/CategoryPage.tsx (client component with filters)
# ============================================================
files.append(("components/category/CategoryPage.tsx", """"use client";

import { useState, useMemo, useEffect } from "react";
import type { Brand, Category, Locale, Product, SortOption } from "@/lib/types";
import ProductCard from "@/components/product/ProductCard";
import ProductFilters, {
  type FilterValues,
} from "@/components/product/ProductFilters";
import ProductSort from "@/components/product/ProductSort";
import Pagination from "@/components/common/Pagination";
import EmptyState from "@/components/common/EmptyState";
import { SlidersHorizontal, X } from "lucide-react";

interface CategoryPageProps {
  locale: Locale;
  categories: Category[];
  brands: Brand[];
  products: Product[];
  initialCategoryId: string | null;
}

const PER_PAGE = 12;

export default function CategoryPage({
  locale,
  categories,
  brands,
  products,
  initialCategoryId,
}: CategoryPageProps) {
  const isFa = locale === "fa";
  const maxPriceLimit = useMemo(
    () => Math.max(...products.map((p) => p.finalPrice), 0),
    [products]
  );

  const [filters, setFilters] = useState<FilterValues>({
    categoryId: initialCategoryId,
    brandIds: [],
    minPrice: 0,
    maxPrice: maxPriceLimit,
    inStockOnly: false,
    discountedOnly: false,
    minRating: 0,
  });

  const [sort, setSort] = useState<SortOption>("popular");
  const [page, setPage] = useState(1);
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);

  // Reset to page 1 when filters/sort change
  useEffect(() => {
    setPage(1);
  }, [filters, sort]);

  const filtered = useMemo(() => {
    let result = [...products];

    if (filters.categoryId) {
      result = result.filter((p) => p.category === filters.categoryId);
    }
    if (filters.brandIds.length > 0) {
      result = result.filter((p) => filters.brandIds.includes(p.brand));
    }
    result = result.filter(
      (p) =>
        p.finalPrice >= filters.minPrice && p.finalPrice <= filters.maxPrice
    );
    if (filters.inStockOnly) {
      result = result.filter((p) => p.inStock);
    }
    if (filters.discountedOnly) {
      result = result.filter((p) => p.discountPercent > 0);
    }
    if (filters.minRating > 0) {
      result = result.filter((p) => p.rating >= filters.minRating);
    }

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
      case "popular":
      default:
        result.sort((a, b) => b.reviewCount - a.reviewCount);
    }

    return result;
  }, [products, filters, sort]);

  const totalPages = Math.ceil(filtered.length / PER_PAGE);
  const paginated = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const handlePageChange = (newPage: number) => {
    setPage(newPage);
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <div className="flex gap-4">
        {/* Desktop sidebar */}
        <div className="hidden lg:block w-64 shrink-0">
          <ProductFilters
            locale={locale}
            categories={categories}
            brands={brands}
            values={filters}
            onChange={setFilters}
            maxPriceLimit={maxPriceLimit}
          />
        </div>

        {/* Main */}
        <div className="flex-1 min-w-0 space-y-3">
          {/* Mobile filter button */}
          <div className="lg:hidden">
            <button
              onClick={() => setMobileFiltersOpen(true)}
              className="w-full bg-white rounded-lg border border-[#E0E0E2] py-2.5 flex items-center justify-center gap-2 text-[13px] text-[#3F4064]"
            >
              <SlidersHorizontal size={16} />
              {isFa ? "فیلترها" : "Filters"}
            </button>
          </div>

          <ProductSort
            value={sort}
            onChange={setSort}
            locale={locale}
            resultCount={filtered.length}
          />

          {paginated.length === 0 ? (
            <div className="bg-white rounded-lg border border-[#E0E0E2]">
              <EmptyState locale={locale} />
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                {paginated.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    locale={locale}
                  />
                ))}
              </div>

              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={handlePageChange}
                locale={locale}
              />
            </>
          )}
        </div>
      </div>

      {/* Mobile filter drawer */}
      {mobileFiltersOpen && (
        <div className="fixed inset-0 z-[100] lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileFiltersOpen(false)}
          />
          <div
            className="absolute top-0 bottom-0 bg-[#F5F5F5] w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] bg-white sticky top-0 z-10">
              <span className="text-[14px] font-bold text-[#3F4064]">
                {isFa ? "فیلترها" : "Filters"}
              </span>
              <button
                onClick={() => setMobileFiltersOpen(false)}
                aria-label="Close filters"
              >
                <X size={20} className="text-[#3F4064]" />
              </button>
            </div>
            <div className="p-3">
              <ProductFilters
                locale={locale}
                categories={categories}
                brands={brands}
                values={filters}
                onChange={setFilters}
                maxPriceLimit={maxPriceLimit}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/category/index.ts
# ============================================================
files.append(("components/category/index.ts", """// components/category/index.ts
export { default as CategoryPage } from "./CategoryPage";
"""))

# ============================================================
# app/[locale]/category/[slug]/page.tsx
# ============================================================
files.append(("app/[locale]/category/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Locale } from "@/lib/types";
import { categories, brands, products } from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";
import { CategoryPage } from "@/components/category";

interface PageProps {
  params: Promise<{ locale: string; slug: string }>;
}

export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    categories.map((cat) => ({ locale, slug: cat.slug }))
  );
}

export default async function CategoryListingPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const category = categories.find((c) => c.slug === slug);
  if (!category) notFound();

  const isFa = typedLocale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4">
      <Breadcrumb
        locale={typedLocale}
        items={[
          {
            labelFa: "دسته‌بندی‌ها",
            labelEn: "Categories",
            href: `/${typedLocale}/categories`,
          },
          {
            labelFa: category.nameFa,
            labelEn: category.nameEn,
          },
        ]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">
        {isFa ? category.nameFa : category.nameEn}
      </h1>

      <CategoryPage
        locale={typedLocale}
        categories={categories}
        brands={brands}
        products={products}
        initialCategoryId={category.id}
      />
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/categories/page.tsx (all categories listing)
# ============================================================
files.append(("app/[locale]/categories/page.tsx", """import Link from "next/link";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CategoriesPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={typedLocale}
        items={[{ labelFa: "دسته‌بندی‌ها", labelEn: "Categories" }]}
      />

      <h1 className="text-[22px] font-bold text-[#3F4064] mb-6">
        {isFa ? "همه دسته‌بندی‌ها" : "All Categories"}
      </h1>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {categories.map((cat) => (
          <Link
            key={cat.id}
            href={`/${typedLocale}/category/${cat.slug}`}
            className="bg-white rounded-lg border border-[#E0E0E2] p-4 hover:shadow-md transition-shadow"
          >
            <h3 className="text-[14px] font-bold text-[#3F4064] mb-3">
              {isFa ? cat.nameFa : cat.nameEn}
            </h3>
            <ul className="space-y-1">
              {cat.subcategories.map((sub) => (
                <li
                  key={sub.id}
                  className="text-[12px] text-[#62666D] hover:text-[#EF4056] transition-colors"
                >
                  {isFa ? sub.nameFa : sub.nameEn}
                </li>
              ))}
            </ul>
          </Link>
        ))}
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
    print("SourcePixcel — Step 09: Category Page")
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
        print("Open: http://localhost:3000/fa/categories")
        print("      http://localhost:3000/fa/category/mobile")
        print("\nNext: run 10_product_detail.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()