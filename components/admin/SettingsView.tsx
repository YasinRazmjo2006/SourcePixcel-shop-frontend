"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Settings as SettingsIcon, RotateCcw } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAdminSettingsStore, useToastStore } from "@/lib/stores";
import SettingsTabs, { type SettingsTab } from "./settings/SettingsTabs";
import SiteSettingsForm from "./settings/SiteSettingsForm";
import PaymentSettingsForm from "./settings/PaymentSettingsForm";
import ShippingSettingsForm from "./settings/ShippingSettingsForm";

interface SettingsViewProps {
  locale: Locale;
}

export default function SettingsView({ locale }: SettingsViewProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const reset = useAdminSettingsStore((s) => s.reset);

  const [activeTab, setActiveTab] = useState<SettingsTab>("site");

  const handleReset = () => {
    if (confirm(isFa ? "همه تنظیمات به حالت پیش‌فرض برگردند؟" : "Reset all settings to default?")) {
      reset();
      pushToast({
        type: "info",
        titleFa: "تنظیمات بازنشانی شد",
        titleEn: "Settings reset",
      });
    }
  };

  const t = {
    title: isFa ? "تنظیمات" : "Settings",
    subtitle: isFa ? "مدیریت پیکربندی فروشگاه" : "Manage store configuration",
    reset: isFa ? "بازنشانی به پیش‌فرض" : "Reset to Default",
  };

  return (
    <div className="space-y-4 md:space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-[#EF4056]/10 flex items-center justify-center shrink-0">
            <SettingsIcon size={20} className="text-[#EF4056]" />
          </div>
          <div>
            <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-0.5">
              {t.title}
            </h1>
            <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
              {t.subtitle}
            </p>
          </div>
        </div>

        <button
          onClick={handleReset}
          className="h-10 px-4 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4444] hover:text-[#EF4444] transition-colors flex items-center gap-2"
        >
          <RotateCcw size={14} />
          {t.reset}
        </button>
      </div>

      {/* Tabs */}
      <SettingsTabs locale={locale} active={activeTab} onChange={setActiveTab} />

      {/* Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === "site" && <SiteSettingsForm locale={locale} />}
          {activeTab === "payment" && <PaymentSettingsForm locale={locale} />}
          {activeTab === "shipping" && <ShippingSettingsForm locale={locale} />}
          {activeTab === "notifications" && (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[12px] text-[#A1A3A8]">
              {isFa ? "تنظیمات اعلان‌ها به زودی..." : "Notification settings coming soon..."}
            </div>
          )}
          {activeTab === "security" && (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[12px] text-[#A1A3A8]">
              {isFa ? "تنظیمات امنیتی به زودی..." : "Security settings coming soon..."}
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
