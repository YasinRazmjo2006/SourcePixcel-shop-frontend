# 29_framer_motion.py
# اضافه کردن Framer Motion برای انیمیشن‌های حرفه‌ای
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/motion.ts — Variants مشترک
# ============================================================
files.append(("lib/motion.ts", """import type { Variants, Transition } from "framer-motion";

// ═══════════════════════════════════════════════════════════════
// TRANSITIONS
// ═══════════════════════════════════════════════════════════════

export const spring: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};

export const springSoft: Transition = {
  type: "spring",
  stiffness: 200,
  damping: 25,
};

export const easeOut: Transition = {
  duration: 0.3,
  ease: [0.16, 1, 0.3, 1],
};

export const easeInOut: Transition = {
  duration: 0.4,
  ease: [0.65, 0, 0.35, 1],
};

export const smooth: Transition = {
  duration: 0.5,
  ease: [0.22, 1, 0.36, 1],
};

// ═══════════════════════════════════════════════════════════════
// PAGE TRANSITIONS
// ═══════════════════════════════════════════════════════════════

export const pageVariants: Variants = {
  initial: {
    opacity: 0,
    y: 8,
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0.16, 1, 0.3, 1],
    },
  },
  exit: {
    opacity: 0,
    y: -8,
    transition: {
      duration: 0.2,
      ease: [0.65, 0, 0.35, 1],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// FADE
// ═══════════════════════════════════════════════════════════════

export const fadeInVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.3 },
  },
};

// ═══════════════════════════════════════════════════════════════
// SLIDE UP (for sections)
// ═══════════════════════════════════════════════════════════════

export const slideUpVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 24,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: [0.22, 1, 0.36, 1],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// SCALE IN (for modals, dropdowns)
// ═══════════════════════════════════════════════════════════════

export const scaleInVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.95,
  },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.2,
      ease: [0.16, 1, 0.3, 1],
    },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: {
      duration: 0.15,
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// STAGGER (for lists)
// ═══════════════════════════════════════════════════════════════

export const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.06,
      delayChildren: 0.05,
    },
  },
};

export const itemVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 12,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.35,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

// ═══════════════════════════════════════════════════════════════
// HOVER EFFECTS
// ═══════════════════════════════════════════════════════════════

export const cardHoverVariants: Variants = {
  rest: {
    y: 0,
    boxShadow: "0 2px 8px -2px rgb(0 0 0 / 0.06)",
  },
  hover: {
    y: -4,
    boxShadow: "0 12px 32px -8px rgb(0 0 0 / 0.12)",
    transition: {
      duration: 0.25,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

export const buttonTapVariants = {
  rest: { scale: 1 },
  hover: { scale: 1.02 },
  tap: { scale: 0.97 },
};

// ═══════════════════════════════════════════════════════════════
// DRAWER (mobile menu, filters)
// ═══════════════════════════════════════════════════════════════

export const drawerVariants = (isFa: boolean): Variants => ({
  hidden: {
    x: isFa ? "100%" : "-100%",
    opacity: 0,
  },
  visible: {
    x: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 30,
    },
  },
  exit: {
    x: isFa ? "100%" : "-100%",
    opacity: 0,
    transition: {
      duration: 0.2,
    },
  },
});

export const backdropVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.2 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

// ═══════════════════════════════════════════════════════════════
// SLIDER (carousel)
// ═══════════════════════════════════════════════════════════════

export const slideVariants: Variants = {
  enter: (direction: number) => ({
    x: direction > 0 ? "100%" : "-100%",
    opacity: 0,
  }),
  center: {
    x: 0,
    opacity: 1,
    transition: {
      duration: 0.4,
      ease: [0.22, 1, 0.36, 1],
    },
  },
  exit: (direction: number) => ({
    x: direction > 0 ? "-100%" : "100%",
    opacity: 0,
    transition: {
      duration: 0.3,
      ease: [0.65, 0, 0.35, 1],
    },
  }),
};
"""))

