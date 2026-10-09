"use client";

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
