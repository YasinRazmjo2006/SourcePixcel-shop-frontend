"use client";

import { useState } from "react";
import Link from "next/link";
import { Smartphone, Loader2, ArrowLeft, ArrowRight, CheckCircle2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { isValidIranianMobile, normalizeMobile } from "@/lib/utils";

interface ForgotPasswordFormProps {
  locale: Locale;
}

export default function ForgotPasswordForm({ locale }: ForgotPasswordFormProps) {
  const isFa = locale === "fa";
  const [mobile, setMobile] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);

  const t = {
    mobile: isFa ? "شماره موبایل" : "Mobile Number",
    submit: isFa ? "ارسال کد بازیابی" : "Send Reset Code",
    sending: isFa ? "در حال ارسال..." : "Sending...",
    required: isFa ? "شماره موبایل الزامی است" : "Mobile is required",
    invalid: isFa ? "شماره موبایل نامعتبر است" : "Invalid mobile number",
    successTitle: isFa ? "کد بازیابی ارسال شد" : "Reset code sent",
    successDesc: isFa
      ? "کد بازیابی به شماره موبایل شما ارسال شد. لطفاً پیامک خود را بررسی کنید."
      : "A reset code has been sent to your mobile. Please check your SMS.",
    backToLogin: isFa ? "بازگشت به ورود" : "Back to Login",
    hint: isFa
      ? "شماره تست: هر شماره معتبر ایرانی"
      : "Test: any valid Iranian mobile",
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!mobile.trim()) {
      setError(t.required);
      return;
    }
    if (!isValidIranianMobile(mobile)) {
      setError(t.invalid);
      return;
    }

    setSubmitting(true);
    setTimeout(() => {
      setSubmitting(false);
      setSuccess(true);
    }, 900);
  };

  if (success) {
    return (
      <div className="text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-[#22C55E]/10 flex items-center justify-center mx-auto">
          <CheckCircle2 size={36} className="text-[#22C55E]" />
        </div>
        <h2 className="text-[16px] font-bold text-[#3F4064]">
          {t.successTitle}
        </h2>
        <p className="text-[12px] text-[#62666D] leading-6">
          {t.successDesc}
        </p>
        <div className="bg-[#F5F5F5] rounded-lg p-3">
          <span className="text-[13px] font-bold text-[#3F4064]" dir="ltr">
            {normalizeMobile(mobile)}
          </span>
        </div>
        <Link
          href={`/${locale}/auth/login`}
          className="inline-flex items-center gap-2 text-[13px] text-[#EF4056] font-medium hover:underline"
        >
          {isFa ? <ArrowRight size={14} /> : <ArrowLeft size={14} />}
          {t.backToLogin}
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-[12px] text-[#62666D] mb-1.5">
          {t.mobile}
        </label>
        <div className="relative">
          <input
            type="tel"
            value={mobile}
            onChange={(e) => {
              setMobile(e.target.value);
              setError(null);
            }}
            placeholder="09123456789"
            dir="ltr"
            className={`w-full h-11 pr-10 pl-3 rounded-lg border text-[13px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
              error
                ? "border-[#EF4444] focus:border-[#EF4444]"
                : "border-[#E0E0E2] focus:border-[#EF4056]"
            }`}
          />
          <Smartphone
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
          />
        </div>
        {error && <p className="text-[11px] text-[#EF4444] mt-1">{error}</p>}
      </div>

      <button
        type="submit"
        disabled={submitting}
        className="w-full h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
      >
        {submitting ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            {t.sending}
          </>
        ) : (
          t.submit
        )}
      </button>

      <p className="text-[11px] text-[#A1A3A8] text-center bg-[#F5F5F5] rounded py-2 px-3">
        {t.hint}
      </p>

      <div className="text-center pt-3 border-t border-[#E0E0E2]">
        <Link
          href={`/${locale}/auth/login`}
          className="inline-flex items-center gap-2 text-[12px] text-[#00BFFF] hover:underline"
        >
          {isFa ? <ArrowRight size={14} /> : <ArrowLeft size={14} />}
          {t.backToLogin}
        </Link>
      </div>
    </form>
  );
}
