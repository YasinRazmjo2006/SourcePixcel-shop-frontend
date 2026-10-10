"use client";

import { motion } from "framer-motion";
import {
  Truck,
  RefreshCw,
  Headphones,
  Award,
  CreditCard,
  Package,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface GuaranteesProps {
  locale: Locale;
}

const GUARANTEES = [
  {
    icon: Truck,
    titleFa: "ارسال سریع",
    titleEn: "Fast Shipping",
    descFa: "ارسال به سراسر ایران در ۲۴ ساعت",
    descEn: "Delivery across Iran within 24 hours",
    color: "#EF4056",
  },
  {
    icon: RefreshCw,
    titleFa: "بازگشت ۷ روزه",
    titleEn: "7-Day Return",
    descFa: "بازگشت آسان بدون قید و شرط",
    descEn: "Easy return without any conditions",
    color: "#22C55E",
  },
  {
    icon: Award,
    titleFa: "ضمانت اصالت",
    titleEn: "Authenticity",
    descFa: "۱۰۰٪ اورجینال و با ضمانت",
    descEn: "100% original with warranty",
    color: "#8B5CF6",
  },
  {
    icon: CreditCard,
    titleFa: "پرداخت امن",
    titleEn: "Secure Payment",
    descFa: "پرداخت آنلاین با رمزنگاری SSL",
    descEn: "Online payment with SSL encryption",
    color: "#00BFFF",
  },
  {
    icon: Headphones,
    titleFa: "پشتیبانی ۲۴/۷",
    titleEn: "24/7 Support",
    descFa: "پاسخگویی در تمام ساعات شبانه‌روز",
    descEn: "Available at all hours",
    color: "#F59E0B",
  },
  {
    icon: Package,
    titleFa: "بسته‌بندی حرفه‌ای",
    titleEn: "Pro Packaging",
    descFa: "بسته‌بندی ایمن و استاندارد",
    descEn: "Safe and standard packaging",
    color: "#EC4899",
  },
];

export default function Guarantees({ locale }: GuaranteesProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-5">
        {isFa ? "تعهدات ما به شما" : "Our Promises to You"}
      </h2>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {GUARANTEES.map((item, i) => {
          const Icon = item.icon;
          return (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="flex items-start gap-3 group"
            >
              <motion.div
                whileHover={{ scale: 1.1, rotate: 5 }}
                className="w-11 h-11 rounded-xl flex items-center justify-center shrink-0"
                style={{ backgroundColor: `${item.color}15` }}
              >
                <Icon size={20} style={{ color: item.color }} />
              </motion.div>
              <div className="min-w-0">
                <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1 group-hover:text-[#EF4056] transition-colors">
                  {isFa ? item.titleFa : item.titleEn}
                </div>
                <div className="text-[10px] text-[#62666D] dark:text-[#A1A3A8] leading-5">
                  {isFa ? item.descFa : item.descEn}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
