# 13_auth.py
# ساخت صفحات احراز هویت
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/auth.ts
# ============================================================
files.append(("lib/stores/auth.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface AuthUser {
  id: string;
  fullName: string;
  mobile: string;
  email?: string;
}

interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (user: AuthUser) => void;
  logout: () => void;
  update: (partial: Partial<AuthUser>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,

      login: (user) => set({ user, isAuthenticated: true }),

      logout: () => set({ user: null, isAuthenticated: false }),

      update: (partial) =>
        set((state) =>
          state.user ? { user: { ...state.user, ...partial } } : state
        ),
    }),
    { name: "sourcepixcel-auth" }
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
export type { AuthUser } from "./auth";
"""))

# ============================================================
# components/auth/AuthCard.tsx
# ============================================================
files.append(("components/auth/AuthCard.tsx", """import Link from "next/link";
import type { Locale } from "@/lib/types";

interface AuthCardProps {
  locale: Locale;
  titleFa: string;
  titleEn: string;
  subtitleFa?: string;
  subtitleEn?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export default function AuthCard({
  locale,
  titleFa,
  titleEn,
  subtitleFa,
  subtitleEn,
  children,
  footer,
}: AuthCardProps) {
  const isFa = locale === "fa";

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-8 bg-[#F5F5F5]">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl border border-[#E0E0E2] p-6 md:p-8 shadow-sm">
          {/* Logo */}
          <Link
            href={`/${locale}`}
            className="flex items-center justify-center mb-6"
          >
            <span className="text-[#EF4056] font-bold text-2xl">
              SourcePixcel
            </span>
          </Link>

          {/* Header */}
          <div className="text-center mb-6">
            <h1 className="text-[18px] font-bold text-[#3F4064] mb-2">
              {isFa ? titleFa : titleEn}
            </h1>
            {(subtitleFa || subtitleEn) && (
              <p className="text-[12px] text-[#62666D] leading-5">
                {isFa ? subtitleFa : subtitleEn}
              </p>
            )}
          </div>

          {children}
        </div>

        {footer && <div className="mt-4">{footer}</div>}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/auth/LoginForm.tsx
# ============================================================
files.append(("components/auth/LoginForm.tsx", """"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Smartphone, Lock, Loader2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAuthStore } from "@/lib/stores";
import { isValidIranianMobile, normalizeMobile } from "@/lib/utils";

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
    // Mock login
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
    `w-full h-11 pr-10 pl-3 rounded-lg border text-[13px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] focus:border-[#EF4056]"
    }`;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Mobile */}
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

      {/* Password */}
      <div>
        <label className="block text-[12px] text-[#62666D] mb-1.5">
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
          <Lock
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{
              [isFa ? "left" : "right"]: isFa ? 36 : 36,
              display: "none",
            } as React.CSSProperties}
          />
        </div>
        {errors.password && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.password}</p>
        )}
      </div>

      {/* Remember + Forgot */}
      <div className="flex items-center justify-between text-[12px]">
        <label className="flex items-center gap-2 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
            className="w-4 h-4 accent-[#EF4056]"
          />
          <span className="text-[#62666D]">{t.remember}</span>
        </label>
        <Link
          href={`/${locale}/auth/forgot-password`}
          className="text-[#00BFFF] hover:underline"
        >
          {t.forgot}
        </Link>
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={submitting}
        className="w-full h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
      >
        {submitting ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            {t.loggingIn}
          </>
        ) : (
          t.login
        )}
      </button>

      {/* Test hint */}
      <p className="text-[11px] text-[#A1A3A8] text-center bg-[#F5F5F5] rounded py-2 px-3">
        {t.hint}
      </p>

      {/* Register link */}
      <div className="text-center text-[12px] text-[#62666D] pt-3 border-t border-[#E0E0E2]">
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
"""))

# ============================================================
# components/auth/RegisterForm.tsx
# ============================================================
files.append(("components/auth/RegisterForm.tsx", """"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Smartphone, User, Mail, Loader2, Check } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAuthStore } from "@/lib/stores";
import {
  isValidIranianMobile,
  isValidEmail,
  getPasswordStrength,
  normalizeMobile,
} from "@/lib/utils";

interface RegisterFormProps {
  locale: Locale;
}

export default function RegisterForm({ locale }: RegisterFormProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const login = useAuthStore((s) => s.login);

  const [fullName, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [terms, setTerms] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});

  const t = {
    fullName: isFa ? "نام و نام خانوادگی" : "Full Name",
    mobile: isFa ? "شماره موبایل" : "Mobile Number",
    email: isFa ? "ایمیل (اختیاری)" : "Email (optional)",
    password: isFa ? "رمز عبور" : "Password",
    confirm: isFa ? "تکرار رمز عبور" : "Confirm Password",
    terms: isFa
      ? "قوانین و مقررات را می‌پذیرم"
      : "I accept the terms and conditions",
    register: isFa ? "ثبت‌نام" : "Register",
    registering: isFa ? "در حال ثبت‌نام..." : "Registering...",
    haveAccount: isFa ? "حساب کاربری دارید؟" : "Already have an account?",
    login: isFa ? "ورود" : "Login",
    strength: isFa ? "قدرت رمز:" : "Strength:",
    weak: isFa ? "ضعیف" : "Weak",
    medium: isFa ? "متوسط" : "Medium",
    strong: isFa ? "قوی" : "Strong",
    required: isFa ? "الزامی" : "Required",
    mobileInvalid: isFa ? "شماره موبایل نامعتبر است" : "Invalid mobile number",
    emailInvalid: isFa ? "ایمیل نامعتبر است" : "Invalid email",
    passwordShort: isFa
      ? "رمز عبور باید حداقل ۶ کاراکتر باشد"
      : "Password must be at least 6 characters",
    passwordMismatch: isFa
      ? "رمز عبور و تکرار آن مطابقت ندارند"
      : "Passwords do not match",
    termsRequired: isFa
      ? "پذیرش قوانین الزامی است"
      : "You must accept the terms",
    nameShort: isFa ? "نام باید حداقل ۳ کاراکتر باشد" : "Name must be at least 3 characters",
  };

  const strength = getPasswordStrength(password);
  const strengthColors = {
    weak: "bg-[#EF4444]",
    medium: "bg-[#F59E0B]",
    strong: "bg-[#22C55E]",
  };
  const strengthLabels = {
    weak: t.weak,
    medium: t.medium,
    strong: t.strong,
  };
  const strengthWidth = { weak: "33%", medium: "66%", strong: "100%" };

  const validate = () => {
    const e: Record<string, string | undefined> = {};
    if (!fullName.trim()) e.fullName = t.required;
    else if (fullName.trim().length < 3) e.fullName = t.nameShort;

    if (!mobile.trim()) e.mobile = t.required;
    else if (!isValidIranianMobile(mobile)) e.mobile = t.mobileInvalid;

    if (email.trim() && !isValidEmail(email)) e.email = t.emailInvalid;

    if (!password) e.password = t.required;
    else if (password.length < 6) e.password = t.passwordShort;

    if (!confirm) e.confirm = t.required;
    else if (confirm !== password) e.confirm = t.passwordMismatch;

    if (!terms) e.terms = t.termsRequired;

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
        fullName: fullName.trim(),
        mobile: normalizeMobile(mobile),
        email: email.trim() || undefined,
      });
      router.push(`/${locale}/account`);
    }, 900);
  };

  const inputClass = (field: string) =>
    `w-full h-11 pr-10 pl-3 rounded-lg border text-[13px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] focus:border-[#EF4056]"
    }`;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Full name */}
      <div>
        <label className="block text-[12px] text-[#62666D] mb-1.5">
          {t.fullName}
        </label>
        <div className="relative">
          <input
            type="text"
            value={fullName}
            onChange={(e) => {
              setFullName(e.target.value);
              setErrors((p) => ({ ...p, fullName: undefined }));
            }}
            placeholder={isFa ? "علی محمدی" : "John Doe"}
            className={inputClass("fullName")}
          />
          <User
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
          />
        </div>
        {errors.fullName && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.fullName}</p>
        )}
      </div>

      {/* Mobile */}
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
              setErrors((p) => ({ ...p, mobile: undefined }));
            }}
            placeholder="09123456789"
            dir="ltr"
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

      {/* Email */}
      <div>
        <label className="block text-[12px] text-[#62666D] mb-1.5">
          {t.email}
        </label>
        <div className="relative">
          <input
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setErrors((p) => ({ ...p, email: undefined }));
            }}
            placeholder="you@example.com"
            dir="ltr"
            className={inputClass("email")}
          />
          <Mail
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
          />
        </div>
        {errors.email && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.email}</p>
        )}
      </div>

      {/* Password */}
      <div>
        <label className="block text-[12px] text-[#62666D] mb-1.5">
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
            className={inputClass("password")}
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8] hover:text-[#62666D]"
            style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
          >
            {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>

        {/* Strength meter */}
        {password && (
          <div className="mt-2">
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] text-[#A1A3A8]">{t.strength}</span>
              <span className="text-[10px] text-[#62666D] font-medium">
                {strengthLabels[strength]}
              </span>
            </div>
            <div className="h-1 bg-[#F5F5F5] rounded-full overflow-hidden">
              <div
                className={`h-full transition-all ${strengthColors[strength]}`}
                style={{ width: strengthWidth[strength] }}
              />
            </div>
          </div>
        )}
        {errors.password && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.password}</p>
        )}
      </div>

      {/* Confirm */}
      <div>
        <label className="block text-[12px] text-[#62666D] mb-1.5">
          {t.confirm}
        </label>
        <div className="relative">
          <input
            type={showPassword ? "text" : "password"}
            value={confirm}
            onChange={(e) => {
              setConfirm(e.target.value);
              setErrors((p) => ({ ...p, confirm: undefined }));
            }}
            placeholder="••••••••"
            dir="ltr"
            className={inputClass("confirm")}
          />
          {confirm && confirm === password && (
            <Check
              size={16}
              className="absolute top-1/2 -translate-y-1/2 text-[#22C55E]"
              style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
            />
          )}
        </div>
        {errors.confirm && (
          <p className="text-[11px] text-[#EF4444] mt-1">{errors.confirm}</p>
        )}
      </div>

      {/* Terms */}
      <label className="flex items-start gap-2 cursor-pointer select-none text-[12px] text-[#62666D]">
        <input
          type="checkbox"
          checked={terms}
          onChange={(e) => {
            setTerms(e.target.checked);
            setErrors((p) => ({ ...p, terms: undefined }));
          }}
          className="w-4 h-4 mt-0.5 accent-[#EF4056] shrink-0"
        />
        <span>
          {t.terms}{" "}
          <Link
            href={`/${locale}/terms`}
            className="text-[#00BFFF] hover:underline"
          >
            ({isFa ? "مشاهده" : "view"})
          </Link>
        </span>
      </label>
      {errors.terms && (
        <p className="text-[11px] text-[#EF4444] -mt-2">{errors.terms}</p>
      )}

      {/* Submit */}
      <button
        type="submit"
        disabled={submitting}
        className="w-full h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors disabled:opacity-60 flex items-center justify-center gap-2"
      >
        {submitting ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            {t.registering}
          </>
        ) : (
          t.register
        )}
      </button>

      {/* Login link */}
      <div className="text-center text-[12px] text-[#62666D] pt-3 border-t border-[#E0E0E2]">
        {t.haveAccount}{" "}
        <Link
          href={`/${locale}/auth/login`}
          className="text-[#EF4056] font-medium hover:underline"
        >
          {t.login}
        </Link>
      </div>
    </form>
  );
}
"""))

# ============================================================
# components/auth/ForgotPasswordForm.tsx
# ============================================================
files.append(("components/auth/ForgotPasswordForm.tsx", """"use client";

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
"""))

# ============================================================
# components/auth/index.ts
# ============================================================
files.append(("components/auth/index.ts", """// components/auth/index.ts
export { default as AuthCard } from "./AuthCard";
export { default as LoginForm } from "./LoginForm";
export { default as RegisterForm } from "./RegisterForm";
export { default as ForgotPasswordForm } from "./ForgotPasswordForm";
"""))

# ============================================================
# app/[locale]/auth/layout.tsx (shared auth layout)
# ============================================================
files.append(("app/[locale]/auth/layout.tsx", """export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
"""))

# ============================================================
# app/[locale]/auth/login/page.tsx
# ============================================================
files.append(("app/[locale]/auth/login/page.tsx", """import type { Locale } from "@/lib/types";
import { AuthCard, LoginForm } from "@/components/auth";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function LoginPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AuthCard
      locale={typedLocale}
      titleFa="ورود به حساب کاربری"
      titleEn="Sign in to your account"
      subtitleFa="برای دسترسی به حساب کاربری، شماره موبایل و رمز عبور خود را وارد کنید."
      subtitleEn="Enter your mobile number and password to access your account."
    >
      <LoginForm locale={typedLocale} />
    </AuthCard>
  );
}
"""))

# ============================================================
# app/[locale]/auth/register/page.tsx
# ============================================================
files.append(("app/[locale]/auth/register/page.tsx", """import type { Locale } from "@/lib/types";
import { AuthCard, RegisterForm } from "@/components/auth";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function RegisterPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AuthCard
      locale={typedLocale}
      titleFa="ایجاد حساب کاربری"
      titleEn="Create your account"
      subtitleFa="برای ثبت‌نام، فرم زیر را تکمیل کنید."
      subtitleEn="Fill in the form below to create your account."
    >
      <RegisterForm locale={typedLocale} />
    </AuthCard>
  );
}
"""))

# ============================================================
# app/[locale]/auth/forgot-password/page.tsx
# ============================================================
files.append(("app/[locale]/auth/forgot-password/page.tsx", """import type { Locale } from "@/lib/types";
import { AuthCard, ForgotPasswordForm } from "@/components/auth";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ForgotPasswordPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AuthCard
      locale={typedLocale}
      titleFa="بازیابی رمز عبور"
      titleEn="Reset your password"
      subtitleFa="شماره موبایل خود را وارد کنید تا کد بازیابی برای شما ارسال شود."
      subtitleEn="Enter your mobile number to receive a reset code."
    >
      <ForgotPasswordForm locale={typedLocale} />
    </AuthCard>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 13: Auth")
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
        print("Now run: npm run dev")
        print("Test:")
        print("  Login:    http://localhost:3000/fa/auth/login")
        print("  Register: http://localhost:3000/fa/auth/register")
        print("  Forgot:   http://localhost:3000/fa/auth/forgot-password")
        print("\nNext: run 14_account.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()