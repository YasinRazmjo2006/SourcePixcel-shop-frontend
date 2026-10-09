# 04_utils.py
# ساخت توابع کمکی پروژه SourcePixcel
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/utils/format.ts
# ============================================================
files.append(("lib/utils/format.ts", """// lib/utils/format.ts
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
    return fixed.replace(/\\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]);
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
"""))

# ============================================================
# lib/utils/validators.ts
# ============================================================
files.append(("lib/utils/validators.ts", """// lib/utils/validators.ts

// ─── Iranian Mobile Number ────────────────────────────────────────────────────

/**
 * Validate Iranian mobile number.
 * Format: 09XXXXXXXXX (11 digits, starts with 09)
 */
export function isValidIranianMobile(mobile: string): boolean {
  const cleaned = mobile.replace(/[\\s\\-()]/g, "");
  return /^09\\d{9}$/.test(cleaned);
}

/**
 * Normalize Iranian mobile number (keep only digits).
 */
export function normalizeMobile(mobile: string): string {
  return mobile.replace(/[^0-9]/g, "");
}

/**
 * Format Iranian mobile for display: 0912 345 6789
 */
export function formatMobileDisplay(mobile: string): string {
  const cleaned = normalizeMobile(mobile);
  if (cleaned.length !== 11) return mobile;
  return `${cleaned.slice(0, 4)} ${cleaned.slice(4, 7)} ${cleaned.slice(7)}`;
}

// ─── Email ────────────────────────────────────────────────────────────────────

/**
 * Validate email address.
 */
export function isValidEmail(email: string): boolean {
  return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email);
}

// ─── National ID (Melli Code) ─────────────────────────────────────────────────

/**
 * Validate Iranian national ID (10 digits with checksum).
 */
export function isValidIranianNationalId(code: string): boolean {
  const cleaned = code.replace(/[^0-9]/g, "");
  if (cleaned.length !== 10) return false;
  if (/^(\\d)\\1{9}$/.test(cleaned)) return false;

  const check = parseInt(cleaned[9], 10);
  let sum = 0;
  for (let i = 0; i < 9; i++) {
    sum += parseInt(cleaned[i], 10) * (10 - i);
  }
  const remainder = sum % 11;
  return remainder < 2 ? check === remainder : check === 11 - remainder;
}

// ─── Postal Code ──────────────────────────────────────────────────────────────

/**
 * Validate Iranian postal code (10 digits).
 */
export function isValidIranianPostalCode(code: string): boolean {
  const cleaned = code.replace(/[^0-9]/g, "");
  return /^\\d{10}$/.test(cleaned);
}

// ─── Password ─────────────────────────────────────────────────────────────────

/**
 * Check password strength.
 * Returns: 'weak' | 'medium' | 'strong'
 */
export function getPasswordStrength(password: string): "weak" | "medium" | "strong" {
  if (password.length < 6) return "weak";
  
  let score = 0;
  if (password.length >= 8) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++;
  
  if (score >= 4) return "strong";
  if (score >= 2) return "medium";
  return "weak";
}

/**
 * Validate password (minimum 6 characters).
 */
export function isValidPassword(password: string): boolean {
  return password.length >= 6;
}
"""))

# ============================================================
# lib/utils/index.ts (barrel export)
# ============================================================
files.append(("lib/utils/index.ts", """// lib/utils/index.ts
export {
  formatPrice,
  formatPriceWithCurrency,
  calcFinalPrice,
  formatDiscount,
  formatRating,
  formatReviewCount,
  truncate,
  getProductTitle,
  getCategoryName,
  getBrandName,
  formatDate,
  localePath,
  cn,
  getStockLabel,
  scrollToTop,
} from "./format";

export {
  isValidIranianMobile,
  normalizeMobile,
  formatMobileDisplay,
  isValidEmail,
  isValidIranianNationalId,
  isValidIranianPostalCode,
  getPasswordStrength,
  isValidPassword,
} from "./validators";
"""))

