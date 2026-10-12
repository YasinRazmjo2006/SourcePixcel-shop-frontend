# 41_admin_analytics.py
# Step 4: Analytics Page with advanced charts
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# components/admin/analytics/DateRangePicker.tsx
# ============================================================
files.append(("components/admin/analytics/DateRangePicker.tsx", """\"use client\";

import { useState, useRef, useEffect } from \"react\";
import { motion, AnimatePresence } from \"framer-motion\";
import { Calendar, ChevronDown, Check } from \"lucide-react\";
import type { Locale, DateRangePreset } from \"@/lib/types\";

interface DateRangePickerProps {
  locale: Locale;
  value: DateRangePreset;
  onChange: (preset: DateRangePreset) => void;
}

const PRESETS: Array<{ value: DateRangePreset; fa: string; en: string }> = [
  { value: \"today\", fa: \"امروز\", en: \"Today\" },
  { value: \"yesterday\", fa: \"دیروز\", en: \"Yesterday\" },
  { value: \"last7days\", fa: \"۷ روز گذشته\", en: \"Last 7 Days\" },
  { value: \"last30days\", fa: \"۳۰ روز گذشته\", en: \"Last 30 Days\" },
  { value: \"last90days\", fa: \"۹۰ روز گذشته\", en: \"Last 90 Days\" },
  { value: \"thisMonth\", fa: \"این ماه\", en: \"This Month\" },
  { value: \"lastMonth\", fa: \"ماه گذشته\", en: \"Last Month\" },
  { value: \"thisYear\", fa: \"امسال\", en: \"This Year\" },
];

export default function DateRangePicker({
  locale,
  value,
  onChange,
}: DateRangePickerProps) {
  const isFa = locale === \"fa\";
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener(\"mousedown\", handler);
    return () => document.removeEventListener(\"mousedown\", handler);
  }, []);

  const current = PRESETS.find((p) => p.value === value);

  return (
    <div ref={ref} className=\"relative\">
      <button
        onClick={() => setOpen((v) => !v)}
        className=\"flex items-center gap-2 h-10 px-4 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] transition-colors\"
      >
        <Calendar size={14} className=\"text-[#A1A3A8]\" />
        <span className=\"font-medium\">
          {isFa ? current?.fa : current?.en}
        </span>
        <motion.div animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronDown size={14} className=\"text-[#A1A3A8]\" />
        </motion.div>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.96 }}
            transition={{ duration: 0.15 }}
            className={`absolute top-full mt-2 w-56 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl shadow-2xl overflow-hidden z-50 ${
              isFa ? \"right-0\" : \"left-0\"
            }`}
          >
            <div className=\"p-1.5\">
              {PRESETS.map((preset) => (
                <button
                  key={preset.value}
                  onClick={() => {
                    onChange(preset.value);
                    setOpen(false);
                  }}
                  className={`w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg text-[12px] transition-colors ${
                    value === preset.value
                      ? \"bg-[#EF4056]/5 text-[#EF4056] font-medium\"
                      : \"text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]\"
                  }`}
                >
                  <span>{isFa ? preset.fa : preset.en}</span>
                  {value === preset.value && (
                    <Check size={14} className=\"text-[#EF4056]\" />
                  )}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
"""))

