"use client";

import { Target } from "lucide-react";
import type { Locale } from "@/lib/types";
import ChartCard from "../charts/ChartCard";
import RadialProgress from "./RadialProgress";

interface GoalsCardProps {
  locale: Locale;
}

export default function GoalsCard({ locale }: GoalsCardProps) {
  const isFa = locale === "fa";

  const goals = [
    {
      id: "revenue",
      value: 82,
      color: "#22C55E",
      label: isFa ? "درآمد" : "Revenue",
      sublabel: isFa ? "۸۲٪ از هدف" : "82% of goal",
    },
    {
      id: "orders",
      value: 67,
      color: "#EF4056",
      label: isFa ? "سفارشات" : "Orders",
      sublabel: isFa ? "۶۷٪ از هدف" : "67% of goal",
    },
    {
      id: "users",
      value: 91,
      color: "#00BFFF",
      label: isFa ? "کاربران" : "Users",
      sublabel: isFa ? "۹۱٪ از هدف" : "91% of goal",
    },
    {
      id: "conversion",
      value: 54,
      color: "#8B5CF6",
      label: isFa ? "تبدیل" : "Conversion",
      sublabel: isFa ? "۵۴٪ از هدف" : "54% of goal",
    },
  ];

  return (
    <ChartCard
      titleFa="اهداف ماهانه"
      titleEn="Monthly Goals"
      subtitleFa="پیشرفت اهداف تعیین‌شده"
      subtitleEn="Progress toward set goals"
      icon={Target}
      delay={0.3}
    >
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {goals.map((goal, i) => (
          <RadialProgress
            key={goal.id}
            value={goal.value}
            color={goal.color}
            label={goal.label}
            sublabel={goal.sublabel}
            size={100}
            thickness={8}
            delay={0.4 + i * 0.1}
          />
        ))}
      </div>
    </ChartCard>
  );
}
