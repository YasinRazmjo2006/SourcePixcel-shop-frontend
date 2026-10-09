# 07_product_card.py
# ساخت کامپوننت‌های محصول
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/product/RatingStars.tsx
# ============================================================
files.append(("components/product/RatingStars.tsx", """import { Star } from "lucide-react";

interface RatingStarsProps {
  rating: number;
  size?: number;
  showValue?: boolean;
}

export default function RatingStars({
  rating,
  size = 12,
  showValue = false,
}: RatingStarsProps) {
  const full = Math.floor(rating);
  const hasHalf = rating - full >= 0.5;
  const empty = 5 - full - (hasHalf ? 1 : 0);

  return (
    <div className="flex items-center gap-1">
      <div className="flex items-center gap-[1px]">
        {Array.from({ length: full }).map((_, i) => (
          <Star
            key={`full-${i}`}
            size={size}
            className="fill-[#F9A825] text-[#F9A825]"
          />
        ))}
        {hasHalf && (
          <div className="relative" style={{ width: size, height: size }}>
            <Star size={size} className="text-[#E0E0E2] absolute inset-0" />
            <div
              className="absolute inset-0 overflow-hidden"
              style={{ width: size / 2 }}
            >
              <Star
                size={size}
                className="fill-[#F9A825] text-[#F9A825]"
              />
            </div>
          </div>
        )}
        {Array.from({ length: empty }).map((_, i) => (
          <Star key={`empty-${i}`} size={size} className="text-[#E0E0E2]" />
        ))}
      </div>
      {showValue && (
        <span className="text-[11px] text-[#A1A3A8] mr-1">
          {rating.toFixed(1)}
        </span>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/product/PriceTag.tsx
# ============================================================
files.append(("components/product/PriceTag.tsx", """import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

interface PriceTagProps {
  price: number;
  finalPrice: number;
  discountPercent: number;
  locale: Locale;
  size?: "sm" | "md" | "lg";
}

export default function PriceTag({
  price,
  finalPrice,
  discountPercent,
  locale,
  size = "md",
}: PriceTagProps) {
  const isFa = locale === "fa";
  const hasDiscount = discountPercent > 0;

  const sizeClasses = {
    sm: { price: "text-[13px]", old: "text-[10px]", badge: "text-[10px] px-1" },
    md: { price: "text-[15px]", old: "text-[11px]", badge: "text-[11px] px-1.5" },
    lg: { price: "text-[20px]", old: "text-[13px]", badge: "text-[12px] px-2" },
  }[size];

  return (
    <div className="flex flex-col items-start gap-1">
      {hasDiscount && (
        <div className="flex items-center gap-2">
          <span
            className={`${sizeClasses.badge} bg-[#EF4056] text-white rounded font-bold`}
          >
            {discountPercent.toLocaleString(isFa ? "fa-IR" : "en-US")}٪
          </span>
          <span
            className={`${sizeClasses.old} text-[#A1A3A8] line-through`}
          >
            {formatPrice(price, locale)}
          </span>
        </div>
      )}
      <div className="flex items-center gap-1">
        <span className={`${sizeClasses.price} font-bold text-[#3F4064]`}>
          {formatPrice(finalPrice, locale)}
        </span>
        <span className="text-[11px] text-[#62666D]">
          {isFa ? "تومان" : "Toman"}
        </span>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/product/ProductCard.tsx
# ============================================================
files.append(("components/product/ProductCard.tsx", """"use client";

import Link from "next/link";
import Image from "next/image";
import { Heart, ShoppingCart, Eye } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore } from "@/lib/stores";
import RatingStars from "./RatingStars";
import PriceTag from "./PriceTag";

interface ProductCardProps {
  product: Product;
  locale: Locale;
  variant?: "default" | "compact";
}

export default function ProductCard({
  product,
  locale,
  variant = "default",
}: ProductCardProps) {
  const isFa = locale === "fa";
  const addToCart = useCartStore((s) => s.addItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);
  const isInWishlist = useWishlistStore((s) => s.ids.includes(product.id));

  const title = isFa ? product.titleFa : product.titleEn;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!product.inStock) return;
    addToCart(product.id, 1);
  };

  const handleToggleWishlist = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleWishlist(product.id);
  };

  return (
    <div className="group relative bg-white rounded-lg border border-[#E0E0E2] hover:shadow-lg transition-all duration-200 overflow-hidden">
      {/* Wishlist button (top corner) */}
      <button
        onClick={handleToggleWishlist}
        aria-label={isFa ? "افزودن به علاقه‌مندی" : "Add to wishlist"}
        className={`absolute top-2 z-10 w-7 h-7 rounded-full bg-white/90 backdrop-blur flex items-center justify-center transition-all ${
          isFa ? "left-2" : "right-2"
        } ${
          isInWishlist
            ? "opacity-100"
            : "opacity-0 group-hover:opacity-100"
        }`}
      >
        <Heart
          size={14}
          className={
            isInWishlist
              ? "fill-[#EF4056] text-[#EF4056]"
              : "text-[#62666D]"
          }
        />
      </button>

      {/* Discount badge */}
      {product.discountPercent > 0 && (
        <div
          className={`absolute top-2 z-10 bg-[#EF4056] text-white text-[11px] font-bold rounded px-1.5 py-0.5 ${
            isFa ? "right-2" : "left-2"
          }`}
        >
          {product.discountPercent.toLocaleString(isFa ? "fa-IR" : "en-US")}٪
        </div>
      )}

      {/* Out of stock overlay */}
      {!product.inStock && (
        <div className="absolute inset-0 bg-white/70 z-20 flex items-center justify-center">
          <span className="text-[#62666D] text-[13px] font-medium bg-white px-3 py-1 rounded">
            {isFa ? "ناموجود" : "Out of stock"}
          </span>
        </div>
      )}

      <Link href={`/${locale}/product/${product.slug}`} className="block">
        {/* Image */}
        <div className="aspect-square bg-[#F5F5F5] relative overflow-hidden">
          <Image
            src={product.image}
            alt={title}
            fill
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 20vw"
            className="object-cover group-hover:scale-105 transition-transform duration-300"
          />
        </div>

        {/* Content */}
        <div className={`p-3 ${variant === "compact" ? "pb-2" : ""}`}>
          {/* Title */}
          <h3
            className="text-[13px] text-[#3F4064] leading-5 mb-2 line-clamp-2 min-h-[40px]"
            title={title}
          >
            {title}
          </h3>

          {/* Rating */}
          <div className="flex items-center gap-1 mb-3">
            <RatingStars rating={product.rating} size={11} />
            <span className="text-[10px] text-[#A1A3A8]">
              ({product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")})
            </span>
          </div>

          {/* Price */}
          <PriceTag
            price={product.price}
            finalPrice={product.finalPrice}
            discountPercent={product.discountPercent}
            locale={locale}
            size="sm"
          />
        </div>
      </Link>

      {/* Add to cart button (bottom corner) */}
      {variant === "default" && (
        <button
          onClick={handleAddToCart}
          disabled={!product.inStock}
          aria-label={isFa ? "افزودن به سبد خرید" : "Add to cart"}
          className={`absolute bottom-3 w-8 h-8 rounded-full flex items-center justify-center transition-all ${
            isFa ? "left-3" : "right-3"
          } ${
            product.inStock
              ? "bg-[#EF4056] text-white hover:bg-[#d63850]"
              : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
          }`}
        >
          <ShoppingCart size={15} />
        </button>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/product/index.ts (barrel export)
# ============================================================
files.append(("components/product/index.ts", """// components/product/index.ts
export { default as ProductCard } from "./ProductCard";
export { default as RatingStars } from "./RatingStars";
export { default as PriceTag } from "./PriceTag";
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 07: ProductCard")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("Next: run 08_home.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()