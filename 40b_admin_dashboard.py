# 40b_admin_dashboard.py
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

files.append(("components/admin/dashboard/KpiCards.tsx", """\"use client\";

import { useEffect, useRef, useState } from \"react\";
import { motion, useInView } from \"framer-motion\";
import { TrendingUp, TrendingDown, DollarSign, ShoppingCart, Users, Package, type LucideIcon } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { formatCompact, formatPercent } from \"@/lib/utils\";
import { analyticsOverview } from \"@/lib/data\";

interface KpiCardsProps {
  locale: Locale;
}

function AnimatedNumber({ value, formatter }: { value: number; formatter: (v: number) => string }) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: \"-50px\" });

  useEffect(() => {
    if (!inView) return;
    const duration = 1200;
    const steps = 50;
    const stepTime = duration / steps;
    const increment = value / steps;
    let step = 0;
    const timer = setInterval(() => {
      step++;
      setDisplay(Math.min(increment * step, value));
      if (step >= steps) {
        clearInterval(timer);
        setDisplay(value);
      }
    }, stepTime);
    return () => clearInterval(timer);
  }, [inView, value]);

  return <span ref={ref}>{formatter(display)}</span>;
}

export default function KpiCards({ locale }: KpiCardsProps) {
  const isFa = locale === \"fa\";

  const kpis: Array<{
    id: string; icon: LucideIcon; labelFa: string; labelEn: string;
    value: number; change: number; color: string;
  }> = [
    { id: \"revenue\", icon: DollarSign, labelFa: \"درآمد کل\", labelEn: \"Total Revenue\", value: analyticsOverview.totalRevenue, change: analyticsOverview.revenueChange, color: \"#22C55E\" },
    { id: \"orders\", icon: ShoppingCart, labelFa: \"سفارشات\", labelEn: \"Total Orders\", value: analyticsOverview.totalOrders, change: analyticsOverview.ordersChange, color: \"#EF4056\" },
    { id: \"users\", icon: Users, labelFa: \"کاربران\", labelEn: \"Total Users\", value: analyticsOverview.totalUsers, change: analyticsOverview.usersChange, color: \"#00BFFF\" },
    { id: \"products\", icon: Package, labelFa: \"محصولات\", labelEn: \"Products\", value: analyticsOverview.totalProducts, change: analyticsOverview.productsChange, color: \"#8B5CF6\" },
  ];

  return (
    <div className=\"grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4\">
      {kpis.map((kpi, i) => {
        const Icon = kpi.icon;
        const isUp = kpi.change >= 0;
        const hasChange = kpi.change !== 0;
        return (
          <motion.div
            key={kpi.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06, duration: 0.4 }}
            whileHover={{ y: -3 }}
            className=\"bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 relative overflow-hidden\"
          >
            <div className=\"flex items-center justify-between mb-3\">
              <div className=\"w-10 h-10 rounded-lg flex items-center justify-center\" style={{ backgroundColor: `${kpi.color}15` }}>
                <Icon size={18} style={{ color: kpi.color }} />
              </div>
              {hasChange && (
                <div className={`flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${isUp ? \"bg-[#22C55E]/10 text-[#22C55E]\" : \"bg-[#EF4444]/10 text-[#EF4444]\"}`}>
                  {isUp ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
                  {formatPercent(kpi.change, locale)}
                </div>
              )}
            </div>
            <div className=\"text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-1.5 tabular-nums\">
              {kpi.id === \"revenue\" ? (
                <>
                  <AnimatedNumber value={kpi.value} formatter={(v) => formatCompact(v, locale)} />
                  <span className=\"text-[11px] text-[#A1A3A8] font-normal mr-1\"> {isFa ? \"تومان\" : \"T\"}</span>
                </>
              ) : (
                <AnimatedNumber value={kpi.value} formatter={(v) => isFa ? Math.round(v).toLocaleString(\"fa-IR\") : Math.round(v).toLocaleString(\"en-US\")} />
              )}
            </div>
            <div className=\"text-[11px] text-[#A1A3A8]\">{isFa ? kpi.labelFa : kpi.labelEn}</div>
          </motion.div>
        );
      })}
    </div>
  );
}
"""))

