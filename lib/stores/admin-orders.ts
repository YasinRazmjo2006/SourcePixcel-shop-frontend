"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AdminOrder, AdminOrderStatus } from "@/lib/types";
import { adminOrders as initialOrders } from "@/lib/data";

interface AdminOrdersState {
  orders: AdminOrder[];
  updateStatus: (id: string, status: AdminOrderStatus) => void;
  addTrackingCode: (id: string, code: string) => void;
  deleteOrder: (id: string) => void;
  reset: () => void;
}

export const useAdminOrdersStore = create<AdminOrdersState>()(
  persist(
    (set) => ({
      orders: initialOrders,

      updateStatus: (id, status) =>
        set((state) => ({
          orders: state.orders.map((o) =>
            o.id === id
              ? { ...o, status, updatedAt: new Date().toISOString() }
              : o
          ),
        })),

      addTrackingCode: (id, code) =>
        set((state) => ({
          orders: state.orders.map((o) =>
            o.id === id ? { ...o, trackingCode: code } : o
          ),
        })),

      deleteOrder: (id) =>
        set((state) => ({
          orders: state.orders.filter((o) => o.id !== id),
        })),

      reset: () => set({ orders: initialOrders }),
    }),
    { name: "sourcepixcel-admin-orders" }
  )
);
