# 18_dark_mode.py
# ساخت حالت تاریک
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/theme.ts
# ============================================================
files.append(("lib/stores/theme.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type ThemeMode = "light" | "dark";

interface ThemeState {
  mode: ThemeMode;
  setMode: (mode: ThemeMode) => void;
  toggle: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      mode: "light",

      setMode: (mode) => {
        set({ mode });
        if (typeof document !== "undefined") {
          document.documentElement.classList.toggle("dark", mode === "dark");
        }
      },

      toggle: () => {
        const next = get().mode === "light" ? "dark" : "light";
        get().setMode(next);
      },
    }),
    { name: "sourcepixcel-theme" }
  )
);
"""))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", """// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
"""))

# ============================================================
# components/common/ThemeProvider.tsx
# ============================================================
files.append(("components/common/ThemeProvider.tsx", """"use client";

import { useEffect } from "react";
import { useThemeStore } from "@/lib/stores";

export default function ThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const mode = useThemeStore((s) => s.mode);

  useEffect(() => {
    // Apply theme on mount
    document.documentElement.classList.toggle("dark", mode === "dark");
  }, [mode]);

  return <>{children}</>;
}
"""))

# ============================================================
# components/common/ThemeToggle.tsx
# ============================================================
files.append(("components/common/ThemeToggle.tsx", """"use client";

import { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";
import { useThemeStore } from "@/lib/stores";

interface ThemeToggleProps {
  locale?: "fa" | "en";
}

export default function ThemeToggle({ locale = "fa" }: ThemeToggleProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const mode = useThemeStore((s) => s.mode);
  const toggle = useThemeStore((s) => s.toggle);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="w-7 h-7 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E]" />
    );
  }

  return (
    <button
      onClick={toggle}
      aria-label={isFa ? "تغییر تم" : "Toggle theme"}
      title={
        mode === "light"
          ? isFa
            ? "حالت تاریک"
            : "Dark mode"
          : isFa
          ? "حالت روشن"
          : "Light mode"
      }
      className="w-7 h-7 rounded-full flex items-center justify-center text-[#62666D] hover:text-[#EF4056] transition-colors"
    >
      {mode === "light" ? <Moon size={14} /> : <Sun size={14} />}
    </button>
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
"""))

# ============================================================
# app/globals.css (updated with dark mode)
# ============================================================
files.append(("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  box-sizing: border-box;
}

html,
body {
  padding: 0;
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
  background: #F5F5F5;
  color: #3F4064;
  transition: background-color 0.2s ease, color 0.2s ease;
}

html.dark,
html.dark body {
  background: #0F0F12;
  color: #E5E5EA;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  cursor: pointer;
}

[dir="rtl"] {
  text-align: right;
}

[dir="ltr"] {
  text-align: left;
}

/* Scrollbar */
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
"""))

# ============================================================
# tailwind.config.ts (updated with darkMode: 'class')
# ============================================================
files.append(("tailwind.config.ts", """import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#EF4056",
        secondary: "#00BFFF",
        dark: "#3F4064",
        muted: "#62666D",
        light: "#A1A3A8",
        border: "#E0E0E2",
        bg: "#F5F5F5",
      },
    },
  },
  plugins: [],
};
export default config;
"""))

# ============================================================
# app/layout.tsx (wrapped with ThemeProvider)
# ============================================================
files.append(("app/layout.tsx", """import "./globals.css";
import ThemeProvider from "@/components/common/ThemeProvider";

export const metadata = {
  title: "SourcePixcel",
  description: "Bilingual e-commerce store (Persian/English)",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fa" dir="rtl" suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  const stored = localStorage.getItem('sourcepixcel-theme');
                  if (stored) {
                    const parsed = JSON.parse(stored);
                    if (parsed && parsed.state && parsed.state.mode === 'dark') {
                      document.documentElement.classList.add('dark');
                    }
                  }
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
"""))