files.append(("components/admin/dashboard/SalesChart.tsx", """\"use client\";

import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from \"recharts\";
import { TrendingUp } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { monthlySales } from \"@/lib/data\";
import { formatCompact, formatPrice } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";
import ChartTooltip from \"../charts/ChartTooltip\";

interface SalesChartProps { locale: Locale; }

export default function SalesChart({ locale }: SalesChartProps) {
  const isFa = locale === \"fa\";
  const data = monthlySales.map((item) => ({ ...item, label: isFa ? item.monthFa : item.month }));

  return (
    <ChartCard
      titleFa=\"نمودار فروش سالانه\"
      titleEn=\"Annual Sales\"
      subtitleFa=\"فروش ۱۲ ماه گذشته\"
      subtitleEn=\"Last 12 months\"
      icon={TrendingUp}
      delay={0.1}
    >
      <div className=\"h-[280px] -mx-2\">
        <ResponsiveContainer width=\"100%\" height=\"100%\">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id=\"salesGradient\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\">
                <stop offset=\"0%\" stopColor=\"#EF4056\" stopOpacity={0.3} />
                <stop offset=\"100%\" stopColor=\"#EF4056\" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#E0E0E2\" opacity={0.4} vertical={false} />
            <XAxis dataKey=\"label\" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} interval={0} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} tickFormatter={(v) => formatCompact(v, locale)} width={55} orientation={isFa ? \"right\" : \"left\"} />
            <Tooltip content={<ChartTooltip formatter={(v) => `${formatPrice(Number(v), locale)} ${isFa ? \"تومان\" : \"T\"}`} />} />
            <Area type=\"monotone\" dataKey=\"sales\" name={isFa ? \"فروش\" : \"Sales\"} stroke=\"#EF4056\" strokeWidth={2.5} fill=\"url(#salesGradient)\" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
"""))

files.append(("components/admin/dashboard/CategoryChart.tsx", """\"use client\";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from \"recharts\";
import { BarChart3 } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { categorySales } from \"@/lib/data\";
import { formatCompact, formatPrice } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";
import ChartTooltip from \"../charts/ChartTooltip\";

interface CategoryChartProps { locale: Locale; }

export default function CategoryChart({ locale }: CategoryChartProps) {
  const isFa = locale === \"fa\";
  const data = categorySales.slice(0, 8).map((item) => ({ ...item, label: isFa ? item.nameFa : item.nameEn }));

  return (
    <ChartCard
      titleFa=\"فروش بر اساس دسته‌بندی\"
      titleEn=\"Sales by Category\"
      subtitleFa=\"۸ دسته‌بندی برتر\"
      subtitleEn=\"Top 8 categories\"
      icon={BarChart3}
      delay={0.15}
    >
      <div className=\"h-[280px] -mx-2\">
        <ResponsiveContainer width=\"100%\" height=\"100%\">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#E0E0E2\" opacity={0.4} vertical={false} />
            <XAxis dataKey=\"label\" axisLine={false} tickLine={false} tick={{ fontSize: 9, fill: \"#A1A3A8\" }} interval={0} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} tickFormatter={(v) => formatCompact(v, locale)} width={55} orientation={isFa ? \"right\" : \"left\"} />
            <Tooltip content={<ChartTooltip formatter={(v) => `${formatPrice(Number(v), locale)}`} />} />
            <Bar dataKey=\"sales\" name={isFa ? \"فروش\" : \"Sales\"} radius={[6, 6, 0, 0]}>
              {data.map((entry, i) => (<Cell key={i} fill={entry.color} />))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
"""))

