# 24_admin.py
# پنل ادمین کامل
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/admin.ts
# ============================================================
files.append(("lib/stores/admin.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AdminState {
  isAdmin: boolean;
  adminName: string | null;
  login: (name: string) => void;
  logout: () => void;
}

export const useAdminStore = create<AdminState>()(
  persist(
    (set) => ({
      isAdmin: false,
      adminName: null,
      login: (name) => set({ isAdmin: true, adminName: name }),
      logout: () => set({ isAdmin: false, adminName: null }),
    }),
    { name: "sourcepixcel-admin" }
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
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
"""))

# ============================================================
# components/admin/AdminGuard.tsx
# ============================================================
files.append(("components/admin/AdminGuard.tsx", """"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAdminStore } from "@/lib/stores";

interface AdminGuardProps {
  locale: string;
  children: React.ReactNode;
}

export default function AdminGuard({ locale, children }: AdminGuardProps) {
  const router = useRouter();
  const pathname = usePathname();
  const isAdmin = useAdminStore((s) => s.isAdmin);
  const [mounted, setMounted] = useState(false);

  const isLoginPage = pathname.includes("/admin/login");

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isAdmin && !isLoginPage) {
      router.replace(`/${locale}/admin/login`);
    }
  }, [mounted, isAdmin, isLoginPage, router, locale]);

  if (!mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Loading...
      </div>
    );
  }

  if (!isAdmin && !isLoginPage) {
    return (
      <div className="min-h-screen flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Redirecting to login...
      </div>
    );
  }

  return <>{children}</>;
}
"""))

# ============================================================
# components/admin/AdminSidebar.tsx
# ============================================================
files.append(("components/admin/AdminSidebar.tsx", """"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  Package,
  ShoppingCart,
  Users,
  Tag,
  BarChart3,
  Settings,
  LogOut,
  Home,
  X,
} from "lucide-react";
import { useAdminStore } from "@/lib/stores";

interface AdminSidebarProps {
  locale: string;
  mobileOpen?: boolean;
  onClose?: () => void;
}