# ============================================================
# components/admin/analytics/AnalyticsStats.tsx
# ============================================================
files.append(("components/admin/analytics/AnalyticsStats.tsx", """\"use client\";

import { motion } from \"framer-motion\";
import { TrendingUp, TrendingDown, Clock, MousePointerClick, Users, ShoppingBag } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { formatCompact, formatPercent } from \"@/lib/utils\";

interface AnalyticsStatsProps {
  locale: Locale;
}

interface Stat {
  id: string;
  icon: typeof Clock;
  labelFa: string;
  labelEn: string;
  value: number;
  formatted: string;
  change: number;
  color: string;
}

export default function AnalyticsStats({ locale }: AnalyticsStatsProps) {
  const isFa = locale === \"fa\";

  const stats: Stat[] = [
    {
      id: \"session\",
      icon: Clock,
      labelFa: \"میانگین زمان سشن\",
      labelEn: \"Avg Session Duration\",
      value: 285,
      formatted: isFa ? \"۴ دقیقه ۴۵ ثانیه\" : \"4m 45s\",
      change: 8.5,
      color: \"#8B5CF6\",
    },
    {
      id: \"rate\",
      icon: MousePointerClick,
      labelFa: \"نرخ پرش\",
      labelEn: \"Bounce Rate\",
      value: 32.4,
      formatted: isFa ? \"۳۲.۴٪\" : \"32.4%\",
      change: -5.2,
      color: \"#F59E0B\",
    },
    {
      id: \"conversion\",
      icon: ShoppingBag,
      labelFa: \"نرخ تبدیل\",
      labelEn: \"Conversion Rate\",
      value: 3.42,
      formatted: isFa ? \"۳.۴۲٪\" : \"3.42%\",
      change: 12.3,
      color: \"#22C55E\",
    },
    {
      id: \"newusers\",
      icon: Users,
      labelFa: \"کاربران جدید\",
      labelEn: \"New Users\",
      value: 342,
      formatted: isFa ? \"۳۴۲\" : \"342\",
      change: 15.8,
      color: \"#00BFFF\",
    },
  ];

  return (
    <div className=\"grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4\">
      {stats.map((stat, i) => {
        const Icon = stat.icon;
        const isUp = stat.change >= 0;
        return (
          <motion.div
            key={stat.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.06, duration: 0.4 }}
            className=\"bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4\"
          >
            <div className=\"flex items-center justify-between mb-3\">
              <div
                className=\"w-10 h-10 rounded-lg flex items-center justify-center\"
                style={{ backgroundColor: `${stat.color}15` }}
              >
                <Icon size={18} style={{ color: stat.color }} />
              </div>
              <div
                className={`flex items-center gap-0.5 text-[10px] font-bold px-1.5 py-0.5 rounded-full ${
                  isUp
                    ? \"bg-[#22C55E]/10 text-[#22C55E]\"
                    : \"bg-[#EF4444]/10 text-[#EF4444]\"
                }`}
              >
                {isUp ? <TrendingUp size={11} /> : <TrendingDown size={11} />}
                {formatPercent(stat.change, locale)}
              </div>
            </div>
            <div className=\"text-[18px] md:text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-1.5\">
              {stat.formatted}
            </div>
            <div className=\"text-[11px] text-[#A1A3A8]\">
              {isFa ? stat.labelFa : stat.labelEn}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
"""))

# ============================================================
# components/admin/analytics/MultiLineChart.tsx
# ============================================================
files.append(("components/admin/analytics/MultiLineChart.tsx", """\"use client\";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from \"recharts\";
import { Activity } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { monthlySales } from \"@/lib/data\";
import { formatCompact } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";
import ChartTooltip from \"../charts/ChartTooltip\";

interface MultiLineChartProps {
  locale: Locale;
}

export default function MultiLineChart({ locale }: MultiLineChartProps) {
  const isFa = locale === \"fa\";
  const data = monthlySales.map((item) => ({
    ...item,
    label: isFa ? item.monthFa : item.month,
    conversion: Number(((item.orders / item.visitors) * 100).toFixed(2)),
  }));

  return (
    <ChartCard
      titleFa=\"مقایسه شاخص‌ها\"
      titleEn=\"Metrics Comparison\"
      subtitleFa=\"سفارشات، بازدیدکنندگان و نرخ تبدیل\"
      subtitleEn=\"Orders, visitors and conversion rate\"
      icon={Activity}
      delay={0.1}
    >
      <div className=\"h-[320px] -mx-2\">
        <ResponsiveContainer width=\"100%\" height=\"100%\">
          <LineChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#E0E0E2\" opacity={0.4} vertical={false} />
            <XAxis dataKey=\"label\" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} />
            <YAxis yAxisId=\"left\" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} tickFormatter={(v) => formatCompact(v, locale)} width={50} orientation={isFa ? \"right\" : \"left\"} />
            <YAxis yAxisId=\"right\" orientation={isFa ? \"left\" : \"right\"} axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} tickFormatter={(v) => `${v}%`} width={40} />
            <Tooltip content={<ChartTooltip />} />
            <Legend wrapperStyle={{ fontSize: \"11px\", paddingTop: \"10px\" }} iconType=\"circle\" iconSize={8} />
            <Line yAxisId=\"left\" type=\"monotone\" dataKey=\"orders\" name={isFa ? \"سفارشات\" : \"Orders\"} stroke=\"#EF4056\" strokeWidth={2.5} dot={{ r: 3 }} />
            <Line yAxisId=\"left\" type=\"monotone\" dataKey=\"visitors\" name={isFa ? \"بازدیدکننده\" : \"Visitors\"} stroke=\"#00BFFF\" strokeWidth={2.5} dot={{ r: 3 }} />
            <Line yAxisId=\"right\" type=\"monotone\" dataKey=\"conversion\" name={isFa ? \"نرخ تبدیل\" : \"Conversion\"} stroke=\"#22C55E\" strokeWidth={2.5} strokeDasharray=\"5 5\" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
"""))

