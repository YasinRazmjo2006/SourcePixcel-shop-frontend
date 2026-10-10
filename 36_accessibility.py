# 36_accessibility.py
# بهبود دسترسی‌پذیری (A11y) در کل سایت
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/a11y/SkipLink.tsx — پرش به محتوا
# ============================================================
files.append(("components/a11y/SkipLink.tsx", """"use client";

import { useEffect, useState } from "react";

interface SkipLinkProps {
  locale?: "fa" | "en";
}

/**
 * SkipLink — allows keyboard users to skip navigation
 * and jump directly to main content.
 */
export default function SkipLink({ locale = "fa" }: SkipLinkProps) {
  const isFa = locale === "fa";
  const [isFocused, setIsFocused] = useState(false);

  return (
    <a
      href="#main-content"
      onFocus={() => setIsFocused(true)}
      onBlur={() => setIsFocused(false)}
      className={`fixed top-0 z-[9999] bg-[#EF4056] text-white text-[13px] font-bold px-4 py-3 rounded-b-lg shadow-lg transition-transform duration-200 ${
        isFocused ? "translate-y-0" : "-translate-y-full"
      }`}
      style={{ [isFa ? "right" : "left"]: 16 }}
    >
      {isFa ? "پرش به محتوای اصلی" : "Skip to main content"}
    </a>
  );
}
"""))

# ============================================================
# components/a11y/ScreenReaderAnnouncer.tsx
# ============================================================
files.append(("components/a11y/ScreenReaderAnnouncer.tsx", """"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

/**
 * ScreenReaderAnnouncer — announces page changes to screen readers.
 * Improves SPA navigation accessibility.
 */
export default function ScreenReaderAnnouncer() {
  const pathname = usePathname();
  const [announcement, setAnnouncement] = useState("");

  useEffect(() => {
    // Extract page name from pathname
    const segments = pathname.split("/").filter(Boolean);
    const page = segments[segments.length - 1] ?? "home";
    setAnnouncement(`Navigated to ${page}`);
  }, [pathname]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  );
}
"""))

# ============================================================
# components/a11y/FocusTrap.tsx — تله فوکوس برای modal
# ============================================================
files.append(("components/a11y/FocusTrap.tsx", """"use client";

import { useEffect, useRef } from "react";

interface FocusTrapProps {
  children: React.ReactNode;
  active?: boolean;
  onEscape?: () => void;
}

/**
 * FocusTrap — traps focus inside a container (for modals/dialogs).
 * Also handles Escape key.
 */
export default function FocusTrap({
  children,
  active = true,
  onEscape,
}: FocusTrapProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!active) return;

    const container = containerRef.current;
    if (!container) return;

    // Store previously focused element
    const previouslyFocused = document.activeElement as HTMLElement;

    // Focus first focusable element
    const focusableSelector =
      'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';
    const focusableElements = container.querySelectorAll<HTMLElement>(
      focusableSelector
    );
    if (focusableElements.length > 0) {
      focusableElements[0].focus();
    }

    // Trap focus
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && onEscape) {
        e.preventDefault();
        onEscape();
        return;
      }

      if (e.key !== "Tab") return;

      const focusables = container.querySelectorAll<HTMLElement>(
        focusableSelector
      );
      if (focusables.length === 0) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      previouslyFocused?.focus?.();
    };
  }, [active, onEscape]);

  return <div ref={containerRef}>{children}</div>;
}
"""))

# ============================================================
# components/a11y/VisuallyHidden.tsx
# ============================================================
files.append(("components/a11y/VisuallyHidden.tsx", """interface VisuallyHiddenProps {
  children: React.ReactNode;
  as?: "span" | "div";
}

/**
 * VisuallyHidden — hides content visually but keeps it for screen readers.
 */
export default function VisuallyHidden({
  children,
  as: Tag = "span",
}: VisuallyHiddenProps) {
  return (
    <Tag className="sr-only">
      {children}
    </Tag>
  );
}
"""))

