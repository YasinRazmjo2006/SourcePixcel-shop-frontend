"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AdminState {
  isAdmin: boolean;
  adminName: string | null;
  login: (name: string) => void;
  logout: () => void;
}

export const useAdminStore = create<AdminState>()(
  persist(
    (set) => ({
      isAdmin: false,
      adminName: null,
      login: (name) => set({ isAdmin: true, adminName: name }),
      logout: () => set({ isAdmin: false, adminName: null }),
    }),
    { name: "sourcepixcel-admin" }
  )
);
