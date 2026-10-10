# 34_typography.py
# بهبود Typography و Spacing در کل سایت
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/ui/Typography.tsx — کامپوننت‌های متن استاندارد
# ============================================================
files.append(("components/ui/Typography.tsx", """"use client";

import { cn } from "@/lib/utils";

// ═══════════════════════════════════════════════════════════════
// HEADINGS
// ═══════════════════════════════════════════════════════════════

interface HeadingProps {
  children: React.ReactNode;
  className?: string;
  as?: "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
}

export function H1({ children, className, as: Tag = "h1" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[26px] md:text-[32px] font-black leading-tight tracking-tight text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

export function H2({ children, className, as: Tag = "h2" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[20px] md:text-[24px] font-extrabold leading-snug tracking-tight text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

export function H3({ children, className, as: Tag = "h3" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[16px] md:text-[18px] font-bold leading-normal text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

export function H4({ children, className, as: Tag = "h4" }: HeadingProps) {
  return (
    <Tag
      className={cn(
        "text-[14px] md:text-[15px] font-bold leading-normal text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

// ═══════════════════════════════════════════════════════════════
// TEXT
// ═══════════════════════════════════════════════════════════════

interface TextProps {
  children: React.ReactNode;
  className?: string;
  as?: "p" | "span" | "div";
  size?: "xs" | "sm" | "base" | "lg";
  muted?: boolean;
  weight?: "normal" | "medium" | "semibold" | "bold";
}

export function Text({
  children,
  className,
  as: Tag = "p",
  size = "base",
  muted = false,
  weight = "normal",
}: TextProps) {
  const sizes = {
    xs: "text-[11px] leading-5",
    sm: "text-[12px] leading-6",
    base: "text-[13px] leading-7",
    lg: "text-[14px] md:text-[15px] leading-8",
  };

  const weights = {
    normal: "font-normal",
    medium: "font-medium",
    semibold: "font-semibold",
    bold: "font-bold",
  };

  return (
    <Tag
      className={cn(
        sizes[size],
        weights[weight],
        muted
          ? "text-[#62666D] dark:text-[#A1A3A8]"
          : "text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </Tag>
  );
}

// ═══════════════════════════════════════════════════════════════
// MUTED TEXT
// ═══════════════════════════════════════════════════════════════

export function MutedText({
  children,
  className,
  size = "sm",
}: {
  children: React.ReactNode;
  className?: string;
  size?: "xs" | "sm" | "base";
}) {
  const sizes = {
    xs: "text-[10px] leading-4",
    sm: "text-[11px] leading-5",
    base: "text-[12px] leading-6",
  };

  return (
    <p
      className={cn(
        sizes[size],
        "text-[#A1A3A8] dark:text-[#6B7280]",
        className
      )}
    >
      {children}
    </p>
  );
}

// ═══════════════════════════════════════════════════════════════
// LABEL
// ═══════════════════════════════════════════════════════════════

export function Label({
  children,
  className,
  required,
}: {
  children: React.ReactNode;
  className?: string;
  required?: boolean;
}) {
  return (
    <label
      className={cn(
        "block text-[12px] font-medium text-[#62666D] dark:text-[#A1A3A8] mb-1.5",
        className
      )}
    >
      {children}
      {required && <span className="text-[#EF4056] ml-1">*</span>}
    </label>
  );
}

// ═══════════════════════════════════════════════════════════════
// PRICE TEXT
// ═══════════════════════════════════════════════════════════════

export function PriceText({
  children,
  className,
  size = "base",
  discount,
}: {
  children: React.ReactNode;
  className?: string;
  size?: "sm" | "base" | "lg" | "xl";
  discount?: boolean;
}) {
  const sizes = {
    sm: "text-[13px]",
    base: "text-[15px]",
    lg: "text-[18px]",
    xl: "text-[24px]",
  };

  return (
    <span
      className={cn(
        sizes[size],
        "font-bold tabular-nums",
        discount
          ? "text-[#EF4056]"
          : "text-[#3F4064] dark:text-[#E5E5EA]",
        className
      )}
    >
      {children}
    </span>
  );
}

// ═══════════════════════════════════════════════════════════════
// DIVIDER
// ═══════════════════════════════════════════════════════════════

export function Divider({
  className,
  spacing = "md",
}: {
  className?: string;
  spacing?: "sm" | "md" | "lg";
}) {
  const spacings = {
    sm: "my-3",
    md: "my-4",
    lg: "my-6",
  };

  return (
    <div
      className={cn(
        "border-t border-[#E0E0E2] dark:border-[#2A2A2E]",
        spacings[spacing],
        className
      )}
    />
  );
}

// ═══════════════════════════════════════════════════════════════
// SECTION
// ═══════════════════════════════════════════════════════════════

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  spacing?: "sm" | "md" | "lg";
}

export function Section({
  children,
  className,
  spacing = "md",
}: SectionProps) {
  const spacings = {
    sm: "space-y-3",
    md: "space-y-4",
    lg: "space-y-6",
  };

  return <div className={cn(spacings[spacing], className)}>{children}</div>;
}

// ═══════════════════════════════════════════════════════════════
// CONTAINER
// ═══════════════════════════════════════════════════════════════

export function Container({
  children,
  className,
  size = "default",
}: {
  children: React.ReactNode;
  className?: string;
  size?: "default" | "narrow" | "wide";
}) {
  const sizes = {
    narrow: "max-w-3xl",
    default: "max-w-[1400px]",
    wide: "max-w-[1600px]",
  };

  return (
    <div className={cn("mx-auto px-4 md:px-6", sizes[size], className)}>
      {children}
    </div>
  );
}
"""))

