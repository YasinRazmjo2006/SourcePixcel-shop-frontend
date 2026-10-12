"use client";

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
