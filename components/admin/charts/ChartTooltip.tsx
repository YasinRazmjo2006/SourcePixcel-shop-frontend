"use client";

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
    <div className="bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-xl px-3 py-2 text-[12px] min-w-[140px]">
      {label !== undefined && (
        <div className="font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1.5 pb-1.5 border-b border-[#F5F5F5] dark:border-[#2A2A2E]">
          {labelFormatter ? labelFormatter(label) : label}
        </div>
      )}
      <div className="space-y-1">
        {payload.map((entry, i) => (
          <div key={i} className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-1.5">
              <span
                className="w-2 h-2 rounded-full shrink-0"
                style={{ backgroundColor: entry.color }}
              />
              <span className="text-[#62666D] dark:text-[#A1A3A8]">
                {entry.name}
              </span>
            </div>
            <span className="font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
              {formatter
                ? formatter(entry.value ?? 0)
                : typeof entry.value === "number"
                ? entry.value.toLocaleString()
                : entry.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
