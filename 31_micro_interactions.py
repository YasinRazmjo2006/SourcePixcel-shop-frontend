# 31_micro_interactions.py
# Micro-interactions: ripple, checkbox, spinner, input focus, toast
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# FIX: ProductGallery.tsx — باگ isFa
# ============================================================
files.append(("components/product/ProductGallery.tsx", """"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, ZoomIn } from "lucide-react";
import { SmartImage } from "@/components/common";

interface ProductGalleryProps {
  images: string[];
  alt: string;
  category?: string;
}

export default function ProductGallery({
  images,
  alt,
  category,
}: ProductGalleryProps) {
  const [active, setActive] = useState(0);

  const next = () => setActive((p) => (p + 1) % images.length);
  const prev = () => setActive((p) => (p - 1 + images.length) % images.length);

  return (
    <div className="flex flex-col-reverse md:flex-row gap-3">
      {/* Thumbnails */}
      <div className="flex md:flex-col gap-2 overflow-x-auto md:overflow-visible pb-1 md:pb-0">
        {images.map((img, i) => (
          <motion.button
            key={i}
            onClick={() => setActive(i)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`w-14 h-14 md:w-16 md:h-16 shrink-0 rounded-lg border-2 overflow-hidden transition-colors relative ${
              i === active
                ? "border-[#EF4056]"
                : "border-[#E0E0E2] dark:border-[#2A2A2E] hover:border-[#A1A3A8]"
            }`}
            aria-label={`Image ${i + 1}`}
          >
            <SmartImage
              src={img}
              alt={`${alt} thumbnail ${i + 1}`}
              fill
              sizes="64px"
              className="object-cover"
              category={category}
            />
          </motion.button>
        ))}
      </div>

      {/* Main image */}
      <div className="flex-1 relative group">
        <div className="aspect-square bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={active}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
              className="absolute inset-0"
            >
              <SmartImage
                src={images[active]}
                alt={alt}
                fill
                sizes="(max-width: 768px) 100vw, 50vw"
                className="object-contain p-4"
                priority
                category={category}
              />
            </motion.div>
          </AnimatePresence>
        </div>

        {images.length > 1 && (
          <>
            <motion.button
              onClick={prev}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              aria-label="Previous image"
              className="absolute top-1/2 -translate-y-1/2 right-2 w-9 h-9 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronRight size={18} />
            </motion.button>
            <motion.button
              onClick={next}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              aria-label="Next image"
              className="absolute top-1/2 -translate-y-1/2 left-2 w-9 h-9 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronLeft size={18} />
            </motion.button>
          </>
        )}

        {/* Zoom hint */}
        <div
          className="absolute top-3 opacity-0 group-hover:opacity-100 transition-opacity"
          style={{ left: 12 }}
        >
          <div className="w-8 h-8 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#62666D] shadow-md">
            <ZoomIn size={14} />
          </div>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/ui/RippleButton.tsx — دکمه با افکت ripple
# ============================================================
files.append(("components/ui/RippleButton.tsx", """"use client";

import { useState, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface Ripple {
  id: number;
  x: number;
  y: number;
  size: number;
}

interface RippleButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "success" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
  rippleColor?: string;
}

export default function RippleButton({
  children,
  variant = "primary",
  size = "md",
  fullWidth = false,
  rippleColor,
  className,
  onClick,
  disabled,
  ...props
}: RippleButtonProps) {
  const [ripples, setRipples] = useState<Ripple[]>([]);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleClick = useCallback(
    (e: React.MouseEvent<HTMLButtonElement>) => {
      if (disabled) return;

      const button = buttonRef.current;
      if (button) {
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height) * 2;
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        const id = Date.now();
        setRipples((prev) => [...prev, { id, x, y, size }]);

        setTimeout(() => {
          setRipples((prev) => prev.filter((r) => r.id !== id));
        }, 600);
      }

      onClick?.(e);
    },
    [disabled, onClick]
  );

  const variantClasses = {
    primary: "bg-[#EF4056] text-white hover:bg-[#d63850]",
    secondary:
      "bg-[#00BFFF] text-white hover:bg-[#0099cc]",
    success: "bg-[#22C55E] text-white hover:bg-[#1da34d]",
    danger: "bg-[#EF4444] text-white hover:bg-[#d63030]",
    ghost:
      "bg-transparent text-[#3F4064] dark:text-[#E5E5EA] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]",
  };

  const sizeClasses = {
    sm: "h-9 px-4 text-[12px]",
    md: "h-11 px-6 text-[13px]",
    lg: "h-12 px-8 text-[14px]",
  };

  const defaultRippleColor = rippleColor ?? "rgba(255, 255, 255, 0.5)";

  return (
    <motion.button
      ref={buttonRef}
      onClick={handleClick}
      disabled={disabled}
      whileHover={!disabled ? { scale: 1.02 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
      className={`relative overflow-hidden rounded-lg font-bold transition-colors flex items-center justify-center gap-2 ${
        variantClasses[variant]
      } ${sizeClasses[size]} ${fullWidth ? "w-full" : ""} ${
        disabled ? "opacity-40 cursor-not-allowed" : ""
      } ${className ?? ""}`}
      {...props}
    >
      <AnimatePresence>
        {ripples.map((ripple) => (
          <motion.span
            key={ripple.id}
            initial={{ scale: 0, opacity: 1 }}
            animate={{ scale: 1, opacity: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="absolute rounded-full pointer-events-none"
            style={{
              left: ripple.x,
              top: ripple.y,
              width: ripple.size,
              height: ripple.size,
              backgroundColor: defaultRippleColor,
            }}
          />
        ))}
      </AnimatePresence>

      <span className="relative z-10 flex items-center gap-2">{children}</span>
    </motion.button>
  );
}
"""))

# ============================================================
# components/ui/AnimatedCheckbox.tsx
# ============================================================
files.append(("components/ui/AnimatedCheckbox.tsx", """"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

interface AnimatedCheckboxProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  label?: string;
  disabled?: boolean;
}

export default function AnimatedCheckbox({
  checked,
  onChange,
  label,
  disabled = false,
}: AnimatedCheckboxProps) {
  return (
    <label
      className={`flex items-center gap-2.5 cursor-pointer select-none group ${
        disabled ? "opacity-50 cursor-not-allowed" : ""
      }`}
    >
      <motion.div
        onClick={() => !disabled && onChange(!checked)}
        whileHover={!disabled ? { scale: 1.08 } : {}}
        whileTap={!disabled ? { scale: 0.92 } : {}}
        className={`w-5 h-5 rounded-md border-2 flex items-center justify-center transition-colors shrink-0 ${
          checked
            ? "bg-[#EF4056] border-[#EF4056]"
            : "bg-white dark:bg-[#1A1A1E] border-[#E0E0E2] dark:border-[#3A3A40] group-hover:border-[#EF4056]"
        }`}
      >
        <motion.div
          initial={false}
          animate={
            checked
              ? { scale: 1, opacity: 1 }
              : { scale: 0, opacity: 0 }
          }
          transition={{
            type: "spring",
            stiffness: 500,
            damping: 30,
          }}
        >
          <Check size={12} className="text-white" strokeWidth={3.5} />
        </motion.div>
      </motion.div>

      {label && (
        <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] group-hover:text-[#3F4064] dark:group-hover:text-[#E5E5EA] transition-colors">
          {label}
        </span>
      )}
    </label>
  );
}
"""))

# ============================================================
# components/ui/AnimatedInput.tsx
# ============================================================
files.append(("components/ui/AnimatedInput.tsx", """"use client";

import { forwardRef, useState, type InputHTMLAttributes } from "react";
import { motion } from "framer-motion";

interface AnimatedInputProps
  extends Omit<InputHTMLAttributes<HTMLInputElement>, "onChange"> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
  value: string;
  onChange: (value: string) => void;
}

const AnimatedInput = forwardRef<HTMLInputElement, AnimatedInputProps>(
  (
    { label, error, icon, value, onChange, className, ...props },
    ref
  ) => {
    const [isFocused, setIsFocused] = useState(false);

    return (
      <div className="w-full">
        {label && (
          <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {label}
          </label>
        )}

        <div className="relative">
          <input
            ref={ref}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            className={`w-full h-11 px-3 ${
              icon ? "pr-10" : ""
            } rounded-lg bg-white dark:bg-[#1A1A1E] border text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
              error
                ? "border-[#EF4444] focus:border-[#EF4444]"
                : "border-[#E0E0E2] dark:border-[#2A2A2E]"
            } ${className ?? ""}`}
            {...props}
          />

          {icon && (
            <div
              className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8] pointer-events-none"
              style={{ right: 12 }}
            >
              {icon}
            </div>
          )}

          {/* Animated underline */}
          <motion.div
            initial={false}
            animate={{
              scaleX: isFocused && !error ? 1 : 0,
              opacity: isFocused && !error ? 1 : 0,
            }}
            transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="absolute bottom-0 left-2 right-2 h-[2px] bg-[#EF4056] rounded-full origin-center"
          />
        </div>

        {error && (
          <motion.p
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-[11px] text-[#EF4444] mt-1"
          >
            {error}
          </motion.p>
        )}
      </div>
    );
  }
);

AnimatedInput.displayName = "AnimatedInput";

export default AnimatedInput;
"""))

# ============================================================
# components/ui/Spinner.tsx — لودینگ اسپینر
# ============================================================
files.append(("components/ui/Spinner.tsx", """"use client";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: string;
}

export default function Spinner({
  size = "md",
  color = "#EF4056",
}: SpinnerProps) {
  const sizes = {
    sm: 16,
    md: 24,
    lg: 40,
  };

  const px = sizes[size];

  return (
    <div
      className="relative inline-block"
      style={{ width: px, height: px }}
      role="status"
      aria-label="Loading"
    >
      <div
        className="absolute inset-0 rounded-full border-2 opacity-20"
        style={{ borderColor: color }}
      />
      <div
        className="absolute inset-0 rounded-full border-2 border-transparent animate-spin"
        style={{
          borderTopColor: color,
          animationDuration: "0.7s",
        }}
      />
    </div>
  );
}
"""))

# ============================================================
# components/ui/DotsLoader.tsx
# ============================================================
files.append(("components/ui/DotsLoader.tsx", """"use client";

interface DotsLoaderProps {
  color?: string;
  size?: number;
}

export default function DotsLoader({
  color = "#EF4056",
  size = 8,
}: DotsLoaderProps) {
  return (
    <div className="flex items-center gap-1.5" role="status" aria-label="Loading">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="rounded-full animate-bounce"
          style={{
            width: size,
            height: size,
            backgroundColor: color,
            animationDelay: `${i * 0.15}s`,
            animationDuration: "0.6s",
          }}
        />
      ))}
    </div>
  );
}
"""))

# ============================================================
# components/ui/index.ts
# ============================================================
files.append(("components/ui/index.ts", """// components/ui/index.ts
export { default as RippleButton } from "./RippleButton";
export { default as AnimatedCheckbox } from "./AnimatedCheckbox";
export { default as AnimatedInput } from "./AnimatedInput";
export { default as Spinner } from "./Spinner";
export { default as DotsLoader } from "./DotsLoader";
"""))

# ============================================================
# components/common/ToastContainer.tsx (improved with animations)
# ============================================================
files.append(("components/common/ToastContainer.tsx", """"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle2,
  XCircle,
  Info,
  AlertTriangle,
  X,
} from "lucide-react";
import { useToastStore, type ToastType } from "@/lib/stores";

