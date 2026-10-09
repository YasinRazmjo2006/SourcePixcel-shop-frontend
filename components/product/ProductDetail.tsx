"use client";

import { useState } from "react";
import Link from "next/link";
import {
  Heart,
  ShoppingCart,
  Truck,
  ShieldCheck,
  RotateCcw,
  Share2,
  Check,
} from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore } from "@/lib/stores";
import { getBrandById } from "@/lib/data";
import RatingStars from "./RatingStars";
import PriceTag from "./PriceTag";
import ProductGallery from "./ProductGallery";
import QuantitySelector from "./QuantitySelector";

interface ProductDetailProps {
  product: Product;
  locale: Locale;
}

export default function ProductDetail({ product, locale }: ProductDetailProps) {
  const isFa = locale === "fa";
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  const addToCart = useCartStore((s) => s.addItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);
  const isInWishlist = useWishlistStore((s) => s.ids.includes(product.id));

  const brand = getBrandById(product.brand);
  const title = isFa ? product.titleFa : product.titleEn;

  const images = [
    product.image,
    `https://picsum.photos/seed/sp${product.id}a/600/600`,
    `https://picsum.photos/seed/sp${product.id}b/600/600`,
    `https://picsum.photos/seed/sp${product.id}c/600/600`,
  ];

  const handleAddToCart = () => {
    if (!product.inStock) return;
    addToCart(product.id, quantity);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const features = [
    { icon: Truck, fa: "ارسال سریع", en: "Fast Shipping" },
    { icon: ShieldCheck, fa: "ضمانت اصالت", en: "Authenticity" },
    { icon: RotateCcw, fa: "۷ روز بازگشت", en: "7-Day Return" },
  ];

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 md:p-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
        {/* Gallery */}
        <ProductGallery images={images} alt={title} />

        {/* Info */}
        <div className="flex flex-col">
          {/* Breadcrumb-ish brand line */}
          {brand && (
            <div className="text-[12px] text-[#A1A3A8] mb-2">
              {isFa ? "برند:" : "Brand:"}{" "}
              <Link
                href={`/${locale}/category/${product.category}`}
                className="text-[#00BFFF] hover:underline"
              >
                {isFa ? brand.nameFa : brand.nameEn}
              </Link>
            </div>
          )}

          {/* Title */}
          <h1 className="text-[18px] md:text-[20px] font-bold text-[#3F4064] leading-7 mb-3">
            {title}
          </h1>

          {/* Rating */}
          <div className="flex items-center gap-2 mb-4">
            <RatingStars rating={product.rating} size={14} />
            <span className="text-[12px] text-[#A1A3A8]">
              ({product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
              {isFa ? "نظر" : "reviews"})
            </span>
          </div>

          {/* Tags */}
          {product.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {product.tags.map((tag, i) => (
                <span
                  key={i}
                  className="text-[11px] bg-[#F5F5F5] text-[#62666D] px-2 py-1 rounded"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Divider */}
          <div className="border-t border-[#E0E0E2] my-4" />

          {/* Price */}
          <div className="mb-4">
            <PriceTag
              price={product.price}
              finalPrice={product.finalPrice}
              discountPercent={product.discountPercent}
              locale={locale}
              size="lg"
            />
          </div>

          {/* Stock status */}
          <div className="mb-4">
            <span
              className={`text-[13px] font-medium flex items-center gap-2 ${
                product.inStock ? "text-[#22C55E]" : "text-[#EF4444]"
              }`}
            >
              {product.inStock ? (
                <>
                  <Check size={16} />
                  {isFa ? "موجود در انبار" : "In stock"}
                </>
              ) : (
                <>
                  {isFa ? "ناموجود" : "Out of stock"}
                </>
              )}
            </span>
          </div>

          {/* Quantity + Actions */}
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mb-5">
            <QuantitySelector
              value={quantity}
              onChange={setQuantity}
              max={10}
              locale={locale}
            />
          </div>

          <div className="flex items-center gap-3 mb-6">
            <button
              onClick={handleAddToCart}
              disabled={!product.inStock}
              className={`flex-1 h-11 rounded-lg text-[14px] font-bold flex items-center justify-center gap-2 transition-colors ${
                product.inStock
                  ? added
                    ? "bg-[#22C55E] text-white"
                    : "bg-[#EF4056] text-white hover:bg-[#d63850]"
                  : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
              }`}
            >
              <ShoppingCart size={18} />
              {added
                ? isFa
                  ? "به سبد اضافه شد"
                  : "Added to cart"
                : isFa
                ? "افزودن به سبد خرید"
                : "Add to cart"}
            </button>

            <button
              onClick={() => toggleWishlist(product.id)}
              aria-label={isFa ? "علاقه‌مندی" : "Wishlist"}
              className={`w-11 h-11 rounded-lg border flex items-center justify-center transition-colors ${
                isInWishlist
                  ? "border-[#EF4056] bg-[#EF4056]/5"
                  : "border-[#E0E0E2] hover:border-[#EF4056]"
              }`}
            >
              <Heart
                size={18}
                className={
                  isInWishlist
                    ? "fill-[#EF4056] text-[#EF4056]"
                    : "text-[#62666D]"
                }
              />
            </button>

            <button
              aria-label={isFa ? "اشتراک‌گذاری" : "Share"}
              className="w-11 h-11 rounded-lg border border-[#E0E0E2] flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
            >
              <Share2 size={18} />
            </button>
          </div>

          {/* Features */}
          <div className="bg-[#FAFAFA] rounded-lg p-3 space-y-2">
            {features.map((f, i) => {
              const Icon = f.icon;
              return (
                <div
                  key={i}
                  className="flex items-center gap-2 text-[12px] text-[#62666D]"
                >
                  <Icon size={14} className="text-[#A1A3A8]" />
                  <span>{isFa ? f.fa : f.en}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
