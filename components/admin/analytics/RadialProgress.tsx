"use client";

import { motion } from "framer-motion";
import type { Locale } from "@/lib/types";

interface RadialProgressProps {
  value: number;
  max?: number;
  size?: number;
  thickness?: number;
  color?: string;
  label: string;
  sublabel?: string;
  delay?: number;
}

export default function RadialProgress({
  value,
  max = 100,
  size = 100,
  thickness = 8,
  color = "#EF4056",
  label,
  sublabel,
  delay = 0,
}: RadialProgressProps) {
  const radius = (size - thickness) / 2;
  const circumference = 2 * Math.PI * radius;
  const percentage = Math.min(100, (value / max) * 100);
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="#F5F5F5"
            strokeWidth={thickness}
            fill="none"
            className="dark:stroke-[#2A2A2E]"
          />
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={thickness}
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ delay, duration: 1, ease: [0.16, 1, 0.3, 1] }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
            {Math.round(percentage)}%
          </div>
        </div>
      </div>
      <div className="text-center">
        <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
          {label}
        </div>
        {sublabel && (
          <div className="text-[10px] text-[#A1A3A8] mt-0.5">{sublabel}</div>
        )}
      </div>
    </div>
  );
}
