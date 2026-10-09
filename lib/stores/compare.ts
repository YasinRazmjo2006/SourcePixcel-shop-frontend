"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

const MAX_COMPARE = 4;

interface CompareState {
  ids: number[];
  toggle: (productId: number) => void;
  has: (productId: number) => boolean;
  remove: (productId: number) => void;
  clear: () => void;
  isFull: () => boolean;
}

export const useCompareStore = create<CompareState>()(
  persist(
    (set, get) => ({
      ids: [],

      toggle: (productId) => {
        set((state) => {
          if (state.ids.includes(productId)) {
            return { ids: state.ids.filter((id) => id !== productId) };
          }
          if (state.ids.length >= MAX_COMPARE) {
            return state;
          }
          return { ids: [...state.ids, productId] };
        });
      },

      has: (productId) => get().ids.includes(productId),

      remove: (productId) => {
        set((state) => ({
          ids: state.ids.filter((id) => id !== productId),
        }));
      },

      clear: () => set({ ids: [] }),

      isFull: () => get().ids.length >= MAX_COMPARE,
    }),
    { name: "sourcepixcel-compare" }
  )
);

export const COMPARE_MAX = MAX_COMPARE;
