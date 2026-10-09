import {
  Truck,
  ShieldCheck,
  RotateCcw,
  Headphones,
  Award,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface ServiceBadgesProps {
  locale: Locale;
}

export default function ServiceBadges({ locale }: ServiceBadgesProps) {
  const isFa = locale === "fa";

  const badges = [
    {
      icon: Truck,
      fa: "ارسال سریع",
      en: "Fast Shipping",
      color: "#EF4056",
      bg: "#EF4056",
    },
    {
      icon: ShieldCheck,
      fa: "پرداخت امن",
      en: "Secure Payment",
      color: "#22C55E",
      bg: "#22C55E",
    },
    {
      icon: RotateCcw,
      fa: "۷ روز بازگشت",
      en: "7-Day Return",
      color: "#00BFFF",
      bg: "#00BFFF",
    },
    {
      icon: Headphones,
      fa: "پشتیبانی ۲۴/۷",
      en: "24/7 Support",
      color: "#F59E0B",
      bg: "#F59E0B",
    },
    {
      icon: Award,
      fa: "ضمانت اصالت",
      en: "Authentic",
      color: "#8B5CF6",
      bg: "#8B5CF6",
    },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
      <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
        {badges.map((b, i) => {
          const Icon = b.icon;
          return (
            <div
              key={i}
              className="flex flex-col items-center gap-2 text-center group cursor-pointer"
            >
              <div
                className="w-12 h-12 rounded-full flex items-center justify-center transition-transform group-hover:scale-110"
                style={{ backgroundColor: `${b.bg}15` }}
              >
                <Icon size={22} style={{ color: b.color }} />
              </div>
              <span className="text-[11px] md:text-[12px] text-[#62666D] dark:text-[#A1A3A8] font-medium">
                {isFa ? b.fa : b.en}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
