# 35_performance.py
# بهینه‌سازی عملکرد و سرعت سایت
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# next.config.js — تنظیمات بهینه‌شده
# ============================================================
files.append(("next.config.js", """/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output
  reactStrictMode: true,
  poweredByHeader: false,

  // Compression
  compress: true,

  // Source maps (disable in production for smaller bundle)
  productionBrowserSourceMaps: false,

  // Images
  images: {
    unoptimized: true,
    formats: ["image/avif", "image/webp"],
    remotePatterns: [
      { protocol: "https", hostname: "loremflickr.com", pathname: "/**" },
      { protocol: "https", hostname: "picsum.photos", pathname: "/**" },
      { protocol: "https", hostname: "images.unsplash.com", pathname: "/**" },
    ],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
    minimumCacheTTL: 60 * 60 * 24 * 365, // 1 year
  },

  // Experimental optimizations
  experimental: {
    optimizePackageImports: [
      "lucide-react",
      "framer-motion",
      "date-fns",
    ],
    optimizeCss: false, // Keep false to avoid issues with static export
  },

  // Compiler options
  compiler: {
    // Remove console.log in production
    removeConsole:
      process.env.NODE_ENV === "production"
        ? { exclude: ["error", "warn"] }
        : false,
  },

  // Headers for caching
  async headers() {
    return [
      {
        source: "/images/:path*",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
      {
        source: "/fonts/:path*",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
    ];
  },

  // Webpack customizations
  webpack: (config, { isServer, dev }) => {
    // Reduce bundle size in production
    if (!dev && !isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: "all",
          cacheGroups: {
            default: false,
            vendors: false,
            // Vendor chunk
            vendor: {
              name: "vendor",
              chunks: "all",
              test: /node_modules/,
              priority: 20,
            },
            // Separate framer-motion
            framerMotion: {
              name: "framer-motion",
              test: /[\\\\/]node_modules[\\\\/]framer-motion[\\\\/]/,
              chunks: "all",
              priority: 30,
            },
            // Separate lucide
            lucide: {
              name: "lucide",
              test: /[\\\\/]node_modules[\\\\/]lucide-react[\\\\/]/,
              chunks: "all",
              priority: 30,
            },
            // Common chunk
            common: {
              name: "common",
              minChunks: 2,
              chunks: "all",
              priority: 10,
              reuseExistingChunk: true,
            },
          },
        },
      };
    }

    return config;
  },

  // Static export
  output: "export",
  trailingSlash: true,
};

module.exports = nextConfig;
"""))

# ============================================================
# lib/hooks/useDebounce.ts
# ============================================================
files.append(("lib/hooks/useDebounce.ts", """import { useEffect, useState } from "react";

/**
 * Debounce a value.
 * Useful for search inputs and expensive operations.
 */
export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}
"""))

# ============================================================
# lib/hooks/useIntersectionObserver.ts
# ============================================================
files.append(("lib/hooks/useIntersectionObserver.ts", """import { useEffect, useRef, useState } from "react";

interface UseIntersectionObserverOptions {
  threshold?: number;
  rootMargin?: string;
  triggerOnce?: boolean;
}

/**
 * Intersection Observer hook for lazy loading components.
 */
export function useIntersectionObserver<T extends HTMLElement = HTMLDivElement>(
  options: UseIntersectionObserverOptions = {}
) {
  const { threshold = 0.1, rootMargin = "50px", triggerOnce = true } = options;
  const ref = useRef<T>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    if (typeof IntersectionObserver === "undefined") {
      setIsVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          if (triggerOnce) {
            observer.unobserve(element);
          }
        } else if (!triggerOnce) {
          setIsVisible(false);
        }
      },
      { threshold, rootMargin }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [threshold, rootMargin, triggerOnce]);

  return { ref, isVisible };
}
"""))

# ============================================================
# lib/hooks/useMediaQuery.ts
# ============================================================
files.append(("lib/hooks/useMediaQuery.ts", """import { useEffect, useState } from "react";

/**
 * Media query hook for responsive rendering.
 */
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined") return;

    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);

    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };

    mediaQuery.addEventListener("change", handler);
    return () => mediaQuery.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

// Predefined breakpoints
export const useIsMobile = () => useMediaQuery("(max-width: 767px)");
export const useIsTablet = () =>
  useMediaQuery("(min-width: 768px) and (max-width: 1023px)");
export const useIsDesktop = () => useMediaQuery("(min-width: 1024px)");
export const usePrefersReducedMotion = () =>
  useMediaQuery("(prefers-reduced-motion: reduce)");
"""))

