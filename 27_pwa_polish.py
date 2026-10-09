# 27_pwa_polish.py
# PWA + میانبرهای کیبورد + بهینه‌سازی نهایی
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/settings.ts (user preferences)
# ============================================================
files.append(("lib/stores/settings.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsState {
  // Appearance
  reduceMotion: boolean;
  fontSize: "small" | "medium" | "large";
  // Notifications
  emailNotifications: boolean;
  pushNotifications: boolean;
  // Behavior
  autoPlayVideos: boolean;
  showPrices: boolean;
}

interface SettingsActions {
  setReduceMotion: (value: boolean) => void;
  setFontSize: (value: "small" | "medium" | "large") => void;
  setEmailNotifications: (value: boolean) => void;
  setPushNotifications: (value: boolean) => void;
  setAutoPlayVideos: (value: boolean) => void;
  setShowPrices: (value: boolean) => void;
  reset: () => void;
}

const DEFAULTS: SettingsState = {
  reduceMotion: false,
  fontSize: "medium",
  emailNotifications: true,
  pushNotifications: false,
  autoPlayVideos: false,
  showPrices: true,
};

export const useSettingsStore = create<SettingsState & SettingsActions>()(
  persist(
    (set) => ({
      ...DEFAULTS,
      setReduceMotion: (value) => set({ reduceMotion: value }),
      setFontSize: (value) => set({ fontSize: value }),
      setEmailNotifications: (value) => set({ emailNotifications: value }),
      setPushNotifications: (value) => set({ pushNotifications: value }),
      setAutoPlayVideos: (value) => set({ autoPlayVideos: value }),
      setShowPrices: (value) => set({ showPrices: value }),
      reset: () => set(DEFAULTS),
    }),
    { name: "sourcepixcel-settings" }
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
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
"""))

# ============================================================
# components/common/KeyboardShortcuts.tsx
# ============================================================
files.append(("components/common/KeyboardShortcuts.tsx", """"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Command, X, Keyboard } from "lucide-react";
import type { Locale } from "@/lib/types";

interface KeyboardShortcutsProps {
  locale: Locale;
}

interface Shortcut {
  keys: string[];
  labelFa: string;
  labelEn: string;
}

export default function KeyboardShortcuts({ locale }: KeyboardShortcutsProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const [showHelp, setShowHelp] = useState(false);

  const shortcuts: Shortcut[] = [
    {
      keys: ["Ctrl", "K"],
      labelFa: "جستجو",
      labelEn: "Search",
    },
    {
      keys: ["Ctrl", "H"],
      labelFa: "صفحه اصلی",
      labelEn: "Home",
    },
    {
      keys: ["Ctrl", "C"],
      labelFa: "سبد خرید",
      labelEn: "Cart",
    },
    {
      keys: ["Ctrl", "W"],
      labelFa: "علاقه‌مندی‌ها",
      labelEn: "Wishlist",
    },
    {
      keys: ["Ctrl", "A"],
      labelFa: "حساب کاربری",
      labelEn: "Account",
    },
    {
      keys: ["Ctrl", "P"],
      labelFa: "پنل ادمین",
      labelEn: "Admin Panel",
    },
    {
      keys: ["Shift", "?"],
      labelFa: "راهنمای میانبرها",
      labelEn: "Show this help",
    },
    {
      keys: ["Esc"],
      labelFa: "بستن پنجره‌ها",
      labelEn: "Close dialogs",
    },
  ];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInput =
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable;

      // Ctrl+K → focus search
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        const searchInput = document.querySelector<HTMLInputElement>(
          'input[type="text"][placeholder*="جستجو"], input[type="text"][placeholder*="Search"]'
        );
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        } else {
          router.push(`/${locale}/search`);
        }
        return;
      }

      // Ctrl+H → home
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "h") {
        e.preventDefault();
        router.push(`/${locale}`);
        return;
      }

      // Ctrl+C → cart (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "c") {
        // Don't prevent default if there's a text selection
        if (!window.getSelection()?.toString()) {
          e.preventDefault();
          router.push(`/${locale}/cart`);
        }
        return;
      }

      // Ctrl+W → wishlist (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "w") {
        e.preventDefault();
        router.push(`/${locale}/account/wishlist`);
        return;
      }

      // Ctrl+A → account (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "a") {
        e.preventDefault();
        router.push(`/${locale}/account`);
        return;
      }

      // Ctrl+P → admin panel (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "p") {
        e.preventDefault();
        router.push(`/${locale}/admin`);
        return;
      }

      // Shift+? → help
      if (e.shiftKey && e.key === "?") {
        if (!isInput) {
          e.preventDefault();
          setShowHelp((v) => !v);
        }
        return;
      }

      // Esc → close help
      if (e.key === "Escape" && showHelp) {
        setShowHelp(false);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [router, locale, showHelp]);

  if (!showHelp) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={() => setShowHelp(false)}
      />
      <div className="relative bg-white dark:bg-[#1A1A1E] rounded-2xl border border-[#E0E0E2] dark:border-[#2A2A2E] shadow-2xl w-full max-w-lg max-h-[85vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center">
              <Keyboard size={18} className="text-[#EF4056]" />
            </div>
            <div>
              <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {isFa ? "میانبرهای کیبورد" : "Keyboard Shortcuts"}
              </h2>
              <p className="text-[10px] text-[#A1A3A8]">
                {isFa
                  ? "برای جابجایی سریع‌تر در سایت"
                  : "Move faster around the site"}
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowHelp(false)}
            aria-label="Close"
            className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* List */}
        <div className="p-4 max-h-[60vh] overflow-y-auto">
          <div className="space-y-2">
            {shortcuts.map((sc, i) => (
              <div
                key={i}
                className="flex items-center justify-between gap-3 py-2.5 px-3 rounded-lg hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              >
                <span className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA]">
                  {isFa ? sc.labelFa : sc.labelEn}
                </span>
                <div className="flex items-center gap-1">
                  {sc.keys.map((key, j) => (
                    <span key={j}>
                      <kbd className="inline-flex items-center justify-center min-w-[28px] h-7 px-2 rounded-md bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[10px] font-mono font-bold text-[#3F4064] dark:text-[#E5E5EA] shadow-sm">
                        {key}
                      </kbd>
                      {j < sc.keys.length - 1 && (
                        <span className="text-[#A1A3A8] text-[10px] mx-1">
                          +
                        </span>
                      )}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E] bg-[#FAFAFA] dark:bg-[#0F0F12]">
          <div className="flex items-center justify-center gap-2 text-[10px] text-[#A1A3A8]">
            <Command size={12} />
            <span>
              {isFa
                ? "برای بستن این پنجره، Esc را بزنید"
                : "Press Esc to close this dialog"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/common/OfflineBanner.tsx
# ============================================================
files.append(("components/common/OfflineBanner.tsx", """"use client";

import { useEffect, useState } from "react";
import { WifiOff, Wifi } from "lucide-react";
import type { Locale } from "@/lib/types";

interface OfflineBannerProps {
  locale: Locale;
}

export default function OfflineBanner({ locale }: OfflineBannerProps) {
  const isFa = locale === "fa";
  const [isOnline, setIsOnline] = useState(true);
  const [showBack, setShowBack] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setIsOnline(navigator.onLine);

    const handleOnline = () => {
      setIsOnline(true);
      setShowBack(true);
      setTimeout(() => setShowBack(false), 3000);
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!mounted) return null;
  if (isOnline && !showBack) return null;

  if (isOnline && showBack) {
    return (
      <div className="fixed top-16 left-1/2 -translate-x-1/2 z-[80] bg-[#22C55E] text-white text-[12px] font-medium px-4 py-2 rounded-full shadow-lg flex items-center gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
        <Wifi size={14} />
        {isFa ? "اتصال اینترنت برقرار شد" : "You are back online"}
      </div>
    );
  }

  return (
    <div className="fixed top-16 left-1/2 -translate-x-1/2 z-[80] bg-[#EF4444] text-white text-[12px] font-medium px-4 py-2 rounded-full shadow-lg flex items-center gap-2">
      <WifiOff size={14} />
      {isFa
        ? "اتصال اینترنت قطع است"
        : "You are offline"}
    </div>
  );
}
"""))

# ============================================================
# components/common/index.ts (updated)
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
export { default as StaticPage } from "./StaticPage";
export { default as ThemeProvider } from "./ThemeProvider";
export { default as ThemeToggle } from "./ThemeToggle";
export { default as JsonLd } from "./JsonLd";
export { default as ToastContainer } from "./ToastContainer";
export { default as Skeleton } from "./Skeleton";
export { default as ProductCardSkeleton } from "./ProductCardSkeleton";
export { default as ErrorBoundary } from "./ErrorBoundary";
export { default as KeyboardShortcuts } from "./KeyboardShortcuts";
export { default as OfflineBanner } from "./OfflineBanner";
"""))

# ============================================================
# components/account/InvoiceView.tsx
# ============================================================
files.append(("components/account/InvoiceView.tsx", """"use client";

import Image from "next/image";
import { Printer, ArrowRight, ArrowLeft } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import type { MockOrder } from "@/lib/data";
import { products as allProducts } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface InvoiceViewProps {
  locale: Locale;
  order: MockOrder;
  onBack: () => void;
}

export default function InvoiceView({
  locale,
  order,
  onBack,
}: InvoiceViewProps) {
  const isFa = locale === "fa";

  const lines = order.items
    .map((item) => {
      const product = allProducts.find((p) => p.id === item.productId);
      return product ? { ...item, product } : null;
    })
    .filter((x): x is typeof x & { product: Product } => x !== null);

  const subtotal = lines.reduce(
    (s, l) => s + l.priceAtPurchase * l.quantity,
    0
  );
  const shipping = 45_000;

  const t = {
    invoice: isFa ? "فاکتور سفارش" : "Order Invoice",
    orderNumber: isFa ? "شماره سفارش" : "Order Number",
    date: isFa ? "تاریخ" : "Date",
    status: isFa ? "وضعیت" : "Status",
    shippingAddress: isFa ? "آدرس ارسال" : "Shipping Address",
    product: isFa ? "محصول" : "Product",
    quantity: isFa ? "تعداد" : "Qty",
    unitPrice: isFa ? "قیمت واحد" : "Unit Price",
    total: isFa ? "جمع" : "Total",
    subtotal: isFa ? "جمع کالاها" : "Subtotal",
    shippingCost: isFa ? "هزینه ارسال" : "Shipping",
    grandTotal: isFa ? "مبلغ نهایی" : "Grand Total",
    print: isFa ? "چاپ فاکتور" : "Print Invoice",
    back: isFa ? "بازگشت" : "Back",
    companyName: isFa ? "فروشگاه SourcePixcel" : "SourcePixcel Store",
    companyAddress: isFa
      ? "تهران، خیابان ولیعصر، پلاک ۱۲۳"
      : "Tehran, Valiasr St., No. 123",
    companyPhone: "021-12345678",
    companyEmail: "support@sourcepixcel.com",
    thankYou: isFa
      ? "از خرید شما سپاسگزاریم"
      : "Thank you for your purchase",
    terms: isFa
      ? "این فاکتور به عنوان رسید خرید معتبر است."
      : "This invoice is a valid purchase receipt.",
    statusLabels: {
      pending: isFa ? "در انتظار پرداخت" : "Pending",
      processing: isFa ? "در حال پردازش" : "Processing",
      shipped: isFa ? "ارسال شده" : "Shipped",
      delivered: isFa ? "تحویل داده شده" : "Delivered",
      cancelled: isFa ? "لغو شده" : "Cancelled",
    },
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <>
      {/* Action buttons (hidden in print) */}
      <div className="no-print flex items-center justify-between gap-3 mb-4 flex-wrap">
        <button
          onClick={onBack}
          className="h-10 px-4 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-2"
        >
          {isFa ? <ArrowRight size={16} /> : <ArrowLeft size={16} />}
          {t.back}
        </button>
        <button
          onClick={handlePrint}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Printer size={16} />
          {t.print}
        </button>
      </div>

      {/* Invoice */}
      <div className="print-content bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-6 md:p-8">
        {/* Header */}
        <div className="flex items-start justify-between gap-4 pb-6 border-b-2 border-[#EF4056] mb-6 flex-wrap">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 rounded-xl bg-[#EF4056] flex items-center justify-center text-white text-[22px] font-bold">
                S
              </div>
              <div>
                <div className="text-[18px] font-bold text-[#EF4056]">
                  SourcePixcel
                </div>
                <div className="text-[11px] text-[#A1A3A8]">
                  {t.companyAddress}
                </div>
              </div>
            </div>
            <div className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] space-y-1">
              <div>📞 {t.companyPhone}</div>
              <div>✉️ {t.companyEmail}</div>
            </div>
          </div>

          <div className="text-start">
            <div className="text-[22px] md:text-[26px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
              {t.invoice}
            </div>
            <div className="space-y-1.5 text-[12px]">
              <div className="flex items-center gap-2">
                <span className="text-[#A1A3A8]">{t.orderNumber}:</span>
                <span
                  className="font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums"
                  dir="ltr"
                >
                  {order.id}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[#A1A3A8]">{t.date}:</span>
                <span className="text-[#3F4064] dark:text-[#E5E5EA]">
                  {order.date}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[#A1A3A8]">{t.status}:</span>
                <span className="inline-block text-[10px] font-medium px-2 py-0.5 rounded-full bg-[#22C55E]/10 text-[#22C55E]">
                  {t.statusLabels[order.status]}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Shipping address */}
        <div className="mb-6">
          <h3 className="text-[12px] font-bold text-[#A1A3A8] uppercase mb-2">
            {t.shippingAddress}
          </h3>
          <p className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA] leading-6">
            {order.shippingAddress}
          </p>
        </div>

        {/* Items table */}
        <div className="overflow-x-auto mb-6">
          <table className="w-full">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[11px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-right p-3 font-medium">{t.product}</th>
                <th className="text-right p-3 font-medium w-20">{t.quantity}</th>
                <th className="text-right p-3 font-medium w-32">{t.unitPrice}</th>
                <th className="text-right p-3 font-medium w-32">{t.total}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {lines.map((line, idx) => (
                <tr key={idx}>
                  <td className="p-3">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0 no-print">
                        <Image
                          src={line.product.image}
                          alt={
                            isFa
                              ? line.product.titleFa
                              : line.product.titleEn
                          }
                          fill
                          sizes="48px"
                          className="object-cover"
                        />
                      </div>
                      <div>
                        <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
                          {isFa
                            ? line.product.titleFa
                            : line.product.titleEn}
                        </div>
                        <div
                          className="text-[10px] text-[#A1A3A8]"
                          dir="ltr"
                        >
                          SP-
                          {line.product.id.toString().padStart(5, "0")}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="p-3 text-[12px] text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {isFa
                      ? line.quantity.toLocaleString("fa-IR")
                      : line.quantity}
                  </td>
                  <td className="p-3 text-[12px] text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {formatPrice(line.priceAtPurchase, locale)}
                  </td>
                  <td className="p-3 text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {formatPrice(
                      line.priceAtPurchase * line.quantity,
                      locale
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Totals */}
        <div className="flex justify-end mb-6">
          <div className="w-full max-w-xs space-y-2 text-[12px]">
            <div className="flex items-center justify-between">
              <span className="text-[#62666D] dark:text-[#A1A3A8]">
                {t.subtotal}
              </span>
              <span className="text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                {formatPrice(subtotal, locale)}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#62666D] dark:text-[#A1A3A8]">
                {t.shippingCost}
              </span>
              <span className="text-[#22C55E] tabular-nums">
                {formatPrice(shipping, locale)}
              </span>
            </div>
            <div className="flex items-center justify-between pt-2 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.grandTotal}
              </span>
              <span className="text-[15px] font-bold text-[#EF4056] tabular-nums">
                {formatPrice(subtotal + shipping, locale)}{" "}
                <span className="text-[10px] text-[#A1A3A8] font-normal">
                  {isFa ? "تومان" : "T"}
                </span>
              </span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-6 border-t border-dashed border-[#E0E0E2] dark:border-[#2A2A2E]">
          <div className="text-center space-y-2">
            <div className="text-[14px] font-bold text-[#EF4056]">
              {t.thankYou}
            </div>
            <div className="text-[11px] text-[#A1A3A8]">{t.terms}</div>
            <div className="pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] text-[10px] text-[#A1A3A8]">
              {t.companyName} — {new Date().getFullYear()}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
"""))

# ============================================================
# components/account/OrderDetailView.tsx (updated with invoice toggle)
# ============================================================
files.append(("components/account/OrderDetailView.tsx", """"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  MapPin,
  Package,
  Truck,
  CheckCircle2,
  Receipt,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import type { MockOrder } from "@/lib/data";
import { products as allProducts } from "@/lib/data";
import { formatPrice } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";
import InvoiceView from "./InvoiceView";

interface OrderDetailViewProps {
  locale: Locale;
  order: MockOrder;
}

export default function OrderDetailView({
  locale,
  order,
}: OrderDetailViewProps) {
  const isFa = locale === "fa";
  const [showInvoice, setShowInvoice] = useState(false);

  const lines = order.items
    .map((item) => {
      const product = allProducts.find((p) => p.id === item.productId);
      return product ? { ...item, product } : null;
    })
    .filter((x): x is typeof x & { product: NonNullable<typeof x>["product"] } => x !== null);

  const steps = [
    { id: "pending", icon: Package, fa: "ثبت شده", en: "Placed" },
    { id: "processing", icon: Package, fa: "در حال پردازش", en: "Processing" },
    { id: "shipped", icon: Truck, fa: "ارسال شده", en: "Shipped" },
    { id: "delivered", icon: CheckCircle2, fa: "تحویل داده شده", en: "Delivered" },
  ];

  const statusIndex = steps.findIndex((s) => s.id === order.status);

  if (showInvoice) {
    return (
      <InvoiceView
        locale={locale}
        order={order}
        onBack={() => setShowInvoice(false)}
      />
    );
  }

  return (
    <div className="space-y-4">
      {/* Back + invoice button */}
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <Link
          href={`/${locale}/account/orders`}
          className="inline-flex items-center gap-2 text-[12px] text-[#00BFFF] hover:text-[#EF4056] transition-colors"
        >
          <ArrowRight
            size={14}
            className={isFa ? "" : "rotate-180"}
          />
          {isFa ? "بازگشت به سفارشات" : "Back to orders"}
        </Link>

        <button
          onClick={() => setShowInvoice(true)}
          className="h-9 px-4 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-2"
        >
          <Receipt size={14} />
          {isFa ? "مشاهده فاکتور" : "View Invoice"}
        </button>
      </div>

      {/* Header */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
          <div>
            <div className="text-[11px] text-[#A1A3A8] mb-1">
              {isFa ? "شماره سفارش" : "Order Number"}
            </div>
            <div className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
              {order.id}
            </div>
          </div>
          <OrderStatusBadge status={order.status} locale={locale} />
        </div>

        {/* Progress */}
        <div className="flex items-center justify-between max-w-2xl mx-auto mt-6">
          {steps.map((step, i) => {
            const Icon = step.icon;
            const done = i <= statusIndex;
            const active = i === statusIndex;
            return (
              <div key={step.id} className="flex items-center flex-1">
                <div className="flex flex-col items-center gap-2 shrink-0">
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${
                      done
                        ? active
                          ? "bg-[#EF4056] text-white"
                          : "bg-[#22C55E] text-white"
                        : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#A1A3A8]"
                    }`}
                  >
                    <Icon size={16} />
                  </div>
                  <span
                    className={`text-[10px] text-center whitespace-nowrap ${
                      done ? "text-[#3F4064] dark:text-[#E5E5EA] font-medium" : "text-[#A1A3A8]"
                    }`}
                  >
                    {isFa ? step.fa : step.en}
                  </span>
                </div>
                {i < steps.length - 1 && (
                  <div
                    className={`flex-1 h-[2px] mx-2 mb-6 ${
                      i < statusIndex ? "bg-[#22C55E]" : "bg-[#E0E0E2] dark:bg-[#2A2A2E]"
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Items */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
          {isFa ? "محصولات سفارش" : "Order Items"}
        </h3>
        <div className="space-y-3">
          {lines.map((line, i) => (
            <div
              key={i}
              className="flex items-center gap-3 pb-3 border-b border-[#F5F5F5] dark:border-[#2A2A2E] last:border-0 last:pb-0"
            >
              <Link
                href={`/${locale}/product/${line.product.slug}`}
                className="w-14 h-14 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0"
              >
                <Image
                  src={line.product.image}
                  alt={isFa ? line.product.titleFa : line.product.titleEn}
                  fill
                  sizes="56px"
                  className="object-cover"
                />
              </Link>
              <div className="flex-1 min-w-0">
                <Link
                  href={`/${locale}/product/${line.product.slug}`}
                  className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 hover:text-[#EF4056]"
                >
                  {isFa ? line.product.titleFa : line.product.titleEn}
                </Link>
                <div className="text-[11px] text-[#A1A3A8] mt-1">
                  {isFa
                    ? `${line.quantity.toLocaleString("fa-IR")} عدد`
                    : `${line.quantity} pcs`}
                </div>
              </div>
              <div className="text-left shrink-0">
                <div className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                  {formatPrice(line.priceAtPurchase * line.quantity, locale)}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] mt-4 pt-4 flex justify-between items-center">
          <span className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {isFa ? "مجموع" : "Total"}
          </span>
          <div className="flex items-center gap-1">
            <span className="text-[18px] font-bold text-[#EF4056]">
              {formatPrice(order.total, locale)}
            </span>
            <span className="text-[11px] text-[#62666D]">
              {isFa ? "تومان" : "Toman"}
            </span>
          </div>
        </div>
      </div>

      {/* Shipping */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
          <MapPin size={16} className="text-[#EF4056]" />
          {isFa ? "آدرس ارسال" : "Shipping Address"}
        </h3>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6">
          {order.shippingAddress}
        </p>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/globals.css (updated with print styles)
# ============================================================
files.append(("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  box-sizing: border-box;
}

html,
body {
  padding: 0;
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
  background: #F5F5F5;
  color: #3F4064;
  transition: background-color 0.2s ease, color 0.2s ease;
}

html.dark,
html.dark body {
  background: #0F0F12;
  color: #E5E5EA;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  cursor: pointer;
}

[dir="rtl"] {
  text-align: right;
}

[dir="ltr"] {
  text-align: left;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #F5F5F5;
}
html.dark ::-webkit-scrollbar-track {
  background: #1A1A1E;
}
::-webkit-scrollbar-thumb {
  background: #E0E0E2;
  border-radius: 4px;
}
html.dark ::-webkit-scrollbar-thumb {
  background: #3A3A40;
}
::-webkit-scrollbar-thumb:hover {
  background: #A1A3A8;
}
html.dark ::-webkit-scrollbar-thumb:hover {
  background: #52525A;
}

/* ─── Print styles ─────────────────────────────────────────── */
@media print {
  @page {
    margin: 1cm;
    size: A4;
  }

  body {
    background: white !important;
    color: black !important;
  }

  /* Hide everything except the invoice */
  body * {
    visibility: hidden;
  }

  .print-content,
  .print-content * {
    visibility: visible;
  }

  .print-content {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    background: white !important;
    border: none !important;
    padding: 20px !important;
  }

  /* Hide all UI elements inside print content */
  .no-print {
    display: none !important;
  }

  /* Force light colors */
  .print-content {
    color: black !important;
  }

  .print-content h1,
  .print-content h2,
  .print-content h3,
  .print-content h4,
  .print-content p,
  .print-content td,
  .print-content th,
  .print-content span,
  .print-content div {
    color: black !important;
  }

  /* Keep red for headers */
  .print-content .text-\\[\\#EF4056\\],
  .print-content [style*="color: rgb(239, 64, 86)"],
  .print-content [style*="#EF4056"] {
    color: #EF4056 !important;
  }

  /* Table styling */
  .print-content table {
    border-collapse: collapse;
    width: 100%;
  }

  .print-content th,
  .print-content td {
    border: 1px solid #ddd;
    padding: 8px;
  }

  .print-content thead {
    background: #f5f5f5 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Keep gradient */
  .print-content .bg-gradient-to-r {
    background: #EF4056 !important;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Prevent page breaks inside cards */
  .print-content > div {
    page-break-inside: avoid;
  }
}

/* ─── Animations ──────────────────────────────────────────── */
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slide-in-from-top-2 {
  from {
    transform: translateY(-8px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-in {
  animation: fade-in 0.2s ease-out;
}

.fade-in {
  animation: fade-in 0.2s ease-out;
}

.slide-in-from-top-2 {
  animation: slide-in-from-top-2 0.3s ease-out;
}

/* Reduce motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
"""))

# ============================================================
# next.config.js (performance optimized)
# ============================================================
files.append(("next.config.js", """/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: "https", hostname: "loremflickr.com", pathname: "/**" },
      { protocol: "https", hostname: "picsum.photos", pathname: "/**" },
      { protocol: "https", hostname: "images.unsplash.com", pathname: "/**" },
    ],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy:
      "default-src 'self'; script-src 'none'; sandbox;",
  },

  // Performance
  reactStrictMode: true,

  // Compression
  compress: true,

  // Production source maps
  productionBrowserSourceMaps: false,

  // Power header
  poweredByHeader: false,

  // Experimental optimizations
  experimental: {
    optimizePackageImports: ["lucide-react"],
  },

  // Webpack customizations
  webpack: (config, { isServer }) => {
    // Bundle analyzer (only when ANALYZE env is set)
    if (process.env.ANALYZE === "true") {
      const BundleAnalyzer = require("@next/bundle-analyzer");
      config.plugins.push(
        new BundleAnalyzer({
          enabled: true,
        })
      );
    }
    return config;
  },
};

module.exports = nextConfig;
"""))

# ============================================================
# app/[locale]/layout.tsx (updated with KeyboardShortcuts + OfflineBanner)
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BottomNav from "@/components/layout/BottomNav";
import ToastContainer from "@/components/common/ToastContainer";
import KeyboardShortcuts from "@/components/common/KeyboardShortcuts";
import OfflineBanner from "@/components/common/OfflineBanner";
import type { Locale } from "@/lib/types";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <div
      dir={locale === "fa" ? "rtl" : "ltr"}
      lang={locale}
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      <Header locale={typedLocale} />
      <main style={{ flex: 1 }} className="pb-16 lg:pb-0">
        {children}
      </main>
      <Footer locale={typedLocale} />
      <BottomNav locale={typedLocale} />
      <ToastContainer />
      <KeyboardShortcuts locale={typedLocale} />
      <OfflineBanner locale={typedLocale} />
    </div>
  );
}
"""))

# ============================================================
# components/layout/Footer.tsx (add keyboard hint)
# ============================================================
files.append(("components/layout/Footer.tsx", """import Link from "next/link";
import {
  Instagram, Twitter, Linkedin, Youtube,
  Phone, Mail, MapPin, ShieldCheck, Truck,
  RotateCcw, Headphones, Award, Keyboard,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface FooterProps {
  locale: Locale;
}

export default function Footer({ locale }: FooterProps) {
  const isFa = locale === "fa";

  const t = {
    aboutTitle: isFa ? "درباره SourcePixcel" : "About SourcePixcel",
    aboutText: isFa
      ? "SourcePixcel یک فروشگاه اینترنتی مدرن است که با هدف ارائه بهترین تجربه خرید آنلاین برای کاربران ایرانی طراحی شده است."
      : "SourcePixcel is a modern online store designed to provide the best online shopping experience for Iranian users.",
    customerService: isFa ? "خدمات مشتریان" : "Customer Service",
    quickLinks: isFa ? "دسترسی سریع" : "Quick Links",
    followUs: isFa ? "با ما همراه باشید" : "Follow Us",
    contact: isFa ? "تماس با ما" : "Contact Us",
    faq: isFa ? "سوالات متداول" : "FAQ",
    returns: isFa ? "رویه بازگرداندن کالا" : "Return Policy",
    shipping: isFa ? "شرایط ارسال" : "Shipping Info",
    privacy: isFa ? "حریم خصوصی" : "Privacy Policy",
    terms: isFa ? "شرایط استفاده" : "Terms of Use",
    about: isFa ? "درباره ما" : "About Us",
    contactLink: isFa ? "تماس با ما" : "Contact Us",
    blog: isFa ? "وبلاگ" : "Blog",
    careers: isFa ? "فرصت‌های شغلی" : "Careers",
    freeShipping: isFa ? "ارسال سریع" : "Fast Shipping",
    securePayment: isFa ? "پرداخت امن" : "Secure Payment",
    returnGuarantee: isFa ? "۷ روز ضمانت بازگشت" : "7-Day Return",
    support: isFa ? "پشتیبانی ۲۴/۷" : "24/7 Support",
    authentic: isFa ? "ضمانت اصالت کالا" : "Authentic Products",
    copyright: isFa
      ? "تمامی حقوق مادی و معنوی این سایت متعلق به SourcePixcel می‌باشد."
      : "All rights reserved by SourcePixcel.",
    shortcuts: isFa
      ? "میانبرهای کیبورد: Shift + ?"
      : "Keyboard shortcuts: Shift + ?",
  };

  const serviceBadges = [
    { icon: Truck, label: t.freeShipping },
    { icon: ShieldCheck, label: t.securePayment },
    { icon: RotateCcw, label: t.returnGuarantee },
    { icon: Headphones, label: t.support },
    { icon: Award, label: t.authentic },
  ];

  const customerServiceLinks = [
    { href: `/${locale}/faq`, label: t.faq },
    { href: `/${locale}/faq`, label: t.returns },
    { href: `/${locale}/faq`, label: t.shipping },
    { href: `/${locale}/contact`, label: t.contactLink },
  ];

  const quickLinks = [
    { href: `/${locale}/about`, label: t.about },
    { href: `/${locale}/contact`, label: t.contactLink },
    { href: `/${locale}/blog`, label: t.blog },
    { href: `/${locale}/about`, label: t.careers },
  ];

  const legalLinks = [
    { href: `/${locale}/privacy`, label: t.privacy },
    { href: `/${locale}/terms`, label: t.terms },
  ];

  const socialLinks = [
    { icon: Instagram, href: "https://instagram.com", label: "Instagram" },
    { icon: Twitter, href: "https://twitter.com", label: "Twitter" },
    { icon: Linkedin, href: "https://linkedin.com", label: "LinkedIn" },
    { icon: Youtube, href: "https://youtube.com", label: "YouTube" },
  ];

  return (
    <footer className="bg-white dark:bg-[#1A1A1E] border-t border-[#E0E0E2] dark:border-[#2A2A2E] mt-12">
      {/* Service badges */}
      <div className="border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 py-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {serviceBadges.map((badge, i) => {
              const Icon = badge.icon;
              return (
                <div key={i} className="flex flex-col items-center gap-2 text-center">
                  <div className="w-12 h-12 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center">
                    <Icon size={22} className="text-[#62666D] dark:text-[#A1A3A8]" />
                  </div>
                  <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    {badge.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Columns */}
      <div className="max-w-[1400px] mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.aboutTitle}
            </h3>
            <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6">
              {t.aboutText}
            </p>
          </div>

          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.customerService}
            </h3>
            <ul className="space-y-2">
              {customerServiceLinks.map((link, i) => (
                <li key={i}>
                  <Link
                    href={link.href}
                    className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.quickLinks}
            </h3>
            <ul className="space-y-2">
              {quickLinks.map((link, i) => (
                <li key={i}>
                  <Link
                    href={link.href}
                    className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {t.contact}
            </h3>
            <ul className="space-y-3 mb-6">
              <li className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                <Phone size={14} className="text-[#A1A3A8] shrink-0" />
                <span dir="ltr">021-12345678</span>
              </li>
              <li className="flex items-center gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                <Mail size={14} className="text-[#A1A3A8] shrink-0" />
                <span dir="ltr">support@sourcepixcel.com</span>
              </li>
              <li className="flex items-start gap-2 text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                <MapPin size={14} className="text-[#A1A3A8] shrink-0 mt-0.5" />
                <span>
                  {isFa ? "تهران، خیابان ولیعصر، پلاک ۱۲۳" : "Tehran, Valiasr St., No. 123"}
                </span>
              </li>
            </ul>

            <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
              {t.followUs}
            </h3>
            <div className="flex items-center gap-3">
              {socialLinks.map((social, i) => {
                const Icon = social.icon;
                return (
                  <a
                    key={i}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={social.label}
                    className="w-9 h-9 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#EF4056] hover:text-white transition-colors"
                  >
                    <Icon size={16} />
                  </a>
                );
              })}
            </div>
          </div>
        </div>

        {/* Keyboard hint */}
        <div className="mt-8 pt-6 border-t border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center gap-2 text-[11px] text-[#A1A3A8]">
          <Keyboard size={14} />
          <span>{t.shortcuts}</span>
        </div>
      </div>

      {/* Trust badges + Legal */}
      <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4 flex-wrap justify-center">
              <div className="w-16 h-16 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "نماد اعتماد" : "Trust Seal"}
              </div>
              <div className="w-16 h-16 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "ساماندهی" : "Regulated"}
              </div>
              <div className="w-16 h-16 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "اتحادیه" : "Union"}
              </div>
            </div>

            <div className="flex items-center gap-4 flex-wrap justify-center">
              {legalLinks.map((link, i) => (
                <Link
                  key={i}
                  href={link.href}
                  className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Copyright */}
      <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] bg-[#F5F5F5] dark:bg-[#0F0F12]">
        <div className="max-w-[1400px] mx-auto px-4 py-4 text-center">
          <p className="text-[12px] text-[#A1A3A8]">
            © {new Date().getFullYear()} SourcePixcel — {t.copyright}
          </p>
        </div>
      </div>
    </footer>
  );
}
"""))

# ============================================================
# README.md (final)
# ============================================================
files.append(("README.md", """# SourcePixcel

Bilingual (Persian / English) e-commerce frontend built with Next.js 15.

## Stack

- Next.js 15.5.9 (App Router)
- React 19.2.0
- TypeScript 5
- Tailwind CSS 3.4
- Zustand 5 (state management)
- lucide-react (icons)

## Features

- Bilingual support (Persian RTL / English LTR)
- 68 mock products, 12 categories, 30 brands
- Product listing with filters + sort + pagination
- Product detail with gallery, tabs, reviews
- Cart with localStorage persistence
- Multi-step checkout + **simulated Zarinpal payment gateway**
- Auth pages (login, register, forgot password)
- User dashboard (orders, wishlist, addresses, profile)
- Product comparison (up to 4 products)
- Blog with list + detail
- Search with live autocomplete
- Dark mode with localStorage
- Toast notifications
- Skeleton loaders
- Error boundaries
- **Admin panel** (dashboard, products, orders)
- **Notification system** with badge
- **Bottom navigation** (mobile)
- **Keyboard shortcuts** (Ctrl+K, Ctrl+H, Ctrl+C, Shift+?)
- **Offline detection banner**
- **Invoice printing** for orders
- SEO: sitemap, robots, JSON-LD, Open Graph
- PWA manifest

## Installation

    npm install --registry=https://mirror-npm.runflare.com

## Development

    npm run dev

## Build

    npm run build
    npm start

## Test Credentials

### User
- Any valid Iranian mobile (`09XXXXXXXXX`)
- Any password with 6+ characters

### Admin Panel
- URL: `/{locale}/admin/login`
- Username: `admin`
- Password: `admin123`

### Coupon
- Code: `SOURCE10` (10% off)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + K | Focus search |
| Ctrl + H | Go home |
| Ctrl + C | Cart |
| Ctrl + W | Wishlist |
| Ctrl + A | Account |
| Ctrl + P | Admin panel |
| Shift + ? | Show help |
| Esc | Close dialogs |

## URLs

### Persian
- Home: /fa
- Categories: /fa/categories
- Cart: /fa/cart
- Checkout: /fa/checkout
- Login: /fa/auth/login
- Account: /fa/account
- Compare: /fa/compare
- Blog: /fa/blog
- Search: /fa/search
- Admin: /fa/admin

### English
Replace `/fa/` with `/en/`.

## SEO URLs

- Sitemap: /sitemap.xml
- Robots: /robots.txt
- Manifest: /manifest.webmanifest

## Project Structure

    app/
      [locale]/
        admin/         Admin panel
        account/       User dashboard
        auth/          Login, Register
        blog/          Blog
        cart/          Cart
        checkout/      Checkout + Payment
        compare/       Compare
        product/       Product detail
        search/        Search
        ... (about, contact, faq, terms, privacy)
    components/
      admin/           Admin panel components
      account/         User dashboard + Invoice
      auth/            Auth forms
      blog/            Blog components
      cart/            Cart components
      checkout/        Checkout components
      common/          Shared (Breadcrumb, Skeleton, Toast, etc.)
      compare/         Compare components
      home/            Home page sections
      layout/          Header, Footer, BottomNav
      notifications/   Notification bell
      payment/         Zarinpal gateway + callback
      product/         Product components
      search/          Search + autocomplete
    lib/
      data/            Mock data
      stores/          Zustand stores
      types/           TypeScript types
      utils/           Helpers

## License

Demo project. All rights reserved.
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 27: PWA + Polish")
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
        print("  1) Press Shift+? to see keyboard shortcuts")
        print("  2) Press Ctrl+K to focus search")
        print("  3) Go to /fa/account/orders/{id} → View Invoice → Print")
        print("  4) Disconnect internet → see offline banner")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()