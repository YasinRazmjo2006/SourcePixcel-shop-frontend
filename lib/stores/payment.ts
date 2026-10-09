"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface PaymentTransaction {
  id: string;
  authority: string;
  amount: number;
  status: "pending" | "success" | "failed" | "cancelled";
  cardNumber?: string;
  refId?: string;
  createdAt: number;
  paidAt?: number;
  orderNumber?: string;
}

interface PaymentState {
  transactions: PaymentTransaction[];
  createTransaction: (amount: number) => PaymentTransaction;
  updateTransaction: (
    authority: string,
    updates: Partial<PaymentTransaction>
  ) => void;
  getByAuthority: (authority: string) => PaymentTransaction | undefined;
  clearAll: () => void;
}

export const usePaymentStore = create<PaymentState>()(
  persist(
    (set, get) => ({
      transactions: [],

      createTransaction: (amount) => {
        const authority = `A0000000000000000000000000${Date.now()
          .toString()
          .slice(-8)}`;
        const txn: PaymentTransaction = {
          id: `txn-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
          authority,
          amount,
          status: "pending",
          createdAt: Date.now(),
        };
        set((state) => ({
          transactions: [txn, ...state.transactions].slice(0, 50),
        }));
        return txn;
      },

      updateTransaction: (authority, updates) => {
        set((state) => ({
          transactions: state.transactions.map((t) =>
            t.authority === authority ? { ...t, ...updates } : t
          ),
        }));
      },

      getByAuthority: (authority) =>
        get().transactions.find((t) => t.authority === authority),

      clearAll: () => set({ transactions: [] }),
    }),
    { name: "sourcepixcel-payments" }
  )
);