# ============================================================
# lib/data/iran-provinces.ts (for later use)
# ============================================================
files.append(("lib/data/iran-provinces.ts", """// lib/data/iran-provinces.ts
// List of Iranian provinces and major cities (for shipping forms)

export interface Province {
  id: string;
  nameFa: string;
  nameEn: string;
  cities: { id: string; nameFa: string; nameEn: string }[];
}

export const iranProvinces: Province[] = [
  {
    id: "tehran",
    nameFa: "تهران",
    nameEn: "Tehran",
    cities: [
      { id: "tehran", nameFa: "تهران", nameEn: "Tehran" },
      { id: "karaj", nameFa: "کرج", nameEn: "Karaj" },
      { id: "varamin", nameFa: "ورامین", nameEn: "Varamin" },
      { id: "shahriar", nameFa: "شهریار", nameEn: "Shahriar" },
    ],
  },
  {
    id: "isfahan",
    nameFa: "اصفهان",
    nameEn: "Isfahan",
    cities: [
      { id: "isfahan", nameFa: "اصفهان", nameEn: "Isfahan" },
      { id: "kashan", nameFa: "کاشان", nameEn: "Kashan" },
      { id: "najafabad", nameFa: "نجف‌آباد", nameEn: "Najafabad" },
    ],
  },
  {
    id: "fars",
    nameFa: "فارس",
    nameEn: "Fars",
    cities: [
      { id: "shiraz", nameFa: "شیراز", nameEn: "Shiraz" },
      { id: "marvdasht", nameFa: "مرودشت", nameEn: "Marvdasht" },
      { id: "jahrom", nameFa: "جهرم", nameEn: "Jahrom" },
    ],
  },
  {
    id: "khorasan-razavi",
    nameFa: "خراسان رضوی",
    nameEn: "Khorasan Razavi",
    cities: [
      { id: "mashhad", nameFa: "مشهد", nameEn: "Mashhad" },
      { id: "neyshabur", nameFa: "نیشابور", nameEn: "Neyshabur" },
      { id: "sabzevar", nameFa: "سبزوار", nameEn: "Sabzevar" },
    ],
  },
  {
    id: "azerbaijan-east",
    nameFa: "آذربایجان شرقی",
    nameEn: "East Azerbaijan",
    cities: [
      { id: "tabriz", nameFa: "تبریز", nameEn: "Tabriz" },
      { id: "maragheh", nameFa: "مراغه", nameEn: "Maragheh" },
      { id: "marand", nameFa: "مرند", nameEn: "Marand" },
    ],
  },
  {
    id: "khuzestan",
    nameFa: "خوزستان",
    nameEn: "Khuzestan",
    cities: [
      { id: "ahvaz", nameFa: "اهواز", nameEn: "Ahvaz" },
      { id: "abadan", nameFa: "آبادان", nameEn: "Abadan" },
      { id: "dezful", nameFa: "دزفول", nameEn: "Dezful" },
    ],
  },
  {
    id: "gilan",
    nameFa: "گیلان",
    nameEn: "Gilan",
    cities: [
      { id: "rasht", nameFa: "رشت", nameEn: "Rasht" },
      { id: "anzali", nameFa: "انزلی", nameEn: "Anzali" },
      { id: "lahijan", nameFa: "لاهیجان", nameEn: "Lahijan" },
    ],
  },
  {
    id: "mazandaran",
    nameFa: "مازندران",
    nameEn: "Mazandaran",
    cities: [
      { id: "sari", nameFa: "ساری", nameEn: "Sari" },
      { id: "babol", nameFa: "بابل", nameEn: "Babol" },
      { id: "amol", nameFa: "آمل", nameEn: "Amol" },
    ],
  },
];

export const getProvinceById = (id: string) =>
  iranProvinces.find((p) => p.id === id);

export const getCitiesByProvince = (provinceId: string) =>
  getProvinceById(provinceId)?.cities ?? [];
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 04: Utils")
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
        print("Next: run 05_header.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()