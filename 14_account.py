# 14_account.py
# ساخت پنل کاربر
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/data/mock-orders.ts
# ============================================================
files.append(("lib/data/mock-orders.ts", """// lib/data/mock-orders.ts
// Mock orders for demo purposes

export interface OrderItem {
  productId: number;
  quantity: number;
  priceAtPurchase: number;
}

export interface MockOrder {
  id: string;
  date: string;
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  items: OrderItem[];
  total: number;
  shippingAddress: string;
}

export const mockOrders: MockOrder[] = [
  {
    id: "SP-20240001",
    date: "1403/06/15",
    status: "delivered",
    items: [
      { productId: 1, quantity: 1, priceAtPurchase: 66_240_000 },
      { productId: 24, quantity: 1, priceAtPurchase: 14_760_000 },
    ],
    total: 81_000_000,
    shippingAddress: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  },
  {
    id: "SP-20240002",
    date: "1403/06/20",
    status: "shipped",
    items: [{ productId: 37, quantity: 1, priceAtPurchase: 38_000_000 }],
    total: 38_000_000,
    shippingAddress: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  },
  {
    id: "SP-20240003",
    date: "1403/07/01",
    status: "processing",
    items: [
      { productId: 11, quantity: 1, priceAtPurchase: 90_250_000 },
      { productId: 44, quantity: 2, priceAtPurchase: 7_480_000 },
    ],
    total: 105_210_000,
    shippingAddress: "اصفهان، خیابان چهارباغ، پلاک ۴۵",
  },
  {
    id: "SP-20240004",
    date: "1403/07/10",
    status: "pending",
    items: [{ productId: 60, quantity: 1, priceAtPurchase: 10_000_000 }],
    total: 10_000_000,
    shippingAddress: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  },
];

export const getOrderById = (id: string): MockOrder | undefined =>
  mockOrders.find((o) => o.id === id);
"""))

# ============================================================
# lib/data/index.ts (updated)
# ============================================================
files.append(("lib/data/index.ts", """// lib/data/index.ts
export {
  categories,
  brands,
  products,
  getProductBySlug,
  getProductsByCategory,
  getProductsByBrand,
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
  getCategoryById,
  getBrandById,
  getProductsBySubcategory,
} from "./products";

export {
  mockOrders,
  getOrderById,
} from "./mock-orders";
export type { MockOrder, OrderItem } from "./mock-orders";
"""))

# ============================================================
# components/account/AccountSidebar.tsx
# ============================================================
files.append(("components/account/AccountSidebar.tsx", """"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  Package,
  Heart,
  MapPin,
  User,
  LogOut,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAuthStore, useWishlistStore } from "@/lib/stores";

interface AccountSidebarProps {
  locale: Locale;
}

export default function AccountSidebar({ locale }: AccountSidebarProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const wishlistCount = useWishlistStore((s) => s.ids.length);

  const links = [
    {
      href: `/${locale}/account`,
      icon: LayoutDashboard,
      fa: "داشبورد",
      en: "Dashboard",
      exact: true,
    },
    {
      href: `/${locale}/account/orders`,
      icon: Package,
      fa: "سفارشات",
      en: "Orders",
    },
    {
      href: `/${locale}/account/wishlist`,
      icon: Heart,
      fa: "علاقه‌مندی‌ها",
      en: "Wishlist",
      badge: wishlistCount,
    },
    {
      href: `/${locale}/account/addresses`,
      icon: MapPin,
      fa: "آدرس‌ها",
      en: "Addresses",
    },
    {
      href: `/${locale}/account/profile`,
      icon: User,
      fa: "پروفایل",
      en: "Profile",
    },
  ];

  const isActive = (href: string, exact?: boolean) =>
    exact ? pathname === href : pathname.startsWith(href);

  const handleLogout = () => {
    logout();
    router.push(`/${locale}`);
  };

  return (
    <aside className="bg-white rounded-lg border border-[#E0E0E2] p-4">
      {/* User card */}
      {user && (
        <div className="flex items-center gap-3 pb-4 mb-4 border-b border-[#E0E0E2]">
          <div className="w-12 h-12 rounded-full bg-[#EF4056] text-white flex items-center justify-center font-bold text-[16px] shrink-0">
            {user.fullName[0]}
          </div>
          <div className="min-w-0">
            <div className="text-[13px] font-bold text-[#3F4064] truncate">
              {user.fullName}
            </div>
            <div className="text-[11px] text-[#A1A3A8]" dir="ltr">
              {user.mobile}
            </div>
          </div>
        </div>
      )}

      {/* Links */}
      <nav className="space-y-1">
        {links.map((link) => {
          const Icon = link.icon;
          const active = isActive(link.href, link.exact);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-[13px] transition-colors ${
                active
                  ? "bg-[#EF4056]/5 text-[#EF4056] font-medium"
                  : "text-[#62666D] hover:bg-[#F5F5F5] hover:text-[#EF4056]"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon size={16} />
                <span>{isFa ? link.fa : link.en}</span>
              </div>
              {link.badge !== undefined && link.badge > 0 && (
                <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
                  {link.badge}
                </span>
              )}
            </Link>
          );
        })}

        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] text-[#EF4444] hover:bg-[#EF4444]/5 transition-colors mt-2 border-t border-[#E0E0E2] pt-3"
        >
          <LogOut size={16} />
          <span>{isFa ? "خروج از حساب" : "Logout"}</span>
        </button>
      </nav>
    </aside>
  );
}
"""))

