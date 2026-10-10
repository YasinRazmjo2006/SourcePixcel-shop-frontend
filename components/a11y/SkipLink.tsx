"use client";

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
