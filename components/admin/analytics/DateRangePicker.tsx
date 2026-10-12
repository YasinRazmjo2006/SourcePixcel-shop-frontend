"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Calendar, ChevronDown, Check } from "lucide-react";
import type { Locale, DateRangePreset } from "@/lib/types";

interface DateRangePickerProps {
  locale: Locale;
  value: DateRangePreset;
  onChange: (preset: DateRangePreset) => void;
}

const PRESETS: Array<{ value: DateRangePreset; fa: string; en: string }> = [
  { value: "today", fa: "امروز", en: "Today" },
  { value: "yesterday", fa: "دیروز", en: "Yesterday" },
  { value: "last7days", fa: "۷ روز گذشته", en: "Last 7 Days" },
  { value: "last30days", fa: "۳۰ روز گذشته", en: "Last 30 Days" },
  { value: "last90days", fa: "۹۰ روز گذشته", en: "Last 90 Days" },
  { value: "thisMonth", fa: "این ماه", en: "This Month" },
  { value: "lastMonth", fa: "ماه گذشته", en: "Last Month" },
  { value: "thisYear", fa: "امسال", en: "This Year" },
];

export default function DateRangePicker({
  locale,
  value,
  onChange,
}: DateRangePickerProps) {
  const isFa = locale === "fa";
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const current = PRESETS.find((p) => p.value === value);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-2 h-10 px-4 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] transition-colors"
      >
        <Calendar size={14} className="text-[#A1A3A8]" />
        <span className="font-medium">
          {isFa ? current?.fa : current?.en}
        </span>
        <motion.div animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronDown size={14} className="text-[#A1A3A8]" />
        </motion.div>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
            className={`absolute top-full mt-2 w-56 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl shadow-2xl overflow-hidden z-50 ${
              isFa ? "right-0" : "left-0"
            }`}
          >
            <div className="p-1.5">
              {PRESETS.map((preset) => (
                <button
                  key={preset.value}
                  onClick={() => {
                    onChange(preset.value);
                    setOpen(false);
                  }}
                  className={`w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg text-[12px] transition-colors ${
                    value === preset.value
                      ? "bg-[#EF4056]/5 text-[#EF4056] font-medium"
                      : "text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
                  }`}
                >
                  <span>{isFa ? preset.fa : preset.en}</span>
                  {value === preset.value && (
                    <Check size={14} className="text-[#EF4056]" />
                  )}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
