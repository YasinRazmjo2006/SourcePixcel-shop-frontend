# 28_fonts.py
# اضافه کردن فونت‌های حرفه‌ای Vazirmatn + Inter
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/fonts.ts — تنظیمات فونت‌های Next.js
# ============================================================
files.append(("lib/fonts.ts", """import { Vazirmatn, Inter } from "next/font/google";

/**
 * Vazirmatn — Persian font (RTL)
 * Weights: 300, 400, 500, 600, 700, 800, 900
 */
export const vazirmatn = Vazirmatn({
  subsets: ["arabic", "latin"],
  weight: ["300", "400", "500", "600", "700", "800", "900"],
  variable: "--font-vazirmatn",
  display: "swap",
  preload: true,
  fallback: ["system-ui", "Tahoma", "Arial", "sans-serif"],
});

/**
 * Inter — English font (LTR)
 * Weights: 300, 400, 500, 600, 700, 800, 900
 */
export const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800", "900"],
  variable: "--font-inter",
  display: "swap",
  preload: true,
  fallback: ["system-ui", "-apple-system", "Segoe UI", "sans-serif"],
});
"""))

# ============================================================
# app/layout.tsx — استفاده از فونت‌ها
# ============================================================
files.append(("app/layout.tsx", """import "./globals.css";
import ThemeProvider from "@/components/common/ThemeProvider";
import { vazirmatn, inter } from "@/lib/fonts";

export const metadata = {
  title: "SourcePixcel — فروشگاه آنلاین مدرن",
  description: "فروشگاه اینترنتی SourcePixcel | خرید آنلاین با ارسال سریع و ضمانت اصالت",
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
    <html
      lang="fa"
      dir="rtl"
      suppressHydrationWarning
      className={`${vazirmatn.variable} ${inter.variable}`}
    >
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
# tailwind.config.ts — استفاده از متغیرهای فونت
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
      fontFamily: {
        // English font (LTR)
        sans: [
          "var(--font-inter)",
          "var(--font-vazirmatn)",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "sans-serif",
        ],
        // Persian font (RTL) — used via [dir="rtl"]
        fa: [
          "var(--font-vazirmatn)",
          "system-ui",
          "Tahoma",
          "Arial",
          "sans-serif",
        ],
        en: [
          "var(--font-inter)",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "sans-serif",
        ],
        // Numbers/mono
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          "monospace",
        ],
      },
      // Enhanced typography scale
      fontSize: {
        "2xs": ["0.625rem", { lineHeight: "1rem" }],       // 10px
        xs: ["0.75rem", { lineHeight: "1.125rem" }],        // 12px
        sm: ["0.8125rem", { lineHeight: "1.25rem" }],       // 13px
        base: ["0.875rem", { lineHeight: "1.5rem" }],       // 14px
        md: ["0.9375rem", { lineHeight: "1.625rem" }],      // 15px
        lg: ["1.0625rem", { lineHeight: "1.75rem" }],       // 17px
        xl: ["1.1875rem", { lineHeight: "1.875rem" }],      // 19px
        "2xl": ["1.375rem", { lineHeight: "2rem" }],        // 22px
        "3xl": ["1.625rem", { lineHeight: "2.25rem" }],     // 26px
        "4xl": ["2rem", { lineHeight: "2.5rem" }],          // 32px
        "5xl": ["2.5rem", { lineHeight: "3rem" }],          // 40px
      },
      // Enhanced spacing
      spacing: {
        "4.5": "1.125rem",
        "5.5": "1.375rem",
        "6.5": "1.625rem",
        "7.5": "1.875rem",
        "13": "3.25rem",
        "15": "3.75rem",
        "17": "4.25rem",
        "18": "4.5rem",
        "19": "4.75rem",
        "21": "5.25rem",
        "22": "5.5rem",
        "26": "6.5rem",
      },
      // Better letter spacing for Persian
      letterSpacing: {
        persian: "0",
        tighter: "-0.02em",
        tight: "-0.01em",
        normal: "0",
        wide: "0.02em",
        wider: "0.04em",
      },
      // Better line heights for Persian
      lineHeight: {
        persian: "1.9",
        relaxed: "1.75",
        loose: "2",
      },
      // Enhanced shadows
      boxShadow: {
        xs: "0 1px 2px 0 rgb(0 0 0 / 0.04)",
        sm: "0 1px 3px 0 rgb(0 0 0 / 0.06), 0 1px 2px -1px rgb(0 0 0 / 0.06)",
        DEFAULT: "0 2px 8px -2px rgb(0 0 0 / 0.06), 0 4px 12px -4px rgb(0 0 0 / 0.04)",
        md: "0 4px 12px -2px rgb(0 0 0 / 0.08), 0 6px 20px -6px rgb(0 0 0 / 0.06)",
        lg: "0 8px 24px -4px rgb(0 0 0 / 0.10), 0 12px 40px -8px rgb(0 0 0 / 0.08)",
        xl: "0 16px 48px -8px rgb(0 0 0 / 0.14), 0 24px 64px -12px rgb(0 0 0 / 0.10)",
        "2xl": "0 24px 64px -12px rgb(0 0 0 / 0.18)",
        inner: "inset 0 2px 4px 0 rgb(0 0 0 / 0.04)",
        none: "none",
      },
      // Animations
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "scale-in": {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        shimmer: {
          "100%": { transform: "translateX(100%)" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.2s ease-out",
        "slide-up": "slide-up 0.3s ease-out",
        "scale-in": "scale-in 0.2s ease-out",
        shimmer: "shimmer 1.5s infinite",
      },
    },
  },
  plugins: [],
};

export default config;
"""))

