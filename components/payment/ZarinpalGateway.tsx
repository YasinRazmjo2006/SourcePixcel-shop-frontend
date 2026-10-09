"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  CreditCard,
  ShieldCheck,
  Loader2,
  X,
  AlertCircle,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { usePaymentStore } from "@/lib/stores";
import { formatPrice } from "@/lib/utils";

interface ZarinpalGatewayProps {
  locale: Locale;
  amount: number;
  orderNumber: string;
  onSuccess: (refId: string, cardNumber: string) => void;
  onCancel: () => void;
}

type CardStep = "enter-card" | "enter-otp" | "processing" | "failed";

export default function ZarinpalGateway({
  locale,
  amount,
  orderNumber,
  onSuccess,
  onCancel,
}: ZarinpalGatewayProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const createTransaction = usePaymentStore((s) => s.createTransaction);
  const updateTransaction = usePaymentStore((s) => s.updateTransaction);

  const [cardNumber, setCardNumber] = useState("");
  const [expiryMonth, setExpiryMonth] = useState("");
  const [expiryYear, setExpiryYear] = useState("");
  const [cvv2, setCvv2] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState<CardStep>("enter-card");
  const [error, setError] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes

  // Countdown timer
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 0) {
          clearInterval(timer);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const fmtTimer = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    const pad = (n: number) => String(n).padStart(2, "0");
    const result = `${pad(m)}:${pad(s)}`;
    return isFa ? result.replace(/\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]) : result;
  };

  const formatCardNumber = (value: string) => {
    const digits = value.replace(/\D/g, "").slice(0, 16);
    return digits.replace(/(\d{4})(?=\d)/g, "$1 ");
  };

  const handleCardNumberChange = (value: string) => {
    setCardNumber(formatCardNumber(value));
    setError(null);
  };

  const validateCard = (): boolean => {
    const digits = cardNumber.replace(/\s/g, "");
    if (digits.length !== 16) {
      setError(isFa ? "شماره کارت باید ۱۶ رقم باشد" : "Card number must be 16 digits");
      return false;
    }
    if (!expiryMonth || !expiryYear) {
      setError(isFa ? "تاریخ انقضا را وارد کنید" : "Enter expiry date");
      return false;
    }
    if (cvv2.length < 3) {
      setError(isFa ? "CVV2 باید حداقل ۳ رقم باشد" : "CVV2 must be at least 3 digits");
      return false;
    }
    return true;
  };

  const handleCardSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateCard()) return;

    // Create transaction
    const txn = createTransaction(amount);
    sessionStorage.setItem("sourcepixcel-txn-authority", txn.authority);

    setStep("enter-otp");
  };

  const handleOtpSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (otp.length !== 6) {
      setError(isFa ? "کد OTP باید ۶ رقم باشد" : "OTP must be 6 digits");
      return;
    }

    setStep("processing");

    const authority = sessionStorage.getItem("sourcepixcel-txn-authority") || "";

    // Simulate gateway processing
    setTimeout(() => {
      // 90% success rate
      const isSuccess = Math.random() > 0.1;

      if (isSuccess) {
        const refId = Math.floor(100000000 + Math.random() * 900000000).toString();
        const maskedCard = cardNumber.replace(/\s/g, "").slice(-4);
        const fullMasked = `****-****-****-${maskedCard}`;

        updateTransaction(authority, {
          status: "success",
          refId,
          cardNumber: fullMasked,
          paidAt: Date.now(),
          orderNumber,
        });

        sessionStorage.setItem("sourcepixcel-payment-result", "success");
        sessionStorage.setItem("sourcepixcel-payment-refid", refId);
        sessionStorage.setItem("sourcepixcel-payment-order", orderNumber);

        onSuccess(refId, fullMasked);
      } else {
        updateTransaction(authority, {
          status: "failed",
          orderNumber,
        });
        setStep("failed");
      }
    }, 2500);
  };

  const t = {
    gateway: isFa ? "درگاه پرداخت زرین‌پال" : "Zarinpal Payment Gateway",
    sandbox: isFa ? "محیط آزمایشی (Sandbox)" : "Sandbox Environment",
    amount: isFa ? "مبلغ قابل پرداخت" : "Amount to Pay",
    orderNumber: isFa ? "شماره سفارش" : "Order Number",
    cardNumber: isFa ? "شماره کارت" : "Card Number",
    expiry: isFa ? "تاریخ انقضا" : "Expiry Date",
    month: isFa ? "ماه" : "Month",
    year: isFa ? "سال" : "Year",
    cvv2: isFa ? "CVV2" : "CVV2",
    otp: isFa ? "رمز پویا" : "OTP Code",
    otpHint: isFa
      ? "کد ۶ رقمی ارسال‌شده به موبایل شما را وارد کنید"
      : "Enter the 6-digit code sent to your mobile",
    pay: isFa ? "پرداخت" : "Pay",
    submit: isFa ? "ادامه" : "Continue",
    cancel: isFa ? "انصراف" : "Cancel",
    processing: isFa ? "در حال پردازش پرداخت..." : "Processing payment...",
    failed: isFa ? "پرداخت ناموفق" : "Payment Failed",
    failedDesc: isFa
      ? "متأسفانه پرداخت شما انجام نشد. لطفاً دوباره تلاش کنید."
      : "Unfortunately, your payment failed. Please try again.",
    tryAgain: isFa ? "تلاش مجدد" : "Try Again",
    backToCheckout: isFa ? "بازگشت به فروشگاه" : "Back to Store",
    secure: isFa ? "پرداخت امن با رمزنگاری SSL" : "Secure payment with SSL",
    timeLeft: isFa ? "زمان باقی‌مانده" : "Time left",
    hint: isFa
      ? "برای تست: هر ۱۶ رقم کارت + CVV ۳ رقمی + OTP ۶ رقمی"
      : "Test: any 16-digit card + 3-digit CVV + 6-digit OTP",
  };

  return (
    <div className="min-h-screen bg-[#F5F5F5] dark:bg-[#0F0F12] flex flex-col">
      {/* Gateway header */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] shadow-sm">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#F9A825] to-[#FFB300] flex items-center justify-center text-white text-[18px] font-bold">
              Z
            </div>
            <div>
              <div className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.gateway}
              </div>
              <div className="text-[10px] text-[#A1A3A8]">{t.sandbox}</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 bg-[#F5F5F5] dark:bg-[#2A2A2E] px-3 py-1.5 rounded-lg">
              <div className="w-2 h-2 rounded-full bg-[#22C55E] animate-pulse" />
              <span className="text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                {t.timeLeft}: <span className="font-bold tabular-nums">{fmtTimer(timeLeft)}</span>
              </span>
            </div>
            <button
              onClick={onCancel}
              className="w-9 h-9 rounded-lg flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              aria-label={t.cancel}
            >
              <X size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* Body */}
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          {/* Amount card */}
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 mb-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[11px] text-[#A1A3A8]">{t.amount}</span>
              <span className="text-[10px] text-[#A1A3A8]" dir="ltr">
                {orderNumber}
              </span>
            </div>
            <div className="flex items-center gap-1">
              <span className="text-[24px] font-bold text-[#EF4056]">
                {formatPrice(amount, locale)}
              </span>
              <span className="text-[12px] text-[#62666D]">
                {isFa ? "تومان" : "Toman"}
              </span>
            </div>
          </div>

          {/* Form */}
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
            {/* Enter card */}
            {step === "enter-card" && (
              <form onSubmit={handleCardSubmit} className="space-y-4">
                <div className="flex items-center gap-2 mb-4">
                  <CreditCard size={18} className="text-[#EF4056]" />
                  <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                    {isFa ? "اطلاعات کارت بانکی" : "Card Information"}
                  </h2>
                </div>

                {/* Card number */}
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {t.cardNumber}
                  </label>
                  <input
                    type="text"
                    inputMode="numeric"
                    value={cardNumber}
                    onChange={(e) => handleCardNumberChange(e.target.value)}
                    placeholder="0000 0000 0000 0000"
                    dir="ltr"
                    className="w-full h-11 px-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[14px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#F9A825] focus:bg-white dark:focus:bg-[#1A1A1E] transition-colors text-center tabular-nums tracking-wider"
                    maxLength={19}
                    autoFocus
                  />
                </div>

                {/* Expiry + CVV2 */}
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                      {t.month}
                    </label>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={expiryMonth}
                      onChange={(e) =>
                        setExpiryMonth(e.target.value.replace(/\D/g, "").slice(0, 2))
                      }
                      placeholder="MM"
                      dir="ltr"
                      className="w-full h-11 px-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#F9A825] text-center tabular-nums"
                      maxLength={2}
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                      {t.year}
                    </label>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={expiryYear}
                      onChange={(e) =>
                        setExpiryYear(e.target.value.replace(/\D/g, "").slice(0, 2))
                      }
                      placeholder="YY"
                      dir="ltr"
                      className="w-full h-11 px-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#F9A825] text-center tabular-nums"
                      maxLength={2}
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                      {t.cvv2}
                    </label>
                    <input
                      type="text"
                      inputMode="numeric"
                      value={cvv2}
                      onChange={(e) =>
                        setCvv2(e.target.value.replace(/\D/g, "").slice(0, 4))
                      }
                      placeholder="123"
                      dir="ltr"
                      className="w-full h-11 px-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#F9A825] text-center tabular-nums"
                      maxLength={4}
                    />
                  </div>
                </div>

                {error && (
                  <div className="bg-[#EF4444]/10 border border-[#EF4444]/30 rounded-lg p-2.5 flex items-center gap-2">
                    <AlertCircle size={14} className="text-[#EF4444] shrink-0" />
                    <span className="text-[11px] text-[#EF4444]">{error}</span>
                  </div>
                )}

                <div className="bg-[#F9A825]/10 border border-[#F9A825]/30 rounded-lg p-2.5">
                  <p className="text-[10px] text-[#F9A825] text-center">
                    {t.hint}
                  </p>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={onCancel}
                    className="flex-1 h-11 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                  >
                    {t.cancel}
                  </button>
                  <button
                    type="submit"
                    className="flex-1 h-11 rounded-lg bg-[#F9A825] text-white text-[13px] font-bold hover:bg-[#E09600] transition-colors"
                  >
                    {t.submit}
                  </button>
                </div>
              </form>
            )}

            {/* Enter OTP */}
            {step === "enter-otp" && (
              <form onSubmit={handleOtpSubmit} className="space-y-4">
                <div className="flex items-center gap-2 mb-4">
                  <ShieldCheck size={18} className="text-[#22C55E]" />
                  <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                    {t.otp}
                  </h2>
                </div>

                <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6">
                  {t.otpHint}
                </p>

                <input
                  type="text"
                  inputMode="numeric"
                  value={otp}
                  onChange={(e) => {
                    setOtp(e.target.value.replace(/\D/g, "").slice(0, 6));
                    setError(null);
                  }}
                  placeholder="- - - - - -"
                  dir="ltr"
                  className="w-full h-14 px-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border-2 border-[#E0E0E2] dark:border-[#3A3A40] text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#F9A825] text-center tabular-nums tracking-[8px]"
                  maxLength={6}
                  autoFocus
                />

                {error && (
                  <div className="bg-[#EF4444]/10 border border-[#EF4444]/30 rounded-lg p-2.5 flex items-center gap-2">
                    <AlertCircle size={14} className="text-[#EF4444] shrink-0" />
                    <span className="text-[11px] text-[#EF4444]">{error}</span>
                  </div>
                )}

                <div className="bg-[#22C55E]/10 border border-[#22C55E]/30 rounded-lg p-2.5">
                  <p className="text-[10px] text-[#22C55E] text-center">
                    {isFa ? "برای تست: هر ۶ رقم" : "Test: any 6 digits"}
                  </p>
                </div>

                <div className="flex gap-2 pt-2">
                  <button
                    type="button"
                    onClick={() => setStep("enter-card")}
                    className="flex-1 h-11 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                  >
                    {isFa ? "بازگشت" : "Back"}
                  </button>
                  <button
                    type="submit"
                    className="flex-1 h-11 rounded-lg bg-[#22C55E] text-white text-[13px] font-bold hover:bg-[#1da34d] transition-colors"
                  >
                    {t.pay}
                  </button>
                </div>
              </form>
            )}

            {/* Processing */}
            {step === "processing" && (
              <div className="py-12 text-center">
                <div className="relative w-20 h-20 mx-auto mb-5">
                  <div className="absolute inset-0 rounded-full border-4 border-[#F9A825]/20" />
                  <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-[#F9A825] animate-spin" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <Loader2 size={28} className="text-[#F9A825] animate-pulse" />
                  </div>
                </div>
                <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
                  {t.processing}
                </h3>
                <p className="text-[11px] text-[#A1A3A8]">
                  {isFa
                    ? "لطفاً صفحه را نبندید"
                    : "Please do not close this page"}
                </p>
              </div>
            )}

            {/* Failed */}
            {step === "failed" && (
              <div className="py-8 text-center">
                <div className="w-20 h-20 rounded-full bg-[#EF4444]/10 flex items-center justify-center mx-auto mb-4">
                  <AlertCircle size={44} className="text-[#EF4444]" />
                </div>
                <h3 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
                  {t.failed}
                </h3>
                <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6 mb-6">
                  {t.failedDesc}
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setStep("enter-card");
                      setOtp("");
                      setError(null);
                    }}
                    className="flex-1 h-11 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors"
                  >
                    {t.tryAgain}
                  </button>
                  <button
                    onClick={onCancel}
                    className="flex-1 h-11 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                  >
                    {t.backToCheckout}
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Trust */}
          <div className="flex items-center justify-center gap-2 mt-4 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
            <ShieldCheck size={14} className="text-[#22C55E]" />
            {t.secure}
          </div>
        </div>
      </div>
    </div>
  );
}