export default function AdminSidebar({
  locale,
  mobileOpen,
  onClose,
}: AdminSidebarProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const router = useRouter();
  const adminName = useAdminStore((s) => s.adminName);
  const logout = useAdminStore((s) => s.logout);

  const links = [
    {
      href: `/${locale}/admin`,
      icon: LayoutDashboard,
      fa: "داشبورد",
      en: "Dashboard",
      exact: true,
    },
    {
      href: `/${locale}/admin/products`,
      icon: Package,
      fa: "محصولات",
      en: "Products",
    },
    {
      href: `/${locale}/admin/orders`,
      icon: ShoppingCart,
      fa: "سفارشات",
      en: "Orders",
      badge: 4,
    },
    {
      href: `/${locale}/admin/users`,
      icon: Users,
      fa: "کاربران",
      en: "Users",
    },
    {
      href: `/${locale}/admin/discounts`,
      icon: Tag,
      fa: "تخفیف‌ها",
      en: "Discounts",
    },
    {
      href: `/${locale}/admin/reports`,
      icon: BarChart3,
      fa: "گزارشات",
      en: "Reports",
    },
    {
      href: `/${locale}/admin/settings`,
      icon: Settings,
      fa: "تنظیمات",
      en: "Settings",
    },
  ];

  const isActive = (href: string, exact?: boolean) =>
    exact ? pathname === href : pathname.startsWith(href);

  const handleLogout = () => {
    logout();
    router.push(`/${locale}/admin/login`);
  };

  return (
    <aside
      className={`bg-[#1A1A1E] text-white w-64 shrink-0 flex flex-col ${
        mobileOpen
          ? "fixed inset-y-0 z-[100] shadow-2xl"
          : "hidden lg:flex"
      }`}
      style={
        mobileOpen
          ? ({ [isFa ? "right" : "left"]: 0 } as React.CSSProperties)
          : undefined
      }
    >
      {/* Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-[#2A2A2E]">
        <Link
          href={`/${locale}/admin`}
          className="flex items-center gap-2"
        >
          <div className="w-8 h-8 rounded-lg bg-[#EF4056] flex items-center justify-center">
            <span className="text-white font-bold text-[14px]">S</span>
          </div>
          <div>
            <div className="text-[13px] font-bold">SourcePixcel</div>
            <div className="text-[9px] text-white/50">
              {isFa ? "پنل مدیریت" : "Admin Panel"}
            </div>
          </div>
        </Link>
        {mobileOpen && (
          <button
            onClick={onClose}
            className="text-white/70 hover:text-white"
            aria-label="Close"
          >
            <X size={20} />
          </button>
        )}
      </div>

      {/* User info */}
      <div className="p-3 border-b border-[#2A2A2E]">
        <div className="flex items-center gap-3 px-2 py-2">
          <div className="w-9 h-9 rounded-full bg-[#EF4056] flex items-center justify-center text-white font-bold text-[13px] shrink-0">
            {adminName?.[0] ?? "A"}
          </div>
          <div className="min-w-0">
            <div className="text-[12px] font-bold truncate">
              {adminName ?? "Admin"}
            </div>
            <div className="text-[10px] text-white/50">
              {isFa ? "مدیر سیستم" : "Administrator"}
            </div>
          </div>
        </div>
      </div>

      {/* Links */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {links.map((link) => {
          const Icon = link.icon;
          const active = isActive(link.href, link.exact);
          return (
            <Link
              key={link.href}
              href={link.href}
              onClick={onClose}
              className={`flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-[13px] transition-colors ${
                active
                  ? "bg-[#EF4056] text-white font-medium"
                  : "text-white/70 hover:bg-[#2A2A2E] hover:text-white"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon size={16} />
                <span>{isFa ? link.fa : link.en}</span>
              </div>
              {link.badge !== undefined && link.badge > 0 && (
                <span className="bg-white text-[#EF4056] text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
                  {link.badge}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-[#2A2A2E] space-y-1">
        <Link
          href={`/${locale}`}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] text-white/70 hover:bg-[#2A2A2E] hover:text-white transition-colors"
        >
          <Home size={16} />
          <span>{isFa ? "بازگشت به سایت" : "Back to store"}</span>
        </Link>
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors"
        >
          <LogOut size={16} />
          <span>{isFa ? "خروج" : "Logout"}</span>
        </button>
      </div>
    </aside>
  );
}
"""))

# ============================================================
# components/admin/AdminStats.tsx
# ============================================================
files.append(("components/admin/AdminStats.tsx", """import {
  TrendingUp,
  TrendingDown,
  ShoppingCart,
  Users,
  Package,
  DollarSign,
} from "lucide-react";

interface AdminStatsProps {
  locale: string;
}

export default function AdminStats({ locale }: AdminStatsProps) {
  const isFa = locale === "fa";

  const stats = [
    {
      icon: DollarSign,
      labelFa: "فروش امروز",
      labelEn: "Today's Sales",
      value: "۱۲,۴۵۰,۰۰۰",
      suffix: isFa ? "تومان" : "T",
      change: 12.5,
      changeUp: true,
      color: "#22C55E",
    },
    {
      icon: ShoppingCart,
      labelFa: "سفارشات امروز",
      labelEn: "Today's Orders",
      value: isFa ? "۴۸" : "48",
      suffix: "",
      change: 8.2,
      changeUp: true,
      color: "#EF4056",
    },
    {
      icon: Users,
      labelFa: "کاربران جدید",
      labelEn: "New Users",
      value: isFa ? "۲۳" : "23",
      suffix: "",
      change: 3.1,
      changeUp: false,
      color: "#00BFFF",
    },
    {
      icon: Package,
      labelFa: "محصولات",
      labelEn: "Products",
      value: isFa ? "۶۸" : "68",
      suffix: "",
      change: 0,
      changeUp: true,
      color: "#8B5CF6",
    },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, i) => {
        const Icon = stat.icon;
        return (
          <div
            key={i}
            className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4"
          >
            <div className="flex items-center justify-between mb-3">
              <div
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ backgroundColor: `${stat.color}15` }}
              >
                <Icon size={20} style={{ color: stat.color }} />
              </div>
              {stat.change !== 0 && (
                <div
                  className={`flex items-center gap-1 text-[10px] font-medium ${
                    stat.changeUp ? "text-[#22C55E]" : "text-[#EF4444]"
                  }`}
                >
                  {stat.changeUp ? (
                    <TrendingUp size={12} />
                  ) : (
                    <TrendingDown size={12} />
                  )}
                  {stat.change}%
                </div>
              )}
            </div>
            <div className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-1">
              {stat.value}
              {stat.suffix && (
                <span className="text-[11px] text-[#A1A3A8] font-normal mr-1">
                  {stat.suffix}
                </span>
              )}
            </div>
            <div className="text-[11px] text-[#A1A3A8]">
              {isFa ? stat.labelFa : stat.labelEn}
            </div>
          </div>
        );
      })}
    </div>
  );
}
"""))

# ============================================================
# components/admin/SalesChart.tsx
# ============================================================
files.append(("components/admin/SalesChart.tsx", """interface SalesChartProps {
  locale: string;
}

const DATA = [40, 65, 45, 80, 55, 90, 75, 95, 60, 85, 70, 100];
const MONTHS_FA = ["فرو", "ارد", "خرد", "تیر", "مرد", "شهر", "مهر", "آبا", "آذر", "دی", "بهم", "اسف"];
const MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export default function SalesChart({ locale }: SalesChartProps) {
  const isFa = locale === "fa";
  const months = isFa ? MONTHS_FA : MONTHS_EN;

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {isFa ? "نمودار فروش سالانه" : "Annual Sales Chart"}
          </h3>
          <p className="text-[11px] text-[#A1A3A8] mt-1">
            {isFa ? "فروش ماهانه در سال ۱۴۰۳" : "Monthly sales in 2025"}
          </p>
        </div>
        <div className="flex items-center gap-3 text-[10px]">
          <div className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-[#EF4056]" />
            <span className="text-[#62666D] dark:text-[#A1A3A8]">
              {isFa ? "فروش" : "Sales"}
            </span>
          </div>
        </div>
      </div>

      <div className="flex items-end justify-between gap-1 md:gap-2 h-40">
        {DATA.map((value, i) => (
          <div key={i} className="flex-1 flex flex-col items-center gap-2 group">
            <div className="relative w-full flex justify-center">
              <div
                className="w-full max-w-[32px] rounded-t-md transition-all duration-500 group-hover:opacity-90 relative"
                style={{
                  height: `${value * 1.4}px`,
                  background: `linear-gradient(180deg, #EF4056 0%, #d63850 100%)`,
                }}
              >
                <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-[#3F4064] text-white text-[9px] px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                  {value}M
                </div>
              </div>
            </div>
            <span className="text-[9px] text-[#A1A3A8]">{months[i]}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/admin/TopProducts.tsx
# ============================================================
files.append(("components/admin/TopProducts.tsx", """import Image from "next/image";
import { products } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface TopProductsProps {
  locale: string;
}

export default function TopProducts({ locale }: TopProductsProps) {
  const isFa = locale === "fa";
  const top = products.slice(0, 5);

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
        {isFa ? "پرفروش‌ترین محصولات" : "Top Selling Products"}
      </h3>

      <div className="space-y-3">
        {top.map((product, i) => (
          <div key={product.id} className="flex items-center gap-3">
            <div className="w-6 h-6 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center text-[11px] font-bold text-[#62666D] dark:text-[#A1A3A8] shrink-0">
              {isFa ? (i + 1).toLocaleString("fa-IR") : i + 1}
            </div>
            <div className="w-10 h-10 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
              <Image
                src={product.image}
                alt={isFa ? product.titleFa : product.titleEn}
                fill
                sizes="40px"
                className="object-cover"
              />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 font-medium">
                {isFa ? product.titleFa : product.titleEn}
              </div>
              <div className="text-[10px] text-[#A1A3A8]">
                {product.reviewCount.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
                {isFa ? "فروش" : "sales"}
              </div>
            </div>
            <div className="text-[11px] font-bold text-[#EF4056] shrink-0">
              {formatPrice(product.finalPrice, isFa ? "fa" : "en")}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/admin/RecentOrders.tsx
# ============================================================
files.append(("components/admin/RecentOrders.tsx", """import Link from "next/link";
import { mockOrders } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface RecentOrdersProps {
  locale: string;
}

const STATUS_STYLES: Record<string, { bg: string; text: string; labelFa: string; labelEn: string }> = {
  pending: { bg: "#F59E0B", text: "#F59E0B", labelFa: "در انتظار", labelEn: "Pending" },
  processing: { bg: "#00BFFF", text: "#00BFFF", labelFa: "در حال پردازش", labelEn: "Processing" },
  shipped: { bg: "#8B5CF6", text: "#8B5CF6", labelFa: "ارسال شده", labelEn: "Shipped" },
  delivered: { bg: "#22C55E", text: "#22C55E", labelFa: "تحویل شده", labelEn: "Delivered" },
  cancelled: { bg: "#EF4444", text: "#EF4444", labelFa: "لغو شده", labelEn: "Cancelled" },
};

export default function RecentOrders({ locale }: RecentOrdersProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "سفارشات اخیر" : "Recent Orders"}
        </h3>
        <Link
          href={`/${locale}/admin/orders`}
          className="text-[11px] text-[#00BFFF] hover:text-[#EF4056]"
        >
          {isFa ? "مشاهده همه" : "See all"}
        </Link>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[500px]">
          <thead>
            <tr className="text-[10px] text-[#A1A3A8] uppercase">
              <th className="text-right pb-2 font-medium">
                {isFa ? "شماره" : "ID"}
              </th>
              <th className="text-right pb-2 font-medium">
                {isFa ? "مشتری" : "Customer"}
              </th>
              <th className="text-right pb-2 font-medium">
                {isFa ? "مبلغ" : "Amount"}
              </th>
              <th className="text-right pb-2 font-medium">
                {isFa ? "وضعیت" : "Status"}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
            {mockOrders.map((order) => {
              const status = STATUS_STYLES[order.status];
              return (
                <tr key={order.id} className="text-[12px]">
                  <td className="py-3 text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                    {order.id}
                  </td>
                  <td className="py-3 text-[#62666D] dark:text-[#A1A3A8]">
                    {order.shippingAddress.split("،")[0]}
                  </td>
                  <td className="py-3 font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                    {formatPrice(order.total, isFa ? "fa" : "en")}
                  </td>
                  <td className="py-3">
                    <span
                      className="text-[10px] px-2 py-1 rounded-full font-medium"
                      style={{
                        backgroundColor: `${status.bg}15`,
                        color: status.text,
                      }}
                    >
                      {isFa ? status.labelFa : status.labelEn}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/admin/DashboardView.tsx
# ============================================================
files.append(("components/admin/DashboardView.tsx", """import AdminStats from "./AdminStats";
import SalesChart from "./SalesChart";
import TopProducts from "./TopProducts";
import RecentOrders from "./RecentOrders";

interface DashboardViewProps {
  locale: string;
}

export default function DashboardView({ locale }: DashboardViewProps) {
  const isFa = locale === "fa";

  return (
    <div className="space-y-4">
      {/* Header */}
      <div>
        <h1 className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {isFa ? "داشبورد" : "Dashboard"}
        </h1>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? "خلاصه‌ای از عملکرد فروشگاه SourcePixcel"
            : "Overview of SourcePixcel store performance"}
        </p>
      </div>

      {/* Stats */}
      <AdminStats locale={locale} />

      {/* Chart + Top Products */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <SalesChart locale={locale} />
        </div>
        <div className="lg:col-span-1">
          <TopProducts locale={locale} />
        </div>
      </div>

      {/* Recent Orders */}
      <RecentOrders locale={locale} />
    </div>
  );
}
"""))

# ============================================================
# components/admin/ProductsView.tsx
# ============================================================
files.append(("components/admin/ProductsView.tsx", """"use client";

import { useState, useMemo } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Eye,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { products as allProducts, getCategoryById, getBrandById } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface ProductsViewProps {
  locale: string;
}

const PER_PAGE = 10;

export default function ProductsView({ locale }: ProductsViewProps) {
  const isFa = locale === "fa";
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    if (!q) return allProducts;
    return allProducts.filter(
      (p) =>
        p.titleFa.toLowerCase().includes(q) ||
        p.titleEn.toLowerCase().includes(q) ||
        p.brand.toLowerCase().includes(q)
    );
  }, [query]);

  const totalPages = Math.ceil(filtered.length / PER_PAGE);
  const paginated = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const t = {
    title: isFa ? "مدیریت محصولات" : "Products Management",
    subtitle: isFa
      ? `${filtered.length} محصول موجود`
      : `${filtered.length} products`,
    searchPlaceholder: isFa ? "جستجوی محصول..." : "Search product...",
    addNew: isFa ? "افزودن محصول" : "Add Product",
    product: isFa ? "محصول" : "Product",
    category: isFa ? "دسته" : "Category",
    brand: isFa ? "برند" : "Brand",
    price: isFa ? "قیمت" : "Price",
    stock: isFa ? "موجودی" : "Stock",
    actions: isFa ? "عملیات" : "Actions",
    inStock: isFa ? "موجود" : "In stock",
    outOfStock: isFa ? "ناموجود" : "Out",
    edit: isFa ? "ویرایش" : "Edit",
    delete: isFa ? "حذف" : "Delete",
    view: isFa ? "مشاهده" : "View",
    confirmDelete: isFa
      ? "آیا مطمئن هستید؟"
      : "Are you sure?",
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {t.title}
          </h1>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.subtitle}
          </p>
        </div>
        <button className="h-10 px-4 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2">
          <Plus size={16} />
          {t.addNew}
        </button>
      </div>

      {/* Search */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-3">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder={t.searchPlaceholder}
            className="w-full h-10 pr-10 pl-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-transparent focus:border-[#EF4056] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors"
            style={{
              paddingRight: isFa ? 40 : 12,
              paddingLeft: isFa ? 12 : 40,
            }}
          />
          <Search
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
          />
        </div>
      </div>

      {/* Table */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[11px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-right p-3 font-medium">{t.product}</th>
                <th className="text-right p-3 font-medium">{t.category}</th>
                <th className="text-right p-3 font-medium">{t.brand}</th>
                <th className="text-right p-3 font-medium">{t.price}</th>
                <th className="text-right p-3 font-medium">{t.stock}</th>
                <th className="text-right p-3 font-medium">{t.actions}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {paginated.map((p) => {
                const category = getCategoryById(p.category);
                const brand = getBrandById(p.brand);
                return (
                  <tr
                    key={p.id}
                    className="hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors"
                  >
                    <td className="p-3">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
                          <Image
                            src={p.image}
                            alt={isFa ? p.titleFa : p.titleEn}
                            fill
                            sizes="48px"
                            className="object-cover"
                          />
                        </div>
                        <div className="min-w-0">
                          <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 max-w-[220px]">
                            {isFa ? p.titleFa : p.titleEn}
                          </div>
                          <div className="text-[10px] text-[#A1A3A8]" dir="ltr">
                            SP-{p.id.toString().padStart(5, "0")}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {category ? (isFa ? category.nameFa : category.nameEn) : "—"}
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {brand ? (isFa ? brand.nameFa : brand.nameEn) : "—"}
                    </td>
                    <td className="p-3">
                      <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                        {formatPrice(p.finalPrice, isFa ? "fa" : "en")}
                      </div>
                      {p.discountPercent > 0 && (
                        <div className="text-[10px] text-[#EF4056]">
                          {p.discountPercent}% {isFa ? "تخفیف" : "off"}
                        </div>
                      )}
                    </td>
                    <td className="p-3">
                      <span
                        className={`text-[10px] px-2 py-1 rounded-full font-medium ${
                          p.inStock
                            ? "bg-[#22C55E]/10 text-[#22C55E]"
                            : "bg-[#EF4444]/10 text-[#EF4444]"
                        }`}
                      >
                        {p.inStock ? t.inStock : t.outOfStock}
                      </span>
                    </td>
                    <td className="p-3">
                      <div className="flex items-center gap-1">
                        <Link
                          href={`/${locale}/product/${p.slug}`}
                          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
                          title={t.view}
                        >
                          <Eye size={14} />
                        </Link>
                        <button
                          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#F59E0B] hover:bg-[#F59E0B]/10 transition-colors"
                          title={t.edit}
                        >
                          <Edit size={14} />
                        </button>
                        <button
                          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors"
                          title={t.delete}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex-wrap gap-3">
            <span className="text-[11px] text-[#A1A3A8]">
              {isFa
                ? `صفحه ${page.toLocaleString("fa-IR")} از ${totalPages.toLocaleString("fa-IR")}`
                : `Page ${page} of ${totalPages}`}
            </span>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="w-8 h-8 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="w-8 h-8 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/admin/OrdersView.tsx
# ============================================================
files.append(("components/admin/OrdersView.tsx", """import Link from "next/link";
import { Eye } from "lucide-react";
import { mockOrders } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface OrdersViewProps {
  locale: string;
}

const STATUS_STYLES: Record<string, { bg: string; text: string; labelFa: string; labelEn: string }> = {
  pending: { bg: "#F59E0B", text: "#F59E0B", labelFa: "در انتظار", labelEn: "Pending" },
  processing: { bg: "#00BFFF", text: "#00BFFF", labelFa: "در حال پردازش", labelEn: "Processing" },
  shipped: { bg: "#8B5CF6", text: "#8B5CF6", labelFa: "ارسال شده", labelEn: "Shipped" },
  delivered: { bg: "#22C55E", text: "#22C55E", labelFa: "تحویل شده", labelEn: "Delivered" },
  cancelled: { bg: "#EF4444", text: "#EF4444", labelFa: "لغو شده", labelEn: "Cancelled" },
};

export default function OrdersView({ locale }: OrdersViewProps) {
  const isFa = locale === "fa";

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {isFa ? "مدیریت سفارشات" : "Orders Management"}
        </h1>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? `${mockOrders.length} سفارش`
            : `${mockOrders.length} orders`}
        </p>
      </div>

      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[11px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-right p-3 font-medium">{isFa ? "شماره" : "ID"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "تاریخ" : "Date"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "مشتری" : "Customer"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "مبلغ" : "Amount"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "وضعیت" : "Status"}</th>
                <th className="text-right p-3 font-medium">{isFa ? "عملیات" : "Actions"}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {mockOrders.map((order) => {
                const status = STATUS_STYLES[order.status];
                return (
                  <tr
                    key={order.id}
                    className="hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors"
                  >
                    <td className="p-3 text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                      {order.id}
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {order.date}
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {order.shippingAddress.split("،")[0]}
                    </td>
                    <td className="p-3 text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                      {formatPrice(order.total, isFa ? "fa" : "en")}
                    </td>
                    <td className="p-3">
                      <span
                        className="text-[10px] px-2 py-1 rounded-full font-medium"
                        style={{
                          backgroundColor: `${status.bg}15`,
                          color: status.text,
                        }}
                      >
                        {isFa ? status.labelFa : status.labelEn}
                      </span>
                    </td>
                    <td className="p-3">
                      <Link
                        href={`/${locale}/account/orders/${order.id}`}
                        className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
                      >
                        <Eye size={14} />
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/admin/index.ts
# ============================================================
files.append(("components/admin/index.ts", """// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as AdminSidebar } from "./AdminSidebar";
export { default as AdminStats } from "./AdminStats";
export { default as SalesChart } from "./SalesChart";
export { default as TopProducts } from "./TopProducts";
export { default as RecentOrders } from "./RecentOrders";
export { default as DashboardView } from "./DashboardView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
"""))

# ============================================================
# app/[locale]/admin/layout.tsx
# ============================================================
files.append(("app/[locale]/admin/layout.tsx", """"use client";

import { useState } from "react";
import { Menu } from "lucide-react";
import AdminSidebar from "@/components/admin/AdminSidebar";
import AdminGuard from "@/components/admin/AdminGuard";

export default function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);

  // Note: params is a Promise in Next.js 15, but client components
  // can't await it. We'll use a workaround by reading from pathname.
  // For simplicity, we'll get locale from window.location on client.
  const [locale, setLocale] = useState("fa");

  // Read locale on mount
  if (typeof window !== "undefined") {
    const match = window.location.pathname.match(/^\\/(fa|en)/);
    const detected = match?.[1] ?? "fa";
    if (detected !== locale) {
      setLocale(detected);
    }
  }

  return (
    <AdminGuard locale={locale}>
      <div className="min-h-screen flex bg-[#F5F5F5] dark:bg-[#0F0F12]">
        {/* Mobile menu button */}
        <button
          onClick={() => setMobileOpen(true)}
          className="lg:hidden fixed top-4 right-4 z-[90] w-10 h-10 rounded-lg bg-[#EF4056] text-white flex items-center justify-center shadow-lg"
          aria-label="Open menu"
        >
          <Menu size={20} />
        </button>

        <AdminSidebar
          locale={locale}
          mobileOpen={mobileOpen}
          onClose={() => setMobileOpen(false)}
        />

        <main className="flex-1 min-w-0 p-4 md:p-6">{children}</main>
      </div>
    </AdminGuard>
  );
}
"""))

# ============================================================
# app/[locale]/admin/page.tsx
# ============================================================
files.append(("app/[locale]/admin/page.tsx", """import DashboardView from "@/components/admin/DashboardView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminDashboardPage({ params }: PageProps) {
  const { locale } = await params;
  return <DashboardView locale={locale} />;
}
"""))

# ============================================================
# app/[locale]/admin/products/page.tsx
# ============================================================
files.append(("app/[locale]/admin/products/page.tsx", """import ProductsView from "@/components/admin/ProductsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminProductsPage({ params }: PageProps) {
  const { locale } = await params;
  return <ProductsView locale={locale} />;
}
"""))

# ============================================================
# app/[locale]/admin/orders/page.tsx
# ============================================================
files.append(("app/[locale]/admin/orders/page.tsx", """import OrdersView from "@/components/admin/OrdersView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminOrdersPage({ params }: PageProps) {
  const { locale } = await params;
  return <OrdersView locale={locale} />;
}
"""))

# ============================================================
# components/admin/AdminLoginForm.tsx
# ============================================================
files.append(("components/admin/AdminLoginForm.tsx", """"use client";

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
"""))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", """// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as AdminSidebar } from "./AdminSidebar";
export { default as AdminStats } from "./AdminStats";
export { default as SalesChart } from "./SalesChart";
export { default as TopProducts } from "./TopProducts";
export { default as RecentOrders } from "./RecentOrders";
export { default as DashboardView } from "./DashboardView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as AdminLoginForm } from "./AdminLoginForm";
"""))

# ============================================================
# app/[locale]/admin/login/page.tsx
# ============================================================
files.append(("app/[locale]/admin/login/page.tsx", """import AdminLoginForm from "@/components/admin/AdminLoginForm";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminLoginPage({ params }: PageProps) {
  const { locale } = await params;
  return <AdminLoginForm locale={locale} />;
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 24: Admin Panel")
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
        print("  1) Go to http://localhost:3000/fa/admin")
        print("  2) You will be redirected to /fa/admin/login")
        print("  3) Login with: admin / admin123")
        print("  4) You'll see the admin dashboard")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()