# ============================================================
# components/ui/index.ts (updated)
# ============================================================
files.append(("components/ui/index.ts", """// components/ui/index.ts
export { default as RippleButton } from "./RippleButton";
export { default as AnimatedCheckbox } from "./AnimatedCheckbox";
export { default as AnimatedInput } from "./AnimatedInput";
export { default as Spinner } from "./Spinner";
export { default as DotsLoader } from "./DotsLoader";

export {
  H1,
  H2,
  H3,
  H4,
  Text,
  MutedText,
  Label,
  PriceText,
  Divider,
  Section,
  Container,
} from "./Typography";
"""))

# ============================================================
# app/globals.css — بهبود typography و spacing
# ============================================================
files.append(("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

/* ═══════════════════════════════════════════════════════════════
   ROOT VARIABLES
   ═══════════════════════════════════════════════════════════════ */

:root {
  --spacing-unit: 0.25rem;

  /* Typography scale (perfect fourth — 1.333 ratio) */
  --text-2xs: 0.625rem; /* 10px */
  --text-xs: 0.75rem; /* 12px */
  --text-sm: 0.8125rem; /* 13px */
  --text-base: 0.875rem; /* 14px */
  --text-md: 0.9375rem; /* 15px */
  --text-lg: 1.0625rem; /* 17px */
  --text-xl: 1.1875rem; /* 19px */
  --text-2xl: 1.375rem; /* 22px */
  --text-3xl: 1.625rem; /* 26px */
  --text-4xl: 2rem; /* 32px */

  /* Line heights */
  --leading-tight: 1.3;
  --leading-snug: 1.45;
  --leading-normal: 1.6;
  --leading-relaxed: 1.75;
  --leading-persian: 1.9;
  --leading-loose: 2;

  /* Letter spacing */
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.02em;
}

/* ═══════════════════════════════════════════════════════════════
   BASE
   ═══════════════════════════════════════════════════════════════ */

* {
  box-sizing: border-box;
}

html,
body {
  padding: 0;
  margin: 0;
  background: #F5F5F5;
  color: #3F4064;
  font-family: var(--font-inter), var(--font-vazirmatn), system-ui, sans-serif;
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1, "tnum";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Persian (RTL) */
[dir="rtl"],
[dir="rtl"] body {
  font-family: var(--font-vazirmatn), system-ui, Tahoma, Arial, sans-serif;
  line-height: var(--leading-persian);
  letter-spacing: 0;
  word-spacing: 0.05em;
}

/* English (LTR) */
[dir="ltr"],
[dir="ltr"] body {
  font-family: var(--font-inter), system-ui, -apple-system, sans-serif;
  line-height: var(--leading-normal);
  letter-spacing: var(--tracking-tight);
}

html.dark,
html.dark body {
  background: #0F0F12;
  color: #E5E5EA;
}

/* ═══════════════════════════════════════════════════════════════
   HEADINGS
   ═══════════════════════════════════════════════════════════════ */

h1, h2, h3, h4, h5, h6 {
  margin: 0;
  font-weight: 700;
  color: #3F4064;
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}

h1 { font-weight: 900; letter-spacing: -0.03em; }
h2 { font-weight: 800; letter-spacing: -0.02em; }
h3 { font-weight: 700; }
h4 { font-weight: 700; }

html.dark h1, html.dark h2, html.dark h3,
html.dark h4, html.dark h5, html.dark h6 {
  color: #E5E5EA;
}

[dir="rtl"] h1,
[dir="rtl"] h2,
[dir="rtl"] h3 {
  letter-spacing: 0;
  font-weight: 800;
}

/* ═══════════════════════════════════════════════════════════════
   PARAGRAPHS & LISTS
   ═══════════════════════════════════════════════════════════════ */

p {
  margin: 0;
}

[dir="rtl"] p {
  line-height: var(--leading-persian);
}

[dir="rtl"] li {
  line-height: var(--leading-persian);
}

ul, ol {
  padding-inline-start: 1.5rem;
}

/* ═══════════════════════════════════════════════════════════════
   LINKS & BUTTONS
   ═══════════════════════════════════════════════════════════════ */

a {
  color: inherit;
  text-decoration: none;
  transition: color 0.15s ease;
}

button {
  font-family: inherit;
  cursor: pointer;
  transition: all 0.15s ease;
}

button:disabled {
  cursor: not-allowed;
}

*:focus-visible {
  outline: 2px solid #EF4056;
  outline-offset: 2px;
  border-radius: 6px;
}

*:focus:not(:focus-visible) {
  outline: none;
}

/* ═══════════════════════════════════════════════════════════════
   TEXT UTILITIES
   ═══════════════════════════════════════════════════════════════ */

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

[dir="rtl"] .tabular-nums {
  font-feature-settings: "tnum", "ss01";
}

/* Balanced text wrapping (modern browsers) */
.text-balance {
  text-wrap: balance;
}

.text-pretty {
  text-wrap: pretty;
}

/* Persian numbers */
.persian-nums {
  font-feature-settings: "ss01";
}

/* ═══════════════════════════════════════════════════════════════
   SCROLLBAR
   ═══════════════════════════════════════════════════════════════ */

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #F5F5F5;
}

html.dark ::-webkit-scrollbar-track {
  background: #1A1A1E;
}

::-webkit-scrollbar-thumb {
  background: #E0E0E2;
  border-radius: 4px;
}

html.dark ::-webkit-scrollbar-thumb {
  background: #3A3A40;
}

::-webkit-scrollbar-thumb:hover {
  background: #A1A3A8;
}

html.dark ::-webkit-scrollbar-thumb:hover {
  background: #52525A;
}

/* ═══════════════════════════════════════════════════════════════
   SELECTION
   ═══════════════════════════════════════════════════════════════ */

::selection {
  background: #EF4056;
  color: white;
}

::-moz-selection {
  background: #EF4056;
  color: white;
}

/* ═══════════════════════════════════════════════════════════════
   LINE CLAMP
   ═══════════════════════════════════════════════════════════════ */

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ═══════════════════════════════════════════════════════════════
   PROSE
   ═══════════════════════════════════════════════════════════════ */

.prose {
  color: #62666D;
  line-height: var(--leading-loose);
}

[dir="rtl"] .prose {
  line-height: var(--leading-persian);
}

.prose p {
  margin-bottom: 1.25rem;
}

.prose h2 {
  font-size: var(--text-2xl);
  font-weight: 800;
  color: #3F4064;
  margin-top: 2rem;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.prose h3 {
  font-size: var(--text-lg);
  font-weight: 700;
  color: #3F4064;
  margin-top: 1.75rem;
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.prose ul,
.prose ol {
  margin-bottom: 1.25rem;
  padding-inline-start: 1.5rem;
}

.prose li {
  margin-bottom: 0.5rem;
}

.prose strong {
  font-weight: 700;
  color: #3F4064;
}

.prose blockquote {
  border-inline-start: 3px solid #EF4056;
  padding-inline-start: 1rem;
  margin: 1.5rem 0;
  font-style: italic;
  color: #62666D;
}

html.dark .prose {
  color: #A1A3A8;
}

html.dark .prose h2,
html.dark .prose h3,
html.dark .prose strong {
  color: #E5E5EA;
}

/* ═══════════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════════ */

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes scale-in {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes shimmer {
  100% { transform: translateX(100%); }
}

.animate-fade-in { animation: fade-in 0.2s ease-out; }
.animate-slide-up { animation: slide-up 0.3s ease-out; }
.animate-scale-in { animation: scale-in 0.2s ease-out; }

.skeleton-shimmer {
  position: relative;
  overflow: hidden;
}

.skeleton-shimmer::after {
  content: "";
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
  animation: shimmer 1.5s infinite;
}

html.dark .skeleton-shimmer::after {
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
}

/* Smooth scroll */
html {
  scroll-behavior: smooth;
  scroll-padding-top: 80px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ═══════════════════════════════════════════════════════════════
   PRINT
   ═══════════════════════════════════════════════════════════════ */

@media print {
  @page {
    margin: 1cm;
    size: A4;
  }

  body {
    background: white !important;
    color: black !important;
  }

  body * {
    visibility: hidden;
  }

  .print-content,
  .print-content * {
    visibility: visible;
  }

  .print-content {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    background: white !important;
    border: none !important;
    padding: 20px !important;
    color: black !important;
  }

  .no-print {
    display: none !important;
  }

  .print-content h1, .print-content h2, .print-content h3,
  .print-content h4, .print-content p, .print-content td,
  .print-content th, .print-content span, .print-content div {
    color: black !important;
  }

  .print-content table {
    border-collapse: collapse;
    width: 100%;
  }

  .print-content th,
  .print-content td {
    border: 1px solid #ddd;
    padding: 8px;
  }

  .print-content thead {
    background: #f5f5f5 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .print-content > div {
    page-break-inside: avoid;
  }
}
"""))

# ============================================================
# app/[locale]/page.tsx (updated with Container + Section)
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

        <BrandLogos locale={typedLocale} />

        {discounted.length > 0 && (
          <ProductSection
            titleFa="تخفیف‌دارها"
            titleEn="Discounted"
            products={discounted}
            locale={typedLocale}
            seeAllHref="/search?discount=1"
          />
        )}

        <Guarantees locale={typedLocale} />
        <StatsCounter locale={typedLocale} />
        <TrustBadges locale={typedLocale} />
        <PaymentMethods locale={typedLocale} />
        <Testimonials locale={typedLocale} />
        <BlogPreview locale={typedLocale} />
        <Newsletter locale={typedLocale} />
      </Container>
    </>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 34: Typography & Spacing")
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
        print("  3) Open http://localhost:3000/fa")
        print("\nYou should notice:")
        print("  ✓ Better heading hierarchy")
        print("  ✓ Persian text has more line-height")
        print("  ✓ Tabular numbers in prices")
        print("  ✓ Consistent spacing between sections")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()