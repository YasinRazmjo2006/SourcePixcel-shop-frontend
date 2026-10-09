"use client";

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
      className="w-7 h-7 rounded-full flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
    >
      {mode === "light" ? <Moon size={14} /> : <Sun size={14} />}
    </button>
  );
}