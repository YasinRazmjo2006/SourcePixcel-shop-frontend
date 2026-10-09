interface SalesChartProps {
  locale: string;
}

const DATA = [40, 65, 45, 80, 55, 90, 75, 95, 60, 85, 70, 100];
const MONTHS_FA = ["فرو", "ارد", "خرد", "تیر", "مرد", "شهر", "مهر", "آبا", "آذر", "دی", "بهم", "اسف"];
const MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export default function SalesChart({ locale }: SalesChartProps) {
  const isFa = locale === "fa";
  const months = isFa ? MONTHS_FA : MONTHS_EN;

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {isFa ? "نمودار فروش سالانه" : "Annual Sales Chart"}
          </h3>
          <p className="text-[11px] text-[#A1A3A8] mt-1">
            {isFa ? "فروش ماهانه در سال ۱۴۰۳" : "Monthly sales in 2025"}
          </p>
        </div>
        <div className="flex items-center gap-3 text-[10px]">
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#EF4056]" />
            <span className="text-[#62666D] dark:text-[#A1A3A8]">
              {isFa ? "فروش" : "Sales"}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-end justify-between gap-1 md:gap-2 h-40">
        {DATA.map((value, i) => (
          <div key={i} className="flex-1 flex flex-col items-center gap-2 group">
            <div className="relative w-full flex justify-center">
              <div
                className="w-full max-w-[32px] rounded-t-md transition-all duration-500 group-hover:opacity-90 relative"
                style={{
                  height: `${value * 1.4}px`,
                  background: `linear-gradient(180deg, #EF4056 0%, #d63850 100%)`,
                }}
              >
                <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-[#3F4064] text-white text-[9px] px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                  {value}M
                </div>
              </div>
            </div>
            <span className="text-[9px] text-[#A1A3A8]">{months[i]}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
