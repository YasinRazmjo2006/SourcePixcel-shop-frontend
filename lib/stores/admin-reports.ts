"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type ReportType = "sales" | "orders" | "users" | "products" | "custom";
export type ReportFormat = "csv" | "excel" | "pdf";

export interface SavedReport {
  id: string;
  name: string;
  type: ReportType;
  format: ReportFormat;
  createdAt: number;
  schedule?: "daily" | "weekly" | "monthly";
}

interface AdminReportsState {
  savedReports: SavedReport[];
  addReport: (report: Omit<SavedReport, "id" | "createdAt">) => void;
  removeReport: (id: string) => void;
  clearAll: () => void;
}

export const useAdminReportsStore = create<AdminReportsState>()(
  persist(
    (set) => ({
      savedReports: [
        {
          id: "report-1",
          name: "فروش ماهانه",
          type: "sales",
          format: "excel",
          createdAt: Date.now() - 86400000 * 3,
          schedule: "monthly",
        },
        {
          id: "report-2",
          name: "گزارش سفارشات هفتگی",
          type: "orders",
          format: "pdf",
          createdAt: Date.now() - 86400000 * 7,
          schedule: "weekly",
        },
      ],

      addReport: (report) =>
        set((state) => ({
          savedReports: [
            {
              ...report,
              id: `report-${Date.now()}`,
              createdAt: Date.now(),
            },
            ...state.savedReports,
          ],
        })),

      removeReport: (id) =>
        set((state) => ({
          savedReports: state.savedReports.filter((r) => r.id !== id),
        })),

      clearAll: () => set({ savedReports: [] }),
    }),
    { name: "sourcepixcel-admin-reports" }
  )
);