const ICONS = {
  success: CheckCircle2,
  error: XCircle,
  info: Info,
  warning: AlertTriangle,
};

const COLORS: Record<ToastType, string> = {
  success: "bg-[#22C55E] text-white",
  error: "bg-[#EF4444] text-white",
  info: "bg-[#00BFFF] text-white",
  warning: "bg-[#F59E0B] text-white",
};

const PROGRESS_COLORS: Record<ToastType, string> = {
  success: "bg-[#16A34A]",
  error: "bg-[#DC2626]",
  info: "bg-[#0284C7]",
  warning: "bg-[#D97706]",
};

export default function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);
  const remove = useToastStore((s) => s.remove);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[200] flex flex-col gap-2 pointer-events-none w-full max-w-sm px-4">
      <AnimatePresence mode="popLayout">
        {toasts.map((toast) => {
          const Icon = ICONS[toast.type];
          const duration = toast.duration ?? 3500;

          return (
            <motion.div
              key={toast.id}
              layout
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{
                type: "spring",
                stiffness: 400,
                damping: 30,
              }}
              className={`${COLORS[toast.type]} rounded-lg shadow-lg pointer-events-auto overflow-hidden`}
            >
              <div className="p-3 flex items-start gap-3">
                <motion.div
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{
                    delay: 0.1,
                    type: "spring",
                    stiffness: 500,
                    damping: 25,
                  }}
                >
                  <Icon size={18} className="shrink-0 mt-0.5" />
                </motion.div>

                <div className="flex-1 text-[13px]">
                  <div className="font-bold">{toast.titleFa}</div>
                  {toast.messageFa && (
                    <div className="text-[12px] opacity-90 mt-0.5 line-clamp-2">
                      {toast.messageFa}
                    </div>
                  )}
                </div>

                <motion.button
                  whileHover={{ scale: 1.15, rotate: 90 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => remove(toast.id)}
                  aria-label="Close"
                  className="shrink-0 opacity-70 hover:opacity-100 transition-opacity"
                >
                  <X size={16} />
                </motion.button>
              </div>

              {/* Progress bar */}
              {duration > 0 && (
                <motion.div
                  initial={{ scaleX: 1 }}
                  animate={{ scaleX: 0 }}
                  transition={{ duration: duration / 1000, ease: "linear" }}
                  className={`h-[3px] origin-left ${PROGRESS_COLORS[toast.type]}`}
                />
              )}
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
"""))

# ============================================================
# components/common/Skeleton.tsx (improved with shimmer)
# ============================================================
files.append(("components/common/Skeleton.tsx", """interface SkeletonProps {
  className?: string;
  variant?: "text" | "circle" | "rect";
  width?: string | number;
  height?: string | number;
}

export default function Skeleton({
  className = "",
  variant = "rect",
  width,
  height,
}: SkeletonProps) {
  const base =
    "bg-[#E0E0E2] dark:bg-[#2A2A2E] relative overflow-hidden skeleton-shimmer";
  const shape =
    variant === "circle"
      ? "rounded-full"
      : variant === "text"
      ? "rounded"
      : "rounded-lg";

  return (
    <div
      className={`${base} ${shape} ${className}`}
      style={{ width, height }}
    />
  );
}
"""))

# ============================================================
# components/product/QuantitySelector.tsx (updated)
# ============================================================
files.append(("components/product/QuantitySelector.tsx", """"use client";

import { motion } from "framer-motion";
import { Minus, Plus } from "lucide-react";
import type { Locale } from "@/lib/types";

interface QuantitySelectorProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  locale: Locale;
}

export default function QuantitySelector({
  value,
  onChange,
  min = 1,
  max = 10,
  locale,
}: QuantitySelectorProps) {
  const isFa = locale === "fa";

  const dec = () => onChange(Math.max(min, value - 1));
  const inc = () => onChange(Math.min(max, value + 1));

  return (
    <div className="flex items-center gap-3">
      <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
        {isFa ? "تعداد:" : "Quantity:"}
      </span>
      <div className="flex items-center gap-1 border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg overflow-hidden">
        <motion.button
          onClick={inc}
          disabled={value >= max}
          whileHover={value < max ? { scale: 1.1 } : {}}
          whileTap={value < max ? { scale: 0.9 } : {}}
          aria-label="Increase quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
        >
          <Plus size={16} />
        </motion.button>

        <div className="w-10 text-center relative overflow-hidden">
          <motion.span
            key={value}
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 10, opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums block"
          >
            {isFa ? value.toLocaleString("fa-IR") : value}
          </motion.span>
        </div>

        <motion.button
          onClick={dec}
          disabled={value <= min}
          whileHover={value > min ? { scale: 1.1 } : {}}
          whileTap={value > min ? { scale: 0.9 } : {}}
          aria-label="Decrease quantity"
          className="w-8 h-8 flex items-center justify-center text-[#EF4056] disabled:opacity-30 hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
        >
          <Minus size={16} />
        </motion.button>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/auth/LoginForm.tsx (updated with RippleButton)
# ============================================================
files.append(("components/auth/LoginForm.tsx", """"use client";

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
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 31: Micro-interactions")
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
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/auth/login")
        print("\nYou should see:")
        print("  ✓ Ripple effect on login button")
        print("  ✓ Animated checkbox")
        print("  ✓ Shimmer skeletons")
        print("  ✓ Toast with progress bar")
        print("  ✓ Quantity selector with animation")
        print("  ✓ Fixed ProductGallery bug")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()