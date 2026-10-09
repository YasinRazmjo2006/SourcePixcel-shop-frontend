"use client";

import Link from "next/link";
import Image from "next/image";
import { Trash2, Plus, Minus, Heart, Store } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore } from "@/lib/stores";
import { formatPrice } from "@/lib/utils";
import { getBrandById } from "@/lib/data";

interface CartLineProps {
  product: Product;
  quantity: number;
  locale: Locale;
}

export default function CartLine({ product, quantity, locale }: CartLineProps) {
  const isFa = locale === "fa";
  const updateQuantity = useCartStore((s) => s.updateQuantity);
  const removeItem = useCartStore((s) => s.removeItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);

  const brand = getBrandById(product.brand);
  const title = isFa ? product.titleFa : product.titleEn;
  const lineTotal = product.finalPrice * quantity;
  const lineOriginal = product.price * quantity;

  const dec = () => updateQuantity(product.id, quantity - 1);
  const inc = () => updateQuantity(product.id, quantity + 1);
  const remove = () => removeItem(product.id);

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 flex gap-4">
      {/* Image */}
      <Link
        href={`/${locale}/product/${product.slug}`}
        className="w-20 h-20 md:w-28 md:h-28 shrink-0 rounded-lg bg-[#F5F5F5] overflow-hidden relative"
      >
        <Image
          src={product.image}
          alt={title}
          fill
          sizes="120px"
          className="object-cover"
        />
      </Link>

      {/* Info */}
      <div className="flex-1 min-w-0 flex flex-col">
        <div className="flex items-start justify-between gap-3">
          <Link
            href={`/${locale}/product/${product.slug}`}
            className="text-[13px] md:text-[14px] text-[#3F4064] leading-5 line-clamp-2 hover:text-[#EF4056] transition-colors"
          >
            {title}
          </Link>

          <button
            onClick={remove}
            aria-label={isFa ? "حذف" : "Remove"}
            className="text-[#A1A3A8] hover:text-[#EF4444] transition-colors shrink-0"
          >
            <Trash2 size={16} />
          </button>
        </div>

        {/* Brand */}
        {brand && (
          <div className="flex items-center gap-1 text-[11px] text-[#A1A3A8] mt-1">
            <Store size={11} />
            <span>{isFa ? brand.nameFa : brand.nameEn}</span>
          </div>
        )}

        {/* Actions row */}
        <div className="flex items-end justify-between gap-3 mt-auto pt-3">
          {/* Quantity */}
          <div className="flex items-center gap-2 border border-[#E0E0E2] rounded-lg">
            <button
              onClick={inc}
              aria-label="Increase"
              className="w-7 h-7 flex items-center justify-center text-[#EF4056] hover:bg-[#F5F5F5] rounded-r-lg transition-colors"
            >
              <Plus size={14} />
            </button>
            <span className="w-6 text-center text-[13px] font-bold text-[#3F4064] tabular-nums">
              {isFa ? quantity.toLocaleString("fa-IR") : quantity}
            </span>
            <button
              onClick={dec}
              aria-label="Decrease"
              className="w-7 h-7 flex items-center justify-center text-[#EF4056] hover:bg-[#F5F5F5] rounded-l-lg transition-colors"
            >
              <Minus size={14} />
            </button>
          </div>

          {/* Price */}
          <div className="text-right">
            {product.discountPercent > 0 && (
              <div className="text-[11px] text-[#A1A3A8] line-through">
                {formatPrice(lineOriginal, locale)}
              </div>
            )}
            <div className="flex items-center gap-1">
              <span className="text-[14px] md:text-[15px] font-bold text-[#3F4064]">
                {formatPrice(lineTotal, locale)}
              </span>
              <span className="text-[10px] text-[#62666D]">
                {isFa ? "تومان" : "Toman"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