# ============================================================
# components/layout/Header.tsx (updated with ThemeToggle + dark mode classes)
# ============================================================
files.append(("components/layout/Header.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Search,
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
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore, useWishlistStore, useCompareStore } from "@/lib/stores";
import ThemeToggle from "@/components/common/ThemeToggle";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
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

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    searchPlaceholder: isFa ? "جستجو در SourcePixcel" : "Search in SourcePixcel",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
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
            <span className="text-[#E0E0E2] dark:text-[#2A2A2E]">|</span>
            <Link
              href={`/${locale}/compare`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <GitCompareArrows size={14} />
              {mounted && compareCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {compareCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/account/wishlist`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <Heart size={14} />
              {mounted && wishlistCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {wishlistCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/cart`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <ShoppingCart size={14} />
              {mounted && totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          <button
            className="lg:hidden text-[#3F4064] dark:text-[#E5E5EA]"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>

          <Link href={`/${locale}`} className="text-[#EF4056] font-bold text-xl shrink-0">
            SourcePixcel
          </Link>

          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <div className="relative">
              <input
                type="text"
                placeholder={t.searchPlaceholder}
                className="w-full h-10 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-sm text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] transition-colors"
                style={{ paddingRight: isFa ? 40 : 16, paddingLeft: isFa ? 16 : 40 }}
              />
              <Search
                size={18}
                className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
                style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
              />
            </div>
          </div>

          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} />
            <span>{t.account}</span>
          </Link>

          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2] dark:bg-[#2A2A2E]" />

          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors relative"
          >
            <ShoppingCart size={20} />
            <span>{t.cart}</span>
            {mounted && totalItems > 0 && (
              <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* Mega menu */}
        <div className="hidden lg:block border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
          <div className="max-w-[1400px] mx-auto px-4">
            <nav className="flex items-center gap-1 h-12">
              {categories.map((cat) => {
                const Icon = ICON_MAP[cat.icon] ?? Cable;
                const isOpen = openCategory === cat.id;
                return (
                  <div
                    key={cat.id}
                    className="relative"
                    onMouseEnter={() => setOpenCategory(cat.id)}
                    onMouseLeave={() => setOpenCategory(null)}
                  >
                    <Link
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                    >
                      <Icon size={16} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      <ChevronDown size={12} className="opacity-50" />
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        {cat.subcategories.map((sub) => (
                          <Link
                            key={sub.id}
                            href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                            className="block px-4 py-2 text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
                          >
                            {isFa ? sub.nameFa : sub.nameEn}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-[100] lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
          />
          <div
            className="absolute top-0 bottom-0 bg-white dark:bg-[#1A1A1E] w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button onClick={() => setMobileOpen(false)} aria-label="Close menu">
                <X size={24} className="text-[#3F4064] dark:text-[#E5E5EA]" />
              </button>
            </div>

            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  {isFa ? "حالت تاریک" : "Dark mode"}
                </span>
                <ThemeToggle locale={locale} />
              </div>

              <div className="relative mb-4">
                <input
                  type="text"
                  placeholder={t.searchPlaceholder}
                  className="w-full h-10 px-4 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-sm"
                />
              </div>

              <div className="mb-4">
                <Link
                  href={`/${locale}/auth/login`}
                  className="block text-center bg-[#EF4056] text-white rounded-lg py-2 text-sm font-medium"
                >
                  {t.login}
                </Link>
              </div>

              <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] pt-4">
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                {categories.map((cat) => {
                  const Icon = ICON_MAP[cat.icon] ?? Cable;
                  return (
                    <Link
                      key={cat.id}
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-3 py-2 text-sm text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056]"
                    >
                      <Icon size={18} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
"""))

# ============================================================
# components/layout/Footer.tsx (updated with dark mode classes)
# ============================================================
files.append(("components/layout/Footer.tsx", """import Link from "next/link";
import {
  Instagram, Twitter, Linkedin, Youtube,
  Phone, Mail, MapPin, ShieldCheck, Truck,
  RotateCcw, Headphones, Award,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface FooterProps {
  locale: Locale;
}

export default function Footer({ locale }: FooterProps) {
  const isFa = locale === "fa";

  const t = {
    aboutTitle: isFa ? "درباره SourcePixcel" : "About SourcePixcel",
    aboutText: isFa
      ? "SourcePixcel یک فروشگاه اینترنتی مدرن است که با هدف ارائه بهترین تجربه خرید آنلاین برای کاربران ایرانی طراحی شده است."
      : "SourcePixcel is a modern online store designed to provide the best online shopping experience for Iranian users.",
    customerService: isFa ? "خدمات مشتریان" : "Customer Service",
    quickLinks: isFa ? "دسترسی سریع" : "Quick Links",
    followUs: isFa ? "با ما همراه باشید" : "Follow Us",
    contact: isFa ? "تماس با ما" : "Contact Us",
    faq: isFa ? "سوالات متداول" : "FAQ",
    returns: isFa ? "رویه بازگرداندن کالا" : "Return Policy",
    shipping: isFa ? "شرایط ارسال" : "Shipping Info",
    privacy: isFa ? "حریم خصوصی" : "Privacy Policy",
    terms: isFa ? "شرایط استفاده" : "Terms of Use",
    about: isFa ? "درباره ما" : "About Us",
    contactLink: isFa ? "تماس با ما" : "Contact Us",
    blog: isFa ? "وبلاگ" : "Blog",
    careers: isFa ? "فرصت‌های شغلی" : "Careers",
    freeShipping: isFa ? "ارسال سریع" : "Fast Shipping",
    securePayment: isFa ? "پرداخت امن" : "Secure Payment",
    returnGuarantee: isFa ? "۷ روز ضمانت بازگشت" : "7-Day Return",
    support: isFa ? "پشتیبانی ۲۴/۷" : "24/7 Support",
    authentic: isFa ? "ضمانت اصالت کالا" : "Authentic Products",
    copyright: isFa
      ? "تمامی حقوق مادی و معنوی این سایت متعلق به SourcePixcel می‌باشد."
      : "All rights reserved by SourcePixcel.",
  };

  const serviceBadges = [
    { icon: Truck, label: t.freeShipping },
    { icon: ShieldCheck, label: t.securePayment },
    { icon: RotateCcw, label: t.returnGuarantee },
    { icon: Headphones, label: t.support },
    { icon: Award, label: t.authentic },
  ];

  const customerServiceLinks = [
    { href: `/${locale}/faq`, label: t.faq },
    { href: `/${locale}/faq`, label: t.returns },
    { href: `/${locale}/faq`, label: t.shipping },
    { href: `/${locale}/contact`, label: t.contactLink },
  ];

  const quickLinks = [
    { href: `/${locale}/about`, label: t.about },
    { href: `/${locale}/contact`, label: t.contactLink },
    { href: `/${locale}/blog`, label: t.blog },
    { href: `/${locale}/about`, label: t.careers },
  ];

  const legalLinks = [
    { href: `/${locale}/privacy`, label: t.privacy },
    { href: `/${locale}/terms`, label: t.terms },
  ];

  const socialLinks = [
    { icon: Instagram, href: "https://instagram.com", label: "Instagram" },
    { icon: Twitter, href: "https://twitter.com", label: "Twitter" },
    { icon: Linkedin, href: "https://linkedin.com", label: "LinkedIn" },
    { icon: Youtube, href: "https://youtube.com", label: "YouTube" },
  ];

  return (
    <footer className="bg-white dark:bg-[#1A1A1E] border-t border-[#E0E0E2] dark:border-[#2A2A2E] mt-12">
      {/* Service badges */}
      <div className="border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 py-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {serviceBadges.map((badge, i) => {
              const Icon = badge.icon;
              return (
                <div key={i} className="flex flex-col items-center gap-2 text-center">
                  <div className="w-12 h-12 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center">
                    <Icon size={22} className="text-[#62666D] dark:text-[#A1A3A8]" />
                  </div>
                  <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    {badge.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Columns */}
      <div className="max-w-[1400px] mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.aboutTitle}
            </h3>
            <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6">
              {t.aboutText}
            </p>
          </div>

          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.customerService}
            </h3>
            <ul className="space-y-2">
              {customerServiceLinks.map((link, i) => (
                <li key={i}>
                  <Link
                    href={link.href}
                    className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.quickLinks}
            </h3>
            <ul className="space-y-2">
              {quickLinks.map((link, i) => (
                <li key={i}>
                  <Link
                    href={link.href}
                    className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.contact}
            </h3>
            <ul className="space-y-3 mb-6">
              <li className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                <Phone size={14} className="text-[#A1A3A8] shrink-0" />
                <span dir="ltr">021-12345678</span>
              </li>
              <li className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                <Mail size={14} className="text-[#A1A3A8] shrink-0" />
                <span dir="ltr">support@sourcepixcel.com</span>
              </li>
              <li className="flex items-start gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                <MapPin size={14} className="text-[#A1A3A8] shrink-0 mt-0.5" />
                <span>
                  {isFa ? "تهران، خیابان ولیعصر، پلاک ۱۲۳" : "Tehran, Valiasr St., No. 123"}
                </span>
              </li>
            </ul>

            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
              {t.followUs}
            </h3>
            <div className="flex items-center gap-3">
              {socialLinks.map((social, i) => {
                const Icon = social.icon;
                return (
                  <a
                    key={i}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={social.label}
                    className="w-9 h-9 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#EF4056] hover:text-white transition-colors"
                  >
                    <Icon size={16} />
                  </a>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Trust badges + Legal */}
      <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4 flex-wrap justify-center">
              <div className="w-16 h-16 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "نماد اعتماد" : "Trust Seal"}
              </div>
              <div className="w-16 h-16 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "ساماندهی" : "Regulated"}
              </div>
              <div className="w-16 h-16 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "اتحادیه" : "Union"}
              </div>
            </div>

            <div className="flex items-center gap-4 flex-wrap justify-center">
              {legalLinks.map((link, i) => (
                <Link
                  key={i}
                  href={link.href}
                  className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] bg-[#F5F5F5] dark:bg-[#0F0F12]">
        <div className="max-w-[1400px] mx-auto px-4 py-4 text-center">
          <p className="text-[12px] text-[#A1A3A8]">
            © {new Date().getFullYear()} SourcePixcel — {t.copyright}
          </p>
        </div>
      </div>
    </footer>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 18: Dark Mode")
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
        print("Now run: npm run dev")
        print("Test: Click the moon/sun icon in the top bar")
        print("\nNext: run 19_seo.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()