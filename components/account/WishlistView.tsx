"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useWishlistStore } from "@/lib/stores";
import ProductCard from "@/components/product/ProductCard";
import { EmptyState } from "@/components/common";

interface WishlistViewProps {
  locale: Locale;
}

export default function WishlistView({ locale }: WishlistViewProps) {
  const isFa = locale === "fa";
  const ids = useWishlistStore((s) => s.ids);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const items: Product[] = ids
    .map((id) => allProducts.find((p) => p.id === id))
    .filter((p): p is Product => p !== undefined);

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="space-y-3">
        <h1 className="text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "علاقه‌مندی‌ها" : "Wishlist"}
        </h1>
        <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
          <EmptyState
            locale={locale}
            type="wishlist"
            titleFa="لیست علاقه‌مندی‌ها خالی است"
            titleEn="Your wishlist is empty"
            messageFa="محصولات مورد علاقه خود را با کلیک روی آیکون قلب اضافه کنید و بعداً به راحتی به سبد خرید اضافه کنید."
            messageEn="Add products to your wishlist by clicking the heart icon, and easily add them to your cart later."
            actionLabelFa="مشاهده محصولات"
            actionLabelEn="Browse products"
            actionHref={`/${locale}`}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "علاقه‌مندی‌ها" : "Wishlist"}
        </h1>
        <span className="text-[12px] text-[#A1A3A8]">
          {isFa
            ? `${items.length.toLocaleString("fa-IR")} کالا`
            : `${items.length} items`}
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {items.map((product, i) => (
          <motion.div
            key={product.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.04 }}
          >
            <ProductCard product={product} locale={locale} />
          </motion.div>
        ))}
      </div>
    </div>
  );
}
