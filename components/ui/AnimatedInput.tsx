"use client";

import { forwardRef, useState, type InputHTMLAttributes } from "react";
import { motion } from "framer-motion";

interface AnimatedInputProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, "onChange"> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
  value: string;
  onChange: (value: string) => void;
}

const AnimatedInput = forwardRef<HTMLInputElement, AnimatedInputProps>(
  (
    { label, error, icon, value, onChange, className, ...props },
    ref
  ) => {
    const [isFocused, setIsFocused] = useState(false);

    return (
      <div className="w-full">
        {label && (
          <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {label}
          </label>
        )}

        <div className="relative">
          <input
            ref={ref}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            className={`w-full h-11 px-3 ${
              icon ? "pr-10" : ""
            } rounded-lg bg-white dark:bg-[#1A1A1E] border text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
              error
                ? "border-[#EF4444] focus:border-[#EF4444]"
                : "border-[#E0E0E2] dark:border-[#2A2A2E]"
            } ${className ?? ""}`}
            {...props}
          />

          {icon && (
            <div
              className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8] pointer-events-none"
              style={{ right: 12 }}
            >
              {icon}
            </div>
          )}

          {/* Animated underline */}
          <motion.div
            initial={false}
            animate={{
              scaleX: isFocused && !error ? 1 : 0,
              opacity: isFocused && !error ? 1 : 0,
            }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="absolute bottom-0 left-2 right-2 h-[2px] bg-[#EF4056] rounded-full origin-center"
          />
        </div>

        {error && (
          <motion.p
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-[11px] text-[#EF4444] mt-1"
          >
            {error}
          </motion.p>
        )}
      </div>
    );
  }
);

AnimatedInput.displayName = "AnimatedInput";

export default AnimatedInput;
