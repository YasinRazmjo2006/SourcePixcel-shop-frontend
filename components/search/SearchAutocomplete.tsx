"use client";

import { useState, useEffect, useRef, useMemo } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { Search, X, TrendingUp, ArrowLeft, ArrowRight, Loader2 } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts, categories } from "@/lib/data";

interface SearchAutocompleteProps {
  locale: Locale;
  onClose?: () => void;
}

const MAX_RESULTS = 6;
const DEBOUNCE_MS = 200;

export default function SearchAutocomplete({
  locale,
  onClose,
}: SearchAutocompleteProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const wrapperRef = useRef<HTMLDivElement>(null);

  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);

  // Debounce
  useEffect(() => {
    if (query === debouncedQuery) return;
    setIsLoading(true);
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
      setIsLoading(false);
    }, DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [query, debouncedQuery]);

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Filter products
  const results = useMemo(() => {
    const q = debouncedQuery.toLowerCase().trim();
    if (!q) return [];
    return allProducts
      .filter((p) => {
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
      })
      .slice(0, MAX_RESULTS);
  }, [debouncedQuery]);

  // Match categories
  const matchedCategories = useMemo(() => {
    const q = debouncedQuery.toLowerCase().trim();
    if (!q || q.length < 2) return [];
    return categories
      .filter(
        (c) =>
          c.nameFa.toLowerCase().includes(q) ||
          c.nameEn.toLowerCase().includes(q)
      )
      .slice(0, 3);
  }, [debouncedQuery]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!query.trim()) return;
    setIsOpen(false);
    onClose?.();
    router.push(`/${locale}/search?q=${encodeURIComponent(query.trim())}`);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen || results.length === 0) {
      if (e.key === "Enter") handleSubmit();
      return;
    }

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightedIndex((prev) => (prev + 1) % results.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightedIndex((prev) =>
        prev <= 0 ? results.length - 1 : prev - 1
      );
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (highlightedIndex >= 0 && results[highlightedIndex]) {
        router.push(`/${locale}/product/${results[highlightedIndex].slug}`);
        setIsOpen(false);
        onClose?.();
      } else {
        handleSubmit();
      }
    } else if (e.key === "Escape") {
      setIsOpen(false);
    }
  };

  const clearQuery = () => {
    setQuery("");
    setDebouncedQuery("");
    setHighlightedIndex(-1);
  };

  const showDropdown =
    isOpen && (query.trim().length > 0);

  return (
    <div ref={wrapperRef} className="relative w-full">
      <form onSubmit={handleSubmit}>
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setIsOpen(true);
              setHighlightedIndex(-1);
            }}
            onFocus={() => setIsOpen(true)}
            onKeyDown={handleKeyDown}
            placeholder={isFa ? "جستجو در SourcePixcel" : "Search in SourcePixcel"}
            className="w-full h-10 md:h-11 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[13px] md:text-[14px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] focus:bg-white dark:focus:bg-[#1A1A1E] transition-colors"
            style={{
              paddingRight: isFa ? 80 : 16,
              paddingLeft: isFa ? 16 : 80,
            }}
          />
          <div
            className="absolute top-1/2 -translate-y-1/2 flex items-center gap-1"
            style={{ [isFa ? "left" : "right"]: 8 } as React.CSSProperties}
          >
            {isLoading && query !== debouncedQuery && (
              <Loader2 size={16} className="text-[#A1A3A8] animate-spin" />
            )}
            {query && !isLoading && (
              <button
                type="button"
                onClick={clearQuery}
                aria-label="Clear"
                className="w-7 h-7 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#3A3A40] transition-colors"
              >
                <X size={14} />
              </button>
            )}
            <button
              type="submit"
              aria-label="Search"
              className="w-8 h-8 rounded-lg bg-[#EF4056] text-white flex items-center justify-center hover:bg-[#d63850] transition-colors"
            >
              <Search size={15} />
            </button>
          </div>
        </div>
      </form>

      {/* Dropdown */}
      {showDropdown && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] shadow-2xl overflow-hidden z-50 max-h-[500px] overflow-y-auto">
          {/* Loading */}
          {isLoading && results.length === 0 && (
            <div className="p-6 text-center">
              <Loader2
                size={24}
                className="text-[#EF4056] animate-spin mx-auto mb-2"
              />
              <p className="text-[12px] text-[#A1A3A8]">
                {isFa ? "در حال جستجو..." : "Searching..."}
              </p>
            </div>
          )}

          {/* No results */}
          {!isLoading && results.length === 0 && debouncedQuery.trim() && (
            <div className="p-6 text-center">
              <div className="w-12 h-12 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
                <Search size={22} className="text-[#A1A3A8]" />
              </div>
              <p className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] font-medium mb-1">
                {isFa ? "نتیجه‌ای یافت نشد" : "No results found"}
              </p>
              <p className="text-[11px] text-[#A1A3A8]">
                {isFa
                  ? "عبارت دیگری را امتحان کنید"
                  : "Try a different keyword"}
              </p>
            </div>
          )}

          {/* Categories */}
          {matchedCategories.length > 0 && (
            <div className="border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <div className="px-4 py-2 text-[10px] font-bold text-[#A1A3A8] uppercase tracking-wider">
                {isFa ? "دسته‌بندی‌ها" : "Categories"}
              </div>
              <div className="flex flex-wrap gap-2 px-4 pb-3">
                {matchedCategories.map((cat) => (
                  <Link
                    key={cat.id}
                    href={`/${locale}/category/${cat.slug}`}
                    onClick={() => {
                      setIsOpen(false);
                      onClose?.();
                    }}
                    className="text-[11px] bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#3F4064] dark:text-[#E5E5EA] px-3 py-1.5 rounded-full hover:bg-[#EF4056] hover:text-white transition-colors"
                  >
                    {isFa ? cat.nameFa : cat.nameEn}
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* Products */}
          {results.length > 0 && (
            <div>
              <div className="px-4 py-2 text-[10px] font-bold text-[#A1A3A8] uppercase tracking-wider flex items-center gap-1">
                <TrendingUp size={11} />
                {isFa ? "محصولات" : "Products"}
              </div>
              {results.map((product, idx) => {
                const isHighlighted = idx === highlightedIndex;
                return (
                  <Link
                    key={product.id}
                    href={`/${locale}/product/${product.slug}`}
                    onClick={() => {
                      setIsOpen(false);
                      onClose?.();
                    }}
                    onMouseEnter={() => setHighlightedIndex(idx)}
                    className={`flex items-center gap-3 px-4 py-2.5 transition-colors ${
                      isHighlighted
                        ? "bg-[#EF4056]/5"
                        : "hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
                    }`}
                  >
                    <div className="w-12 h-12 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
                      <Image
                        src={product.image}
                        alt={isFa ? product.titleFa : product.titleEn}
                        fill
                        sizes="48px"
                        className="object-cover"
                      />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 font-medium">
                        {isFa ? product.titleFa : product.titleEn}
                      </div>
                      <div className="text-[11px] text-[#EF4056] font-bold mt-0.5">
                        {product.finalPrice.toLocaleString(
                          isFa ? "fa-IR" : "en-US"
                        )}{" "}
                        <span className="text-[10px] text-[#A1A3A8] font-normal">
                          {isFa ? "تومان" : "T"}
                        </span>
                      </div>
                    </div>
                    {isFa ? (
                      <ArrowLeft
                        size={14}
                        className="text-[#A1A3A8] shrink-0"
                      />
                    ) : (
                      <ArrowRight
                        size={14}
                        className="text-[#A1A3A8] shrink-0"
                      />
                    )}
                  </Link>
                );
              })}
            </div>
          )}

          {/* See all */}
          {query.trim() && (
            <button
              onClick={() => handleSubmit()}
              className="w-full border-t border-[#E0E0E2] dark:border-[#2A2A2E] px-4 py-3 text-[12px] text-[#EF4056] font-medium hover:bg-[#EF4056]/5 transition-colors flex items-center justify-center gap-2"
            >
              <Search size={13} />
              {isFa
                ? `مشاهده همه نتایج برای "${query}"`
                : `See all results for "${query}"`}
            </button>
          )}
        </div>
      )}
    </div>
  );
}
