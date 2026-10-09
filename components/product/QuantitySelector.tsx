"use client";

import { Minus, Plus } from "lucide-react";
import type { Locale } from "@/lib/types";

interface QuantitySelectorProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  locale: Locale;
}

export default function QuantitySelector({
  value,
  onChange,
  min = 1,
  max = 10,
  locale,
}: QuantitySelectorProps) {
  const isFa = locale === "fa";

  const dec = () => onChange(Math.max(min, value - 1));
  const inc = () => onChange(Math.min(max, value + 1));

  return (
    <div className="flex items-center gap-3">
      <span className="text-[12px] text-[#62666D]">
        {isFa ? "تعداد:" : "Quantity:"}
      </span>
      <div className="flex items-center gap-2 border border-[#E0E0E2] rounded-lg">
        <button
          onClick={inc}
          disabled={value >= max}
          aria-label="Increase quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] rounded-r-lg transition-colors"
        >
          <Plus size={16} />
        </button>
        <span className="w-8 text-center text-[14px] font-bold text-[#3F4064] tabular-nums">
          {isFa ? value.toLocaleString("fa-IR") : value}
        </span>
        <button
          onClick={dec}
          disabled={value <= min}
          aria-label="Decrease quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] rounded-l-lg transition-colors"
        >
          <Minus size={16} />
        </button>
      </div>
    </div>
  );
}
