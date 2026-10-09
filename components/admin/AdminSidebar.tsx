"use client";

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
