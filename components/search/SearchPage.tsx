"use client";

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
