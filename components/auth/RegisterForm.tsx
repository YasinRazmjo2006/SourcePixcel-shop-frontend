"use client";

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
