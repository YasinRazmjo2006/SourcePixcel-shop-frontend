"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product } from "@/lib/types";
import { products as initialProducts } from "@/lib/data";

interface AdminProductsState {
  products: Product[];
  addProduct: (product: Product) => void;
  updateProduct: (id: number, updates: Partial<Product>) => void;
  deleteProduct: (id: number) => void;
  deleteProducts: (ids: number[]) => void;
  toggleStock: (id: number) => void;
  reset: () => void;
}

export const useAdminProductsStore = create<AdminProductsState>()(
  persist(
    (set) => ({
      products: initialProducts,

      addProduct: (product) =>
        set((state) => ({
          products: [product, ...state.products],
        })),

      updateProduct: (id, updates) =>
        set((state) => ({
          products: state.products.map((p) =>
            p.id === id ? { ...p, ...updates } : p
          ),
        })),

      deleteProduct: (id) =>
        set((state) => ({
          products: state.products.filter((p) => p.id !== id),
        })),

      deleteProducts: (ids) =>
        set((state) => ({
          products: state.products.filter((p) => !ids.includes(p.id)),
        })),

      toggleStock: (id) =>
        set((state) => ({
          products: state.products.map((p) =>
            p.id === id ? { ...p, inStock: !p.inStock } : p
          ),
        })),

      reset: () => set({ products: initialProducts }),
    }),
    { name: "sourcepixcel-admin-products" }
  )
);
