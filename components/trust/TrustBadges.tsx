"use client";

import { motion } from "framer-motion";
import {
  ShieldCheck,
  Award,
  Lock,
  BadgeCheck,
  FileCheck,
  Building2,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface TrustBadgesProps {
  locale: Locale;
  variant?: "default" | "compact";
}

const BADGES = [
  {
    icon: ShieldCheck,
    labelFa: "نماد اعتماد الکترونیکی",
    labelEn: "E-Trust Seal",
    color: "#22C55E",
  },
  {
    icon: BadgeCheck,
    labelFa: "ساماندهی رسانه‌های دیجیتال",
    labelEn: "Digital Media Regulation",
    color: "#00BFFF",
  },
  {
    icon: Building2,
    labelFa: "اتحادیه کشوری کسب‌وکار",
    labelEn: "National Business Union",
    color: "#8B5CF6",
  },
  {
    icon: Lock,
    labelFa: "پرداخت امن SSL",
    labelEn: "SSL Secure Payment",
    color: "#F59E0B",
  },
  {
    icon: Award,
    labelFa: "برترین فروشگاه آنلاین",
    labelEn: "Top Online Store",
    color: "#EF4056",
  },
  {
    icon: FileCheck,
    labelFa: "ضمانت بازگشت ۷ روزه",
    labelEn: "7-Day Return Guarantee",
    color: "#10B981",
  },
];

export default function TrustBadges({
  locale,
  variant = "default",
}: TrustBadgesProps) {
  const isFa = locale === "fa";

  if (variant === "compact") {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <h3 className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
          <ShieldCheck size={14} className="text-[#22C55E]" />
          {isFa ? "نشان‌های اعتماد" : "Trust Badges"}
        </h3>
        <div className="grid grid-cols-3 gap-2">
          {BADGES.slice(0, 6).map((badge, i) => {
            const Icon = badge.icon;
            return (
              <motion.div
                key={i}
                whileHover={{ scale: 1.05, y: -2 }}
                className="aspect-square rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex flex-col items-center justify-center gap-1 p-2 cursor-pointer hover:shadow-sm transition-shadow"
                style={{ backgroundColor: `${badge.color}08` }}
              >
                <Icon
                  size={20}
                  style={{ color: badge.color }}
                />
                <span className="text-[8px] text-center text-[#62666D] dark:text-[#A1A3A8] leading-tight">
                  {isFa ? badge.labelFa : badge.labelEn}
                </span>
              </motion.div>
            );
          })}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center gap-2 mb-4">
        <ShieldCheck size={18} className="text-[#22C55E]" />
        <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "چرا SourcePixcel؟" : "Why SourcePixcel?"}
        </h2>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {BADGES.map((badge, i) => {
          const Icon = badge.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              whileHover={{ scale: 1.03, y: -3 }}
              className="flex flex-col items-center gap-2 p-3 rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] cursor-pointer hover:shadow-md transition-all"
              style={{ backgroundColor: `${badge.color}08` }}
            >
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center"
                style={{ backgroundColor: `${badge.color}15` }}
              >
                <Icon size={22} style={{ color: badge.color }} />
              </div>
              <span className="text-[10px] md:text-[11px] text-center text-[#3F4064] dark:text-[#E5E5EA] font-medium leading-tight">
                {isFa ? badge.labelFa : badge.labelEn}
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