# ============================================================
# components/account/OrderStatusBadge.tsx
# ============================================================
files.append(("components/account/OrderStatusBadge.tsx", """import type { Locale } from "@/lib/types";
import type { MockOrder } from "@/lib/data";

interface OrderStatusBadgeProps {
  status: MockOrder["status"];
  locale: Locale;
}

export default function OrderStatusBadge({
  status,
  locale,
}: OrderStatusBadgeProps) {
  const isFa = locale === "fa";

  const map: Record<
    MockOrder["status"],
    { fa: string; en: string; className: string }
  > = {
    pending: {
      fa: "در انتظار پرداخت",
      en: "Pending",
      className: "bg-[#F59E0B]/10 text-[#F59E0B]",
    },
    processing: {
      fa: "در حال پردازش",
      en: "Processing",
      className: "bg-[#00BFFF]/10 text-[#00BFFF]",
    },
    shipped: {
      fa: "ارسال شده",
      en: "Shipped",
      className: "bg-[#8B5CF6]/10 text-[#8B5CF6]",
    },
    delivered: {
      fa: "تحویل داده شده",
      en: "Delivered",
      className: "bg-[#22C55E]/10 text-[#22C55E]",
    },
    cancelled: {
      fa: "لغو شده",
      en: "Cancelled",
      className: "bg-[#EF4444]/10 text-[#EF4444]",
    },
  };

  const item = map[status];

  return (
    <span
      className={`inline-block text-[11px] font-medium px-2 py-1 rounded-full ${item.className}`}
    >
      {isFa ? item.fa : item.en}
    </span>
  );
}
"""))

