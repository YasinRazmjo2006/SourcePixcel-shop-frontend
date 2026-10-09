# 25_notifications.py
# سیستم نوتیفیکیشن + Bottom Navigation موبایل
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/types/notification.ts
# ============================================================
files.append(("lib/types/notification.ts", """// lib/types/notification.ts
export type NotificationType = "order" | "promo" | "system" | "message";

export interface AppNotification {
  id: string;
  type: NotificationType;
  titleFa: string;
  titleEn: string;
  bodyFa: string;
  bodyEn: string;
  dateFa: string;
  dateEn: string;
  read: boolean;
  href?: string;
}
"""))

# ============================================================
# lib/types/index.ts (updated)
# ============================================================
files.append(("lib/types/index.ts", """// lib/types/index.ts
export type {
  Subcategory,
  Category,
  Brand,
  Product,
  CartItem,
  WishlistItem,
  CompareItem,
  FilterState,
  SortOption,
  Locale,
} from "./product";

export type { BlogPost } from "./blog";
export type { Review, ReviewDraft } from "./review";
export type { AppNotification, NotificationType } from "./notification";
"""))

# ============================================================
# lib/stores/notifications.ts
# ============================================================
files.append(("lib/stores/notifications.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AppNotification } from "@/lib/types";

const SEED: AppNotification[] = [
  {
    id: "notif-1",
    type: "order",
    titleFa: "سفارش شما ارسال شد",
    titleEn: "Your order has been shipped",
    bodyFa: "سفارش SP-20240002 با موفقیت ارسال شد. کد پیگیری: 123456789",
    bodyEn: "Order SP-20240002 has been shipped. Tracking: 123456789",
    dateFa: "۲ ساعت پیش",
    dateEn: "2 hours ago",
    read: false,
    href: "/account/orders",
  },
  {
    id: "notif-2",
    type: "promo",
    titleFa: "تخفیف ۴۰٪ روی موبایل‌ها",
    titleEn: "40% off on mobile phones",
    bodyFa: "جشنواره ویژه موبایل تا پایان هفته. با کد SOURCE10 تخفیف بیشتری بگیرید.",
    bodyEn: "Special mobile festival until the end of the week. Use code SOURCE10 for extra discount.",
    dateFa: "۵ ساعت پیش",
    dateEn: "5 hours ago",
    read: false,
    href: "/category/mobile",
  },
  {
    id: "notif-3",
    type: "message",
    titleFa: "پاسخ به نظر شما",
    titleEn: "Reply to your review",
    bodyFa: "تیم پشتیبانی به نظر شما درباره Samsung Galaxy S24 Ultra پاسخ داد.",
    bodyEn: "Support team replied to your review on Samsung Galaxy S24 Ultra.",
    dateFa: "دیروز",
    dateEn: "Yesterday",
    read: false,
  },
  {
    id: "notif-4",
    type: "system",
    titleFa: "به‌روزرسانی اپلیکیشن",
    titleEn: "App update available",
    bodyFa: "نسخه جدید SourcePixcel با امکانات بیشتر منتشر شد.",
    bodyEn: "New version of SourcePixcel is available with more features.",
    dateFa: "۲ روز پیش",
    dateEn: "2 days ago",
    read: true,
  },
  {
    id: "notif-5",
    type: "promo",
    titleFa: "پیشنهاد شگفت‌انگیز جدید",
    titleEn: "New amazing offer",
    bodyFa: "محصولات جدید با تخفیف تا ۳۰٪ به فروشگاه اضافه شدند.",
    bodyEn: "New products with up to 30% off have been added to the store.",
    dateFa: "۳ روز پیش",
    dateEn: "3 days ago",
    read: true,
    href: "/search?discount=1",
  },
];

interface NotificationsState {
  items: AppNotification[];
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  remove: (id: string) => void;
  clearAll: () => void;
  getUnreadCount: () => number;
  reset: () => void;
}

export const useNotificationsStore = create<NotificationsState>()(
  persist(
    (set, get) => ({
      items: SEED,

      markAsRead: (id) => {
        set((state) => ({
          items: state.items.map((n) =>
            n.id === id ? { ...n, read: true } : n
          ),
        }));
      },

      markAllAsRead: () => {
        set((state) => ({
          items: state.items.map((n) => ({ ...n, read: true })),
        }));
      },

      remove: (id) => {
        set((state) => ({
          items: state.items.filter((n) => n.id !== id),
        }));
      },

      clearAll: () => set({ items: [] }),

      getUnreadCount: () => get().items.filter((n) => !n.read).length,

      reset: () => set({ items: SEED }),
    }),
    { name: "sourcepixcel-notifications" }
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
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
"""))

# ============================================================
# components/notifications/NotificationBell.tsx
# ============================================================
files.append(("components/notifications/NotificationBell.tsx", """"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  Bell,
  Package,
  Tag,
  Info,
  MessageSquare,
  Check,
  Trash2,
  X,
} from "lucide-react";
import type { Locale, NotificationType } from "@/lib/types";
import { useNotificationsStore } from "@/lib/stores";

interface NotificationBellProps {
  locale: Locale;
  variant?: "top" | "header";
}

const TYPE_ICONS: Record<NotificationType, React.ComponentType<{ size?: number }>> = {
  order: Package,
  promo: Tag,
  system: Info,
  message: MessageSquare,
};

const TYPE_COLORS: Record<NotificationType, string> = {
  order: "#22C55E",
  promo: "#EF4056",
  system: "#00BFFF",
  message: "#8B5CF6",
};

export default function NotificationBell({
  locale,
  variant = "top",
}: NotificationBellProps) {
  const isFa = locale === "fa";
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  const items = useNotificationsStore((s) => s.items);
  const markAsRead = useNotificationsStore((s) => s.markAsRead);
  const markAllAsRead = useNotificationsStore((s) => s.markAllAsRead);
  const remove = useNotificationsStore((s) => s.remove);
  const clearAll = useNotificationsStore((s) => s.clearAll);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const unreadCount = items.filter((n) => !n.read).length;

  const iconSize = variant === "top" ? 14 : 20;

  return (
    <div ref={wrapperRef} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label={isFa ? "اعلان‌ها" : "Notifications"}
        className={
          variant === "top"
            ? "text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors relative"
            : "text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors flex items-center gap-2 relative"
        }
      >
        <Bell size={iconSize} />
        {variant === "header" && (
          <span>{isFa ? "اعلان‌ها" : "Notifications"}</span>
        )}
        {mounted && unreadCount > 0 && (
          <span
            className={
              variant === "top"
                ? "absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-bold animate-pulse"
                : "bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold animate-pulse"
            }
          >
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div
          className={`absolute top-full mt-2 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl shadow-2xl overflow-hidden z-[60] w-80 md:w-96 ${
            isFa ? "left-0 md:left-auto md:right-0" : "right-0 md:right-auto md:left-0"
          }`}
          style={{
            [isFa ? "left" : "right"]: variant === "top" ? "auto" : 0,
            [isFa ? "right" : "left"]: variant === "top" ? 0 : "auto",
          } as React.CSSProperties}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-3 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
            <div className="flex items-center gap-2">
              <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {isFa ? "اعلان‌ها" : "Notifications"}
              </h3>
              {unreadCount > 0 && (
                <span className="text-[10px] bg-[#EF4056] text-white px-1.5 py-0.5 rounded-full font-bold">
                  {unreadCount}
                </span>
              )}
            </div>
            <div className="flex items-center gap-1">
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="text-[10px] text-[#00BFFF] hover:underline flex items-center gap-1"
                  title={isFa ? "خواندن همه" : "Mark all as read"}
                >
                  <Check size={11} />
                  {isFa ? "خواندن همه" : "Read all"}
                </button>
              )}
              <button
                onClick={() => setOpen(false)}
                className="w-6 h-6 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
                aria-label="Close"
              >
                <X size={14} />
              </button>
            </div>
          </div>

          {/* List */}
          <div className="max-h-[400px] overflow-y-auto">
            {items.length === 0 ? (
              <div className="p-8 text-center">
                <div className="w-14 h-14 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
                  <Bell size={24} className="text-[#A1A3A8]" />
                </div>
                <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  {isFa ? "اعلان جدیدی ندارید" : "No notifications yet"}
                </p>
              </div>
            ) : (
              items.map((notif) => {
                const Icon = TYPE_ICONS[notif.type];
                const color = TYPE_COLORS[notif.type];
                const Wrapper = notif.href ? Link : "div";
                const wrapperProps = notif.href
                  ? {
                      href: `/${locale}${notif.href}`,
                      onClick: () => {
                        markAsRead(notif.id);
                        setOpen(false);
                      },
                    }
                  : {
                      onClick: () => markAsRead(notif.id),
                    };

                return (
                  <Wrapper
                    key={notif.id}
                    {...(wrapperProps as React.ComponentProps<typeof Link>)}
                    className={`flex items-start gap-3 p-3 border-b border-[#F5F5F5] dark:border-[#2A2A2E] last:border-0 hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors cursor-pointer relative group ${
                      !notif.read ? "bg-[#EF4056]/[0.03]" : ""
                    }`}
                  >
                    <div
                      className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                      style={{ backgroundColor: `${color}15` }}
                    >
                      <Icon size={16} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <h4
                          className={`text-[12px] leading-5 line-clamp-1 ${
                            !notif.read
                              ? "font-bold text-[#3F4064] dark:text-[#E5E5EA]"
                              : "font-medium text-[#62666D] dark:text-[#A1A3A8]"
                          }`}
                        >
                          {isFa ? notif.titleFa : notif.titleEn}
                        </h4>
                        {!notif.read && (
                          <div className="w-2 h-2 rounded-full bg-[#EF4056] shrink-0 mt-1.5" />
                        )}
                      </div>
                      <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] leading-5 line-clamp-2 mt-0.5">
                        {isFa ? notif.bodyFa : notif.bodyEn}
                      </p>
                      <span className="text-[10px] text-[#A1A3A8] mt-1 block">
                        {isFa ? notif.dateFa : notif.dateEn}
                      </span>
                    </div>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        remove(notif.id);
                      }}
                      aria-label="Remove"
                      className="w-6 h-6 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#EF4444]/10 hover:text-[#EF4444] opacity-0 group-hover:opacity-100 transition-all shrink-0"
                    >
                      <Trash2 size={12} />
                    </button>
                  </Wrapper>
                );
              })
            )}
          </div>

          {/* Footer */}
          {items.length > 0 && (
            <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] p-2">
              <button
                onClick={clearAll}
                className="w-full text-[11px] text-[#EF4444] hover:bg-[#EF4444]/5 rounded-lg py-2 transition-colors flex items-center justify-center gap-1"
              >
                <Trash2 size={12} />
                {isFa ? "پاک کردن همه" : "Clear all"}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/notifications/index.ts
# ============================================================
files.append(("components/notifications/index.ts", """// components/notifications/index.ts
export { default as NotificationBell } from "./NotificationBell";
"""))

# ============================================================
# components/layout/BottomNav.tsx
# ============================================================
files.append(("components/layout/BottomNav.tsx", """"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  LayoutGrid,
  ShoppingCart,
  Heart,
  User,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { useCartStore, useWishlistStore, useAuthStore } from "@/lib/stores";

interface BottomNavProps {
  locale: Locale;
}

export default function BottomNav({ locale }: BottomNavProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const cartCount = useCartStore((s) =>
    s.items.reduce((sum, i) => sum + i.quantity, 0)
  );
  const wishlistCount = useWishlistStore((s) => s.ids.length);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const links = [
    {
      href: `/${locale}`,
      icon: Home,
      fa: "خانه",
      en: "Home",
      exact: true,
    },
    {
      href: `/${locale}/categories`,
      icon: LayoutGrid,
      fa: "دسته‌ها",
      en: "Categories",
    },
    {
      href: `/${locale}/cart`,
      icon: ShoppingCart,
      fa: "سبد",
      en: "Cart",
      badge: cartCount,
    },
    {
      href: `/${locale}/account/wishlist`,
      icon: Heart,
      fa: "علاقه‌مندی",
      en: "Wishlist",
      badge: wishlistCount,
    },
    {
      href: isAuthenticated ? `/${locale}/account` : `/${locale}/auth/login`,
      icon: User,
      fa: "حساب",
      en: "Account",
    },
  ];

  const isActive = (href: string, exact?: boolean) => {
    if (exact) return pathname === href;
    return pathname.startsWith(href);
  };

  return (
    <nav
      className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 dark:bg-[#1A1A1E]/95 backdrop-blur-md border-t border-[#E0E0E2] dark:border-[#2A2A2E]"
      style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
    >
      <div className="grid grid-cols-5 h-16">
        {links.map((link) => {
          const Icon = link.icon;
          const active = isActive(link.href, link.exact);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex flex-col items-center justify-center gap-1 transition-colors relative ${
                active
                  ? "text-[#EF4056]"
                  : "text-[#62666D] dark:text-[#A1A3A8]"
              }`}
            >
              <div className="relative">
                <Icon size={22} strokeWidth={active ? 2.4 : 2} />
                {link.badge !== undefined && link.badge > 0 && (
                  <span className="absolute -top-1.5 -right-1.5 bg-[#EF4056] text-white text-[9px] rounded-full min-w-[16px] h-[16px] px-1 flex items-center justify-center font-bold">
                    {link.badge > 99 ? "99+" : link.badge}
                  </span>
                )}
              </div>
              <span
                className={`text-[10px] ${
                  active ? "font-bold" : "font-medium"
                }`}
              >
                {isFa ? link.fa : link.en}
              </span>
              {active && (
                <span className="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-[#EF4056] rounded-full" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
"""))

# ============================================================
# components/layout/index.ts
# ============================================================
files.append(("components/layout/index.ts", """// components/layout/index.ts
export { default as Header } from "./Header";
export { default as Footer } from "./Footer";
export { default as BottomNav } from "./BottomNav";
"""))

# ============================================================
# components/layout/Header.tsx (updated to add NotificationBell)
# ============================================================
files.append(("components/layout/Header.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  ShoppingCart,
  Heart,
  User,
  Menu,
  X,
  ChevronDown,
  Smartphone,
  Laptop,
  Tablet,
  Headphones,
  Camera,
  Watch,
  Gamepad2,
  Cable,
  Shirt,
  Footprints,
  Home,
  BookOpen,
  GitCompareArrows,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore, useWishlistStore, useCompareStore } from "@/lib/stores";
import ThemeToggle from "@/components/common/ThemeToggle";
import { SearchAutocomplete } from "@/components/search";
import { NotificationBell } from "@/components/notifications";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Smartphone, Laptop, Tablet, Headphones, Camera, Watch,
  Gamepad2, Cable, Shirt, Footprints, Home, BookOpen,
};

interface HeaderProps {
  locale: Locale;
}

export default function Header({ locale }: HeaderProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openCategory, setOpenCategory] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  const totalItems = useCartStore((s) => s.items.reduce((sum, i) => sum + i.quantity, 0));
  const wishlistCount = useWishlistStore((s) => s.ids.length);
  const compareCount = useCompareStore((s) => s.ids.length);

  useEffect(() => { setMounted(true); }, []);
  useEffect(() => {
    setMobileOpen(false);
    setOpenCategory(null);
  }, [pathname]);

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
  };

  const swapLocale = (newLocale: Locale) => {
    const rest = pathname.replace(/^\\/(fa|en)/, "");
    return `/${newLocale}${rest}`;
  };

  return (
    <>
      {/* Top thin bar */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 h-10 flex items-center justify-between text-[12px]">
          <div className="flex items-center gap-4">
            <Link
              href={swapLocale(isFa ? "en" : "fa")}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
            >
              {isFa ? "English" : "فارسی"}
            </Link>
            <ThemeToggle locale={locale} />
          </div>
          <div className="flex items-center gap-4">
            <Link
              href={`/${locale}/auth/login`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
            >
              {t.login}
            </Link>
            <span className="text-[#E0E0E2] dark:text-[#2A2A2E]">|</span>
            <NotificationBell locale={locale} variant="top" />
            <Link
              href={`/${locale}/compare`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <GitCompareArrows size={14} />
              {mounted && compareCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {compareCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/account/wishlist`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <Heart size={14} />
              {mounted && wishlistCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {wishlistCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/cart`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <ShoppingCart size={14} />
              {mounted && totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          <button
            className="lg:hidden text-[#3F4064] dark:text-[#E5E5EA]"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>

          <Link href={`/${locale}`} className="text-[#EF4056] font-bold text-xl shrink-0">
            SourcePixcel
          </Link>

          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <SearchAutocomplete locale={locale} />
          </div>

          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} />
            <span>{t.account}</span>
          </Link>

          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2] dark:bg-[#2A2A2E]" />

          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors relative"
          >
            <ShoppingCart size={20} />
            <span>{t.cart}</span>
            {mounted && totalItems > 0 && (
              <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* Mega menu */}
        <div className="hidden lg:block border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
          <div className="max-w-[1400px] mx-auto px-4">
            <nav className="flex items-center gap-1 h-12">
              {categories.map((cat) => {
                const Icon = ICON_MAP[cat.icon] ?? Cable;
                const isOpen = openCategory === cat.id;
                return (
                  <div
                    key={cat.id}
                    className="relative"
                    onMouseEnter={() => setOpenCategory(cat.id)}
                    onMouseLeave={() => setOpenCategory(null)}
                  >
                    <Link
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                    >
                      <Icon size={16} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      <ChevronDown size={12} className="opacity-50" />
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        {cat.subcategories.map((sub) => (
                          <Link
                            key={sub.id}
                            href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                            className="block px-4 py-2 text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
                          >
                            {isFa ? sub.nameFa : sub.nameEn}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-[100] lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
          />
          <div
            className="absolute top-0 bottom-0 bg-white dark:bg-[#1A1A1E] w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button onClick={() => setMobileOpen(false)} aria-label="Close menu">
                <X size={24} className="text-[#3F4064] dark:text-[#E5E5EA]" />
              </button>
            </div>

            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  {isFa ? "حالت تاریک" : "Dark mode"}
                </span>
                <ThemeToggle locale={locale} />
              </div>

              <div className="mb-4">
                <SearchAutocomplete locale={locale} onClose={() => setMobileOpen(false)} />
              </div>

              <div className="mb-4">
                <Link
                  href={`/${locale}/auth/login`}
                  className="block text-center bg-[#EF4056] text-white rounded-lg py-2 text-sm font-medium"
                >
                  {t.login}
                </Link>
              </div>

              <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] pt-4">
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                {categories.map((cat) => {
                  const Icon = ICON_MAP[cat.icon] ?? Cable;
                  return (
                    <Link
                      key={cat.id}
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-3 py-2 text-sm text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056]"
                    >
                      <Icon size={18} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
"""))

# ============================================================
# app/[locale]/layout.tsx (updated to add BottomNav + bottom padding)
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BottomNav from "@/components/layout/BottomNav";
import ToastContainer from "@/components/common/ToastContainer";
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
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 25: Notifications + Bottom Nav")
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
        print("  1) Click the bell icon in the top bar")
        print("  2) See 5 seeded notifications")
        print("  3) On mobile: bottom nav with 5 tabs")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()