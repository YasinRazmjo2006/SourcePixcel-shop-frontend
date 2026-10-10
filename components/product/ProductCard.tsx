"use client";

import { memo } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Heart, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore, useToastStore } from "@/lib/stores";
import { SmartImage } from "@/components/common";
import RatingStars from "./RatingStars";
import PriceTag from "./PriceTag";
import CompareButton from "./CompareButton";

interface ProductCardProps {
  product: Product;
  locale: Locale;
  variant?: "default" | "compact";
  priority?: boolean;
}

function ProductCardComponent({
  product,
  locale,
  variant = "default",
  priority = false,
}: ProductCardProps) {
  const isFa = locale === "fa";
  const addToCart = useCartStore((s) => s.addItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);
  const isInWishlist = useWishlistStore((s) => s.ids.includes(product.id));
  const pushToast = useToastStore((s) => s.push);

  const title = isFa ? product.titleFa : product.titleEn;

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!product.inStock) return;
    addToCart(product.id, 1);
    pushToast({
      type: "success",
      titleFa: "به سبد خرید اضافه شد",
      titleEn: "Added to cart",
      messageFa: title,
      messageEn: title,
    });
  };

  const handleToggleWishlist = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleWishlist(product.id);
    pushToast({
      type: isInWishlist ? "info" : "success",
      titleFa: isInWishlist ? "از علاقه‌مندی‌ها حذف شد" : "به علاقه‌مندی‌ها اضافه شد",
      titleEn: isInWishlist ? "Removed from wishlist" : "Added to wishlist",
      messageFa: title,
      messageEn: title,
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
      whileHover={{ y: -4 }}
      className="group relative bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-lg transition-shadow duration-300 overflow-hidden"
    >
      <div
        className={`absolute top-2 z-20 flex flex-col gap-1.5 ${
          isFa ? "left-2" : "right-2"
        }`}
      >
        <button
          onClick={handleToggleWishlist}
          aria-label={isFa ? "افزودن به علاقه‌مندی" : "Add to wishlist"}
          className={`w-7 h-7 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center transition-all ${
            isInWishlist ? "opacity-100" : "opacity-0 group-hover:opacity-100"
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
        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
          <CompareButton productId={product.id} locale={locale} size="sm" />
        </div>
      </div>

      {product.discountPercent > 0 && (
        <div
          className={`absolute top-2 z-10 bg-[#EF4056] text-white text-[11px] font-bold rounded px-1.5 py-0.5 ${
            isFa ? "right-2" : "left-2"
          }`}
        >
          {product.discountPercent.toLocaleString(isFa ? "fa-IR" : "en-US")}٪
        </div>
      )}

      {!product.inStock && (
        <div className="absolute inset-0 bg-white/70 dark:bg-[#1A1A1E]/70 z-20 flex items-center justify-center">
          <span className="text-[#62666D] dark:text-[#A1A3A8] text-[13px] font-medium bg-white dark:bg-[#1A1A1E] px-3 py-1 rounded">
            {isFa ? "ناموجود" : "Out of stock"}
          </span>
        </div>
      )}

      <Link href={`/${locale}/product/${product.slug}`} className="block">
        <div className="aspect-square bg-[#F5F5F5] dark:bg-[#2A2A2E] relative overflow-hidden">
          <motion.div
            className="absolute inset-0"
            whileHover={{ scale: 1.05 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          >
            <SmartImage
              src={product.image}
              alt={title}
              fill
              sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 20vw"
              className="object-cover"
              priority={priority}
              category={product.category}
            />
          </motion.div>
        </div>

        <div className={`p-3 ${variant === "compact" ? "pb-2" : ""}`}>
          <h3
            className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] leading-5 mb-2 line-clamp-2 min-h-[40px]"
            title={title}
          >
            {title}
          </h3>

          <div className="flex items-center gap-1 mb-3">
            <RatingStars rating={product.rating} size={11} />
            <span className="text-[10px] text-[#A1A3A8]">
              ({product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")})
            </span>
          </div>

          <PriceTag
            price={product.price}
            finalPrice={product.finalPrice}
            discountPercent={product.discountPercent}
            locale={locale}
            size="sm"
          />
        </div>
      </Link>

      {variant === "default" && (
        <motion.button
          onClick={handleAddToCart}
          disabled={!product.inStock}
          aria-label={isFa ? "افزودن به سبد خرید" : "Add to cart"}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          className={`absolute bottom-3 w-8 h-8 rounded-full flex items-center justify-center transition-colors ${
            isFa ? "left-3" : "right-3"
          } ${
            product.inStock
              ? "bg-[#EF4056] text-white hover:bg-[#d63850]"
              : "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
          }`}
        >
          <ShoppingCart size={15} />
        </motion.button>
      )}
    </motion.div>
  );
}

// Memoize to prevent unnecessary re-renders
const ProductCard = memo(ProductCardComponent, (prevProps, nextProps) => {
  return (
    prevProps.product.id === nextProps.product.id &&
    prevProps.product.inStock === nextProps.product.inStock &&
    prevProps.product.finalPrice === nextProps.product.finalPrice &&
    prevProps.locale === nextProps.locale &&
    prevProps.variant === nextProps.variant
  );
});

export default ProductCard;
