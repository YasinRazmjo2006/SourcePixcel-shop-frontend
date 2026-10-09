"use client";

import { useState } from "react";
import { CreditCard, ShieldCheck, Loader2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

interface PaymentStepProps {
  locale: Locale;
  total: number;
  onBack: () => void;
  onPay: () => void;
}

export default function PaymentStep({
  locale,
  total,
  onBack,
  onPay,
}: PaymentStepProps) {
  const isFa = locale === "fa";
  const [processing, setProcessing] = useState(false);

  const handlePay = () => {
    setProcessing(true);
    setTimeout(() => {
      onPay();
    }, 1500);
  };

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-5">
        {isFa ? "پرداخت" : "Payment"}
      </h2>

      {/* Simulated gateway */}
      <div className="border-2 border-dashed border-[#E0E0E2] rounded-lg p-6 mb-5 bg-[#FAFAFA]">
        <div className="flex flex-col items-center text-center">
          <div className="w-14 h-14 rounded-full bg-[#EF4056]/10 flex items-center justify-center mb-3">
            <CreditCard size={28} className="text-[#EF4056]" />
          </div>
          <h3 className="text-[14px] font-bold text-[#3F4064] mb-1">
            {isFa ? "درگاه پرداخت زرین‌پال" : "Zarinpal Payment Gateway"}
          </h3>
          <p className="text-[12px] text-[#A1A3A8] mb-4">
            {isFa
              ? "این یک محیط آزمایشی است. پرداخت واقعی انجام نمی‌شود."
              : "This is a test environment. No real payment will be made."}
          </p>

          <div className="bg-white rounded-lg border border-[#E0E0E2] w-full max-w-sm p-4">
            <div className="text-[12px] text-[#62666D] mb-1">
              {isFa ? "مبلغ قابل پرداخت" : "Amount to pay"}
            </div>
            <div className="flex items-center justify-center gap-1">
              <span className="text-[24px] font-bold text-[#EF4056]">
                {formatPrice(total, locale)}
              </span>
              <span className="text-[12px] text-[#62666D]">
                {isFa ? "تومان" : "Toman"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Trust */}
      <div className="flex items-center justify-center gap-2 text-[11px] text-[#62666D] mb-5">
        <ShieldCheck size={14} className="text-[#22C55E]" />
        {isFa
          ? "پرداخت امن با رمزنگاری SSL"
          : "Secure payment with SSL encryption"}
      </div>

      <div className="flex justify-between">
        <button
          type="button"
          onClick={onBack}
          disabled={processing}
          className="h-10 px-6 rounded-lg border border-[#E0E0E2] text-[13px] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40"
        >
          {isFa ? "بازگشت" : "Back"}
        </button>
        <button
          type="button"
          onClick={handlePay}
          disabled={processing}
          className="h-10 px-6 rounded-lg bg-[#22C55E] text-white text-[13px] font-medium hover:bg-[#1da34d] transition-colors disabled:opacity-60 flex items-center gap-2 min-w-[160px] justify-center"
        >
          {processing ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              {isFa ? "در حال پردازش..." : "Processing..."}
            </>
          ) : (
            <>
              <ShieldCheck size={16} />
              {isFa ? "پرداخت" : "Pay Now"}
            </>
          )}
        </button>
      </div>
    </div>
  );
}
