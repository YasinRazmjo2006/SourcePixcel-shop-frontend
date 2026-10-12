import { Activity, Package, Users, Star, CreditCard, AlertTriangle, Settings as SettingsIcon, type LucideIcon } from "lucide-react";
import type { Locale, ActivityType } from "@/lib/types";
import { getRecentActivities } from "@/lib/data";
import { formatRelativeTime } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";

interface ActivityTimelineProps { locale: Locale; }

const CONFIG: Record<ActivityType, { icon: LucideIcon; color: string }> = {
  order: { icon: Package, color: "#22C55E" },
  user: { icon: Users, color: "#00BFFF" },
  review: { icon: Star, color: "#F59E0B" },
  payment: { icon: CreditCard, color: "#8B5CF6" },
  product: { icon: AlertTriangle, color: "#EF4056" },
  system: { icon: SettingsIcon, color: "#94A3B8" },
};

export default function ActivityTimeline({ locale }: ActivityTimelineProps) {
  const isFa = locale === "fa";
  const activities = getRecentActivities(8);

  return (
    <ChartCard titleFa="فعالیت‌های اخیر" titleEn="Recent Activity" subtitleFa="آخرین رویدادها" subtitleEn="Latest events" icon={Activity} delay={0.4}>
      <div className="relative">
        <div className="absolute top-2 bottom-2 right-[15px] w-px bg-gradient-to-b from-[#EF4056]/30 via-[#E0E0E2] to-transparent dark:via-[#2A2A2E]" />
        <div className="space-y-4 relative">
          {activities.map((activity) => {
            const config = CONFIG[activity.type];
            const Icon = config.icon;
            return (
              <div key={activity.id} className="flex gap-3 relative">
                <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 border-2 border-white dark:border-[#1A1A1E] z-10" style={{ backgroundColor: `${config.color}20` }}>
                  <Icon size={14} style={{ color: config.color }} />
                </div>
                <div className="flex-1 min-w-0 pb-1">
                  <div className="flex items-start justify-between gap-2">
                    <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] leading-5">{isFa ? activity.titleFa : activity.titleEn}</div>
                    <span className="text-[10px] text-[#A1A3A8] shrink-0 whitespace-nowrap">{formatRelativeTime(activity.timestamp, locale)}</span>
                  </div>
                  <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] leading-5 line-clamp-2 mt-0.5">{isFa ? activity.descriptionFa : activity.descriptionEn}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </ChartCard>
  );
}
