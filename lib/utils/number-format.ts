// lib/utils/number-format.ts

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
  const num = locale === "fa" ? formatted.replace(/\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[+d]) : formatted;
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
