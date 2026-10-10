"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Smartphone, Loader2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAuthStore } from "@/lib/stores";
import { isValidIranianMobile, normalizeMobile } from "@/lib/utils";
import { RippleButton, AnimatedCheckbox } from "@/components/ui";

interface LoginFormProps {
  locale: Locale;
}

export default function LoginForm({ locale }: LoginFormProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const login = useAuthStore((s) => s.login);

  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [errors, setErrors] = useState<{ mobile?: string; password?: string }>({});
  const [submitting, setSubmitting] = useState(false);

  const t = {
    mobile: isFa ? "شماره موبایل" : "Mobile Number",
    password: isFa ? "رمز عبور" : "Password",
    remember: isFa ? "به خاطر بسپار" : "Remember me",
    forgot: isFa ? "رمز عبور را فراموش کرده‌اید؟" : "Forgot password?",
    login: isFa ? "ورود" : "Login",
    loggingIn: isFa ? "در حال ورود..." : "Logging in...",
    mobileRequired: isFa ? "شماره موبایل الزامی است" : "Mobile is required",
    mobileInvalid: isFa ? "شماره موبایل نامعتبر است" : "Invalid mobile number",
    passwordRequired: isFa ? "رمز عبور الزامی است" : "Password is required",
    passwordShort: isFa
      ? "رمز عبور باید حداقل ۶ کاراکتر باشد"
      : "Password must be at least 6 characters",
    noAccount: isFa ? "حساب کاربری ندارید؟" : "Don't have an account?",
    register: isFa ? "ثبت‌نام" : "Register",
    hint: isFa
      ? "برای تست: هر شماره موبایل معتبر + رمز ۶ رقمی"
      : "Test hint: any valid mobile + 6-char password",
  };

  const validate = () => {
    const e: { mobile?: string; password?: string } = {};
    if (!mobile.trim()) e.mobile = t.mobileRequired;
    else if (!isValidIranianMobile(mobile)) e.mobile = t.mobileInvalid;
    if (!password) e.password = t.passwordRequired;
    else if (password.length < 6) e.password = t.passwordShort;
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    setTimeout(() => {
      login({
        id: `user-${Date.now()}`,
        fullName: isFa ? "کاربر SourcePixcel" : "SourcePixcel User",
        mobile: normalizeMobile(mobile),
      });
      router.push(`/${locale}/account`);
    }, 800);
  };

  const inputClass = (field: "mobile" | "password") =>
    `w-full h-11 pr-10 pl-3 rounded-lg border text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] dark:border-[#2A2A2E] focus:border-[#EF4056]"
    }`;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
          {t.mobile}
        </label>
        <div className="relative">
          <input
            type="tel"
            value={mobile}
            onChange={(e) => {
              setMobile(e.target.value);
              setErrors((p) => ({ ...p, mobile: undefined }));
            }}
            placeholder="09123456789"
            dir="ltr"
            autoComplete="tel"
            className={inputClass("mobile")}
          />
          <Smartphone
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
          />
        </div>
        {errors.mobile && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.mobile}</p>
        )}
      </div>

      <div>
        <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
          {t.password}
        </label>
        <div className="relative">
          <input
            type={showPassword ? "text" : "password"}
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setErrors((p) => ({ ...p, password: undefined }));
            }}
            placeholder="••••••••"
            dir="ltr"
            autoComplete="current-password"
            className={inputClass("password")}
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            aria-label={showPassword ? "Hide" : "Show"}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8] hover:text-[#62666D]"
            style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
          >
            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>
        {errors.password && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.password}</p>
        )}
      </div>

      <div className="flex items-center justify-between text-[12px]">
        <AnimatedCheckbox
          checked={remember}
          onChange={setRemember}
          label={t.remember}
        />
        <Link
          href={`/${locale}/auth/forgot-password`}
          className="text-[#00BFFF] hover:underline"
        >
          {t.forgot}
        </Link>
      </div>

      <RippleButton
        type="submit"
        disabled={submitting}
        fullWidth
        size="md"
      >
        {submitting ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            {t.loggingIn}
          </>
        ) : (
          t.login
        )}
      </RippleButton>

      <p className="text-[11px] text-[#A1A3A8] text-center bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded py-2 px-3">
        {t.hint}
      </p>

      <div className="text-center text-[12px] text-[#62666D] dark:text-[#A1A3A8] pt-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
        {t.noAccount}{" "}
        <Link
          href={`/${locale}/auth/register`}
          className="text-[#EF4056] font-medium hover:underline"
        >
          {t.register}
        </Link>
      </div>
    </form>
  );
}
