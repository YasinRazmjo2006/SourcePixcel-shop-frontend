# 45_admin_reports.py
# Step 8: Reports & Export (PDF, Excel, CSV)
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# lib/utils/export-csv.ts
# ============================================================
files.append(("lib/utils/export-csv.ts", '''// lib/utils/export-csv.ts

export interface CsvColumn<T> {
  key: keyof T | string;
  label: string;
  formatter?: (value: unknown, row: T) => string;
}

export function exportToCSV<T extends Record<string, unknown>>(
  data: T[],
  columns: CsvColumn<T>[],
  filename: string
): void {
  if (data.length === 0) return;

  const headers = columns.map((c) => c.label).join(",");

  const rows = data.map((row) =>
    columns
      .map((col) => {
        const value = col.formatter
          ? col.formatter(row[col.key as keyof T], row)
          : String(row[col.key as keyof T] ?? "");
        // Escape quotes and wrap in quotes if contains comma
        const escaped = value.replace(/"/g, '""');
        return /[",\\n]/.test(escaped) ? `"${escaped}"` : escaped;
      })
      .join(",")
  );

  // Add BOM for UTF-8 (Excel support)
  const bom = "\\uFEFF";
  const csv = bom + [headers, ...rows].join("\\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

  downloadBlob(blob, `${filename}.csv`);
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
'''))

# ============================================================
# lib/utils/export-excel.ts
# ============================================================
files.append(("lib/utils/export-excel.ts", '''// lib/utils/export-excel.ts
import * as XLSX from "xlsx";
import type { CsvColumn } from "./export-csv";

export function exportToExcel<T extends Record<string, unknown>>(
  data: T[],
  columns: CsvColumn<T>[],
  filename: string,
  sheetName = "Sheet1"
): void {
  if (data.length === 0) return;

  // Build rows as objects with labels as keys
  const rows = data.map((row) => {
    const obj: Record<string, string | number> = {};
    columns.forEach((col) => {
      const value = col.formatter
        ? col.formatter(row[col.key as keyof T], row)
        : (row[col.key as keyof T] as string | number) ?? "";
      obj[col.label] = value;
    });
    return obj;
  });

  const worksheet = XLSX.utils.json_to_sheet(rows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

  // Auto-size columns
  const colWidths = columns.map((col) => ({
    wch: Math.max(col.label.length, 15),
  }));
  worksheet["!cols"] = colWidths;

  XLSX.writeFile(workbook, `${filename}.xlsx`);
}
'''))

# ============================================================
# lib/utils/export-pdf.ts
# ============================================================
files.append(("lib/utils/export-pdf.ts", '''// lib/utils/export-pdf.ts
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import type { CsvColumn } from "./export-csv";

export interface PdfOptions<T> {
  title: string;
  subtitle?: string;
  data: T[];
  columns: CsvColumn<T>[];
  filename: string;
  locale?: "fa" | "en";
}

export function exportToPDF<T extends Record<string, unknown>>({
  title,
  subtitle,
  data,
  columns,
  filename,
  locale = "fa",
}: PdfOptions<T>): void {
  const doc = new jsPDF({
    orientation: "landscape",
    unit: "mm",
    format: "a4",
  });

  const pageWidth = doc.internal.pageSize.getWidth();

  // Header
  doc.setFillColor(239, 64, 86); // #EF4056
  doc.rect(0, 0, pageWidth, 25, "F");
  doc.setTextColor(255, 255, 255);
  doc.setFontSize(18);
  doc.setFont("helvetica", "bold");
  doc.text(title, pageWidth / 2, 12, { align: "center" });

  if (subtitle) {
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    doc.text(subtitle, pageWidth / 2, 19, { align: "center" });
  }

  // Date
  doc.setTextColor(160, 163, 168);
  doc.setFontSize(9);
  const dateStr =
    locale === "fa"
      ? new Date().toLocaleDateString("fa-IR")
      : new Date().toLocaleDateString("en-US");
  doc.text(`Generated: ${dateStr}`, pageWidth - 10, 32, { align: "right" });

  // Table
  const head = [columns.map((c) => c.label)];
  const body = data.map((row) =>
    columns.map((col) => {
      if (col.formatter) return col.formatter(row[col.key as keyof T], row);
      return String(row[col.key as keyof T] ?? "");
    })
  );

  autoTable(doc, {
    head,
    body,
    startY: 38,
    styles: {
      fontSize: 9,
      cellPadding: 3,
      halign: locale === "fa" ? "right" : "left",
    },
    headStyles: {
      fillColor: [239, 64, 86],
      textColor: [255, 255, 255],
      fontStyle: "bold",
    },
    alternateRowStyles: {
      fillColor: [250, 250, 250],
    },
    margin: { top: 38, left: 10, right: 10 },
    didDrawPage: (data) => {
      // Footer
      const pageCount = doc.getNumberOfPages();
      const pageNum = doc.getCurrentPageInfo().pageNumber;
      doc.setFontSize(8);
      doc.setTextColor(160, 163, 168);
      doc.text(
        `SourcePixcel — Page ${pageNum} of ${pageCount}`,
        pageWidth / 2,
        doc.internal.pageSize.getHeight() - 5,
        { align: "center" }
      );
    },
  });

  doc.save(`${filename}.pdf`);
}
'''))

