"use client";

import { useState } from "react";
import { Mail, Send, CheckCircle2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { isValidEmail } from "@/lib/utils";

interface NewsletterProps {
  locale: Locale;
}

export default function Newsletter({ locale }: NewsletterProps) {
  const isFa = locale === "fa";
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const t = {
    title: isFa ? "عضویت در خبرنامه" : "Join Our Newsletter",
    subtitle: isFa
      ? "از تخفیف‌های ویژه و محصولات جدید باخبر شوید"
      : "Get notified about special offers and new arrivals",
    placeholder: isFa ? "ایمیل خود را وارد کنید" : "Enter your email",
    submit: isFa ? "عضویت" : "Subscribe",
    success: isFa
      ? "با موفقیت عضو خبرنامه شدید!"
      : "You've successfully subscribed!",
    error: isFa ? "ایمیل نامعتبر است" : "Invalid email address",
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValidEmail(email)) {
      setStatus("error");
      return;
    }
    setStatus("success");
    setEmail("");
    setTimeout(() => setStatus("idle"), 3500);
  };

  return (
    <div
      className="rounded-xl overflow-hidden p-6 md:p-8"
      style={{
        background: "linear-gradient(135deg, #3F4064 0%, #2A2A3E 100%)",
      }}
    >
      <div className="flex flex-col md:flex-row items-center gap-6">
        <div className="flex-1 text-center md:text-start">
          <div className="w-12 h-12 rounded-full bg-white/10 flex items-center justify-center mb-3 mx-auto md:mx-0">
            <Mail size={22} className="text-white" />
          </div>
          <h2 className="text-[18px] md:text-[20px] font-bold text-white mb-2">
            {t.title}
          </h2>
          <p className="text-[12px] md:text-[13px] text-white/70">
            {t.subtitle}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex-1 w-full max-w-md">
          <div className="flex gap-2">
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setStatus("idle");
              }}
              placeholder={t.placeholder}
              dir="ltr"
              className="flex-1 h-12 px-4 rounded-lg bg-white/10 backdrop-blur border border-white/20 text-white placeholder:text-white/50 text-[13px] focus:outline-none focus:border-white/50 transition-colors"
            />
            <button
              type="submit"
              className="h-12 px-5 rounded-lg bg-[#EF4056] text-white font-bold text-[13px] hover:bg-[#d63850] transition-colors flex items-center gap-2 whitespace-nowrap"
            >
              <Send size={16} />
              {t.submit}
            </button>
          </div>

          {status === "success" && (
            <div className="flex items-center gap-2 mt-2 text-[#22C55E] text-[12px]">
              <CheckCircle2 size={14} />
              {t.success}
            </div>
          )}
          {status === "error" && (
            <div className="mt-2 text-[#EF4444] text-[12px]">{t.error}</div>
          )}
        </form>
      </div>
    </div>
  );
}