# ============================================================
# components/a11y/index.ts
# ============================================================
files.append(("components/a11y/index.ts", """// components/a11y/index.ts
export { default as SkipLink } from "./SkipLink";
export { default as ScreenReaderAnnouncer } from "./ScreenReaderAnnouncer";
export { default as FocusTrap } from "./FocusTrap";
export { default as VisuallyHidden } from "./VisuallyHidden";
"""))

# ============================================================
# app/globals.css — بهبود sr-only و focus
# ============================================================
files.append(("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

/* ═══════════════════════════════════════════════════════════════
   ACCESSIBILITY
   ═══════════════════════════════════════════════════════════════ */

/* Screen reader only */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Focus visible — visible outline for keyboard users */
*:focus {
  outline: none;
}

*:focus-visible {
  outline: 3px solid #EF4056;
  outline-offset: 2px;
  border-radius: 4px;
  transition: outline-offset 0.15s ease;
}

/* Better focus ring for dark backgrounds */
.dark *:focus-visible {
  outline-color: #FF6B7D;
}

/* Focus ring for buttons */
button:focus-visible,
a:focus-visible,
[role="button"]:focus-visible {
  outline: 3px solid #EF4056;
  outline-offset: 2px;
}

/* Focus ring for inputs */
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
  outline: 3px solid #EF4056;
  outline-offset: 0;
  border-color: #EF4056;
}

/* Reduce motion for users who prefer it */
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

/* High contrast mode support */
@media (prefers-contrast: more) {
  :root {
    --border: #000000;
  }

  body {
    color: #000000;
  }

  a,
  button {
    text-decoration: underline;
  }
}

/* Dark mode contrast improvements */
@media (prefers-contrast: more) and (prefers-color-scheme: dark) {
  body {
    color: #FFFFFF;
  }

  a,
  button {
    text-decoration: underline;
  }
}

/* ═══════════════════════════════════════════════════════════════
   ROOT VARIABLES
   ═══════════════════════════════════════════════════════════════ */

:root {
  --spacing-unit: 0.25rem;
  --text-2xs: 0.625rem;
  --text-xs: 0.75rem;
  --text-sm: 0.8125rem;
  --text-base: 0.875rem;
  --text-md: 0.9375rem;
  --text-lg: 1.0625rem;
  --text-xl: 1.1875rem;
  --text-2xl: 1.375rem;
  --text-3xl: 1.625rem;
  --text-4xl: 2rem;
  --leading-tight: 1.3;
  --leading-snug: 1.45;
  --leading-normal: 1.6;
  --leading-relaxed: 1.75;
  --leading-persian: 1.9;
  --leading-loose: 2;
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

[dir="rtl"],
[dir="rtl"] body {
  font-family: var(--font-vazirmatn), system-ui, Tahoma, Arial, sans-serif;
  line-height: var(--leading-persian);
  letter-spacing: 0;
  word-spacing: 0.05em;
}

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

.text-balance {
  text-wrap: balance;
}

.text-pretty {
  text-wrap: pretty;
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
# app/[locale]/layout.tsx — اضافه کردن SkipLink و Announcer
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BottomNav from "@/components/layout/BottomNav";
import ToastContainer from "@/components/common/ToastContainer";
import KeyboardShortcuts from "@/components/common/KeyboardShortcuts";
import OfflineBanner from "@/components/common/OfflineBanner";
import FontLoader from "@/components/common/FontLoader";
import SkipLink from "@/components/a11y/SkipLink";
import ScreenReaderAnnouncer from "@/components/a11y/ScreenReaderAnnouncer";
import type { Locale } from "@/lib/types";

export async function generateStaticParams() {
  return [{ locale: "fa" }, { locale: "en" }];
}

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
      <SkipLink locale={typedLocale} />
      <ScreenReaderAnnouncer />
      <FontLoader />
      <Header locale={typedLocale} />
      <main
        id="main-content"
        role="main"
        style={{ flex: 1 }}
        className="pb-16 lg:pb-0"
        tabIndex={-1}
      >
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
# components/layout/Header.tsx — بهبود ARIA
# ============================================================
files.append(("components/layout/Header.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ShoppingCart,
  Heart,
  User,
  Menu,
  X,
  ChevronDown,
  Smartphone,
  Laptop,
  Tablet,
  Headphones,
  Camera,
  Watch,
  Gamepad2,
  Cable,
  Shirt,
  Footprints,
  Home,
  BookOpen,
  GitCompareArrows,
  Search,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore, useWishlistStore, useCompareStore } from "@/lib/stores";
import ThemeToggle from "@/components/common/ThemeToggle";
import { SearchAutocomplete } from "@/components/search";
import { NotificationBell } from "@/components/notifications";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string; "aria-hidden"?: boolean }>> = {
  Smartphone, Laptop, Tablet, Headphones, Camera, Watch,
  Gamepad2, Cable, Shirt, Footprints, Home, BookOpen,
};

interface HeaderProps {
  locale: Locale;
}

export default function Header({ locale }: HeaderProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openCategory, setOpenCategory] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  const totalItems = useCartStore((s) => s.items.reduce((sum, i) => sum + i.quantity, 0));
  const wishlistCount = useWishlistStore((s) => s.ids.length);
  const compareCount = useCompareStore((s) => s.ids.length);

  useEffect(() => { setMounted(true); }, []);
  useEffect(() => {
    setMobileOpen(false);
    setOpenCategory(null);
  }, [pathname]);

  // Close mobile menu on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMobileOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
    search: isFa ? "جستجو" : "Search",
    menu: isFa ? "منو" : "Menu",
    closeMenu: isFa ? "بستن منو" : "Close menu",
    cartItems: isFa ? "کالا در سبد" : "items in cart",
    wishlistItems: isFa ? "کالا در علاقه‌مندی" : "items in wishlist",
    compareItems: isFa ? "کالا در مقایسه" : "items in compare",
    notifications: isFa ? "اعلان‌ها" : "Notifications",
  };

  const swapLocale = (newLocale: Locale) => {
    const rest = pathname.replace(/^\\/(fa|en)/, "");
    return `/${newLocale}${rest}`;
  };

  return (
    <>
      {/* Top thin bar */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 h-10 flex items-center justify-between text-[12px]">
          <div className="flex items-center gap-4">
            <Link
              href={swapLocale(isFa ? "en" : "fa")}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
              aria-label={isFa ? "Switch to English" : "تغییر به فارسی"}
            >
              {isFa ? "English" : "فارسی"}
            </Link>
            <ThemeToggle locale={locale} />
          </div>
          <div className="flex items-center gap-4">
            <Link
              href={`/${locale}/auth/login`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
            >
              {t.login}
            </Link>
            <span className="text-[#E0E0E2] dark:text-[#2A2A2E]" aria-hidden="true">
              |
            </span>
            <NotificationBell locale={locale} variant="top" />
            <Link
              href={`/${locale}/compare`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
              aria-label={`${t.compareItems}: ${compareCount}`}
            >
              <GitCompareArrows size={14} aria-hidden="true" />
              {mounted && compareCount > 0 && (
                <span
                  className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center"
                  aria-hidden="true"
                >
                  {compareCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/account/wishlist`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
              aria-label={`${t.wishlistItems}: ${wishlistCount}`}
            >
              <Heart size={14} aria-hidden="true" />
              {mounted && wishlistCount > 0 && (
                <span
                  className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center"
                  aria-hidden="true"
                >
                  {wishlistCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/cart`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
              aria-label={`${t.cartItems}: ${totalItems}`}
            >
              <ShoppingCart size={14} aria-hidden="true" />
              {mounted && totalItems > 0 && (
                <span
                  className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center"
                  aria-hidden="true"
                >
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* Main header */}
      <header className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          <button
            className="lg:hidden text-[#3F4064] dark:text-[#E5E5EA]"
            onClick={() => setMobileOpen(true)}
            aria-label={t.menu}
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
          >
            <Menu size={24} aria-hidden="true" />
          </button>

          <Link
            href={`/${locale}`}
            className="text-[#EF4056] font-bold text-xl shrink-0"
            aria-label="SourcePixcel — Home"
          >
            SourcePixcel
          </Link>

          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <SearchAutocomplete locale={locale} />
          </div>

          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} aria-hidden="true" />
            <span>{t.account}</span>
          </Link>

          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2] dark:bg-[#2A2A2E]" aria-hidden="true" />

          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors relative"
            aria-label={`${t.cart}: ${totalItems} ${t.cartItems}`}
          >
            <ShoppingCart size={20} aria-hidden="true" />
            <span>{t.cart}</span>
            {mounted && totalItems > 0 && (
              <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold" aria-hidden="true">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* Mega menu */}
        <nav
          className="hidden lg:block border-t border-[#E0E0E2] dark:border-[#2A2A2E]"
          aria-label={isFa ? "منوی اصلی" : "Main navigation"}
        >
          <div className="max-w-[1400px] mx-auto px-4">
            <ul className="flex items-center gap-1 h-12 list-none m-0 p-0">
              {categories.map((cat) => {
                const Icon = ICON_MAP[cat.icon] ?? Cable;
                const isOpen = openCategory === cat.id;
                return (
                  <li
                    key={cat.id}
                    className="relative"
                    onMouseEnter={() => setOpenCategory(cat.id)}
                    onMouseLeave={() => setOpenCategory(null)}
                  >
                    <Link
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                      aria-haspopup={cat.subcategories.length > 0}
                      aria-expanded={isOpen}
                    >
                      <Icon size={16} aria-hidden="true" />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      {cat.subcategories.length > 0 && (
                        <ChevronDown size={12} className="opacity-50" aria-hidden="true" />
                      )}
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        <ul className="list-none m-0 p-0">
                          {cat.subcategories.map((sub) => (
                            <li key={sub.id}>
                              <Link
                                href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                                className="block px-4 py-2 text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
                              >
                                {isFa ? sub.nameFa : sub.nameEn}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        </nav>
      </header>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-[100] lg:hidden"
          role="dialog"
          aria-modal="true"
          aria-label={t.menu}
          id="mobile-menu"
        >
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />
          <div
            className="absolute top-0 bottom-0 bg-white dark:bg-[#1A1A1E] w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button
                onClick={() => setMobileOpen(false)}
                aria-label={t.closeMenu}
              >
                <X size={24} className="text-[#3F4064] dark:text-[#E5E5EA]" aria-hidden="true" />
              </button>
            </div>

            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  {isFa ? "حالت تاریک" : "Dark mode"}
                </span>
                <ThemeToggle locale={locale} />
              </div>

              <div className="mb-4">
                <SearchAutocomplete locale={locale} onClose={() => setMobileOpen(false)} />
              </div>

              <div className="mb-4">
                <Link
                  href={`/${locale}/auth/login`}
                  className="block text-center bg-[#EF4056] text-white rounded-lg py-2 text-sm font-medium"
                >
                  {t.login}
                </Link>
              </div>

              <nav className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] pt-4" aria-label={t.allCategories}>
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                <ul className="list-none m-0 p-0">
                  {categories.map((cat) => {
                    const Icon = ICON_MAP[cat.icon] ?? Cable;
                    return (
                      <li key={cat.id}>
                        <Link
                          href={`/${locale}/category/${cat.slug}`}
                          className="flex items-center gap-3 py-2 text-sm text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056]"
                        >
                          <Icon size={18} aria-hidden="true" />
                          <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </nav>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 36: Accessibility")
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
        print("  3) Test accessibility:")
        print("     - Press Tab on home page → see Skip Link")
        print("     - Use keyboard only to navigate")
        print("     - Check focus rings are visible")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()