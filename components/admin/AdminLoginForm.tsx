"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Lock, User, Loader2, ShieldCheck } from "lucide-react";
import { useAdminStore } from "@/lib/stores";

interface AdminLoginFormProps {
  locale: string;
}

export default function AdminLoginForm({ locale }: AdminLoginFormProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const login = useAdminStore((s) => s.login);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const t = {
    title: isFa ? "ورود به پنل مدیریت" : "Admin Panel Login",
    subtitle: isFa
      ? "برای دسترسی به پنل مدیریت، اطلاعات خود را وارد کنید."
      : "Enter your credentials to access the admin panel.",
    username: isFa ? "نام کاربری" : "Username",
    password: isFa ? "رمز عبور" : "Password",
    login: isFa ? "ورود" : "Login",
    loggingIn: isFa ? "در حال ورود..." : "Logging in...",
    hint: isFa
      ? "برای تست: admin / admin123"
      : "Test: admin / admin123",
    invalid: isFa
      ? "نام کاربری یا رمز عبور اشتباه است"
      : "Invalid username or password",
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (username !== "admin" || password !== "admin123") {
      setError(t.invalid);
      return;
    }

    setSubmitting(true);
    setTimeout(() => {
      login("Admin");
      router.push(`/${locale}/admin`);
    }, 700);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-[#0F0F12]">
      <div className="w-full max-w-md">
        <div className="bg-[#1A1A1E] rounded-2xl border border-[#2A2A2E] p-6 md:p-8">
          {/* Logo */}
          <div className="flex items-center justify-center gap-2 mb-6">
            <div className="w-12 h-12 rounded-xl bg-[#EF4056] flex items-center justify-center">
              <ShieldCheck size={24} className="text-white" />
            </div>
          </div>

          <h1 className="text-[18px] font-bold text-white text-center mb-2">
            {t.title}
          </h1>
          <p className="text-[12px] text-white/60 text-center mb-6 leading-6">
            {t.subtitle}
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username */}
            <div>
              <label className="block text-[12px] text-white/70 mb-1.5">
                {t.username}
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  dir="ltr"
                  placeholder="admin"
                  className="w-full h-11 pr-10 pl-3 rounded-lg bg-[#0F0F12] border border-[#2A2A2E] text-[13px] text-white placeholder:text-white/30 focus:outline-none focus:border-[#EF4056] transition-colors"
                />
                <User
                  size={16}
                  className="absolute top-1/2 -translate-y-1/2 text-white/30"
                  style={{ right: 12 }}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-[12px] text-white/70 mb-1.5">
                {t.password}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  dir="ltr"
                  placeholder="••••••••"
                  className="w-full h-11 pr-10 pl-3 rounded-lg bg-[#0F0F12] border border-[#2A2A2E] text-[13px] text-white placeholder:text-white/30 focus:outline-none focus:border-[#EF4056] transition-colors"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((v) => !v)}
                  className="absolute top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60"
                  style={{ right: 12 }}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="bg-[#EF4444]/10 border border-[#EF4444]/30 rounded-lg p-3 text-[12px] text-[#EF4444] text-center">
                {error}
              </div>
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
                  {t.loggingIn}
                </>
              ) : (
                <>
                  <Lock size={16} />
                  {t.login}
                </>
              )}
            </button>

            {/* Hint */}
            <div className="bg-white/5 border border-white/10 rounded-lg p-3 text-[11px] text-white/60 text-center">
              {t.hint}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
