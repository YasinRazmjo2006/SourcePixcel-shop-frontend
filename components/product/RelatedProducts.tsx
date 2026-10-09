import type { Locale, Product } from "@/lib/types";
import ProductCard from "./ProductCard";

interface RelatedProductsProps {
  products: Product[];
  locale: Locale;
}

export default function RelatedProducts({
  products,
  locale,
}: RelatedProductsProps) {
  const isFa = locale === "fa";

  if (products.length === 0) return null;

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-4">
        {isFa ? "محصولات مرتبط" : "Related Products"}
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {products.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            locale={locale}
          />
        ))}
      </div>
    </div>
  );
}