# ============================================================
# lib/hooks/index.ts
# ============================================================
files.append(("lib/hooks/index.ts", """// lib/hooks/index.ts
export { useDebounce } from "./useDebounce";
export { useIntersectionObserver } from "./useIntersectionObserver";
export {
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  usePrefersReducedMotion,
} from "./useMediaQuery";
"""))

# ============================================================
# components/common/LazySection.tsx — Lazy render sections
# ============================================================
files.append(("components/common/LazySection.tsx", """"use client";

import { useIntersectionObserver } from "@/lib/hooks";
import { motion } from "framer-motion";

interface LazySectionProps {
  children: React.ReactNode;
  className?: string;
  fallback?: React.ReactNode;
  minHeight?: number;
}

/**
 * LazySection — only renders content when it enters the viewport.
 * Great for below-the-fold sections with heavy content.
 */
export default function LazySection({
  children,
  className,
  fallback,
  minHeight = 200,
}: LazySectionProps) {
  const { ref, isVisible } = useIntersectionObserver<HTMLDivElement>({
    threshold: 0.05,
    rootMargin: "100px",
  });

  return (
    <div
      ref={ref}
      className={className}
      style={!isVisible ? { minHeight } : undefined}
    >
      {isVisible ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          {children}
        </motion.div>
      ) : (
        fallback ?? (
          <div
            className="animate-pulse bg-[#E0E0E2] dark:bg-[#2A2A2E] rounded-xl"
            style={{ height: minHeight }}
          />
        )
      )}
    </div>
  );
}
"""))

# ============================================================
# components/common/index.ts (updated)
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
export { default as StaticPage } from "./StaticPage";
export { default as ThemeProvider } from "./ThemeProvider";
export { default as ThemeToggle } from "./ThemeToggle";
export { default as JsonLd } from "./JsonLd";
export { default as ToastContainer } from "./ToastContainer";
export { default as Skeleton } from "./Skeleton";
export { default as ProductCardSkeleton } from "./ProductCardSkeleton";
export { default as ErrorBoundary } from "./ErrorBoundary";
export default from "./KeyboardShortcuts";
"""))

# ============================================================
# components/common/index.ts (correct)
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
export { default as StaticPage } from "./StaticPage";
export { default as ThemeProvider } from "./ThemeProvider";
export { default as ThemeToggle } from "./ThemeToggle";
export { default as JsonLd } from "./JsonLd";
export { default as ToastContainer } from "./ToastContainer";
export { default as Skeleton } from "./Skeleton";
export { default as ProductCardSkeleton } from "./ProductCardSkeleton";
export { default as ErrorBoundary } from "./ErrorBoundary";
export { default as KeyboardShortcuts } from "./KeyboardShortcuts";
export { default as OfflineBanner } from "./OfflineBanner";
export { default as FontLoader } from "./FontLoader";
export { default as SmartImage } from "./SmartImage";
export { default as LoadingScreen } from "./LoadingScreen";
export { default as ProgressBar } from "./ProgressBar";
export { default as LazySection } from "./LazySection";
"""))