# ============================================================
# components/admin/analytics/StackedBarChart.tsx
# ============================================================
files.append(("components/admin/analytics/StackedBarChart.tsx", """\"use client\";

import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from \"recharts\";
import { Layers } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { monthlySales } from \"@/lib/data\";
import { formatCompact } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";
import ChartTooltip from \"../charts/ChartTooltip\";

interface StackedBarChartProps {
  locale: Locale;
}

export default function StackedBarChart({ locale }: StackedBarChartProps) {
  const isFa = locale === \"fa\";
  const data = monthlySales.map((item) => ({
    label: isFa ? item.monthFa : item.month,
    desktop: Math.round(item.visitors * 0.5),
    mobile: Math.round(item.visitors * 0.38),
    tablet: Math.round(item.visitors * 0.12),
  }));

  return (
    <ChartCard
      titleFa=\"بازدید بر اساس دستگاه\"
      titleEn=\"Visitors by Device\"
      subtitleFa=\"توزیع دسکتاپ، موبایل و تبلت\"
      subtitleEn=\"Desktop, mobile and tablet distribution\"
      icon={Layers}
      delay={0.15}
    >
      <div className=\"h-[320px] -mx-2\">
        <ResponsiveContainer width=\"100%\" height=\"100%\">
          <BarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray=\"3 3\" stroke=\"#E0E0E2\" opacity={0.4} vertical={false} />
            <XAxis dataKey=\"label\" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: \"#A1A3A8\" }} tickFormatter={(v) => formatCompact(v, locale)} width={50} orientation={isFa ? \"right\" : \"left\"} />
            <Tooltip content={<ChartTooltip />} cursor={{ fill: \"#EF4056\", opacity: 0.05 }} />
            <Legend wrapperStyle={{ fontSize: \"11px\", paddingTop: \"10px\" }} iconType=\"circle\" iconSize={8} />
            <Bar dataKey=\"desktop\" name={isFa ? \"دسکتاپ\" : \"Desktop\"} stackId=\"a\" fill=\"#EF4056\" radius={[0, 0, 0, 0]} />
            <Bar dataKey=\"mobile\" name={isFa ? \"موبایل\" : \"Mobile\"} stackId=\"a\" fill=\"#00BFFF\" />
            <Bar dataKey=\"tablet\" name={isFa ? \"تبلت\" : \"Tablet\"} stackId=\"a\" fill=\"#8B5CF6\" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </ChartCard>
  );
}
"""))