files.append(("components/admin/dashboard/VisitorsChart.tsx", """\"use client\";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from \"recharts\";
import { Users } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { dailyVisitors } from \"@/lib/data\";
import { formatCompact } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";
import ChartTooltip from \"../charts/ChartTooltip\";

interface VisitorsChartProps { locale: Locale; }

export default function VisitorsChart({ locale }: VisitorsChartProps) {
  const isFa = locale === \"fa\";
  const data = dailyVisitors.map((item) => {
    const d = new Date(item.date);
    return { ...item, label: d.toLocaleDateString(isFa ? \"fa-IR\" : \"en-US\", { month: \"short\", day: \"numeric\" }) };
  });

  return (
    <ChartCard
      titleFa=\"بازدیدکنندگان روزانه\"
      titleEn=\"Daily Visitors\"
      subtitleFa=\"۳۰ روز گذشته\"
      subtitleEn=\"Last 30 days\"
      icon={Users}
      delay={0.25}
    >
      <div className=\"h-[280px] -mx-2\">
        <ResponsiveContainer width=\"100%\" height=\"100%\">
          <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#E0E0E2\" opacity={0.4} vertical={false} />
            <XAxis dataKey=\"label\" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} interval={4} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} tickFormatter={(v) => formatCompact(v, locale)} width={45} orientation={isFa ? \"right\" : \"left\"} />
            <Tooltip content={<ChartTooltip />} />
            <Legend wrapperStyle={{ fontSize: \"11px\", paddingTop: \"10px\" }} iconType=\"circle\" iconSize={8} />
            <Line type=\"monotone\" dataKey=\"visitors\" name={isFa ? \"بازدیدکننده\" : \"Visitors\"} stroke=\"#00BFFF\" strokeWidth={2.5} dot={false} />
            <Line type=\"monotone\" dataKey=\"newUsers\" name={isFa ? \"کاربر جدید\" : \"New Users\"} stroke=\"#8B5CF6\" strokeWidth={2.5} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
"""))

files.append(("components/admin/dashboard/SharePieChart.tsx", """\"use client\";

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from \"recharts\";
import { PieChart as PieIcon } from \"lucide-react\";
import { motion } from \"framer-motion\";
import type { Locale } from \"@/lib/types\";
import { categorySales } from \"@/lib/data\";
import { formatPercent, formatCompact } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";
import ChartTooltip from \"../charts/ChartTooltip\";

interface SharePieChartProps { locale: Locale; }

export default function SharePieChart({ locale }: SharePieChartProps) {
  const isFa = locale === \"fa\";
  const top = categorySales.slice(0, 5);
  const others = categorySales.slice(5);
  const othersTotal = others.reduce((sum, c) => sum + c.sales, 0);

  const data = [
    ...top.map((c) => ({ name: isFa ? c.nameFa : c.nameEn, value: c.sales, color: c.color })),
    ...(othersTotal > 0 ? [{ name: isFa ? \"سایر\" : \"Others\", value: othersTotal, color: \"#94A3B8\" }] : []),
  ];

  const total = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <ChartCard
      titleFa=\"سهم دسته‌بندی‌ها\"
      titleEn=\"Category Share\"
      subtitleFa=\"سهم از کل فروش\"
      subtitleEn=\"Share of total sales\"
      icon={PieIcon}
      delay={0.2}
    >
      <div className=\"grid grid-cols-1 md:grid-cols-2 gap-4 items-center\">
        <div className=\"h-[220px] relative\">
          <ResponsiveContainer width=\"100%\" height=\"100%\">
            <PieChart>
              <Pie data={data} dataKey=\"value\" nameKey=\"name\" innerRadius={55} outerRadius={85} paddingAngle={2} stroke=\"none\">
                {data.map((entry, i) => (<Cell key={i} fill={entry.color} />))}
              </Pie>
              <Tooltip content={<ChartTooltip formatter={(v) => formatCompact(Number(v), locale)} />} />
            </PieChart>
          </ResponsiveContainer>
          <div className=\"absolute inset-0 flex items-center justify-center pointer-events-none\">
            <div className=\"text-center\">
              <div className=\"text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums leading-none\">{formatCompact(total, locale)}</div>
              <div className=\"text-[9px] text-[#A1A3A8] mt-1\">{isFa ? \"کل فروش\" : \"Total\"}</div>
            </div>
          </div>
        </div>
        <div className=\"space-y-2\">
          {data.map((item, i) => {
            const percent = (item.value / total) * 100;
            return (
              <motion.div key={i} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 + i * 0.05 }} className=\"flex items-center gap-2\">
                <span className=\"w-3 h-3 rounded-sm shrink-0\" style={{ backgroundColor: item.color }} />
                <span className=\"flex-1 text-[11px] text-[#62666D] dark:text-[#A1A3A8] truncate\">{item.name}</span>
                <span className=\"text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums\">{formatPercent(percent, locale)}</span>
              </motion.div>
            );
          })}
        </div>
      </div>
    </ChartCard>
  );
}
"""))

def main():
    print("=" * 60)
    print("Part 2: KPI + Charts")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")

if __name__ == "__main__":
    main()