# ============================================================
# components/motion/PageTransition.tsx
# ============================================================
files.append(("components/motion/PageTransition.tsx", """"use client";

import { motion } from "framer-motion";
import { pageVariants } from "@/lib/motion";

interface PageTransitionProps {
  children: React.ReactNode;
  className?: string;
}

export default function PageTransition({
  children,
  className,
}: PageTransitionProps) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className={className}
    >
      {children}
    </motion.div>
  );
}
"""))

# ============================================================
# components/motion/AnimatedSection.tsx
# ============================================================
files.append(("components/motion/AnimatedSection.tsx", """"use client";

import { motion, useInView } from "framer-motion";
import { useRef } from "react";
import { slideUpVariants } from "@/lib/motion";

interface AnimatedSectionProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export default function AnimatedSection({
  children,
  className,
  delay = 0,
}: AnimatedSectionProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  return (
    <motion.div
      ref={ref}
      variants={slideUpVariants}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
      transition={{ delay }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
"""))

# ============================================================
# components/motion/StaggerList.tsx
# ============================================================
files.append(("components/motion/StaggerList.tsx", """"use client";

import { motion } from "framer-motion";
import { containerVariants, itemVariants } from "@/lib/motion";

interface StaggerListProps {
  children: React.ReactNode;
  className?: string;
}

interface StaggerItemProps {
  children: React.ReactNode;
  className?: string;
}

export function StaggerList({ children, className }: StaggerListProps) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className={className}
    >
      {children}
    </motion.div>
  );
}

export function StaggerItem({ children, className }: StaggerItemProps) {
  return (
    <motion.div variants={itemVariants} className={className}>
      {children}
    </motion.div>
  );
}
"""))

# ============================================================
# components/motion/AnimatedCard.tsx
# ============================================================
files.append(("components/motion/AnimatedCard.tsx", """"use client";

import { motion } from "framer-motion";
import { cardHoverVariants } from "@/lib/motion";

interface AnimatedCardProps {
  children: React.ReactNode;
  className?: string;
  disabled?: boolean;
}

export default function AnimatedCard({
  children,
  className,
  disabled = false,
}: AnimatedCardProps) {
  if (disabled) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      variants={cardHoverVariants}
      initial="rest"
      whileHover="hover"
      animate="rest"
      className={className}
    >
      {children}
    </motion.div>
  );
}
"""))

# ============================================================
# components/motion/AnimatedButton.tsx
# ============================================================
files.append(("components/motion/AnimatedButton.tsx", """"use client";

import { motion, type HTMLMotionProps } from "framer-motion";
import { buttonTapVariants } from "@/lib/motion";

interface AnimatedButtonProps extends HTMLMotionProps<"button"> {
  children: React.ReactNode;
}

export default function AnimatedButton({
  children,
  ...props
}: AnimatedButtonProps) {
  return (
    <motion.button
      variants={buttonTapVariants}
      initial="rest"
      whileHover="hover"
      whileTap="tap"
      {...props}
    >
      {children}
    </motion.button>
  );
}
"""))

# ============================================================
# components/motion/FadeIn.tsx
# ============================================================
files.append(("components/motion/FadeIn.tsx", """"use client";

import { motion } from "framer-motion";
import { fadeInVariants } from "@/lib/motion";

interface FadeInProps {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export default function FadeIn({
  children,
  className,
  delay = 0,
}: FadeInProps) {
  return (
    <motion.div
      variants={fadeInVariants}
      initial="hidden"
      animate="visible"
      transition={{ delay }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
"""))

# ============================================================
# components/motion/index.ts
# ============================================================
files.append(("components/motion/index.ts", """// components/motion/index.ts
export { default as PageTransition } from "./PageTransition";
export { default as AnimatedSection } from "./AnimatedSection";
export { StaggerList, StaggerItem } from "./StaggerList";
export { default as AnimatedCard } from "./AnimatedCard";
export { default as AnimatedButton } from "./AnimatedButton";
export { default as FadeIn } from "./FadeIn";
"""))

