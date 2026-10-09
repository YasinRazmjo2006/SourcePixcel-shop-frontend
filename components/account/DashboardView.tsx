"use client";
import Link from "next/link";
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