# ============================================================
# components/admin/analytics/ActivityHeatmap.tsx
# ============================================================
files.append(("components/admin/analytics/ActivityHeatmap.tsx", """\"use client\";

import { motion } from \"framer-motion\";
import { Grid3x3 } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { hourlyActivity } from \"@/lib/data\";
import ChartCard from \"../charts/ChartCard\";

interface ActivityHeatmapProps {
  locale: Locale;
}

const DAYS_FA = [\"شنبه\", \"یک\", \"دو\", \"سه\", \"چهار\", \"جمعه\", \"پنج\"];
const DAYS_EN = [\"Sat\", \"Sun\", \"Mon\", \"Tue\", \"Wed\", \"Fri\", \"Thu\"];

export default function ActivityHeatmap({ locale }: ActivityHeatmapProps) {
  const isFa = locale === \"fa\";
  const days = isFa ? DAYS_FA : DAYS_EN;

  // Generate 7x24 grid from hourlyActivity
  const grid = days.map((_, dayIdx) =>
    hourlyActivity.map((h) => ({
      hour: h.hour,
      value: h.activity * (0.7 + (dayIdx / 10)),
    }))
  );

  const maxValue = Math.max(...grid.flat().map((c) => c.value));

  const getColor = (value: number) => {
    const intensity = value / maxValue;
    if (intensity < 0.15) return \"#F5F5F5\";
    if (intensity < 0.3) return \"#FFD4DB\";
    if (intensity < 0.5) return \"#FFA7B5\";
    if (intensity < 0.7) return \"#FF7188\";
    if (intensity < 0.85) return \"#EF4056\";
    return \"#C62F44\";
  };

  return (
    <ChartCard
      titleFa=\"نقشه حرارتی فعالیت\"
      titleEn=\"Activity Heatmap\"
      subtitleFa=\"فعالیت ساعتی در طول هفته\"
      subtitleEn=\"Hourly activity throughout the week\"
      icon={Grid3x3}
      delay={0.2}
    >
      <div className=\"overflow-x-auto -mx-2 px-2\">
        <div className=\"min-w-[600px]\">
          {/* Hour labels */}
          <div className=\"flex items-center gap-1 mb-2 mr-12\">
            {Array.from({ length: 24 }, (_, h) => (
              <div
                key={h}
                className=\"flex-1 text-center text-[9px] text-[#A1A3A8]\"
              >
                {h % 3 === 0 ? (isFa ? h.toLocaleString(\"fa-IR\") : h) : \"\"}
              </div>
            ))}
          </div>

          {/* Grid */}
          <div className=\"space-y-1\">
            {grid.map((row, dayIdx) => (
              <div key={dayIdx} className=\"flex items-center gap-1\">
                <div className=\"w-10 text-[10px] text-[#A1A3A8] shrink-0\">
                  {days[dayIdx]}
                </div>
                <div className=\"flex-1 flex gap-1\">
                  {row.map((cell, h) => (
                    <motion.div
                      key={h}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: dayIdx * 0.02 + h * 0.002 }}
                      className=\"flex-1 aspect-square rounded-sm hover:scale-125 transition-transform cursor-pointer\"
                      style={{ backgroundColor: getColor(cell.value) }}
                      title={`${days[dayIdx]} ${h}:00 — ${Math.round(cell.value)}`}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Legend */}
          <div className=\"flex items-center justify-end gap-2 mt-4\">
            <span className=\"text-[10px] text-[#A1A3A8]\">
              {isFa ? \"کم\" : \"Less\"}
            </span>
            {[\"#F5F5F5\", \"#FFD4DB\", \"#FFA7B5\", \"#FF7188\", \"#EF4056\", \"#C62F44\"].map(
              (color, i) => (
                <div
                  key={i}
                  className=\"w-3 h-3 rounded-sm\"
                  style={{ backgroundColor: color }}
                />
              )
            )}
            <span className=\"text-[10px] text-[#A1A3A8]\">
              {isFa ? \"زیاد\" : \"More\"}
            </span>
          </div>
        </div>
      </div>
    </ChartCard>
  );
}
"""))

# ============================================================
# components/admin/analytics/FunnelChart.tsx
# ============================================================
files.append(("components/admin/analytics/FunnelChart.tsx", """\"use client\";

import { motion } from \"framer-motion\";
import { Filter } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { salesFunnel } from \"@/lib/data\";
import ChartCard from \"../charts/ChartCard\";

interface FunnelChartProps {
  locale: Locale;
}

const COLORS = [\"#EF4056\", \"#FF7188\", \"#F59E0B\", \"#00BFFF\", \"#22C55E\"];

export default function FunnelChart({ locale }: FunnelChartProps) {
  const isFa = locale === \"fa\";

  return (
    <ChartCard
      titleFa=\"قیف فروش\"
      titleEn=\"Sales Funnel\"
      subtitleFa=\"مسیر کاربر از بازدید تا خرید\"
      subtitleEn=\"User journey from visit to purchase\"
      icon={Filter}
      delay={0.25}
    >
      <div className=\"space-y-2\">
        {salesFunnel.map((step, i) => {
          const widthPercent = step.percentage;
          const dropped = i > 0 ? salesFunnel[i - 1].percentage - step.percentage : 0;

          return (
            <motion.div
              key={step.step}
              initial={{ opacity: 0, x: isFa ? 30 : -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.1, duration: 0.4 }}
              className=\"relative\"
            >
              <div className=\"flex items-center gap-3\">
                <div className=\"w-24 md:w-32 shrink-0 text-end\">
                  <div className=\"text-[11px] font-medium text-[#3F4064] dark:text-[#E5E5EA]\">
                    {isFa ? step.stepFa : step.step}
                  </div>
                  <div className=\"text-[10px] text-[#A1A3A8]\">
                    {step.value.toLocaleString(isFa ? \"fa-IR\" : \"en-US\")}
                  </div>
                </div>

                <div className=\"flex-1 relative\">
                  <div className=\"h-10 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg overflow-hidden\">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${widthPercent}%` }}
                      transition={{ delay: 0.3 + i * 0.1, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
                      className=\"h-full rounded-lg relative flex items-center justify-end px-3\"
                      style={{
                        background: `linear-gradient(90deg, ${COLORS[i]}, ${COLORS[i]}dd)`,
                        minWidth: \"50px\",
                      }}
                    >
                      <span className=\"text-[11px] font-bold text-white tabular-nums\">
                        {step.percentage.toFixed(1)}%
                      </span>
                    </motion.div>
                  </div>

                  {dropped > 0 && (
                    <div className=\"absolute -bottom-2 right-2 text-[9px] text-[#EF4444] font-medium bg-white dark:bg-[#1A1A1E] px-1 rounded\">
                      −{dropped.toFixed(1)}%
                    </div>
                  )}
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>
    </ChartCard>
  );
}
"""))

