"use client";

import { motion } from "framer-motion";
import { type LucideIcon } from "lucide-react";

interface ChartCardProps {
  titleFa: string;
  titleEn: string;
  subtitleFa?: string;
  subtitleEn?: string;
  icon?: LucideIcon;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export default function ChartCard({
  titleFa,
  titleEn,
  subtitleFa,
  subtitleEn,
  icon: Icon,
  action,
  children,
  className,
  delay = 0,
}: ChartCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: [0.16, 1, 0.3, 1] }}
      className={`bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden ${className ?? ""}`}
    >
      <div className="flex items-start justify-between gap-3 p-4 md:p-5 border-b border-[#F5F5F5] dark:border-[#2A2A2E]">
        <div className="flex items-start gap-3 min-w-0">
          {Icon && (
            <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center shrink-0">
              <Icon size={16} className="text-[#EF4056]" />
            </div>
          )}
          <div className="min-w-0">
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] truncate">
              {titleFa}
            </h3>
            {(subtitleFa || subtitleEn) && (
              <p className="text-[11px] text-[#A1A3A8] mt-0.5 truncate">
                {subtitleFa}
              </p>
            )}
          </div>
        </div>
        {action}
      </div>
      <div className="p-4 md:p-5">{children}</div>
    </motion.div>
  );
}
