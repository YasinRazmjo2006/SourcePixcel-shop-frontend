import type { Locale, SortOption } from "@/lib/types";

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
