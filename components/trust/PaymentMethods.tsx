import type { Locale } from "@/lib/types";

interface PaymentMethodsProps {
  locale: Locale;
}

export default function PaymentMethods({ locale }: PaymentMethodsProps) {
  const isFa = locale === "fa";

  const methods = [
    { nameFa: "زرین‌پال", nameEn: "Zarinpal", color: "#F9A825", short: "Z" },
    { nameFa: "آی‌دی پی", nameEn: "IDPay", color: "#22C55E", short: "ID" },
    { nameFa: "پی‌پینگ", nameEn: "PayPing", color: "#00BFFF", short: "PP" },
    { nameFa: "نکست‌پی", nameEn: "NextPay", color: "#8B5CF6", short: "NP" },
    { nameFa: "شاپرک", nameEn: "Shaparak", color: "#EF4056", short: "SH" },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
        {isFa ? "درگاه‌های پرداخت معتبر" : "Trusted Payment Gateways"}
      </h3>

      <div className="flex items-center gap-2 flex-wrap">
        {methods.map((method, i) => (
          <div
            key={i}
            className="flex items-center gap-2 px-3 py-2 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-sm transition-shadow cursor-pointer"
          >
            <div
              className="w-6 h-6 rounded flex items-center justify-center text-white text-[10px] font-bold shrink-0"
              style={{ backgroundColor: method.color }}
            >
              {method.short}
            </div>
            <span className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] font-medium">
              {isFa ? method.nameFa : method.nameEn}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
