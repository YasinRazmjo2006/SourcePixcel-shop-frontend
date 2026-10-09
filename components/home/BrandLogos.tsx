import type { Locale } from "@/lib/types";
import { brands } from "@/lib/data";

interface BrandLogosProps {
  locale: Locale;
}

export default function BrandLogos({ locale }: BrandLogosProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-4">
        {isFa ? "برندهای محبوب" : "Popular Brands"}
      </h2>
      <div className="grid grid-cols-3 md:grid-cols-5 lg:grid-cols-8 gap-3">
        {brands.slice(0, 16).map((brand) => (
          <div
            key={brand.id}
            className="aspect-square rounded-lg bg-[#F5F5F5] flex items-center justify-center p-2 hover:bg-[#EF4056]/5 transition-colors cursor-pointer"
          >
            <span className="text-[11px] md:text-[12px] text-[#62666D] font-medium text-center">
              {isFa ? brand.nameFa : brand.nameEn}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
