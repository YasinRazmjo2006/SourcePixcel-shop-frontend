"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

interface AnimatedCheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
}

export default function AnimatedCheckbox({
  checked,
  onChange,
  label,
  disabled = false,
}: AnimatedCheckboxProps) {
  return (
    <label
      className={`flex items-center gap-2.5 cursor-pointer select-none group ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
    >
      <motion.div
        onClick={() => !disabled && onChange(!checked)}
        whileHover={!disabled ? { scale: 1.08 } : {}}
        whileTap={!disabled ? { scale: 0.92 } : {}}
        className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-colors shrink-0 ${
          checked
            ? "bg-[#EF4056] border-[#EF4056]"
            : "bg-white dark:bg-[#1A1A1E] border-[#E0E0E2] dark:border-[#3A3A40] group-hover:border-[#EF4056]"
        }`}
      >
        <motion.div
          initial={false}
          animate={
            checked
              ? { scale: 1, opacity: 1 }
              : { scale: 0, opacity: 0 }
          }
          transition={{
            type: "spring",
            stiffness: 500,
            damping: 30,
          }}
        >
          <Check size={12} className="text-white" strokeWidth={3.5} />
        </motion.div>
      </motion.div>

      {label && (
        <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] group-hover:text-[#3F4064] dark:group-hover:text-[#E5E5EA] transition-colors">
          {label}
        </span>
      )}
    </label>
  );
}