# ============================================================
# components/admin/analytics/RadialProgress.tsx
# ============================================================
files.append(("components/admin/analytics/RadialProgress.tsx", """\"use client\";

import { motion } from \"framer-motion\";
import type { Locale } from \"@/lib/types\";

interface RadialProgressProps {
  value: number;
  max?: number;
  size?: number;
  thickness?: number;
  color?: string;
  label: string;
  sublabel?: string;
  delay?: number;
}

export default function RadialProgress({
  value,
  max = 100,
  size = 100,
  thickness = 8,
  color = \"#EF4056\",
  label,
  sublabel,
  delay = 0,
}: RadialProgressProps) {
  const radius = (size - thickness) / 2;
  const circumference = 2 * Math.PI * radius;
  const percentage = Math.min(100, (value / max) * 100);
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className=\"flex flex-col items-center gap-2\">
      <div className=\"relative\" style={{ width: size, height: size }}>
        <svg width={size} height={size} className=\"-rotate-90\">
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke=\"#F5F5F5\"
            strokeWidth={thickness}
            fill=\"none\"
            className=\"dark:stroke-[#2A2A2E]\"
          />
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke={color}
            strokeWidth={thickness}
            fill=\"none\"
            strokeLinecap=\"round\"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ delay, duration: 1, ease: [0.16, 1, 0.3, 1] }}
          />
        </svg>
        <div className=\"absolute inset-0 flex flex-col items-center justify-center\">
          <div className=\"text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums\">
            {Math.round(percentage)}%
          </div>
        </div>
      </div>
      <div className=\"text-center\">
        <div className=\"text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]\">
          {label}
        </div>
        {sublabel && (
          <div className=\"text-[10px] text-[#A1A3A8] mt-0.5\">{sublabel}</div>
        )}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/admin/analytics/GoalsCard.tsx
# ============================================================
files.append(("components/admin/analytics/GoalsCard.tsx", """\"use client\";

import { Target } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import ChartCard from \"../charts/ChartCard\";
import RadialProgress from \"./RadialProgress\";

interface GoalsCardProps {
  locale: Locale;
}

export default function GoalsCard({ locale }: GoalsCardProps) {
  const isFa = locale === \"fa\";

  const goals = [
    {
      id: \"revenue\",
      value: 82,
      color: \"#22C55E\",
      label: isFa ? \"درآمد\" : \"Revenue\",
      sublabel: isFa ? \"۸۲٪ از هدف\" : \"82% of goal\",
    },
    {
      id: \"orders\",
      value: 67,
      color: \"#EF4056\",
      label: isFa ? \"سفارشات\" : \"Orders\",
      sublabel: isFa ? \"۶۷٪ از هدف\" : \"67% of goal\",
    },
    {
      id: \"users\",
      value: 91,
      color: \"#00BFFF\",
      label: isFa ? \"کاربران\" : \"Users\",
      sublabel: isFa ? \"۹۱٪ از هدف\" : \"91% of goal\",
    },
    {
      id: \"conversion\",
      value: 54,
      color: \"#8B5CF6\",
      label: isFa ? \"تبدیل\" : \"Conversion\",
      sublabel: isFa ? \"۵۴٪ از هدف\" : \"54% of goal\",
    },
  ];

  return (
    <ChartCard
      titleFa=\"اهداف ماهانه\"
      titleEn=\"Monthly Goals\"
      subtitleFa=\"پیشرفت اهداف تعیین‌شده\"
      subtitleEn=\"Progress toward set goals\"
      icon={Target}
      delay={0.3}
    >
      <div className=\"grid grid-cols-2 md:grid-cols-4 gap-4\">
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
"""))

# ============================================================
# components/admin/analytics/index.ts
# ============================================================
files.append(("components/admin/analytics/index.ts", """// components/admin/analytics/index.ts
export { default as DateRangePicker } from \"./DateRangePicker\";
export { default as AnalyticsStats } from \"./AnalyticsStats\";
export { default as MultiLineChart } from \"./MultiLineChart\";
export { default as StackedBarChart } from \"./StackedBarChart\";
export { default as ActivityHeatmap } from \"./ActivityHeatmap\";
export { default as FunnelChart } from \"./FunnelChart\";
export { default as RadialProgress } from \"./RadialProgress\";
export { default as GoalsCard } from \"./GoalsCard\";
"""))

# ============================================================
# components/admin/AnalyticsView.tsx
# ============================================================
files.append(("components/admin/AnalyticsView.tsx", """\"use client\";

import { useState } from \"react\";
import { Download, RefreshCw } from \"lucide-react\";
import type { Locale, DateRangePreset } from \"@/lib/types\";
import {
  DateRangePicker,
  AnalyticsStats,
  MultiLineChart,
  StackedBarChart,
  ActivityHeatmap,
  FunnelChart,
  GoalsCard,
} from \"./analytics\";

interface AnalyticsViewProps {
  locale: Locale;
}

export default function AnalyticsView({ locale }: AnalyticsViewProps) {
  const isFa = locale === \"fa\";
  const [preset, setPreset] = useState<DateRangePreset>(\"last30days\");

  return (
    <div className=\"space-y-4 md:space-y-5\">
      {/* Header */}
      <div className=\"flex items-start justify-between gap-3 flex-wrap\">
        <div>
          <h1 className=\"text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1\">
            {isFa ? \"آنالیتیکس\" : \"Analytics\"}
          </h1>
          <p className=\"text-[12px] text-[#62666D] dark:text-[#A1A3A8]\">
            {isFa
              ? \"تحلیل دقیق عملکرد فروشگاه\"
              : \"In-depth analysis of store performance\"}
          </p>
        </div>

        <div className=\"flex items-center gap-2\">
          <DateRangePicker locale={locale} value={preset} onChange={setPreset} />
          <button className=\"h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-1.5 text-[12px]\">
            <RefreshCw size={14} />
            <span className=\"hidden md:inline\">{isFa ? \"به‌روزرسانی\" : \"Refresh\"}</span>
          </button>
          <button className=\"h-10 px-3 rounded-lg bg-[#EF4056] text-white hover:bg-[#d63850] transition-colors flex items-center gap-1.5 text-[12px] font-medium\">
            <Download size={14} />
            <span className=\"hidden md:inline\">{isFa ? \"دانلود\" : \"Export\"}</span>
          </button>
        </div>
      </div>

      {/* Stats */}
      <AnalyticsStats locale={locale} />

      {/* Multi Line + Stacked */}
      <div className=\"grid grid-cols-1 lg:grid-cols-2 gap-4\">
        <MultiLineChart locale={locale} />
        <StackedBarChart locale={locale} />
      </div>

      {/* Heatmap */}
      <ActivityHeatmap locale={locale} />

      {/* Funnel + Goals */}
      <div className=\"grid grid-cols-1 lg:grid-cols-2 gap-4\">
        <FunnelChart locale={locale} />
        <GoalsCard locale={locale} />
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/admin/analytics/page.tsx
# ============================================================
files.append(("app/[locale]/admin/analytics/page.tsx", """import AnalyticsView from \"@/components/admin/AnalyticsView\";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminAnalyticsPage({ params }: PageProps) {
  const { locale } = await params;
  return <AnalyticsView locale={locale as \"fa\" | \"en\"} />;
}
"""))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", """// components/admin/index.ts
export { default as AdminGuard } from \"./AdminGuard\";
export { default as DashboardView } from \"./DashboardView\";
export { default as AnalyticsView } from \"./AnalyticsView\";
export { default as ProductsView } from \"./ProductsView\";
export { default as OrdersView } from \"./OrdersView\";
export { default as AdminLoginForm } from \"./AdminLoginForm\";

// Layout
export * from \"./layout\";

// Dashboard
export * from \"./dashboard\";

// Analytics
export * from \"./analytics\";

// Charts
export * from \"./charts\";
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 4: Analytics Page")
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
    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/analytics")

if __name__ == "__main__":
    main()