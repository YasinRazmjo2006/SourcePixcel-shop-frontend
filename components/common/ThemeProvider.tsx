"use client";

import { useEffect } from "react";
import { useThemeStore } from "@/lib/stores";

export default function ThemeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const mode = useThemeStore((s) => s.mode);

  useEffect(() => {
    if (typeof document !== "undefined") {
      document.documentElement.classList.toggle("dark", mode === "dark");
    }
  }, [mode]);

  return <>{children}</>;
}