"use client";

import { motion } from "framer-motion";
import {
  Globe,
  CreditCard,
  Truck,
  Bell,
  Shield,
  type LucideIcon,
} from "lucide-react";
import type { Locale } from "@/lib/types";

export type SettingsTab =
  | "site"
  | "payment"
  | "shipping"
  | "notifications"
  | "security";

interface SettingsTabsProps {
  locale: Locale;
  active: SettingsTab;
  onChange: (tab: SettingsTab) => void;
}

export default function SettingsTabs({
  locale,
  active,
  onChange,
}: SettingsTabsProps) {
  const isFa = locale === "fa";

  const tabs: Array<{
    id: SettingsTab;
    icon: LucideIcon;
    fa: string;
    en: string;
  }> = [
    { id: "site", icon: Globe, fa: "اطلاعات سایت", en: "Site Info" },
    { id: "payment", icon: CreditCard, fa: "پرداخت", en: "Payment" },
    { id: "shipping", icon: Truck, fa: "ارسال", en: "Shipping" },
    { id: "notifications", icon: Bell, fa: "اعلان‌ها", en: "Notifications" },
    { id: "security", icon: Shield, fa: "امنیت", en: "Security" },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-1.5 overflow-x-auto">
      <div className="flex items-center gap-1 min-w-max">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = active === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onChange(tab.id)}
              className={`relative flex items-center gap-2 h-10 px-4 rounded-lg text-[12px] font-medium transition-colors whitespace-nowrap ${
                isActive
                  ? "text-white"
                  : "text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="settings-tab-bg"
                  className="absolute inset-0 bg-[#EF4056] rounded-lg"
                  transition={{ type: "spring", stiffness: 400, damping: 30 }}
                />
              )}
              <span className="relative flex items-center gap-2">
                <Icon size={14} />
                {isFa ? tab.fa : tab.en}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
