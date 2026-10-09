import {
  TrendingUp,
  TrendingDown,
  ShoppingCart,
  Users,
  Package,
  DollarSign,
} from "lucide-react";

interface AdminStatsProps {
  locale: string;
}

export default function AdminStats({ locale }: AdminStatsProps) {
  const isFa = locale === "fa";

  const stats = [
    {
      icon: DollarSign,
      labelFa: "فروش امروز",
      labelEn: "Today's Sales",
      value: "۱۲,۴۵۰,۰۰۰",
      suffix: isFa ? "تومان" : "T",
      change: 12.5,
      changeUp: true,
      color: "#22C55E",
    },
    {
      icon: ShoppingCart,
      labelFa: "سفارشات امروز",
      labelEn: "Today's Orders",
      value: isFa ? "۴۸" : "48",
      suffix: "",
      change: 8.2,
      changeUp: true,
      color: "#EF4056",
    },
    {
      icon: Users,
      labelFa: "کاربران جدید",
      labelEn: "New Users",
      value: isFa ? "۲۳" : "23",
      suffix: "",
      change: 3.1,
      changeUp: false,
      color: "#00BFFF",
    },
    {
      icon: Package,
      labelFa: "محصولات",
      labelEn: "Products",
      value: isFa ? "۶۸" : "68",
      suffix: "",
      change: 0,
      changeUp: true,
      color: "#8B5CF6",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, i) => {
        const Icon = stat.icon;
        return (
          <div
            key={i}
            className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4"
          >
            <div className="flex items-center justify-between mb-3">
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: `${stat.color}15` }}
              >
                <Icon size={20} style={{ color: stat.color }} />
              </div>
              {stat.change !== 0 && (
                <div
                  className={`flex items-center gap-1 text-[10px] font-medium ${
                    stat.changeUp ? "text-[#22C55E]" : "text-[#EF4444]"
                  }`}
                >
                  {stat.changeUp ? (
                    <TrendingUp size={12} />
                  ) : (
                    <TrendingDown size={12} />
                  )}
                  {stat.change}%
                </div>
              )}
            </div>
            <div className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-1">
              {stat.value}
              {stat.suffix && (
                <span className="text-[11px] text-[#A1A3A8] font-normal mr-1">
                  {stat.suffix}
                </span>
              )}
            </div>
            <div className="text-[11px] text-[#A1A3A8]">
              {isFa ? stat.labelFa : stat.labelEn}
            </div>
          </div>
        );
      })}
    </div>
  );
}
