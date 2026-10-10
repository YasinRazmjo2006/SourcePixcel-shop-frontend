"use client";

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
