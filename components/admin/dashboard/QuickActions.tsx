"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Plus, Tag, Upload, Download, FileText, Users, Settings as SettingsIcon, type LucideIcon } from "lucide-react";
import type { Locale } from "@/lib/types";

interface QuickActionsProps { locale: Locale; }

export default function QuickActions({ locale }: QuickActionsProps) {
  const isFa = locale === "fa";
  const actions: Array<{ id: string; href: string; icon: LucideIcon; labelFa: string; labelEn: string; color: string }> = [
    { id: "add-product", href: "/admin/products/new", icon: Plus, labelFa: "محصول جدید", labelEn: "New Product", color: "#EF4056" },
    { id: "add-discount", href: "/admin/discounts", icon: Tag, labelFa: "تخفیف جدید", labelEn: "New Discount", color: "#22C55E" },
    { id: "upload", href: "/admin/products", icon: Upload, labelFa: "آپلود محصولات", labelEn: "Upload Products", color: "#00BFFF" },
    { id: "export", href: "/admin/reports", icon: Download, labelFa: "دانلود گزارش", labelEn: "Download Report", color: "#8B5CF6" },
    { id: "reports", href: "/admin/reports", icon: FileText, labelFa: "گزارشات", labelEn: "Reports", color: "#F59E0B" },
    { id: "users", href: "/admin/users", icon: Users, labelFa: "مدیریت کاربران", labelEn: "Manage Users", color: "#EC4899" },
    { id: "settings", href: "/admin/settings", icon: SettingsIcon, labelFa: "تنظیمات", labelEn: "Settings", color: "#94A3B8" },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
      <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">{isFa ? "دسترسی سریع" : "Quick Actions"}</h3>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-2">
        {actions.map((action, i) => {
          const Icon = action.icon;
          return (
            <motion.div key={action.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
              <Link href={`/${locale}${action.href}`} className="flex flex-col items-center gap-2 p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-md hover:border-transparent transition-all group" style={{ backgroundColor: `${action.color}05` }}>
                <div className="w-9 h-9 rounded-lg flex items-center justify-center transition-transform group-hover:scale-110" style={{ backgroundColor: `${action.color}15` }}>
                  <Icon size={16} style={{ color: action.color }} />
                </div>
                <span className="text-[10px] text-[#3F4064] dark:text-[#E5E5EA] font-medium text-center leading-tight">{isFa ? action.labelFa : action.labelEn}</span>
              </Link>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
