// lib/stores/wishlist.ts
"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface WishlistState {
  ids: number[];
  toggle: (productId: number) => void;
  has: (productId: number) => boolean;
  remove: (productId: number) => void;
  clear: () => void;
}

export const useWishlistStore = create<WishlistState>()(
  persist(
    (set, get) => ({
      ids: [],

      toggle: (productId) => {
        set((state) => ({
          ids: state.ids.includes(productId)
            ? state.ids.filter((id) => id !== productId)
            : [...state.ids, productId],
        }));
      },

      has: (productId) => get().ids.includes(productId),

      remove: (productId) => {
        set((state) => ({ ids: state.ids.filter((id) => id !== productId) }));
      },

      clear: () => set({ ids: [] }),
    }),
    { name: "sourcepixcel-wishlist" }
  )
);