# ============================================================
# app/globals.css — بهبود typography
# ============================================================
files.append(("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

/* ═══════════════════════════════════════════════════════════════
   BASE STYLES
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
  font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Persian (RTL) — use Vazirmatn with better line-height */
[dir="rtl"],
[dir="rtl"] body {
  font-family: var(--font-vazirmatn), system-ui, Tahoma, Arial, sans-serif;
  line-height: 1.75;
  letter-spacing: 0;
}

/* English (LTR) — use Inter */
[dir="ltr"],
[dir="ltr"] body {
  font-family: var(--font-inter), system-ui, -apple-system, sans-serif;
  line-height: 1.6;
  letter-spacing: -0.01em;
}

/* Dark mode */
html.dark,
html.dark body {
  background: #0F0F12;
  color: #E5E5EA;
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

/* Focus visible */
*:focus-visible {
  outline: 2px solid #EF4056;
  outline-offset: 2px;
  border-radius: 4px;
}

/* Remove outline for mouse users */
*:focus:not(:focus-visible) {
  outline: none;
}

/* ═══════════════════════════════════════════════════════════════
   TYPOGRAPHY — Headings
   ═══════════════════════════════════════════════════════════════ */

h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
  color: #3F4064;
  margin: 0;
}

html.dark h1,
html.dark h2,
html.dark h3,
html.dark h4,
html.dark h5,
html.dark h6 {
  color: #E5E5EA;
}

h1 { font-weight: 800; }
h2 { font-weight: 800; }
h3 { font-weight: 700; }

/* Persian headings need tighter letter-spacing */
[dir="rtl"] h1,
[dir="rtl"] h2,
[dir="rtl"] h3 {
  letter-spacing: 0;
}

/* ═══════════════════════════════════════════════════════════════
   TEXT SELECTION
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
   NUMBERS — Tabular for prices
   ═══════════════════════════════════════════════════════════════ */

.tabular-nums {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* Persian numbers — better rendering */
[dir="rtl"] .tabular-nums {
  font-feature-settings: "tnum", "ss01";
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
   UTILITIES
   ═══════════════════════════════════════════════════════════════ */

/* Text truncation */
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

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}

/* ═══════════════════════════════════════════════════════════════
   ANIMATIONS
   ═══════════════════════════════════════════════════════════════ */

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

.animate-fade-in {
  animation: fade-in 0.2s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.3s ease-out;
}

.animate-scale-in {
  animation: scale-in 0.2s ease-out;
}

/* Skeleton shimmer */
.skeleton-shimmer {
  position: relative;
  overflow: hidden;
}

.skeleton-shimmer::after {
  content: "";
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: shimmer 1.5s infinite;
}

html.dark .skeleton-shimmer::after {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ═══════════════════════════════════════════════════════════════
   PROSE (article content)
   ═══════════════════════════════════════════════════════════════ */

.prose {
  color: #62666D;
  line-height: 1.9;
}

[dir="rtl"] .prose {
  line-height: 2;
}

.prose p {
  margin-bottom: 1.25rem;
}

.prose h2 {
  font-size: 1.375rem;
  font-weight: 800;
  color: #3F4064;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.prose h3 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #3F4064;
  margin-top: 1.75rem;
  margin-bottom: 0.75rem;
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

html.dark .prose {
  color: #A1A3A8;
}

html.dark .prose h2,
html.dark .prose h3,
html.dark .prose strong {
  color: #E5E5EA;
}

/* ═══════════════════════════════════════════════════════════════
   PRINT STYLES
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
  }

  .no-print {
    display: none !important;
  }

  .print-content {
    color: black !important;
  }

  .print-content h1,
  .print-content h2,
  .print-content h3,
  .print-content h4,
  .print-content p,
  .print-content td,
  .print-content th,
  .print-content span,
  .print-content div {
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
# lib/stores/settings.ts — اضافه کردن انتخاب فونت (اختیاری)
# ============================================================
files.append(("lib/stores/settings.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type FontFamily = "auto" | "vazirmatn" | "inter";
export type FontSize = "small" | "medium" | "large";
export type LineHeight = "compact" | "normal" | "relaxed";

interface SettingsState {
  // Appearance
  fontFamily: FontFamily;
  fontSize: FontSize;
  lineHeight: LineHeight;
  reduceMotion: boolean;

  // Notifications
  emailNotifications: boolean;
  pushNotifications: boolean;

  // Behavior
  autoPlayVideos: boolean;
  showPrices: boolean;
}

interface SettingsActions {
  setFontFamily: (value: FontFamily) => void;
  setFontSize: (value: FontSize) => void;
  setLineHeight: (value: LineHeight) => void;
  setReduceMotion: (value: boolean) => void;
  setEmailNotifications: (value: boolean) => void;
  setPushNotifications: (value: boolean) => void;
  setAutoPlayVideos: (value: boolean) => void;
  setShowPrices: (value: boolean) => void;
  reset: () => void;
}

const DEFAULTS: SettingsState = {
  fontFamily: "auto",
  fontSize: "medium",
  lineHeight: "normal",
  reduceMotion: false,
  emailNotifications: true,
  pushNotifications: false,
  autoPlayVideos: false,
  showPrices: true,
};

export const useSettingsStore = create<SettingsState & SettingsActions>()(
  persist(
    (set) => ({
      ...DEFAULTS,
      setFontFamily: (value) => set({ fontFamily: value }),
      setFontSize: (value) => set({ fontSize: value }),
      setLineHeight: (value) => set({ lineHeight: value }),
      setReduceMotion: (value) => set({ reduceMotion: value }),
      setEmailNotifications: (value) => set({ emailNotifications: value }),
      setPushNotifications: (value) => set({ pushNotifications: value }),
      setAutoPlayVideos: (value) => set({ autoPlayVideos: value }),
      setShowPrices: (value) => set({ showPrices: value }),
      reset: () => set(DEFAULTS),
    }),
    { name: "sourcepixcel-settings" }
  )
);
"""))

# ============================================================
# components/common/FontLoader.tsx — اعمال تنظیمات فونت
# ============================================================
files.append(("components/common/FontLoader.tsx", """"use client";

import { useEffect } from "react";
import { useSettingsStore } from "@/lib/stores";

/**
 * FontLoader — applies user font preferences to <html>
 * Should be placed inside LocaleLayout
 */
export default function FontLoader() {
  const fontFamily = useSettingsStore((s) => s.fontFamily);
  const fontSize = useSettingsStore((s) => s.fontSize);
  const lineHeight = useSettingsStore((s) => s.lineHeight);

  useEffect(() => {
    if (typeof document === "undefined") return;
    const root = document.documentElement;

    // Font family
    root.style.removeProperty("--user-font-family");
    if (fontFamily === "vazirmatn") {
      root.style.setProperty(
        "--user-font-family",
        "var(--font-vazirmatn), system-ui, sans-serif"
      );
    } else if (fontFamily === "inter") {
      root.style.setProperty(
        "--user-font-family",
        "var(--font-inter), system-ui, sans-serif"
      );
    }
    // "auto" = use default (direction-based)

    // Font size
    const sizes = { small: "15px", medium: "16px", large: "18px" };
    root.style.setProperty("font-size", sizes[fontSize]);

    // Line height
    const heights = { compact: "1.5", normal: "1.75", relaxed: "2" };
    root.style.setProperty("--user-line-height", heights[lineHeight]);
  }, [fontFamily, fontSize, lineHeight]);

  return null;
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
export { default as KeyboardShortcuts } from "./KeyboardShortcuts";
export { default as OfflineBanner } from "./OfflineBanner";
export { default as FontLoader } from "./FontLoader";
"""))

# ============================================================
# app/[locale]/layout.tsx — اضافه کردن FontLoader
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BottomNav from "@/components/layout/BottomNav";
import ToastContainer from "@/components/common/ToastContainer";
import KeyboardShortcuts from "@/components/common/KeyboardShortcuts";
import OfflineBanner from "@/components/common/OfflineBanner";
import FontLoader from "@/components/common/FontLoader";
import type { Locale } from "@/lib/types";

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
    print("SourcePixcel — Step 28: Professional Fonts")
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
        print("\nYou should see:")
        print("  ✓ Persian text in Vazirmatn font")
        print("  ✓ English text in Inter font")
        print("  ✓ Better line-height and letter-spacing")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()