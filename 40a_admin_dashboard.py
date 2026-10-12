# 40a_admin_dashboard.py
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

files.append(("lib/utils/number-format.ts", """// lib/utils/number-format.ts

export function formatCompact(value: number, locale: "fa" | "en" = "fa"): string {
  if (locale === "fa") {
    if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(1)} میلیارد`;
    if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)} میلیون`;
    if (value >= 1_000) return `${(value / 1_000).toFixed(0)} هزار`;
    return value.toLocaleString("fa-IR");
  }
  if (value >= 1_000_000_000) return `${(value / 1_000_000_000).toFixed(1)}B`;
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(0)}K`;
  return value.toLocaleString("en-US");
}

export function formatPercent(value: number, locale: "fa" | "en" = "fa"): string {
  const formatted = Math.abs(value).toFixed(1);
  const num = locale === "fa" ? formatted.replace(/\\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[+d]) : formatted;
  const sign = value >= 0 ? "+" : "−";
  return `${sign}${num}٪`;
}

export function formatRelativeTime(timestamp: number, locale: "fa" | "en" = "fa"): string {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);
  if (seconds < 60) return locale === "fa" ? "لحظه‌ای پیش" : "just now";
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return locale === "fa" ? `${minutes} دقیقه پیش` : `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return locale === "fa" ? `${hours} ساعت پیش` : `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days < 30) return locale === "fa" ? `${days} روز پیش` : `${days}d ago`;
  const months = Math.floor(days / 30);
  return locale === "fa" ? `${months} ماه پیش` : `${months}mo ago`;
}
"""))

files.append(("components/admin/charts/ChartCard.tsx", """\"use client\";

import { motion } from \"framer-motion\";
import { type LucideIcon } from \"lucide-react\";

interface ChartCardProps {
  titleFa: string;
  titleEn: string;
  subtitleFa?: string;
  subtitleEn?: string;
  icon?: LucideIcon;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  delay?: number;
}

export default function ChartCard({
  titleFa,
  titleEn,
  subtitleFa,
  subtitleEn,
  icon: Icon,
  action,
  children,
  className,
  delay = 0,
}: ChartCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay, ease: [0.16, 1, 0.3, 1] }}
      className={`bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden ${className ?? \"\"}`}
    >
      <div className=\"flex items-start justify-between gap-3 p-4 md:p-5 border-b border-[#F5F5F5] dark:border-[#2A2A2E]\">
        <div className=\"flex items-start gap-3 min-w-0\">
          {Icon && (
            <div className=\"w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center shrink-0\">
              <Icon size={16} className=\"text-[#EF4056]\" />
            </div>
          )}
          <div className=\"min-w-0\">
            <h3 className=\"text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] truncate\">
              {titleFa}
            </h3>
            {(subtitleFa || subtitleEn) && (
              <p className=\"text-[11px] text-[#A1A3A8] mt-0.5 truncate\">
                {subtitleFa}
              </p>
            )}
          </div>
        </div>
        {action}
      </div>
      <div className=\"p-4 md:p-5\">{children}</div>
    </motion.div>
  );
}
"""))

files.append(("components/admin/charts/ChartTooltip.tsx", """\"use client\";

interface ChartTooltipProps {
  active?: boolean;
  payload?: Array<{
    name?: string;
    value?: number | string;
    color?: string;
  }>;
  label?: string | number;
  formatter?: (value: number | string) => string;
  labelFormatter?: (label: string | number) => string;
}

export default function ChartTooltip({
  active,
  payload,
  label,
  formatter,
  labelFormatter,
}: ChartTooltipProps) {
  if (!active || !payload || payload.length === 0) return null;

  return (
    <div className=\"bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-xl px-3 py-2 text-[12px] min-w-[140px]\">
      {label !== undefined && (
        <div className=\"font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1.5 pb-1.5 border-b border-[#F5F5F5] dark:border-[#2A2A2E]\">
          {labelFormatter ? labelFormatter(label) : label}
        </div>
      )}
      <div className=\"space-y-1\">
        {payload.map((entry, i) => (
          <div key={i} className=\"flex items-center justify-between gap-3\">
            <div className=\"flex items-center gap-1.5\">
              <span
                className=\"w-2 h-2 rounded-full shrink-0\"
                style={{ backgroundColor: entry.color }}
              />
              <span className=\"text-[#62666D] dark:text-[#A1A3A8]\">
                {entry.name}
              </span>
            </div>
            <span className=\"font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums\">
              {formatter
                ? formatter(entry.value ?? 0)
                : typeof entry.value === \"number\"
                ? entry.value.toLocaleString()
                : entry.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
"""))

files.append(("components/admin/charts/index.ts", """// components/admin/charts/index.ts
export { default as ChartCard } from \"./ChartCard\";
export { default as ChartTooltip } from \"./ChartTooltip\";
"""))

def main():
    print("=" * 60)
    print("Part 1: Utilities + Chart Components")
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