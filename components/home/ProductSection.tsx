import Link from "next/link";
import { ChevronLeft } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import ProductCard from "@/components/product/ProductCard";
import { StaggerList, StaggerItem } from "@/components/motion";

interface ProductSectionProps {
  titleFa: string;
  titleEn: string;
  products: Product[];
  locale: Locale;
  seeAllHref?: string;
}

export default function ProductSection({
  titleFa,
  titleEn,
  products,
  locale,
  seeAllHref,
}: ProductSectionProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? titleFa : titleEn}
        </h2>
        {seeAllHref && (
          <Link
            href={`/${locale}${seeAllHref}`}
            className="text-[12px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors"
          >
            {isFa ? "مشاهده همه" : "See all"}
            <ChevronLeft
              size={14}
              className={isFa ? "" : "rotate-180"}
            />
          </Link>
        )}
      </div>

      <StaggerList className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
        {products.map((product) => (
          <StaggerItem key={product.id}>
            <ProductCard product={product} locale={locale} />
          </StaggerItem>
        ))}
      </StaggerList>
    </div>
  );
}