# ============================================================
# app/[locale]/page.tsx — استفاده از LazySection برای بخش‌های پایین
# ============================================================
files.append(("app/[locale]/page.tsx", """import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import {
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
} from "@/lib/data";
import {
  HeroSlider,
  ServiceBadges,
  CategoryCircles,
  AmazingOffer,
  ProductSection,
  BrandLogos,
  BlogPreview,
  Newsletter,
} from "@/components/home";
import {
  StatsCounter,
  TrustBadges,
  Guarantees,
  PaymentMethods,
  Testimonials,
} from "@/components/trust";
import JsonLd from "@/components/common/JsonLd";
import LazySection from "@/components/common/LazySection";
import { Container } from "@/components/ui";
import {
  buildMetadata,
  buildOrganizationSchema,
  buildWebSiteSchema,
} from "@/lib/utils";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return buildMetadata({
    locale: typedLocale,
    titleFa: "SourcePixcel | فروشگاه آنلاین مدرن",
    titleEn: "SourcePixcel | Modern Online Store",
    descriptionFa:
      "فروشگاه اینترنتی SourcePixcel — خرید آنلاین موبایل، لپ‌تاپ، لوازم خانگی، پوشاک و لوازم جانبی با ارسال سریع و ضمانت اصالت.",
    descriptionEn:
      "SourcePixcel online store — shop mobile phones, laptops, home appliances, fashion, and accessories with fast shipping and authenticity guarantee.",
    path: "",
  });
}

const HOME_SECTION_SIZE = 5;

export default async function HomePage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  const featured = getFeaturedProducts().slice(0, HOME_SECTION_SIZE);
  const newProducts = getNewProducts().slice(0, HOME_SECTION_SIZE);
  const discounted = getDiscountedProducts().slice(0, HOME_SECTION_SIZE);

  return (
    <>
      <JsonLd data={[buildOrganizationSchema(), buildWebSiteSchema()]} />
      <Container className="py-4 space-y-4 md:space-y-5">
        {/* Above the fold — always render */}
        <HeroSlider locale={typedLocale} />
        <ServiceBadges locale={typedLocale} />
        <CategoryCircles locale={typedLocale} />
        <AmazingOffer locale={typedLocale} />

        {featured.length > 0 && (
          <ProductSection
            titleFa="پیشنهاد ویژه"
            titleEn="Featured Products"
            products={featured}
            locale={typedLocale}
            seeAllHref="/search?featured=1"
          />
        )}

        {newProducts.length > 0 && (
          <ProductSection
            titleFa="جدیدترین‌ها"
            titleEn="New Arrivals"
            products={newProducts}
            locale={typedLocale}
            seeAllHref="/search?new=1"
          />
        )}

        {/* Below the fold — lazy load */}
        <LazySection minHeight={300}>
          <BrandLogos locale={typedLocale} />
        </LazySection>

        {discounted.length > 0 && (
          <LazySection minHeight={400}>
            <ProductSection
              titleFa="تخفیف‌دارها"
              titleEn="Discounted"
              products={discounted}
              locale={typedLocale}
              seeAllHref="/search?discount=1"
            />
          </LazySection>
        )}

        <LazySection minHeight={250}>
          <Guarantees locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={150}>
          <StatsCounter locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={250}>
          <TrustBadges locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={150}>
          <PaymentMethods locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={350}>
          <Testimonials locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={350}>
          <BlogPreview locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={200}>
          <Newsletter locale={typedLocale} />
        </LazySection>
      </Container>
    </>
  );
}
"""))

# ============================================================
# components/product/ProductCard.tsx — memoized for performance
# ============================================================
files.append(("components/product/ProductCard.tsx", """"use client";

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
"""))

# ============================================================
# app/[locale]/layout.tsx — optimized
# ============================================================
files.append(("app/[locale]/layout.tsx", """import dynamic from "next/dynamic";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import FontLoader from "@/components/common/FontLoader";
import type { Locale } from "@/lib/types";

// Lazy load non-critical components
const BottomNav = dynamic(() => import("@/components/layout/BottomNav"), {
  ssr: false,
});
const ToastContainer = dynamic(
  () => import("@/components/common/ToastContainer"),
  { ssr: false }
);
const KeyboardShortcuts = dynamic(
  () => import("@/components/common/KeyboardShortcuts"),
  { ssr: false }
);
const OfflineBanner = dynamic(
  () => import("@/components/common/OfflineBanner"),
  { ssr: false }
);

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <div
      dir={locale === "fa" ? "rtl" : "ltr"}
      lang={locale}
      className="font-sans"
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      <FontLoader />
      <Header locale={typedLocale} />
      <main style={{ flex: 1 }} className="pb-16 lg:pb-0">
        {children}
      </main>
      <Footer locale={typedLocale} />
      <BottomNav locale={typedLocale} />
      <ToastContainer />
      <KeyboardShortcuts locale={typedLocale} />
      <OfflineBanner locale={typedLocale} />
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 35: Performance Optimization")
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
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Test performance:")
        print("     - Open http://localhost:3000/fa")
        print("     - Press F12 → Lighthouse tab")
        print("     - Click 'Analyze page load'")
        print("\nYou should see:")
        print("  ✓ Better Lighthouse score (>90)")
        print("  ✓ Lazy loaded below-fold sections")
        print("  ✓ Memoized ProductCards (no re-renders)")
        print("  ✓ Code splitting (framer-motion, lucide separate)")
        print("  ✓ Long-term caching headers")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()