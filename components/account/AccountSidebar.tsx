"use client";

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
