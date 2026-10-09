"use client";

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