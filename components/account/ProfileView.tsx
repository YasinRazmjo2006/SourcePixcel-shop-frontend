"use client";

import { useState } from "react";
import { Save, User, Mail, Smartphone, Lock, CheckCircle2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAuthStore } from "@/lib/stores";
import { isValidEmail, isValidIranianMobile } from "@/lib/utils";

interface ProfileViewProps {
  locale: Locale;
}

export default function ProfileView({ locale }: ProfileViewProps) {
  const isFa = locale === "fa";
  const user = useAuthStore((s) => s.user);
  const update = useAuthStore((s) => s.update);

  const [fullName, setFullName] = useState(user?.fullName ?? "");
  const [email, setEmail] = useState(user?.email ?? "");
  const [mobile, setMobile] = useState(user?.mobile ?? "");
  const [saved, setSaved] = useState(false);
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});

  const t = {
    title: isFa ? "پروفایل من" : "My Profile",
    fullName: isFa ? "نام و نام خانوادگی" : "Full Name",
    email: isFa ? "ایمیل" : "Email",
    mobile: isFa ? "شماره موبایل" : "Mobile Number",
    save: isFa ? "ذخیره تغییرات" : "Save Changes",
    saved: isFa ? "تغییرات ذخیره شد" : "Changes saved",
    required: isFa ? "الزامی" : "Required",
    emailInvalid: isFa ? "ایمیل نامعتبر است" : "Invalid email",
    mobileInvalid: isFa ? "شماره موبایل نامعتبر است" : "Invalid mobile number",
  };

  const handleSave = () => {
    const errs: Record<string, string | undefined> = {};
    if (!fullName.trim()) errs.fullName = t.required;
    if (email.trim() && !isValidEmail(email)) errs.email = t.emailInvalid;
    if (!mobile.trim()) errs.mobile = t.required;
    else if (!isValidIranianMobile(mobile)) errs.mobile = t.mobileInvalid;

    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    update({
      fullName: fullName.trim(),
      email: email.trim() || undefined,
      mobile: mobile.trim(),
    });
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  };

  const inputClass = (field: string) =>
    `w-full h-11 pr-10 pl-3 rounded-lg border text-[13px] text-[#3F4064] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] focus:border-[#EF4056]"
    }`;

  return (
    <div className="space-y-4">
      <h1 className="text-[18px] font-bold text-[#3F4064]">{t.title}</h1>

      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <div className="space-y-4">
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
                className={inputClass("fullName")}
              />
              <User
                size={16}
                className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
                style={{ [isFa ? "left" : "right"]: 12 } as React.CSSProperties}
              />
            </div>
            {errors.fullName && (
              <p className="text-[11px] text-[#EF4444] mt-1">
                {errors.fullName}
              </p>
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
        </div>

        <div className="border-t border-[#E0E0E2] mt-5 pt-5 flex items-center justify-between">
          {saved && (
            <div className="flex items-center gap-2 text-[12px] text-[#22C55E]">
              <CheckCircle2 size={16} />
              {t.saved}
            </div>
          )}
          <div className="flex-1" />
          <button
            onClick={handleSave}
            className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
          >
            <Save size={16} />
            {t.save}
          </button>
        </div>
      </div>

      {/* Change password */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <h2 className="text-[14px] font-bold text-[#3F4064] mb-3 flex items-center gap-2">
          <Lock size={16} className="text-[#EF4056]" />
          {isFa ? "تغییر رمز عبور" : "Change Password"}
        </h2>
        <p className="text-[12px] text-[#A1A3A8]">
          {isFa
            ? "برای تغییر رمز عبور، از طریق ایمیل یا پیامک اقدام کنید."
            : "To change your password, use email or SMS recovery."}
        </p>
      </div>
    </div>
  );
}
