"use client";

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