# ============================================================
# components/account/DashboardView.tsx
# ============================================================
files.append(("components/account/DashboardView.tsx", """import Link from "next/link";
import { Package, Heart, MapPin, TrendingUp, ChevronLeft } from "lucide-react";
import type { Locale } from "@/lib/types";
import { mockOrders } from "@/lib/data";
import { useAuthStore, useWishlistStore } from "@/lib/stores";
import { formatPrice } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";

interface DashboardViewProps {
  locale: Locale;
}

export default function DashboardView({ locale }: DashboardViewProps) {
  const isFa = locale === "fa";
  const user = useAuthStore((s) => s.user);
  const wishlistCount = useWishlistStore((s) => s.ids.length);

  const stats = [
    {
      icon: Package,
      labelFa: "سفارشات",
      labelEn: "Orders",
      value: mockOrders.length,
      href: `/${locale}/account/orders`,
    },
    {
      icon: Heart,
      labelFa: "علاقه‌مندی‌ها",
      labelEn: "Wishlist",
      value: wishlistCount,
      href: `/${locale}/account/wishlist`,
    },
    {
      icon: MapPin,
      labelFa: "آدرس‌ها",
      labelEn: "Addresses",
      value: 1,
      href: `/${locale}/account/addresses`,
    },
    {
      icon: TrendingUp,
      labelFa: "مجموع خرید",
      labelEn: "Total spent",
      value: formatPrice(
        mockOrders.reduce((s, o) => s + o.total, 0),
        locale
      ),
      href: `/${locale}/account/orders`,
      isText: true,
    },
  ];

  const recentOrders = mockOrders.slice(0, 3);

  return (
    <div className="space-y-4">
      {/* Welcome */}
      <div className="bg-gradient-to-l from-[#EF4056] to-[#d63850] rounded-lg p-5 text-white">
        <h1 className="text-[18px] font-bold mb-1">
          {isFa ? `سلام ${user?.fullName ?? "کاربر"} 👋` : `Hello ${user?.fullName ?? "User"} 👋`}
        </h1>
        <p className="text-[12px] text-white/90">
          {isFa
            ? "خوش آمدید به پنل کاربری SourcePixcel"
            : "Welcome to your SourcePixcel dashboard"}
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {stats.map((s, i) => {
          const Icon = s.icon;
          return (
            <Link
              key={i}
              href={s.href}
              className="bg-white rounded-lg border border-[#E0E0E2] p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="w-9 h-9 rounded-lg bg-[#F5F5F5] flex items-center justify-center">
                  <Icon size={16} className="text-[#62666D]" />
                </div>
              </div>
              <div
                className={`font-bold text-[#3F4064] mb-0.5 ${
                  s.isText ? "text-[14px]" : "text-[20px]"
                }`}
              >
                {s.isText
                  ? s.value
                  : isFa
                  ? (s.value as number).toLocaleString("fa-IR")
                  : s.value}
              </div>
              <div className="text-[11px] text-[#A1A3A8]">
                {isFa ? s.labelFa : s.labelEn}
              </div>
            </Link>
          );
        })}
      </div>

      {/* Recent orders */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-[14px] font-bold text-[#3F4064]">
            {isFa ? "سفارشات اخیر" : "Recent Orders"}
          </h2>
          <Link
            href={`/${locale}/account/orders`}
            className="text-[12px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1"
          >
            {isFa ? "مشاهده همه" : "See all"}
            <ChevronLeft
              size={14}
              className={isFa ? "" : "rotate-180"}
            />
          </Link>
        </div>

        <div className="space-y-3">
          {recentOrders.map((order) => (
            <Link
              key={order.id}
              href={`/${locale}/account/orders/${order.id}`}
              className="flex items-center gap-3 p-3 rounded-lg border border-[#E0E0E2] hover:border-[#EF4056] transition-colors"
            >
              <div className="w-10 h-10 rounded-lg bg-[#F5F5F5] flex items-center justify-center shrink-0">
                <Package size={18} className="text-[#62666D]" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[12px] font-bold text-[#3F4064]" dir="ltr">
                    {order.id}
                  </span>
                  <OrderStatusBadge status={order.status} locale={locale} />
                </div>
                <div className="text-[11px] text-[#A1A3A8]">
                  {order.date} •{" "}
                  {isFa
                    ? `${order.items.length} کالا`
                    : `${order.items.length} items`}
                </div>
              </div>
              <div className="text-left shrink-0">
                <div className="text-[12px] font-bold text-[#3F4064]">
                  {formatPrice(order.total, locale)}
                </div>
                <div className="text-[10px] text-[#A1A3A8]">
                  {isFa ? "تومان" : "T"}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/account/OrdersView.tsx
# ============================================================
files.append(("components/account/OrdersView.tsx", """import Link from "next/link";
import { Package, ChevronLeft } from "lucide-react";
import type { Locale } from "@/lib/types";
import { mockOrders } from "@/lib/data";
import { formatPrice } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";
import { EmptyState } from "@/components/common";

interface OrdersViewProps {
  locale: Locale;
}

export default function OrdersView({ locale }: OrdersViewProps) {
  const isFa = locale === "fa";

  if (mockOrders.length === 0) {
    return (
      <EmptyState
        locale={locale}
        titleFa="سفارشی یافت نشد"
        titleEn="No orders found"
        messageFa="شما هنوز سفارشی ثبت نکرده‌اید."
        messageEn="You haven't placed any orders yet."
      />
    );
  }

  return (
    <div className="space-y-3">
      <h1 className="text-[18px] font-bold text-[#3F4064] mb-2">
        {isFa ? "سفارشات من" : "My Orders"}
      </h1>

      {mockOrders.map((order) => (
        <Link
          key={order.id}
          href={`/${locale}/account/orders/${order.id}`}
          className="block bg-white rounded-lg border border-[#E0E0E2] p-4 hover:border-[#EF4056] transition-colors"
        >
          <div className="flex items-center justify-between gap-4 mb-3">
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-10 h-10 rounded-lg bg-[#F5F5F5] flex items-center justify-center shrink-0">
                <Package size={18} className="text-[#62666D]" />
              </div>
              <div className="min-w-0">
                <div className="text-[13px] font-bold text-[#3F4064]" dir="ltr">
                  {order.id}
                </div>
                <div className="text-[11px] text-[#A1A3A8]">{order.date}</div>
              </div>
            </div>
            <OrderStatusBadge status={order.status} locale={locale} />
          </div>

          <div className="flex items-center justify-between gap-4 pt-3 border-t border-[#F5F5F5]">
            <div className="text-[11px] text-[#62666D] truncate flex-1">
              {order.shippingAddress}
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <div className="text-[13px] font-bold text-[#3F4064]">
                {formatPrice(order.total, locale)}{" "}
                <span className="text-[10px] text-[#A1A3A8] font-normal">
                  {isFa ? "تومان" : "T"}
                </span>
              </div>
              <ChevronLeft
                size={16}
                className={`text-[#A1A3A8] ${isFa ? "" : "rotate-180"}`}
              />
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
"""))

# ============================================================
# components/account/OrderDetailView.tsx
# ============================================================
files.append(("components/account/OrderDetailView.tsx", """import Link from "next/link";
import Image from "next/image";
import { ArrowRight, MapPin, Package, Truck, CheckCircle2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import type { MockOrder } from "@/lib/data";
import { products as allProducts } from "@/lib/data";
import { formatPrice } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";

interface OrderDetailViewProps {
  locale: Locale;
  order: MockOrder;
}

export default function OrderDetailView({
  locale,
  order,
}: OrderDetailViewProps) {
  const isFa = locale === "fa";

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

  return (
    <div className="space-y-4">
      {/* Back */}
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

      {/* Header */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
          <div>
            <div className="text-[11px] text-[#A1A3A8] mb-1">
              {isFa ? "شماره سفارش" : "Order Number"}
            </div>
            <div className="text-[16px] font-bold text-[#3F4064]" dir="ltr">
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
                        : "bg-[#F5F5F5] text-[#A1A3A8]"
                    }`}
                  >
                    <Icon size={16} />
                  </div>
                  <span
                    className={`text-[10px] text-center whitespace-nowrap ${
                      done ? "text-[#3F4064] font-medium" : "text-[#A1A3A8]"
                    }`}
                  >
                    {isFa ? step.fa : step.en}
                  </span>
                </div>
                {i < steps.length - 1 && (
                  <div
                    className={`flex-1 h-[2px] mx-2 mb-6 ${
                      i < statusIndex ? "bg-[#22C55E]" : "bg-[#E0E0E2]"
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Items */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] mb-4">
          {isFa ? "محصولات سفارش" : "Order Items"}
        </h3>
        <div className="space-y-3">
          {lines.map((line, i) => (
            <div
              key={i}
              className="flex items-center gap-3 pb-3 border-b border-[#F5F5F5] last:border-0 last:pb-0"
            >
              <Link
                href={`/${locale}/product/${line.product.slug}`}
                className="w-14 h-14 rounded-lg bg-[#F5F5F5] overflow-hidden relative shrink-0"
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
                  className="text-[13px] text-[#3F4064] line-clamp-1 hover:text-[#EF4056]"
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
                <div className="text-[13px] font-bold text-[#3F4064]">
                  {formatPrice(line.priceAtPurchase * line.quantity, locale)}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Total */}
        <div className="border-t border-[#E0E0E2] mt-4 pt-4 flex justify-between items-center">
          <span className="text-[14px] font-bold text-[#3F4064]">
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
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] mb-3 flex items-center gap-2">
          <MapPin size={16} className="text-[#EF4056]" />
          {isFa ? "آدرس ارسال" : "Shipping Address"}
        </h3>
        <p className="text-[12px] text-[#62666D] leading-6">
          {order.shippingAddress}
        </p>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/account/WishlistView.tsx
# ============================================================
files.append(("components/account/WishlistView.tsx", """"use client";

import { useEffect, useState } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useWishlistStore } from "@/lib/stores";
import ProductCard from "@/components/product/ProductCard";
import { EmptyState } from "@/components/common";

interface WishlistViewProps {
  locale: Locale;
}

export default function WishlistView({ locale }: WishlistViewProps) {
  const isFa = locale === "fa";
  const ids = useWishlistStore((s) => s.ids);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const items: Product[] = ids
    .map((id) => allProducts.find((p) => p.id === id))
    .filter((p): p is Product => p !== undefined);

  if (!mounted) {
    return (
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="space-y-3">
        <h1 className="text-[18px] font-bold text-[#3F4064]">
          {isFa ? "علاقه‌مندی‌ها" : "Wishlist"}
        </h1>
        <div className="bg-white rounded-lg border border-[#E0E0E2]">
          <EmptyState
            locale={locale}
            titleFa="لیست علاقه‌مندی‌ها خالی است"
            titleEn="Your wishlist is empty"
            messageFa="محصولات مورد علاقه خود را با کلیک روی آیکون قلب اضافه کنید."
            messageEn="Add products to your wishlist by clicking the heart icon."
          />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-[18px] font-bold text-[#3F4064]">
          {isFa ? "علاقه‌مندی‌ها" : "Wishlist"}
        </h1>
        <span className="text-[12px] text-[#A1A3A8]">
          {isFa
            ? `${items.length.toLocaleString("fa-IR")} کالا`
            : `${items.length} items`}
        </span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {items.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            locale={locale}
          />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/account/AddressesView.tsx
# ============================================================
files.append(("components/account/AddressesView.tsx", """"use client";

import { useState } from "react";
import { MapPin, Plus, Trash2, Edit2, X, Check } from "lucide-react";
import type { Locale } from "@/lib/types";
import { iranProvinces, getCitiesByProvince } from "@/lib/data/iran-provinces";

interface Address {
  id: string;
  fullName: string;
  mobile: string;
  province: string;
  city: string;
  postalCode: string;
  address: string;
  isDefault: boolean;
}

interface AddressesViewProps {
  locale: Locale;
}

export default function AddressesView({ locale }: AddressesViewProps) {
  const isFa = locale === "fa";

  const [addresses, setAddresses] = useState<Address[]>([
    {
      id: "addr-1",
      fullName: isFa ? "علی محمدی" : "Ali Mohammadi",
      mobile: "09123456789",
      province: "tehran",
      city: "tehran",
      postalCode: "1234567890",
      address: isFa
        ? "تهران، خیابان ولیعصر، پلاک ۱۲۳، واحد ۴"
        : "Tehran, Valiasr St., No. 123, Unit 4",
      isDefault: true,
    },
  ]);

  const [editing, setEditing] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const t = {
    title: isFa ? "آدرس‌های من" : "My Addresses",
    add: isFa ? "افزودن آدرس جدید" : "Add New Address",
    edit: isFa ? "ویرایش" : "Edit",
    delete: isFa ? "حذف" : "Delete",
    default: isFa ? "پیش‌فرض" : "Default",
    setDefault: isFa ? "انتخاب به عنوان پیش‌فرض" : "Set as default",
    noAddress: isFa ? "آدرسی ثبت نشده" : "No addresses yet",
    fullName: isFa ? "نام گیرنده" : "Recipient Name",
    mobile: isFa ? "شماره موبایل" : "Mobile",
    province: isFa ? "استان" : "Province",
    city: isFa ? "شهر" : "City",
    postalCode: isFa ? "کد پستی" : "Postal Code",
    address: isFa ? "آدرس کامل" : "Full Address",
    save: isFa ? "ذخیره" : "Save",
    cancel: isFa ? "انصراف" : "Cancel",
  };

  const removeAddress = (id: string) => {
    setAddresses((prev) => prev.filter((a) => a.id !== id));
  };

  const setDefault = (id: string) => {
    setAddresses((prev) =>
      prev.map((a) => ({ ...a, isDefault: a.id === id }))
    );
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-[18px] font-bold text-[#3F4064]">{t.title}</h1>
        <button
          onClick={() => setShowForm(true)}
          className="h-9 px-4 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-1"
        >
          <Plus size={14} />
          {t.add}
        </button>
      </div>

      {addresses.length === 0 ? (
        <div className="bg-white rounded-lg border border-[#E0E0E2] p-8 text-center">
          <MapPin size={36} className="text-[#A1A3A8] mx-auto mb-3" />
          <p className="text-[13px] text-[#62666D]">{t.noAddress}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {addresses.map((addr) => {
            const province = iranProvinces.find((p) => p.id === addr.province);
            const city = province?.cities.find((c) => c.id === addr.city);
            return (
              <div
                key={addr.id}
                className="bg-white rounded-lg border border-[#E0E0E2] p-4"
              >
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-bold text-[#3F4064]">
                      {addr.fullName}
                    </span>
                    {addr.isDefault && (
                      <span className="text-[10px] bg-[#22C55E]/10 text-[#22C55E] px-2 py-0.5 rounded-full font-medium">
                        {t.default}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => setDefault(addr.id)}
                      className="w-7 h-7 rounded-lg flex items-center justify-center text-[#22C55E] hover:bg-[#F5F5F5] transition-colors"
                      title={t.setDefault}
                    >
                      <Check size={14} />
                    </button>
                    <button
                      onClick={() => removeAddress(addr.id)}
                      className="w-7 h-7 rounded-lg flex items-center justify-center text-[#EF4444] hover:bg-[#F5F5F5] transition-colors"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>

                <div className="text-[12px] text-[#62666D] leading-6 space-y-0.5">
                  <div>
                    <span className="text-[#A1A3A8]">
                      {isFa ? "موبایل: " : "Mobile: "}
                    </span>
                    <span dir="ltr">{addr.mobile}</span>
                  </div>
                  <div>
                    <span className="text-[#A1A3A8]">
                      {isFa ? "آدرس: " : "Address: "}
                    </span>
                    {isFa ? province?.nameFa : province?.nameEn},{" "}
                    {isFa ? city?.nameFa : city?.nameEn} — {addr.address}
                  </div>
                  <div>
                    <span className="text-[#A1A3A8]">
                      {isFa ? "کد پستی: " : "Postal: "}
                    </span>
                    <span dir="ltr">{addr.postalCode}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* New address modal */}
      {showForm && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setShowForm(false)}
          />
          <div className="relative bg-white rounded-lg max-w-lg w-full max-h-[90vh] overflow-y-auto p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-[16px] font-bold text-[#3F4064]">
                {t.add}
              </h3>
              <button onClick={() => setShowForm(false)}>
                <X size={20} className="text-[#62666D]" />
              </button>
            </div>
            <p className="text-[12px] text-[#A1A3A8] text-center py-8">
              {isFa
                ? "فرم آدرس در این نسخه دمو قابلیت ذخیره‌سازی ندارد."
                : "This form doesn't save in the demo version."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/account/ProfileView.tsx
# ============================================================
files.append(("components/account/ProfileView.tsx", """"use client";

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
"""))

# ============================================================
# components/account/index.ts
# ============================================================
files.append(("components/account/index.ts", """// components/account/index.ts
export { default as AccountSidebar } from "./AccountSidebar";
export { default as DashboardView } from "./DashboardView";
export { default as OrdersView } from "./OrdersView";
export { default as OrderDetailView } from "./OrderDetailView";
export { default as WishlistView } from "./WishlistView";
export { default as AddressesView } from "./AddressesView";
export { default as ProfileView } from "./ProfileView";
export { default as OrderStatusBadge } from "./OrderStatusBadge";
"""))

# ============================================================
# components/account/AccountGuard.tsx
# ============================================================
files.append(("components/account/AccountGuard.tsx", """"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { Locale } from "@/lib/types";
import { useAuthStore } from "@/lib/stores";

interface AccountGuardProps {
  locale: Locale;
  children: React.ReactNode;
}

export default function AccountGuard({ locale, children }: AccountGuardProps) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isAuthenticated) {
      router.replace(`/${locale}/auth/login`);
    }
  }, [mounted, isAuthenticated, router, locale]);

  if (!mounted) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Redirecting to login...
      </div>
    );
  }

  return <>{children}</>;
}
"""))

# ============================================================
# app/[locale]/account/layout.tsx
# ============================================================
files.append(("app/[locale]/account/layout.tsx", """import type { Locale } from "@/lib/types";
import { AccountSidebar, AccountGuard } from "@/components/account";

export default async function AccountLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AccountGuard locale={typedLocale}>
      <div className="max-w-[1400px] mx-auto px-4 py-4">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <div className="lg:col-span-1">
            <AccountSidebar locale={typedLocale} />
          </div>
          <div className="lg:col-span-3">{children}</div>
        </div>
      </div>
    </AccountGuard>
  );
}
"""))

# ============================================================
# app/[locale]/account/page.tsx (Dashboard)
# ============================================================
files.append(("app/[locale]/account/page.tsx", """import type { Locale } from "@/lib/types";
import { DashboardView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AccountPage({ params }: PageProps) {
  const { locale } = await params;
  return <DashboardView locale={locale as Locale} />;
}
"""))

# ============================================================
# app/[locale]/account/orders/page.tsx
# ============================================================
files.append(("app/[locale]/account/orders/page.tsx", """import type { Locale } from "@/lib/types";
import { OrdersView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OrdersPage({ params }: PageProps) {
  const { locale } = await params;
  return <OrdersView locale={locale as Locale} />;
}
"""))

# ============================================================
# app/[locale]/account/orders/[id]/page.tsx
# ============================================================
files.append(("app/[locale]/account/orders/[id]/page.tsx", """import { notFound } from "next/navigation";
import type { Locale } from "@/lib/types";
import { getOrderById } from "@/lib/data";
import { OrderDetailView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string; id: string }>;
}

export default async function OrderDetailPage({ params }: PageProps) {
  const { locale, id } = await params;
  const order = getOrderById(id);
  if (!order) notFound();
  return <OrderDetailView locale={locale as Locale} order={order} />;
}
"""))

# ============================================================
# app/[locale]/account/wishlist/page.tsx
# ============================================================
files.append(("app/[locale]/account/wishlist/page.tsx", """import type { Locale } from "@/lib/types";
import { WishlistView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function WishlistPage({ params }: PageProps) {
  const { locale } = await params;
  return <WishlistView locale={locale as Locale} />;
}
"""))

# ============================================================
# app/[locale]/account/addresses/page.tsx
# ============================================================
files.append(("app/[locale]/account/addresses/page.tsx", """import type { Locale } from "@/lib/types";
import { AddressesView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AddressesPage({ params }: PageProps) {
  const { locale } = await params;
  return <AddressesView locale={locale as Locale} />;
}
"""))

# ============================================================
# app/[locale]/account/profile/page.tsx
# ============================================================
files.append(("app/[locale]/account/profile/page.tsx", """import type { Locale } from "@/lib/types";
import { ProfileView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ProfilePage({ params }: PageProps) {
  const { locale } = await params;
  return <ProfileView locale={locale as Locale} />;
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 14: Account")
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
        print("  1) Login: http://localhost:3000/fa/auth/login")
        print("  2) Account: http://localhost:3000/fa/account")
        print("  3) Orders: http://localhost:3000/fa/account/orders")
        print("\nNext: run 15_search.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()