# ============================================================
# lib/utils/index.ts (updated)
# ============================================================
files.append(("lib/utils/index.ts", '''// lib/utils/index.ts
export {
  formatPrice,
  formatPriceWithCurrency,
  calcFinalPrice,
  formatDiscount,
  formatRating,
  formatReviewCount,
  truncate,
  getProductTitle,
  getCategoryName,
  getBrandName,
  formatDate,
  localePath,
  cn,
  getStockLabel,
  scrollToTop,
} from "./format";

export {
  isValidIranianMobile,
  normalizeMobile,
  formatMobileDisplay,
  isValidEmail,
  isValidIranianNationalId,
  isValidIranianPostalCode,
  getPasswordStrength,
  isValidPassword,
} from "./validators";

export {
  buildMetadata,
  buildProductSchema,
  buildOrganizationSchema,
  buildWebSiteSchema,
  buildBreadcrumbSchema,
  SITE_NAME_EXPORT,
  SITE_URL_EXPORT,
} from "./seo";

export {
  generateBlurPlaceholder,
  getCategoryColor,
  getProductBlur,
  CATEGORY_COLORS,
} from "./blur";

export {
  formatCompact,
  formatPercent,
  formatRelativeTime,
} from "./number-format";

export { exportToCSV, downloadBlob } from "./export-csv";
export type { CsvColumn } from "./export-csv";

export { exportToExcel } from "./export-excel";
export { exportToPDF } from "./export-pdf";
export type { PdfOptions } from "./export-pdf";
'''))

# ============================================================
# lib/stores/admin-reports.ts
# ============================================================
files.append(("lib/stores/admin-reports.ts", '''"use client";

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
'''))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", '''// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export { useAdminStore } from "./admin";
export { useAdminUIStore } from "./admin-ui";
export { useAdminProductsStore } from "./admin-products";
export { useAdminOrdersStore } from "./admin-orders";
export { useAdminReportsStore } from "./admin-reports";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
export type { SavedReport, ReportType, ReportFormat } from "./admin-reports";
'''))

# ============================================================
# components/admin/reports/ReportCard.tsx
# ============================================================
files.append(("components/admin/reports/ReportCard.tsx", '''"use client";

