"use client";

import Link from "next/link";
import Image from "next/image";
import { X, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useCompareStore } from "@/lib/stores";
import { formatPrice, formatRating } from "@/lib/utils";
import { getBrandById, getCategoryById } from "@/lib/data";
import RatingStars from "@/components/product/RatingStars";

interface CompareTableProps {
  locale: Locale;
  products: Product[];
}

export default function CompareTable({ locale, products }: CompareTableProps) {
  const isFa = locale === "fa";
  const remove = useCompareStore((s) => s.remove);
  const clearAll = useCompareStore((s) => s.clear);
  const addToCart = useCartStore((s) => s.addItem);

  const rows = [
    {
      key: "price",
      labelFa: "قیمت",
      labelEn: "Price",
      render: (p: Product) => (
        <div>
          {p.discountPercent > 0 && (
            <div className="text-[11px] text-[#A1A3A8] line-through">
              {formatPrice(p.price, locale)}
            </div>
          )}
          <div className="text-[13px] font-bold text-[#3F4064]">
            {formatPrice(p.finalPrice, locale)}{" "}
            <span className="text-[10px] text-[#A1A3A8] font-normal">
              {isFa ? "تومان" : "T"}
            </span>
          </div>
        </div>
      ),
    },
    {
      key: "brand",
      labelFa: "برند",
      labelEn: "Brand",
      render: (p: Product) => {
        const brand = getBrandById(p.brand);
        return (
          <span className="text-[12px] text-[#3F4064]">
            {brand ? (isFa ? brand.nameFa : brand.nameEn) : p.brand}
          </span>
        );
      },
    },
    {
      key: "category",
      labelFa: "دسته‌بندی",
      labelEn: "Category",
      render: (p: Product) => {
        const cat = getCategoryById(p.category);
        return (
          <span className="text-[12px] text-[#3F4064]">
            {cat ? (isFa ? cat.nameFa : cat.nameEn) : p.category}
          </span>
        );
      },
    },
    {
      key: "rating",
      labelFa: "امتیاز",
      labelEn: "Rating",
      render: (p: Product) => (
        <div className="flex items-center gap-2">
          <RatingStars rating={p.rating} size={12} />
          <span className="text-[11px] text-[#62666D]">
            {formatRating(p.rating, locale)} (
            {p.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")})
          </span>
        </div>
      ),
    },
    {
      key: "stock",
      labelFa: "وضعیت",
      labelEn: "Status",
      render: (p: Product) => (
        <span
          className={`text-[12px] font-medium ${
            p.inStock ? "text-[#22C55E]" : "text-[#EF4444]"
          }`}
        >
          {p.inStock
            ? isFa
              ? "موجود"
              : "In stock"
            : isFa
            ? "ناموجود"
            : "Out of stock"}
        </span>
      ),
    },
    {
      key: "discount",
      labelFa: "تخفیف",
      labelEn: "Discount",
      render: (p: Product) => (
        <span
          className={`text-[12px] font-medium ${
            p.discountPercent > 0 ? "text-[#EF4056]" : "text-[#A1A3A8]"
          }`}
        >
          {p.discountPercent > 0
            ? `${p.discountPercent.toLocaleString(
                isFa ? "fa-IR" : "en-US"
              )}٪`
            : "—"}
        </span>
      ),
    },
    {
      key: "sku",
      labelFa: "کد محصول",
      labelEn: "SKU",
      render: (p: Product) => (
        <span className="text-[11px] text-[#62666D]" dir="ltr">
          SP-{p.id.toString().padStart(5, "0")}
        </span>
      ),
    },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] overflow-hidden">
      <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2]">
        <h2 className="text-[14px] font-bold text-[#3F4064]">
          {isFa
            ? `مقایسه ${products.length} محصول`
            : `Comparing ${products.length} products`}
        </h2>
        <button
          onClick={clearAll}
          className="text-[12px] text-[#EF4056] hover:underline"
        >
          {isFa ? "پاک کردن همه" : "Clear all"}
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[700px]">
          {/* Header: product cards */}
          <thead>
            <tr>
              <th className="w-32 bg-[#FAFAFA] border-b border-[#E0E0E2]"></th>
              {products.map((p) => (
                <th
                  key={p.id}
                  className="p-4 bg-white border-b border-[#E0E0E2] border-l border-[#F5F5F5] align-top"
                >
                  <div className="relative">
                    <button
                      onClick={() => remove(p.id)}
                      aria-label={isFa ? "حذف" : "Remove"}
                      className={`absolute top-0 w-6 h-6 rounded-full bg-white border border-[#E0E0E2] flex items-center justify-center text-[#62666D] hover:text-[#EF4444] hover:border-[#EF4444] transition-colors z-10 ${
                        isFa ? "right-0" : "left-0"
                      }`}
                    >
                      <X size={12} />
                    </button>

                    <Link
                      href={`/${locale}/product/${p.slug}`}
                      className="block"
                    >
                      <div className="w-full aspect-square bg-[#F5F5F5] rounded-lg overflow-hidden relative mb-3">
                        <Image
                          src={p.image}
                          alt={isFa ? p.titleFa : p.titleEn}
                          fill
                          sizes="200px"
                          className="object-cover"
                        />
                      </div>
                      <div className="text-[12px] text-[#3F4064] line-clamp-2 min-h-[40px] hover:text-[#EF4056] transition-colors">
                        {isFa ? p.titleFa : p.titleEn}
                      </div>
                    </Link>

                    <button
                      onClick={() => p.inStock && addToCart(p.id, 1)}
                      disabled={!p.inStock}
                      className={`w-full mt-3 h-8 rounded-lg text-[11px] font-medium flex items-center justify-center gap-1 transition-colors ${
                        p.inStock
                          ? "bg-[#EF4056] text-white hover:bg-[#d63850]"
                          : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
                      }`}
                    >
                      <ShoppingCart size={12} />
                      {isFa ? "افزودن به سبد" : "Add"}
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          {/* Body: comparison rows */}
          <tbody>
            {rows.map((row, rowIdx) => (
              <tr
                key={row.key}
                className={rowIdx % 2 === 0 ? "bg-white" : "bg-[#FAFAFA]"}
              >
                <td className="p-3 text-[12px] text-[#62666D] font-medium border-b border-[#F5F5F5] align-middle">
                  {isFa ? row.labelFa : row.labelEn}
                </td>
                {products.map((p) => (
                  <td
                    key={p.id}
                    className="p-3 border-b border-[#F5F5F5] border-l border-white align-middle"
                  >
                    {row.render(p)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
