import { Vazirmatn, Inter } from "next/font/google";

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
