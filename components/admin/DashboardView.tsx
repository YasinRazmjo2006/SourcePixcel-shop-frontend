import AdminStats from "./AdminStats";
import SalesChart from "./SalesChart";
import TopProducts from "./TopProducts";
import RecentOrders from "./RecentOrders";

interface DashboardViewProps {
  locale: string;
}

export default function DashboardView({ locale }: DashboardViewProps) {
  const isFa = locale === "fa";

  return (
    <div className="space-y-4">
      {/* Header */}
      <div>
        <h1 className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {isFa ? "داشبورد" : "Dashboard"}
        </h1>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? "خلاصه‌ای از عملکرد فروشگاه SourcePixcel"
            : "Overview of SourcePixcel store performance"}
        </p>
      </div>

      {/* Stats */}
      <AdminStats locale={locale} />

      {/* Chart + Top Products */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <SalesChart locale={locale} />
        </div>
        <div className="lg:col-span-1">
          <TopProducts locale={locale} />
        </div>
      </div>

      {/* Recent Orders */}
      <RecentOrders locale={locale} />
    </div>
  );
}
