"use client";

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