import { motion } from "framer-motion";
import {
  DollarSign,
  ShoppingCart,
  Users,
  Package,
  FileText,
  FileSpreadsheet,
  Download,
  Calendar,
  Trash2,
  type LucideIcon,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import type { SavedReport } from "@/lib/stores";

interface ReportCardProps {
  locale: Locale;
  report: SavedReport;
  onDownload: () => void;
  onDelete: () => void;
  delay?: number;
}

const TYPE_CONFIG: Record<
  SavedReport["type"],
  { icon: LucideIcon; color: string; fa: string; en: string }
> = {
  sales: { icon: DollarSign, color: "#22C55E", fa: "فروش", en: "Sales" },
  orders: { icon: ShoppingCart, color: "#EF4056", fa: "سفارشات", en: "Orders" },
  users: { icon: Users, color: "#00BFFF", fa: "کاربران", en: "Users" },
  products: { icon: Package, color: "#8B5CF6", fa: "محصولات", en: "Products" },
  custom: { icon: FileText, color: "#F59E0B", fa: "سفارشی", en: "Custom" },
};

const FORMAT_CONFIG: Record<
  SavedReport["format"],
  { color: string; label: string }
> = {
  csv: { color: "#94A3B8", label: "CSV" },
  excel: { color: "#22C55E", label: "XLSX" },
  pdf: { color: "#EF4056", label: "PDF" },
};

const SCHEDULE_LABELS: Record<
  NonNullable<SavedReport["schedule"]>,
  { fa: string; en: string }
> = {
  daily: { fa: "روزانه", en: "Daily" },
  weekly: { fa: "هفتگی", en: "Weekly" },
  monthly: { fa: "ماهانه", en: "Monthly" },
};

export default function ReportCard({
  locale,
  report,
  onDownload,
  onDelete,
  delay = 0,
}: ReportCardProps) {
  const isFa = locale === "fa";
  const typeConfig = TYPE_CONFIG[report.type];
  const formatConfig = FORMAT_CONFIG[report.format];
  const TypeIcon = typeConfig.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 hover:shadow-md transition-shadow group"
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div
          className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
          style={{ backgroundColor: `${typeConfig.color}15` }}
        >
          <TypeIcon size={18} style={{ color: typeConfig.color }} />
        </div>
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            onClick={onDownload}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
            title={isFa ? "دانلود" : "Download"}
          >
            <Download size={14} />
          </button>
          <button
            onClick={onDelete}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors"
            title={isFa ? "حذف" : "Delete"}
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2 truncate">
        {report.name}
      </h3>

      <div className="flex items-center gap-2 flex-wrap mb-3">
        <span
          className="text-[10px] px-2 py-0.5 rounded-full font-medium"
          style={{
            backgroundColor: `${typeConfig.color}15`,
            color: typeConfig.color,
          }}
        >
          {isFa ? typeConfig.fa : typeConfig.en}
        </span>
        <span
          className="text-[10px] px-2 py-0.5 rounded-full font-bold"
          style={{
            backgroundColor: `${formatConfig.color}15`,
            color: formatConfig.color,
          }}
        >
          {formatConfig.label}
        </span>
        {report.schedule && (
          <span className="text-[10px] px-2 py-0.5 rounded-full font-medium bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] flex items-center gap-1">
            <Calendar size={9} />
            {isFa
              ? SCHEDULE_LABELS[report.schedule].fa
              : SCHEDULE_LABELS[report.schedule].en}
          </span>
        )}
      </div>

      <div className="text-[10px] text-[#A1A3A8]">
        {new Date(report.createdAt).toLocaleDateString(
          isFa ? "fa-IR" : "en-US",
          { year: "numeric", month: "short", day: "numeric" }
        )}
      </div>
    </motion.div>
  );
}
'''))

# ============================================================
# components/admin/reports/ExportButtons.tsx
# ============================================================
files.append(("components/admin/reports/ExportButtons.tsx", '''"use client";

import { FileText, FileSpreadsheet, File } from "lucide-react";
import type { Locale } from "@/lib/types";

interface ExportButtonsProps {
  locale: Locale;
  onExport: (format: "csv" | "excel" | "pdf") => void;
  disabled?: boolean;
}

export default function ExportButtons({
  locale,
  onExport,
  disabled = false,
}: ExportButtonsProps) {
  const isFa = locale === "fa";

  const buttons = [
    {
      format: "csv" as const,
      icon: File,
      label: "CSV",
      color: "#94A3B8",
    },
    {
      format: "excel" as const,
      icon: FileSpreadsheet,
      label: "Excel",
      color: "#22C55E",
    },
    {
      format: "pdf" as const,
      icon: FileText,
      label: "PDF",
      color: "#EF4056",
    },
  ];

  return (
    <div className="flex items-center gap-2 flex-wrap">
      <span className="text-[11px] text-[#A1A3A8]">
        {isFa ? "خروجی:" : "Export:"}
      </span>
      {buttons.map((btn) => {
        const Icon = btn.icon;
        return (
          <button
            key={btn.format}
            onClick={() => onExport(btn.format)}
            disabled={disabled}
            className="h-9 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] font-medium text-[#3F4064] dark:text-[#E5E5EA] hover:shadow-md transition-all flex items-center gap-1.5 disabled:opacity-40 disabled:cursor-not-allowed"
            style={{ borderColor: disabled ? undefined : `${btn.color}30` }}
          >
            <Icon size={13} style={{ color: btn.color }} />
            {btn.label}
          </button>
        );
      })}
    </div>
  );
}
'''))

# ============================================================
# components/admin/reports/ReportBuilder.tsx
# ============================================================
files.append(("components/admin/reports/ReportBuilder.tsx", '''"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  FileText,
  Save,
  Calendar,
  Check,
  X,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import type { ReportType, ReportFormat } from "@/lib/stores";

