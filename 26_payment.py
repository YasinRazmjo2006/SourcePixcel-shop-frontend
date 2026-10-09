# 26_payment.py
# درگاه پرداخت شبیه‌سازی‌شده + صفحه بازگشت
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/payment.ts
# ============================================================
files.append(("lib/stores/payment.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface PaymentTransaction {
  id: string;
  authority: string;
  amount: number;
  status: "pending" | "success" | "failed" | "cancelled";
  cardNumber?: string;
  refId?: string;
  createdAt: number;
  paidAt?: number;
  orderNumber?: string;
}

interface PaymentState {
  transactions: PaymentTransaction[];
  createTransaction: (amount: number) => PaymentTransaction;
  updateTransaction: (
    authority: string,
    updates: Partial<PaymentTransaction>
  ) => void;
  getByAuthority: (authority: string) => PaymentTransaction | undefined;
  clearAll: () => void;
}

export const usePaymentStore = create<PaymentState>()(
  persist(
    (set, get) => ({
      transactions: [],

      createTransaction: (amount) => {
        const authority = `A0000000000000000000000000${Date.now()
          .toString()
          .slice(-8)}`;
        const txn: PaymentTransaction = {
          id: `txn-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
          authority,
          amount,
          status: "pending",
          createdAt: Date.now(),
        };
        set((state) => ({
          transactions: [txn, ...state.transactions].slice(0, 50),
        }));
        return txn;
      },

      updateTransaction: (authority, updates) => {
        set((state) => ({
          transactions: state.transactions.map((t) =>
            t.authority === authority ? { ...t, ...updates } : t
          ),
        }));
      },

      getByAuthority: (authority) =>
        get().transactions.find((t) => t.authority === authority),

      clearAll: () => set({ transactions: [] }),
    }),
    { name: "sourcepixcel-payments" }
  )
);
"""))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", """// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export { useAdminStore } from "./admin";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
"""))

# ============================================================
# components/payment/ZarinpalGateway.tsx
# ============================================================
files.append(("components/payment/ZarinpalGateway.tsx", """"use client";

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
    return isFa ? result.replace(/\\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[parseInt(d)]) : result;
  };

  const formatCardNumber = (value: string) => {
    const digits = value.replace(/\\D/g, "").slice(0, 16);
    return digits.replace(/(\\d{4})(?=\\d)/g, "$1 ");
  };

  const handleCardNumberChange = (value: string) => {
    setCardNumber(formatCardNumber(value));
    setError(null);
  };

  const validateCard = (): boolean => {
    const digits = cardNumber.replace(/\\s/g, "");
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
        const maskedCard = cardNumber.replace(/\\s/g, "").slice(-4);
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
                        setExpiryMonth(e.target.value.replace(/\\D/g, "").slice(0, 2))
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
                        setExpiryYear(e.target.value.replace(/\\D/g, "").slice(0, 2))
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
                        setCvv2(e.target.value.replace(/\\D/g, "").slice(0, 4))
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
                    setOtp(e.target.value.replace(/\\D/g, "").slice(0, 6));
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
"""))

# ============================================================
# components/payment/PaymentCallback.tsx
# ============================================================
files.append(("components/payment/PaymentCallback.tsx", """"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  CheckCircle2,
  XCircle,
  Copy,
  Check,
  Home,
  Package,
  Receipt,
  Calendar,
  CreditCard,
  Loader2,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { usePaymentStore } from "@/lib/stores";
import { formatPrice } from "@/lib/utils";

interface PaymentCallbackProps {
  locale: Locale;
  authority: string;
  status: "success" | "failed" | "cancelled";
}

export default function PaymentCallback({
  locale,
  authority,
  status,
}: PaymentCallbackProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const [copied, setCopied] = useState(false);
  const [secondsLeft, setSecondsLeft] = useState(15);

  const getByAuthority = usePaymentStore((s) => s.getByAuthority);
  const txn = getByAuthority(authority);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Auto-redirect on success
  useEffect(() => {
    if (status !== "success") return;
    const timer = setInterval(() => {
      setSecondsLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          window.location.href = `/${locale}/account/orders`;
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, [status, locale]);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 size={32} className="text-[#EF4056] animate-spin" />
      </div>
    );
  }

  const isSuccess = status === "success";
  const isFailed = status === "failed";
  const isCancelled = status === "cancelled";

  const t = {
    successTitle: isFa ? "پرداخت با موفقیت انجام شد" : "Payment Successful",
    successDesc: isFa
      ? "سفارش شما با موفقیت ثبت شد. کد پیگیری برای شما پیامک خواهد شد."
      : "Your order has been placed successfully. Tracking code will be sent via SMS.",
    failedTitle: isFa ? "پرداخت ناموفق" : "Payment Failed",
    failedDesc: isFa
      ? "متأسفانه پرداخت شما انجام نشد. مبلغ تا ۷۲ ساعت آینده به حساب شما بازمی‌گردد."
      : "Unfortunately, your payment failed. The amount will be refunded within 72 hours.",
    cancelledTitle: isFa ? "پرداخت لغو شد" : "Payment Cancelled",
    cancelledDesc: isFa
      ? "شما پرداخت را لغو کردید. سفارش شما ثبت نشده است."
      : "You cancelled the payment. Your order was not placed.",
    refId: isFa ? "شماره پیگیری" : "Reference ID",
    orderNumber: isFa ? "شماره سفارش" : "Order Number",
    amount: isFa ? "مبلغ پرداختی" : "Amount Paid",
    cardNumber: isFa ? "کارت بانکی" : "Card",
    date: isFa ? "تاریخ پرداخت" : "Payment Date",
    copy: isFa ? "کپی" : "Copy",
    copied: isFa ? "کپی شد" : "Copied",
    viewOrders: isFa ? "مشاهده سفارشات" : "View Orders",
    backHome: isFa ? "بازگشت به خانه" : "Back to Home",
    tryAgain: isFa ? "تلاش مجدد" : "Try Again",
    redirecting: isFa
      ? `انتقال خودکار به صفحه سفارشات در ${secondsLeft} ثانیه...`
      : `Auto-redirecting to orders in ${secondsLeft}s...`,
  };

  const statusColor = isSuccess ? "#22C55E" : isFailed ? "#EF4444" : "#F59E0B";
  const StatusIcon = isSuccess
    ? CheckCircle2
    : isFailed
    ? XCircle
    : XCircle;

  const title = isSuccess
    ? t.successTitle
    : isFailed
    ? t.failedTitle
    : t.cancelledTitle;

  const description = isSuccess
    ? t.successDesc
    : isFailed
    ? t.failedDesc
    : t.cancelledDesc;

  const dateFormatted = txn?.paidAt
    ? new Intl.DateTimeFormat(isFa ? "fa-IR" : "en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(new Date(txn.paidAt))
    : "—";

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-lg">
        {/* Status card */}
        <div className="bg-white dark:bg-[#1A1A1E] rounded-2xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-6 md:p-8">
          {/* Icon */}
          <div
            className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-5"
            style={{ backgroundColor: `${statusColor}15` }}
          >
            <StatusIcon size={48} style={{ color: statusColor }} />
          </div>

          {/* Title */}
          <h1
            className="text-[20px] md:text-[22px] font-bold text-center mb-3"
            style={{ color: statusColor }}
          >
            {title}
          </h1>

          {/* Description */}
          <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] text-center leading-7 mb-6 max-w-md mx-auto">
            {description}
          </p>

          {/* Details */}
          {isSuccess && txn && (
            <div className="bg-[#FAFAFA] dark:bg-[#0F0F12] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 mb-5 space-y-3">
              {/* Reference ID */}
              {txn.refId && (
                <div className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    <Receipt size={14} />
                    <span>{t.refId}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span
                      className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums"
                      dir="ltr"
                    >
                      {txn.refId}
                    </span>
                    <button
                      onClick={() => handleCopy(txn.refId!)}
                      className="w-6 h-6 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#2A2A2E] transition-colors"
                      aria-label={t.copy}
                    >
                      {copied ? (
                        <Check size={12} className="text-[#22C55E]" />
                      ) : (
                        <Copy size={12} />
                      )}
                    </button>
                  </div>
                </div>
              )}

              {/* Order Number */}
              {txn.orderNumber && (
                <div className="flex items-center justify-between gap-3 pt-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
                  <div className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    <Package size={14} />
                    <span>{t.orderNumber}</span>
                  </div>
                  <span
                    className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]"
                    dir="ltr"
                  >
                    {txn.orderNumber}
                  </span>
                </div>
              )}

              {/* Amount */}
              <div className="flex items-center justify-between gap-3 pt-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
                <div className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  <CreditCard size={14} />
                  <span>{t.amount}</span>
                </div>
                <span className="text-[13px] font-bold text-[#EF4056]">
                  {formatPrice(txn.amount, locale)}{" "}
                  <span className="text-[10px] text-[#A1A3A8] font-normal">
                    {isFa ? "تومان" : "T"}
                  </span>
                </span>
              </div>

              {/* Card */}
              {txn.cardNumber && (
                <div className="flex items-center justify-between gap-3 pt-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
                  <div className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    <CreditCard size={14} />
                    <span>{t.cardNumber}</span>
                  </div>
                  <span
                    className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] tabular-nums"
                    dir="ltr"
                  >
                    {txn.cardNumber}
                  </span>
                </div>
              )}

              {/* Date */}
              <div className="flex items-center justify-between gap-3 pt-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
                <div className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  <Calendar size={14} />
                  <span>{t.date}</span>
                </div>
                <span className="text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                  {dateFormatted}
                </span>
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="flex flex-col gap-2">
            {isSuccess ? (
              <Link
                href={`/${locale}/account/orders`}
                className="h-11 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors flex items-center justify-center gap-2"
              >
                <Package size={16} />
                {t.viewOrders}
              </Link>
            ) : (
              <Link
                href={`/${locale}/cart`}
                className="h-11 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors flex items-center justify-center gap-2"
              >
                {t.tryAgain}
              </Link>
            )}

            <Link
              href={`/${locale}`}
              className="h-11 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center justify-center gap-2"
            >
              <Home size={16} />
              {t.backHome}
            </Link>
          </div>

          {/* Auto-redirect notice */}
          {isSuccess && (
            <p className="text-[10px] text-[#A1A3A8] text-center mt-4">
              {t.redirecting}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/payment/index.ts
# ============================================================
files.append(("components/payment/index.ts", """// components/payment/index.ts
export { default as ZarinpalGateway } from "./ZarinpalGateway";
export { default as PaymentCallback } from "./PaymentCallback";
"""))

# ============================================================
# components/checkout/CheckoutPage.tsx (updated with real gateway)
# ============================================================
files.append(("components/checkout/CheckoutPage.tsx", """"use client";

import { useState, useMemo, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { Breadcrumb, EmptyState } from "@/components/common";
import StepIndicator from "./StepIndicator";
import ShippingForm, { type ShippingData } from "./ShippingForm";
import ShippingMethod from "./ShippingMethod";
import OrderReview from "./OrderReview";
import ZarinpalGateway from "@/components/payment/ZarinpalGateway";
import PaymentCallback from "@/components/payment/PaymentCallback";

interface CheckoutPageProps {
  locale: Locale;
}

const STEPS = [
  { fa: "اطلاعات ارسال", en: "Shipping" },
  { fa: "روش ارسال", en: "Method" },
  { fa: "پرداخت", en: "Payment" },
];

const EMPTY_SHIPPING: ShippingData = {
  fullName: "",
  mobile: "",
  province: "",
  city: "",
  postalCode: "",
  address: "",
};

export default function CheckoutPage({ locale }: CheckoutPageProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const [step, setStep] = useState(1);
  const [shipping, setShipping] = useState<ShippingData>(EMPTY_SHIPPING);
  const [shippingMethodId, setShippingMethodId] = useState<string | null>(null);
  const [showGateway, setShowGateway] = useState(false);
  const [paymentResult, setPaymentResult] = useState<{
    status: "success" | "failed" | "cancelled";
    authority: string;
  } | null>(null);

  const items = useCartStore((s) => s.items);
  const clearCart = useCartStore((s) => s.clear);

  useEffect(() => {
    setMounted(true);
  }, []);

  const lines = useMemo(() => {
    return items
      .map((line) => {
        const product = allProducts.find((p) => p.id === line.productId);
        return product ? { product, quantity: line.quantity } : null;
      })
      .filter((x): x is { product: Product; quantity: number } => x !== null);
  }, [items]);

  const totals = useMemo(() => {
    const subtotal = lines.reduce(
      (sum, l) => sum + l.product.price * l.quantity,
      0
    );
    const finalTotal = lines.reduce(
      (sum, l) => sum + l.product.finalPrice * l.quantity,
      0
    );
    const totalDiscount = subtotal - finalTotal;
    const FREE = 5_000_000;

    let shippingCost = 0;
    if (shippingMethodId === "post") {
      shippingCost = finalTotal >= FREE ? 0 : 45_000;
    } else if (shippingMethodId === "tipax") {
      shippingCost = finalTotal >= FREE ? 0 : 85_000;
    } else if (shippingMethodId === "pickup") {
      shippingCost = 0;
    }

    const total = finalTotal + shippingCost;
    return { subtotal, totalDiscount, shippingCost, total };
  }, [lines, shippingMethodId]);

  const [orderNumber] = useState(
    () => `SP-${Date.now().toString().slice(-8)}`
  );

  const handlePay = () => {
    setShowGateway(true);
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleGatewaySuccess = (refId: string) => {
    const authority = sessionStorage.getItem("sourcepixcel-txn-authority") || "";
    clearCart();
    setShowGateway(false);
    setPaymentResult({ status: "success", authority });
  };

  const handleGatewayCancel = () => {
    setShowGateway(false);
    setPaymentResult({ status: "cancelled", authority: "" });
  };

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  // Payment callback result
  if (paymentResult) {
    return (
      <PaymentCallback
        locale={locale}
        authority={paymentResult.authority}
        status={paymentResult.status}
      />
    );
  }

  // Gateway
  if (showGateway) {
    return (
      <ZarinpalGateway
        locale={locale}
        amount={totals.total}
        orderNumber={orderNumber}
        onSuccess={handleGatewaySuccess}
        onCancel={handleGatewayCancel}
      />
    );
  }

  // Empty cart
  if (lines.length === 0) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-4">
        <Breadcrumb
          locale={locale}
          items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
        />
        <EmptyState
          locale={locale}
          titleFa="سبد خرید خالی است"
          titleEn="Your cart is empty"
          messageFa="برای تسویه حساب ابتدا محصولی به سبد خرید اضافه کنید."
          messageEn="Add a product to your cart before checking out."
        />
      </div>
    );
  }

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
        {isFa ? "تسویه حساب" : "Checkout"}
      </h1>

      <StepIndicator currentStep={step} steps={STEPS} locale={locale} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          {step === 1 && (
            <ShippingForm
              locale={locale}
              initialData={shipping}
              onSubmit={(data) => {
                setShipping(data);
                setStep(2);
              }}
            />
          )}

          {step === 2 && (
            <ShippingMethod
              locale={locale}
              selected={shippingMethodId}
              onSelect={setShippingMethodId}
              onNext={() => setStep(3)}
              onBack={() => setStep(1)}
              subtotal={totals.subtotal}
            />
          )}

          {step === 3 && (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
              <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-5">
                {isFa ? "پرداخت" : "Payment"}
              </h2>

              {/* Payment summary */}
              <div className="bg-[#FAFAFA] dark:bg-[#0F0F12] rounded-xl p-4 mb-4 border border-[#E0E0E2] dark:border-[#2A2A2E]">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    {isFa ? "مبلغ قابل پرداخت" : "Amount to Pay"}
                  </span>
                  <span className="text-[18px] font-bold text-[#EF4056]">
                    {formatPrice(totals.total, locale)}{" "}
                    <span className="text-[11px] text-[#62666D] font-normal">
                      {isFa ? "تومان" : "T"}
                    </span>
                  </span>
                </div>
                <div className="text-[11px] text-[#A1A3A8] text-center">
                  {isFa
                    ? "پس از کلیک روی پرداخت، به درگاه زرین‌پال منتقل می‌شوید."
                    : "After clicking pay, you will be redirected to Zarinpal."}
                </div>
              </div>

              {/* Gateway info */}
              <div className="border-2 border-dashed border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl p-5 bg-[#F9A825]/5 mb-5">
                <div className="flex items-center justify-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#F9A825] to-[#FFB300] flex items-center justify-center text-white text-[22px] font-bold">
                    Z
                  </div>
                  <div className="text-center">
                    <div className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                      {isFa ? "درگاه پرداخت زرین‌پال" : "Zarinpal Payment Gateway"}
                    </div>
                    <div className="text-[11px] text-[#A1A3A8]">
                      {isFa ? "محیط آزمایشی (Sandbox)" : "Sandbox Environment"}
                    </div>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  onClick={() => setStep(2)}
                  className="h-11 px-5 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                >
                  {isFa ? "بازگشت" : "Back"}
                </button>
                <button
                  onClick={handlePay}
                  className="flex-1 h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors"
                >
                  {isFa ? "پرداخت و اتمام خرید" : "Pay & Complete Order"}
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Review sidebar */}
        <div className="lg:col-span-1">
          {step >= 2 && shipping.fullName ? (
            <OrderReview
              locale={locale}
              lines={lines}
              shipping={shipping}
              shippingMethodId={shippingMethodId ?? "post"}
              subtotal={totals.subtotal}
              totalDiscount={totals.totalDiscount}
              shippingCost={totals.shippingCost}
              total={totals.total}
            />
          ) : (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5 text-[12px] text-[#A1A3A8] text-center">
              {isFa
                ? "اطلاعات سفارش پس از تکمیل فرم نمایش داده می‌شود."
                : "Order details will appear after completing the form."}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 26: Payment Gateway")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("Now run:")
        print("  Remove-Item -Recurse -Force .next")
        print("  npm run dev")
        print("\nTest:")
        print("  1) Add a product to cart")
        print("  2) Go to /fa/checkout")
        print("  3) Complete steps 1 and 2")
        print("  4) Click 'Pay & Complete Order'")
        print("  5) Enter: card 16 digits, MM/YY, CVV, OTP 6 digits")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()