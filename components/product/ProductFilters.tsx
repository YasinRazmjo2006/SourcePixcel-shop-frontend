"use client";

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