interface ReportBuilderProps {
  locale: Locale;
  onSave: (data: {
    name: string;
    type: ReportType;
    format: ReportFormat;
    schedule?: "daily" | "weekly" | "monthly";
  }) => void;
  onCancel: () => void;
}

export default function ReportBuilder({
  locale,
  onSave,
  onCancel,
}: ReportBuilderProps) {
  const isFa = locale === "fa";

  const [name, setName] = useState("");
  const [type, setType] = useState<ReportType>("sales");
  const [format, setFormat] = useState<ReportFormat>("excel");
  const [schedule, setSchedule] = useState<"" | "daily" | "weekly" | "monthly">("");

  const t = {
    title: isFa ? "ساخت گزارش جدید" : "Create New Report",
    name: isFa ? "نام گزارش" : "Report Name",
    namePlaceholder: isFa ? "مثال: فروش ماهانه" : "e.g. Monthly Sales",
    type: isFa ? "نوع گزارش" : "Report Type",
    format: isFa ? "فرمت خروجی" : "Export Format",
    schedule: isFa ? "زمان‌بندی خودکار (اختیاری)" : "Auto Schedule (Optional)",
    sales: isFa ? "فروش" : "Sales",
    orders: isFa ? "سفارشات" : "Orders",
    users: isFa ? "کاربران" : "Users",
    products: isFa ? "محصولات" : "Products",
    custom: isFa ? "سفارشی" : "Custom",
    none: isFa ? "بدون زمان‌بندی" : "No Schedule",
    daily: isFa ? "روزانه" : "Daily",
    weekly: isFa ? "هفتگی" : "Weekly",
    monthly: isFa ? "ماهانه" : "Monthly",
    save: isFa ? "ذخیره" : "Save",
    cancel: isFa ? "انصراف" : "Cancel",
    required: isFa ? "الزامی" : "Required",
  };

  const types: { value: ReportType; label: string; color: string }[] = [
    { value: "sales", label: t.sales, color: "#22C55E" },
    { value: "orders", label: t.orders, color: "#EF4056" },
    { value: "users", label: t.users, color: "#00BFFF" },
    { value: "products", label: t.products, color: "#8B5CF6" },
    { value: "custom", label: t.custom, color: "#F59E0B" },
  ];

  const formats: { value: ReportFormat; label: string; color: string }[] = [
    { value: "csv", label: "CSV", color: "#94A3B8" },
    { value: "excel", label: "Excel", color: "#22C55E" },
    { value: "pdf", label: "PDF", color: "#EF4056" },
  ];

  const handleSave = () => {
    if (!name.trim()) return;
    onSave({
      name: name.trim(),
      type,
      format,
      schedule: schedule || undefined,
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#EF4056]/30 shadow-lg p-4 md:p-5"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center">
            <FileText size={16} className="text-[#EF4056]" />
          </div>
          <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {t.title}
          </h3>
        </div>
        <button
          onClick={onCancel}
          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
        >
          <X size={16} />
        </button>
      </div>

      <div className="space-y-4">
        {/* Name */}
        <div>
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.name} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={t.namePlaceholder}
            className="w-full h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056] transition-colors"
          />
        </div>

        {/* Type */}
        <div>
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-2">
            {t.type}
          </label>
          <div className="flex flex-wrap gap-2">
            {types.map((tp) => (
              <button
                key={tp.value}
                onClick={() => setType(tp.value)}
                className={`h-8 px-3 rounded-lg text-[11px] font-medium transition-all flex items-center gap-1.5 ${
                  type === tp.value
                    ? "text-white shadow-sm"
                    : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#3A3A40]"
                }`}
                style={
                  type === tp.value
                    ? { backgroundColor: tp.color }
                    : undefined
                }
              >
                {type === tp.value && <Check size={11} />}
                {tp.label}
              </button>
            ))}
          </div>
        </div>

        {/* Format */}
        <div>
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-2">
            {t.format}
          </label>
          <div className="flex flex-wrap gap-2">
            {formats.map((fm) => (
              <button
                key={fm.value}
                onClick={() => setFormat(fm.value)}
                className={`h-8 px-3 rounded-lg text-[11px] font-medium transition-all flex items-center gap-1.5 ${
                  format === fm.value
                    ? "text-white shadow-sm"
                    : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#3A3A40]"
                }`}
                style={
                  format === fm.value
                    ? { backgroundColor: fm.color }
                    : undefined
                }
              >
                {format === fm.value && <Check size={11} />}
                {fm.label}
              </button>
            ))}
          </div>
        </div>

        {/* Schedule */}
        <div>
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-2 flex items-center gap-1">
            <Calendar size={11} />
            {t.schedule}
          </label>
          <div className="flex flex-wrap gap-2">
            {[
              { value: "" as const, label: t.none },
              { value: "daily" as const, label: t.daily },
              { value: "weekly" as const, label: t.weekly },
              { value: "monthly" as const, label: t.monthly },
            ].map((sc) => (
              <button
                key={sc.value || "none"}
                onClick={() => setSchedule(sc.value)}
                className={`h-8 px-3 rounded-lg text-[11px] font-medium transition-colors ${
                  schedule === sc.value
                    ? "bg-[#EF4056] text-white"
                    : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#3A3A40]"
                }`}
              >
                {sc.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-2 mt-5 pt-4 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
        <button
          onClick={onCancel}
          className="flex-1 h-10 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
        >
          {t.cancel}
        </button>
        <button
          onClick={handleSave}
          disabled={!name.trim()}
          className="flex-1 h-10 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center justify-center gap-2 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <Save size={14} />
          {t.save}
        </button>
      </div>
    </motion.div>
  );
}
'''))

# ============================================================
# components/admin/reports/index.ts
# ============================================================
files.append(("components/admin/reports/index.ts", '''// components/admin/reports/index.ts
export { default as ReportCard } from "./ReportCard";
export { default as ExportButtons } from "./ExportButtons";
export { default as ReportBuilder } from "./ReportBuilder";
'''))

# ============================================================
# components/admin/ReportsView.tsx
# ============================================================
files.append(("components/admin/ReportsView.tsx", '''"use client";

import { useState, useMemo, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  FileText,
  Plus,
  Download,
  Users as UsersIcon,
  ShoppingCart,
  Package,
  DollarSign,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import {
  useAdminReportsStore,
  useAdminOrdersStore,
  useAdminProductsStore,
  useToastStore,
} from "@/lib/stores";
import { adminUsers } from "@/lib/data";
import {
  formatPrice,
  formatDate,
  exportToCSV,
  exportToExcel,
  exportToPDF,
  type CsvColumn,
} from "@/lib/utils";
import type { ReportType, ReportFormat } from "@/lib/stores";
import ReportCard from "./reports/ReportCard";
import ReportBuilder from "./reports/ReportBuilder";
import ExportButtons from "./reports/ExportButtons";

interface ReportsViewProps {
  locale: Locale;
}

export default function ReportsView({ locale }: ReportsViewProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const savedReports = useAdminReportsStore((s) => s.savedReports);
  const addReport = useAdminReportsStore((s) => s.addReport);
  const removeReport = useAdminReportsStore((s) => s.removeReport);

  const orders = useAdminOrdersStore((s) => s.orders);
  const products = useAdminProductsStore((s) => s.products);

  const [mounted, setMounted] = useState(false);
  const [builderOpen, setBuilderOpen] = useState(false);
  const [activeType, setActiveType] = useState<ReportType>("orders");

  useEffect(() => setMounted(true), []);

  // Build current data based on type
  const currentData = useMemo(() => {
    if (activeType === "orders") return orders.slice(0, 100);
    if (activeType === "users") return adminUsers.slice(0, 100);
    if (activeType === "products") return products.slice(0, 100);
    return orders.slice(0, 100);
  }, [activeType, orders, products]);

  const columns: CsvColumn<Record<string, unknown>>[] = useMemo(() => {
    if (activeType === "orders") {
      return [
        { key: "id", label: isFa ? "شماره سفارش" : "Order ID" },
        { key: "customerName", label: isFa ? "مشتری" : "Customer" },
        { key: "customerMobile", label: isFa ? "موبایل" : "Mobile" },
        { key: "itemsCount", label: isFa ? "تعداد اقلام" : "Items" },
        {
          key: "total",
          label: isFa ? "مبلغ کل (تومان)" : "Total (T)",
          formatter: (v) => formatPrice(Number(v), locale),
        },
        { key: "status", label: isFa ? "وضعیت" : "Status" },
        {
          key: "createdAt",
          label: isFa ? "تاریخ" : "Date",
          formatter: (v) => formatDate(String(v), locale),
        },
      ];
    }
    if (activeType === "users") {
      return [
        { key: "id", label: "ID" },
        { key: "fullName", label: isFa ? "نام" : "Name" },
        { key: "email", label: isFa ? "ایمیل" : "Email" },
        { key: "mobile", label: isFa ? "موبایل" : "Mobile" },
        { key: "role", label: isFa ? "نقش" : "Role" },
        { key: "city", label: isFa ? "شهر" : "City" },
        { key: "ordersCount", label: isFa ? "تعداد سفارش" : "Orders" },
        {
          key: "totalSpent",
          label: isFa ? "مجموع خرید" : "Total Spent",
          formatter: (v) => formatPrice(Number(v), locale),
        },
      ];
    }
    if (activeType === "products") {
      return [
        { key: "id", label: "ID" },
        {
          key: "titleFa",
          label: isFa ? "عنوان" : "Title",
          formatter: (_v, row) =>
            isFa
              ? String(row.titleFa ?? "")
              : String(row.titleEn ?? ""),
        },
        { key: "brand", label: isFa ? "برند" : "Brand" },
        { key: "category", label: isFa ? "دسته" : "Category" },
        {
          key: "price",
          label: isFa ? "قیمت (تومان)" : "Price (T)",
          formatter: (v) => formatPrice(Number(v), locale),
        },
        {
          key: "finalPrice",
          label: isFa ? "قیمت نهایی" : "Final Price",
          formatter: (v) => formatPrice(Number(v), locale),
        },
        { key: "inStock", label: isFa ? "موجود" : "In Stock" },
      ];
    }
    return [];
  }, [activeType, locale, isFa]);

  const handleExport = (format: ReportFormat) => {
    const filename = `${activeType}-report-${Date.now()}`;
    const title = isFa
      ? `گزارش ${activeType === "orders" ? "سفارشات" : activeType === "users" ? "کاربران" : "محصولات"}`
      : `${activeType} Report`;

    try {
      if (format === "csv") {
        exportToCSV(currentData, columns, filename);
      } else if (format === "excel") {
        exportToExcel(currentData, columns, filename, activeType);
      } else {
        exportToPDF({
          title,
          subtitle: isFa
            ? `${currentData.length} رکورد`
            : `${currentData.length} records`,
          data: currentData,
          columns,
          filename,
          locale,
        });
      }

      pushToast({
        type: "success",
        titleFa: "گزارش دانلود شد",
        titleEn: "Report downloaded",
        messageFa: filename,
        messageEn: filename,
      });
    } catch (error) {
      pushToast({
        type: "error",
        titleFa: "خطا در دانلود",
        titleEn: "Download error",
      });
    }
  };

  const handleSaveReport = (data: {
    name: string;
    type: ReportType;
    format: ReportFormat;
    schedule?: "daily" | "weekly" | "monthly";
  }) => {
    addReport(data);
    setBuilderOpen(false);
    pushToast({
      type: "success",
      titleFa: "گزارش ذخیره شد",
      titleEn: "Report saved",
    });
  };

  const t = {
    title: isFa ? "گزارشات" : "Reports",
    subtitle: isFa
      ? "ساخت، مدیریت و دانلود گزارش‌های سفارشی"
      : "Create, manage and download custom reports",
    newReport: isFa ? "گزارش جدید" : "New Report",
    quickExport: isFa ? "خروجی سریع" : "Quick Export",
    savedReports: isFa ? "گزارش‌های ذخیره شده" : "Saved Reports",
    emptyReports: isFa
      ? "هنوز گزارشی ذخیره نکرده‌اید"
      : "You haven't saved any reports yet",
    orders: isFa ? "سفارشات" : "Orders",
    users: isFa ? "کاربران" : "Users",
    products: isFa ? "محصولات" : "Products",
    sales: isFa ? "فروش" : "Sales",
    records: isFa ? "رکورد" : "records",
  };

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  const quickExportTypes: Array<{
    value: ReportType;
    icon: typeof ShoppingCart;
    label: string;
    color: string;
  }> = [
    { value: "orders", icon: ShoppingCart, label: t.orders, color: "#EF4056" },
    { value: "users", icon: UsersIcon, label: t.users, color: "#00BFFF" },
    { value: "products", icon: Package, label: t.products, color: "#8B5CF6" },
    { value: "sales", icon: DollarSign, label: t.sales, color: "#22C55E" },
  ];

  return (
    <div className="space-y-4 md:space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {t.title}
          </h1>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.subtitle}
          </p>
        </div>
        <button
          onClick={() => setBuilderOpen((v) => !v)}
          className="h-10 px-4 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Plus size={14} />
          {t.newReport}
        </button>
      </div>

      {/* Builder */}
      <AnimatePresence>
        {builderOpen && (
          <ReportBuilder
            locale={locale}
            onSave={handleSaveReport}
            onCancel={() => setBuilderOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Quick Export */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-5">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center">
            <Download size={16} className="text-[#EF4056]" />
          </div>
          <div>
            <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
              {t.quickExport}
            </h2>
            <p className="text-[10px] text-[#A1A3A8]">
              {currentData.length.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
              {t.records}
            </p>
          </div>
        </div>

        {/* Type selector */}
        <div className="flex flex-wrap gap-2 mb-4">
          {quickExportTypes.map((tp) => {
            const Icon = tp.icon;
            return (
              <button
                key={tp.value}
                onClick={() => setActiveType(tp.value)}
                className={`h-9 px-3 rounded-lg text-[11px] font-medium transition-all flex items-center gap-1.5 ${
                  activeType === tp.value
                    ? "text-white shadow-sm"
                    : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#3A3A40]"
                }`}
                style={
                  activeType === tp.value
                    ? { backgroundColor: tp.color }
                    : undefined
                }
              >
                <Icon size={13} />
                {tp.label}
              </button>
            );
          })}
        </div>

        {/* Export buttons */}
        <div className="pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
          <ExportButtons
            locale={locale}
            onExport={handleExport}
            disabled={currentData.length === 0}
          />
        </div>
      </div>

      {/* Saved Reports */}
      <div>
        <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
          <FileText size={16} className="text-[#EF4056]" />
          {t.savedReports}
          <span className="text-[11px] text-[#A1A3A8] font-normal">
            ({savedReports.length.toLocaleString(isFa ? "fa-IR" : "en-US")})
          </span>
        </h2>

        {savedReports.length === 0 ? (
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-12 text-center">
            <div className="w-14 h-14 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
              <FileText size={24} className="text-[#A1A3A8]" />
            </div>
            <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8]">
              {t.emptyReports}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {savedReports.map((report, i) => (
              <ReportCard
                key={report.id}
                locale={locale}
                report={report}
                delay={i * 0.05}
                onDownload={() => {
                  setActiveType(report.type);
                  setTimeout(() => handleExport(report.format), 100);
                }}
                onDelete={() => {
                  removeReport(report.id);
                  pushToast({
                    type: "info",
                    titleFa: "گزارش حذف شد",
                    titleEn: "Report deleted",
                  });
                }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
'''))

# ============================================================
# app/[locale]/admin/reports/page.tsx
# ============================================================
files.append(("app/[locale]/admin/reports/page.tsx", '''import ReportsView from "@/components/admin/ReportsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminReportsPage({ params }: PageProps) {
  const { locale } = await params;
  return <ReportsView locale={locale as "fa" | "en"} />;
}
'''))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", '''// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as DashboardView } from "./DashboardView";
export { default as AnalyticsView } from "./AnalyticsView";
export { default as UsersView } from "./UsersView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as ReportsView } from "./ReportsView";
export { default as AdminLoginForm } from "./AdminLoginForm";

// Layout
export * from "./layout";

// Dashboard
export * from "./dashboard";

// Analytics
export * from "./analytics";

// Users
export * from "./users";

// Products
export * from "./products";

// Orders
export * from "./orders";

// Reports
export * from "./reports";

// Charts
export * from "./charts";
'''))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 8: Reports & Export")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")
    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/reports")

if __name__ == "__main__":
    main()