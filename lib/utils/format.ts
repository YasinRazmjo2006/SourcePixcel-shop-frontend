// lib/utils/format.ts
import type { Locale } from "@/lib/types";

// ─── Price Formatting ─────────────────────────────────────────────────────────

/**
 * Format a number as a price with thousand separators.
 * For fa: uses Persian digits (۱۲۳,۴۵۶)
 * For en: uses English digits (123,456)
 */
export function formatPrice(price: number, locale: Locale = "fa"): string {
  if (locale === "fa") {
    return price.toLocaleString("fa-IR");
  }
  return price.toLocaleString("en-US");
}

/**
 * Format a price with currency label.
 */
export function formatPriceWithCurrency(
  price: number,
  locale: Locale = "fa"
): string {
  const formatted = formatPrice(price, locale);
  return locale === "fa" ? `${formatted} تومان` : `${formatted} Toman`;
}

// ─── Discount ─────────────────────────────────────────────────────────────────

/**
 * Calculate final price after discount.
 */
export function calcFinalPrice(price: number, discountPercent: number): number {
  return Math.round(price * (1 - discountPercent / 100));
}

/**
 * Format discount percentage with percent sign.
 */
export function formatDiscount(percent: number, locale: Locale = "fa"): string {
  const num = locale === "fa" ? percent.toLocaleString("fa-IR") : percent.toString();
  return `${num}٪`;
}

// ─── Rating ───────────────────────────────────────────────────────────────────

/**
 * Format rating with one decimal place.
 */
export function formatRating(rating: number, locale: Locale = "fa"): string {
  const fixed = rating.toFixed(1);
  if (locale === "fa") {
    return fixed.replace(/\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]);
  }
  return fixed;
}

/**
 * Format review count.
 */
export function formatReviewCount(count: number, locale: Locale = "fa"): string {
  if (locale === "fa") {
    return count.toLocaleString("fa-IR");
  }
  return count.toLocaleString("en-US");
}

// ─── Text ─────────────────────────────────────────────────────────────────────

/**
 * Truncate text to a maximum length with ellipsis.
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + "...";
}

/**
 * Get the localized title of a product.
 */
export function getProductTitle(
  product: { titleFa: string; titleEn: string },
  locale: Locale
): string {
  return locale === "fa" ? product.titleFa : product.titleEn;
}

/**
 * Get the localized category name.
 */
export function getCategoryName(
  category: { nameFa: string; nameEn: string },
  locale: Locale
): string {
  return locale === "fa" ? category.nameFa : category.nameEn;
}

/**
 * Get the localized brand name.
 */
export function getBrandName(
  brand: { nameFa: string; nameEn: string },
  locale: Locale
): string {
  return locale === "fa" ? brand.nameFa : brand.nameEn;
}

// ─── Date ─────────────────────────────────────────────────────────────────────

/**
 * Format a date in Jalali (fa) or Gregorian (en).
 */
export function formatDate(date: Date | string | number, locale: Locale = "fa"): string {
  const d = new Date(date);
  if (locale === "fa") {
    return new Intl.DateTimeFormat("fa-IR", {
      year: "numeric",
      month: "long",
      day: "numeric",
    }).format(d);
  }
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(d);
}

// ─── URL ──────────────────────────────────────────────────────────────────────

/**
 * Build a localized URL.
 */
export function localePath(locale: Locale, path: string): string {
  const cleanPath = path.startsWith("/") ? path : `/${path}`;
  return `/${locale}${cleanPath === "/" ? "" : cleanPath}`;
}

// ─── Class Names ──────────────────────────────────────────────────────────────

/**
 * Simple classnames joiner (like clsx).
 */
export function cn(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(" ");
}

// ─── Stock ────────────────────────────────────────────────────────────────────

/**
 * Get stock status label.
 */
export function getStockLabel(inStock: boolean, locale: Locale = "fa"): string {
  if (inStock) {
    return locale === "fa" ? "موجود" : "In stock";
  }
  return locale === "fa" ? "ناموجود" : "Out of stock";
}

// ─── Scroll ───────────────────────────────────────────────────────────────────

/**
 * Scroll to top of page smoothly.
 */
export function scrollToTop(): void {
  if (typeof window !== "undefined") {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}
