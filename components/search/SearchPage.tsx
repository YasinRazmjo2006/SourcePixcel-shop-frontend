"use client";

import { useState, useMemo, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Search as SearchIcon, X } from "lucide-react";
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
  };

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "جستجو", labelEn: "Search" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">{t.title}</h1>

      {/* Search input */}
      <form onSubmit={handleSubmit} className="mb-5">
        <div className="relative max-w-2xl">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={t.placeholder}
            autoFocus
            className="w-full h-12 rounded-lg bg-white border border-[#E0E0E2] text-[14px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] transition-colors"
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
              <button
                type="button"
                onClick={clearSearch}
                aria-label={t.clear}
                className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5]"
              >
                <X size={16} />
              </button>
            )}
            <button
              type="submit"
              className="h-9 px-3 rounded-lg bg-[#EF4056] text-white flex items-center justify-center hover:bg-[#d63850] transition-colors"
            >
              <SearchIcon size={16} />
            </button>
          </div>
        </div>
      </form>

      {/* No query */}
      {!query && (
        <div className="bg-white rounded-lg border border-[#E0E0E2] py-16 px-4 text-center">
          <div className="w-16 h-16 rounded-full bg-[#F5F5F5] flex items-center justify-center mx-auto mb-4">
            <SearchIcon size={28} className="text-[#A1A3A8]" />
          </div>
          <p className="text-[13px] text-[#62666D] max-w-md mx-auto">
            {t.hint}
          </p>
        </div>
      )}

      {/* Results */}
      {query && (
        <>
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <h2 className="text-[14px] text-[#62666D]">
              {t.resultsFor}{" "}
              <span className="font-bold text-[#3F4064]">"{query}"</span>
            </h2>
          </div>

          {paginated.length === 0 ? (
            <div className="bg-white rounded-lg border border-[#E0E0E2]">
              <EmptyState
                locale={locale}
                titleFa="نتیجه‌ای یافت نشد"
                titleEn="No results found"
                messageFa="متأسفانه محصولی با این عبارت پیدا نشد. عبارت دیگری را امتحان کنید."
                messageEn="No products matched your search. Try another keyword."
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
