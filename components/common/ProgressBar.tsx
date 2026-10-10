"use client";

import { motion } from "framer-motion";

interface ProgressBarProps {
  value: number; // 0-100
  color?: string;
  height?: number;
  showLabel?: boolean;
}

export default function ProgressBar({
  value,
  color = "#EF4056",
  height = 4,
  showLabel = false,
}: ProgressBarProps) {
  const clamped = Math.max(0, Math.min(100, value));

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between mb-1">
          <span className="text-[10px] text-[#A1A3A8]">{clamped}%</span>
        </div>
      )}
      <div
        className="w-full bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-full overflow-hidden"
        style={{ height }}
      >
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${clamped}%` }}
          transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
          className="h-full rounded-full"
          style={{
            background: `linear-gradient(90deg, ${color} 0%, ${color}dd 100%)`,
          }}
        />
      </div>
    </div>
  );
}