# ============================================================
# components/product/ProductCard.tsx (updated with motion)
# ============================================================
files.append(("components/product/ProductCard.tsx", """"use client";

import Link from "next/link";
import Image from "next/image";
import { motion } from "framer-motion";
import { Heart, ShoppingCart } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore, useToastStore } from "@/lib/stores";
import RatingStars from "./RatingStars";
import PriceTag from "./PriceTag";
import CompareButton from "./CompareButton";

interface ProductCardProps {
  product: Product;
  locale: Locale;
  variant?: "default" | "compact";
  priority?: boolean;
}

export default function ProductCard({
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
          className={`w-7 h-7 rounded-full bg-white/90 backdrop-blur flex items-center justify-center transition-all ${
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
            <Image
              src={product.image}
              alt={title}
              fill
              sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 20vw"
              className="object-cover"
              priority={priority}
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
"""))

# ============================================================
# components/home/ProductSection.tsx (updated with stagger)
# ============================================================
files.append(("components/home/ProductSection.tsx", """import Link from "next/link";
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
"""))

# ============================================================
# components/home/AmazingOffer.tsx (updated with motion)
# ============================================================
files.append(("components/home/AmazingOffer.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Flame, ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { getDiscountedProducts } from "@/lib/data";
import ProductCard from "@/components/product/ProductCard";

interface AmazingOfferProps {
  locale: Locale;
}

export default function AmazingOffer({ locale }: AmazingOfferProps) {
  const isFa = locale === "fa";
  const [timeLeft, setTimeLeft] = useState({
    hours: 12,
    minutes: 34,
    seconds: 56,
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        let { hours, minutes, seconds } = prev;
        seconds--;
        if (seconds < 0) {
          seconds = 59;
          minutes--;
          if (minutes < 0) {
            minutes = 59;
            hours--;
            if (hours < 0) hours = 23;
          }
        }
        return { hours, minutes, seconds };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const products = getDiscountedProducts().slice(0, 5);

  const fmt = (n: number) => {
    const s = String(n).padStart(2, "0");
    return isFa ? s.replace(/\\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]) : s;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="rounded-xl overflow-hidden bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E]"
    >
      <div className="flex flex-col lg:flex-row">
        {/* Left panel */}
        <motion.div
          initial={{ opacity: 0, x: isFa ? 20 : -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="lg:w-60 p-5 md:p-6 flex lg:flex-col items-center lg:items-start justify-between lg:justify-center gap-4 text-white shrink-0"
          style={{
            background: "linear-gradient(180deg, #EF4056 0%, #d63850 100%)",
          }}
        >
          <div className="flex flex-col items-center lg:items-start gap-2">
            <div className="flex items-center gap-2">
              <motion.div
                animate={{ scale: [1, 1.15, 1] }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center"
              >
                <Flame size={20} className="text-white" />
              </motion.div>
              <div>
                <h2 className="text-[15px] md:text-[17px] font-bold leading-tight">
                  {isFa ? "پیشنهاد شگفت‌انگیز" : "Amazing Offer"}
                </h2>
                <p className="text-[10px] md:text-[11px] text-white/80">
                  {isFa ? "فرصت محدود" : "Limited time"}
                </p>
              </div>
            </div>

            {/* Countdown */}
            <div className="flex items-center gap-1.5 mt-2">
              {[timeLeft.seconds, timeLeft.minutes, timeLeft.hours].map(
                (value, i) => (
                  <span key={i} className="flex items-center gap-1.5">
                    <div className="bg-white text-[#EF4056] rounded-lg px-2 py-1.5 text-[15px] font-bold tabular-nums min-w-[36px] text-center shadow-lg">
                      {fmt(value)}
                    </div>
                    {i < 2 && (
                      <span className="text-white/70 text-[14px] font-bold">
                        :
                      </span>
                    )}
                  </span>
                )
              )}
            </div>
          </div>

          <Link
            href={`/${locale}/search?discount=1`}
            className="text-[11px] md:text-[12px] text-white font-medium bg-white/20 backdrop-blur px-3 py-1.5 rounded-full hover:bg-white/30 transition-colors flex items-center gap-1 whitespace-nowrap"
          >
            {isFa ? "مشاهده همه" : "See all"}
            {isFa ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
          </Link>
        </motion.div>

        {/* Products */}
        <div className="flex-1 p-3 md:p-4">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-2 md:gap-3">
            {products.map((product, index) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 + index * 0.05 }}
              >
                <ProductCard
                  product={product}
                  locale={locale}
                  variant="compact"
                  priority={index === 0}
                />
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
"""))

# ============================================================
# components/home/HeroSlider.tsx (updated with slide animation)
# ============================================================
files.append(("components/home/HeroSlider.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, ArrowLeft, ArrowRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { slideVariants } from "@/lib/motion";

interface Slide {
  id: number;
  bgFrom: string;
  bgTo: string;
  emoji: string;
  titleFa: string;
  titleEn: string;
  subtitleFa: string;
  subtitleEn: string;
  ctaFa: string;
  ctaEn: string;
  href: string;
}

const SLIDES: Slide[] = [
  {
    id: 1,
    bgFrom: "#EF4056",
    bgTo: "#FF7B8A",
    emoji: "📱",
    titleFa: "جشنواره موبایل",
    titleEn: "Mobile Festival",
    subtitleFa: "تا ۴۰٪ تخفیف روی گوشی‌های پرچمدار",
    subtitleEn: "Up to 40% off on flagship phones",
    ctaFa: "مشاهده تخفیف‌ها",
    ctaEn: "See Discounts",
    href: "/category/mobile",
  },
  {
    id: 2,
    bgFrom: "#00BFFF",
    bgTo: "#4DD0FF",
    emoji: "💻",
    titleFa: "لپ‌تاپ‌های حرفه‌ای",
    titleEn: "Pro Laptops",
    subtitleFa: "جدیدترین مدل‌های ایسوس، اپل و لنوو",
    subtitleEn: "Latest Asus, Apple, and Lenovo models",
    ctaFa: "خرید کنید",
    ctaEn: "Shop Now",
    href: "/category/laptop",
  },
  {
    id: 3,
    bgFrom: "#8B5CF6",
    bgTo: "#A78BFA",
    emoji: "🎧",
    titleFa: "صدای بی‌نظیر",
    titleEn: "Ultimate Sound",
    subtitleFa: "هدفون‌های بی‌سیم با نویز کنسلینگ",
    subtitleEn: "Wireless headphones with noise cancelling",
    ctaFa: "مشاهده محصولات",
    ctaEn: "View Products",
    href: "/category/audio",
  },
];

interface HeroSliderProps {
  locale: Locale;
}

export default function HeroSlider({ locale }: HeroSliderProps) {
  const isFa = locale === "fa";
  const [current, setCurrent] = useState(0);
  const [direction, setDirection] = useState(1);

  useEffect(() => {
    const timer = setInterval(() => {
      setDirection(1);
      setCurrent((prev) => (prev + 1) % SLIDES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const goTo = (i: number) => {
    setDirection(i > current ? 1 : -1);
    setCurrent(i);
  };

  const next = () => {
    setDirection(1);
    setCurrent((prev) => (prev + 1) % SLIDES.length);
  };

  const prev = () => {
    setDirection(-1);
    setCurrent((prev) => (prev - 1 + SLIDES.length) % SLIDES.length);
  };

  const slide = SLIDES[current];

  return (
    <div className="relative w-full h-[180px] md:h-[280px] lg:h-[350px] rounded-xl overflow-hidden group">
      {/* Background gradient */}
      <motion.div
        key={`bg-${current}`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="absolute inset-0"
        style={{
          background: `linear-gradient(135deg, ${slide.bgFrom} 0%, ${slide.bgTo} 100%)`,
        }}
      />

      {/* Decorative circles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{ scale: [1, 1.1, 1], opacity: [0.1, 0.15, 0.1] }}
          transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
          className="absolute -top-20 -right-20 w-80 h-80 rounded-full bg-white"
        />
        <motion.div
          animate={{ scale: [1, 1.05, 1], opacity: [0.05, 0.08, 0.05] }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
          className="absolute -bottom-24 -left-24 w-96 h-96 rounded-full bg-white"
        />
      </div>

      {/* Content */}
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={current}
          custom={direction}
          variants={slideVariants}
          initial="enter"
          animate="center"
          exit="exit"
          className="relative h-full flex items-center justify-between px-6 md:px-12 lg:px-16"
        >
          {/* Text side */}
          <div className="flex-1 text-white z-10 max-w-lg">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.5 }}
              className="text-[22px] md:text-[34px] lg:text-[42px] font-bold mb-2 md:mb-3 drop-shadow-lg"
            >
              {isFa ? slide.titleFa : slide.titleEn}
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-[12px] md:text-[15px] lg:text-[17px] text-white/90 mb-4 md:mb-6 drop-shadow"
            >
              {isFa ? slide.subtitleFa : slide.subtitleEn}
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              <Link
                href={`/${locale}${slide.href}`}
                className="inline-flex items-center gap-2 bg-white text-[#3F4064] font-bold text-[12px] md:text-[14px] px-5 md:px-6 py-2.5 md:py-3 rounded-lg hover:bg-white/90 hover:scale-105 transition-all shadow-lg"
              >
                {isFa ? slide.ctaFa : slide.ctaEn}
                {isFa ? <ArrowLeft size={16} /> : <ArrowRight size={16} />}
              </Link>
            </motion.div>
          </div>

          {/* Icon side */}
          <div className="hidden md:flex items-center justify-center shrink-0">
            <motion.div
              animate={{
                y: [0, -10, 0],
                rotate: [0, 3, -3, 0],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="text-[140px] lg:text-[200px] drop-shadow-2xl select-none"
            >
              {slide.emoji}
            </motion.div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Arrows */}
      <button
        onClick={prev}
        aria-label="Previous slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 md:w-11 md:h-11 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white hover:bg-white/30 opacity-0 group-hover:opacity-100 transition-opacity z-20 ${
          isFa ? "right-3" : "left-3"
        }`}
      >
        {isFa ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>
      <button
        onClick={next}
        aria-label="Next slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 md:w-11 md:h-11 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white hover:bg-white/30 opacity-0 group-hover:opacity-100 transition-opacity z-20 ${
          isFa ? "left-3" : "right-3"
        }`}
      >
        {isFa ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>

      {/* Dots */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-20">
        {SLIDES.map((_, i) => (
          <button
            key={i}
            onClick={() => goTo(i)}
            aria-label={`Slide ${i + 1}`}
            className={`h-1.5 rounded-full transition-all ${
              i === current
                ? "bg-white w-8"
                : "bg-white/50 w-2 hover:bg-white/70"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/template.tsx — Page Transitions
# ============================================================
files.append(("app/[locale]/template.tsx", """"use client";

import { motion } from "framer-motion";
import { pageVariants } from "@/lib/motion";

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {children}
    </motion.div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 29: Framer Motion")
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
        print("\nNext steps:")
        print("  1) Make sure framer-motion is installed:")
        print("     npm install framer-motion --registry=https://mirror-npm.runflare.com")
        print("  2) Remove-Item -Recurse -Force .next")
        print("  3) npm run dev")
        print("\nYou should see:")
        print("  ✓ Smooth page transitions")
        print("  ✓ Cards animate on scroll")
        print("  ✓ Hero slider with fade+slide")
        print("  ✓ Floating emoji animation")
        print("  ✓ Countdown pulse on Amazing Offer")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()