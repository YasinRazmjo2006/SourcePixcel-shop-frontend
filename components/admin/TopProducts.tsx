import Image from "next/image";
import { products } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface TopProductsProps {
  locale: string;
}

export default function TopProducts({ locale }: TopProductsProps) {
  const isFa = locale === "fa";
  const top = products.slice(0, 5);

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
        {isFa ? "پرفروش‌ترین محصولات" : "Top Selling Products"}
      </h3>

      <div className="space-y-3">
        {top.map((product, i) => (
          <div key={product.id} className="flex items-center gap-3">
            <div className="w-6 h-6 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center text-[11px] font-bold text-[#62666D] dark:text-[#A1A3A8] shrink-0">
              {isFa ? (i + 1).toLocaleString("fa-IR") : i + 1}
            </div>
            <div className="w-10 h-10 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
              <Image
                src={product.image}
                alt={isFa ? product.titleFa : product.titleEn}
                fill
                sizes="40px"
                className="object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 font-medium">
                {isFa ? product.titleFa : product.titleEn}
              </div>
              <div className="text-[10px] text-[#A1A3A8]">
                {product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
                {isFa ? "فروش" : "sales"}
              </div>
            </div>
            <div className="text-[11px] font-bold text-[#EF4056] shrink-0">
              {formatPrice(product.finalPrice, isFa ? "fa" : "en")}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
