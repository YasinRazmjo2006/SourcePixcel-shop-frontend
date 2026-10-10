"use client";

import { motion } from "framer-motion";
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
      <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
        {isFa ? "تعداد:" : "Quantity:"}
      </span>
      <div className="flex items-center gap-1 border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg overflow-hidden">
        <motion.button
          onClick={inc}
          disabled={value >= max}
          whileHover={value < max ? { scale: 1.1 } : {}}
          whileTap={value < max ? { scale: 0.9 } : {}}
          aria-label="Increase quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
        >
          <Plus size={16} />
        </motion.button>

        <div className="w-10 text-center relative overflow-hidden">
          <motion.span
            key={value}
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 10, opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums block"
          >
            {isFa ? value.toLocaleString("fa-IR") : value}
          </motion.span>
        </div>

        <motion.button
          onClick={dec}
          disabled={value <= min}
          whileHover={value > min ? { scale: 1.1 } : {}}
          whileTap={value > min ? { scale: 0.9 } : {}}
          aria-label="Decrease quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
        >
          <Minus size={16} />
        </motion.button>
      </div>
    </div>
  );
}
