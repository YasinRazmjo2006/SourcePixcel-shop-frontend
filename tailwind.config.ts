import type { Config } from "tailwindcss";

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
