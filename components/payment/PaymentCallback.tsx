"use client";

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
