# 39_admin_layout.py
# Step 2: Admin Layout — sidebar, topbar, breadcrumb, command palette
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/admin-ui.ts — UI state for admin panel
# ============================================================
files.append(("lib/stores/admin-ui.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface AdminUIState {
  sidebarCollapsed: boolean;
  mobileSidebarOpen: boolean;
  commandPaletteOpen: boolean;
  toggleSidebar: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setMobileSidebarOpen: (open: boolean) => void;
  setCommandPaletteOpen: (open: boolean) => void;
}

export const useAdminUIStore = create<AdminUIState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      mobileSidebarOpen: false,
      commandPaletteOpen: false,
      toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) =>
        set({ sidebarCollapsed: collapsed }),
      setMobileSidebarOpen: (open) => set({ mobileSidebarOpen: open }),
      setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
    }),
    {
      name: "sourcepixcel-admin-ui",
      partialize: (state) => ({
        sidebarCollapsed: state.sidebarCollapsed,
      }),
    }
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
export { useAdminUIStore } from "./admin-ui";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
"""))

# ============================================================
# lib/admin-nav.ts — admin navigation config
# ============================================================
files.append(("lib/admin-nav.ts", """// lib/admin-nav.ts
import {
  LayoutDashboard,
  BarChart3,
  Package,
  ShoppingCart,
  Users,
  Tag,
  Star,
  FileText,
  Settings,
  Layers,
  type LucideIcon,
} from "lucide-react";

export interface AdminNavItem {
  id: string;
  href: string;
  labelFa: string;
  labelEn: string;
  icon: LucideIcon;
  badge?: number | "dynamic";
  children?: AdminNavItem[];
  exact?: boolean;
}

export const ADMIN_NAV: AdminNavItem[] = [
  {
    id: "dashboard",
    href: "/admin",
    labelFa: "داشبورد",
    labelEn: "Dashboard",
    icon: LayoutDashboard,
    exact: true,
  },
  {
    id: "analytics",
    href: "/admin/analytics",
    labelFa: "آنالیتیکس",
    labelEn: "Analytics",
    icon: BarChart3,
  },
  {
    id: "products",
    href: "/admin/products",
    labelFa: "محصولات",
    labelEn: "Products",
    icon: Package,
    children: [
      {
        id: "products-list",
        href: "/admin/products",
        labelFa: "لیست محصولات",
        labelEn: "Products List",
        icon: Package,
        exact: true,
      },
      {
        id: "categories",
        href: "/admin/categories",
        labelFa: "دسته‌بندی‌ها",
        labelEn: "Categories",
        icon: Layers,
      },
    ],
  },
  {
    id: "orders",
    href: "/admin/orders",
    labelFa: "سفارشات",
    labelEn: "Orders",
    icon: ShoppingCart,
    badge: 4,
  },
  {
    id: "users",
    href: "/admin/users",
    labelFa: "کاربران",
    labelEn: "Users",
    icon: Users,
  },
  {
    id: "discounts",
    href: "/admin/discounts",
    labelFa: "تخفیف‌ها",
    labelEn: "Discounts",
    icon: Tag,
  },
  {
    id: "reviews",
    href: "/admin/reviews",
    labelFa: "نظرات",
    labelEn: "Reviews",
    icon: Star,
  },
  {
    id: "reports",
    href: "/admin/reports",
    labelFa: "گزارشات",
    labelEn: "Reports",
    icon: FileText,
  },
  {
    id: "settings",
    href: "/admin/settings",
    labelFa: "تنظیمات",
    labelEn: "Settings",
    icon: Settings,
  },
];

// Flatten nav for command palette
export interface FlatNavItem {
  id: string;
  href: string;
  labelFa: string;
  labelEn: string;
  icon: LucideIcon;
}

export const FLAT_ADMIN_NAV: FlatNavItem[] = ADMIN_NAV.flatMap((item) => {
  const self = {
    id: item.id,
    href: item.href,
    labelFa: item.labelFa,
    labelEn: item.labelEn,
    icon: item.icon,
  };
  const children = (item.children ?? []).map((child) => ({
    id: child.id,
    href: child.href,
    labelFa: child.labelFa,
    labelEn: child.labelEn,
    icon: child.icon,
  }));
  return [self, ...children];
});
"""))

# ============================================================
# components/admin/layout/AdminSidebar.tsx — upgraded
# ============================================================
files.append(("components/admin/layout/AdminSidebar.tsx", """"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronDown,
  ChevronLeft,
  LogOut,
  Home,
  X,
  PanelLeftClose,
  PanelLeftOpen,
} from "lucide-react";
import { useAdminStore, useAdminUIStore } from "@/lib/stores";
import { ADMIN_NAV, type AdminNavItem } from "@/lib/admin-nav";

interface AdminSidebarProps {
  locale: string;
}

export default function AdminSidebar({ locale }: AdminSidebarProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const router = useRouter();

  const adminName = useAdminStore((s) => s.adminName);
  const logout = useAdminStore((s) => s.logout);

  const collapsed = useAdminUIStore((s) => s.sidebarCollapsed);
  const mobileOpen = useAdminUIStore((s) => s.mobileSidebarOpen);
  const toggleSidebar = useAdminUIStore((s) => s.toggleSidebar);
  const setMobileOpen = useAdminUIStore((s) => s.setMobileSidebarOpen);

  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const isActive = (href: string, exact?: boolean) => {
    const full = `/${locale}${href}`;
    if (exact) return pathname === full;
    return pathname.startsWith(full);
  };

  const toggleExpand = (id: string) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const handleLogout = () => {
    logout();
    router.push(`/${locale}/admin/login`);
  };

  const sidebarContent = (
    <>
      {/* Header */}
      <div
        className={`h-16 flex items-center border-b border-[#2A2A2E] px-3 ${
          collapsed ? "justify-center" : "justify-between"
        }`}
      >
        <Link
          href={`/${locale}/admin`}
          className="flex items-center gap-2 overflow-hidden"
          onClick={() => setMobileOpen(false)}
        >
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[#EF4056] to-[#d63850] flex items-center justify-center shrink-0 shadow-lg">
            <span className="text-white font-black text-[16px]">S</span>
          </div>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              className="leading-tight"
            >
              <div className="text-[13px] font-bold text-white whitespace-nowrap">
                SourcePixcel
              </div>
              <div className="text-[9px] text-white/40 whitespace-nowrap">
                {isFa ? "پنل مدیریت" : "Admin Panel"}
              </div>
            </motion.div>
          )}
        </Link>

        {mobileOpen && (
          <button
            onClick={() => setMobileOpen(false)}
            className="text-white/60 hover:text-white lg:hidden"
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        )}

        {!mobileOpen && !collapsed && (
          <button
            onClick={toggleSidebar}
            className="hidden lg:flex text-white/50 hover:text-white transition-colors"
            aria-label="Collapse sidebar"
          >
            <PanelLeftClose size={16} />
          </button>
        )}

        {!mobileOpen && collapsed && (
          <button
            onClick={toggleSidebar}
            className="hidden lg:flex text-white/50 hover:text-white transition-colors absolute top-5 left-1/2 -translate-x-1/2"
            aria-label="Expand sidebar"
            style={{ display: "none" }}
          >
            <PanelLeftOpen size={16} />
          </button>
        )}
      </div>

      {/* User card */}
      {!collapsed && (
        <div className="p-3 border-b border-[#2A2A2E]">
          <div className="flex items-center gap-3 px-2 py-2 rounded-xl bg-white/[0.03] border border-white/5">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#EF4056] to-[#d63850] flex items-center justify-center text-white font-bold text-[13px] shrink-0">
              {adminName?.[0] ?? "A"}
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-[12px] font-bold text-white truncate">
                {adminName ?? "Admin"}
              </div>
              <div className="text-[10px] text-emerald-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                {isFa ? "آنلاین" : "Online"}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto overflow-x-hidden">
        {ADMIN_NAV.map((item) => (
          <NavItem
            key={item.id}
            item={item}
            locale={locale}
            collapsed={collapsed}
            isActive={isActive}
            expanded={!!expanded[item.id]}
            onToggleExpand={() => toggleExpand(item.id)}
            onNavigate={() => setMobileOpen(false)}
          />
        ))}
      </nav>

      {/* Footer */}
      <div className="p-3 border-t border-[#2A2A2E] space-y-1">
        <Link
          href={`/${locale}`}
          onClick={() => setMobileOpen(false)}
          className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] text-white/70 hover:bg-white/5 hover:text-white transition-colors ${
            collapsed ? "justify-center" : ""
          }`}
        >
          <Home size={16} className="shrink-0" />
          {!collapsed && <span>{isFa ? "بازگشت به سایت" : "Back to store"}</span>}
        </Link>
        <button
          onClick={handleLogout}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] text-red-400 hover:bg-red-500/10 transition-colors ${
            collapsed ? "justify-center" : ""
          }`}
        >
          <LogOut size={16} className="shrink-0" />
          {!collapsed && <span>{isFa ? "خروج از حساب" : "Logout"}</span>}
        </button>
      </div>
    </>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside
        className={`hidden lg:flex flex-col bg-[#1A1A1E] border-r border-[#2A2A2E] transition-all duration-300 ease-out shrink-0 relative ${
          collapsed ? "w-20" : "w-64"
        }`}
      >
        {sidebarContent}
      </aside>

      {/* Mobile sidebar */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[90] lg:hidden"
              onClick={() => setMobileOpen(false)}
            />
            <motion.aside
              initial={{ x: isFa ? "100%" : "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: isFa ? "100%" : "-100%" }}
              transition={{ type: "spring", stiffness: 300, damping: 30 }}
              className="fixed top-0 bottom-0 w-72 max-w-[85%] flex flex-col bg-[#1A1A1E] z-[100] lg:hidden shadow-2xl"
              style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
            >
              {sidebarContent}
            </motion.aside>
          </>
        )}
      </AnimatePresence>
    </>
  );
}

// ═══════════════════════════════════════════════════════════════
// NavItem Component
// ═══════════════════════════════════════════════════════════════

interface NavItemProps {
  item: AdminNavItem;
  locale: string;
  collapsed: boolean;
  isActive: (href: string, exact?: boolean) => boolean;
  expanded: boolean;
  onToggleExpand: () => void;
  onNavigate: () => void;
}

function NavItem({
  item,
  locale,
  collapsed,
  isActive,
  expanded,
  onToggleExpand,
  onNavigate,
}: NavItemProps) {
  const isFa = locale === "fa";
  const Icon = item.icon;
  const active = isActive(item.href, item.exact);
  const hasChildren = (item.children ?? []).length > 0;
  const childActive = hasChildren
    ? item.children!.some((c) => isActive(c.href, c.exact))
    : false;

  const baseClasses = `group flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-[13px] transition-all ${
    active || childActive
      ? "bg-[#EF4056] text-white font-medium shadow-lg shadow-[#EF4056]/20"
      : "text-white/70 hover:bg-white/5 hover:text-white"
  } ${collapsed ? "justify-center" : ""}`;

  if (hasChildren && !collapsed) {
    return (
      <div>
        <button
          onClick={onToggleExpand}
          className={`w-full ${baseClasses}`}
          aria-expanded={expanded}
        >
          <div className="flex items-center gap-3 min-w-0">
            <Icon size={16} className="shrink-0" />
            <span className="truncate">{isFa ? item.labelFa : item.labelEn}</span>
          </div>
          <motion.div
            animate={{ rotate: expanded ? 180 : 0 }}
            transition={{ duration: 0.2 }}
          >
            <ChevronDown size={14} />
          </motion.div>
        </button>
        <AnimatePresence>
          {expanded && (
            <motion.ul
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="overflow-hidden list-none m-0 p-0 mt-1 ml-4 border-l border-white/10 space-y-0.5 pl-2"
            >
              {item.children!.map((child) => {
                const ChildIcon = child.icon;
                const childActive = isActive(child.href, child.exact);
                return (
                  <li key={child.id}>
                    <Link
                      href={`/${locale}${child.href}`}
                      onClick={onNavigate}
                      className={`flex items-center gap-2 px-3 py-2 rounded-lg text-[12px] transition-colors ${
                        childActive
                          ? "text-[#EF4056] font-medium bg-[#EF4056]/5"
                          : "text-white/50 hover:text-white hover:bg-white/5"
                      }`}
                    >
                      <ChildIcon size={14} />
                      <span className="truncate">
                        {isFa ? child.labelFa : child.labelEn}
                      </span>
                    </Link>
                  </li>
                );
              })}
            </motion.ul>
          )}
        </AnimatePresence>
      </div>
    );
  }

  return (
    <Link
      href={`/${locale}${item.href}`}
      onClick={onNavigate}
      className={baseClasses}
      title={collapsed ? (isFa ? item.labelFa : item.labelEn) : undefined}
    >
      <div className="flex items-center gap-3 min-w-0">
        <Icon size={16} className="shrink-0" />
        {!collapsed && (
          <span className="truncate">{isFa ? item.labelFa : item.labelEn}</span>
        )}
      </div>
      {!collapsed && item.badge !== undefined && typeof item.badge === "number" && item.badge > 0 && (
        <span
          className={`text-[10px] rounded-full min-w-[20px] h-5 px-1.5 flex items-center justify-center font-bold shrink-0 ${
            active
              ? "bg-white text-[#EF4056]"
              : "bg-[#EF4056] text-white"
          }`}
        >
          {item.badge}
        </span>
      )}
    </Link>
  );
}
"""))

# ============================================================
# components/admin/layout/AdminTopbar.tsx
# ============================================================
files.append(("components/admin/layout/AdminTopbar.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Menu,
  Search,
  Bell,
  Sun,
  Moon,
  ExternalLink,
  ChevronDown,
  User as UserIcon,
  LogOut,
  Settings as SettingsIcon,
  Command,
} from "lucide-react";
import { useAdminStore, useAdminUIStore, useThemeStore, useNotificationsStore } from "@/lib/stores";

interface AdminTopbarProps {
  locale: string;
}

export default function AdminTopbar({ locale }: AdminTopbarProps) {
  const isFa = locale === "fa";
  const router = useRouter();

  const adminName = useAdminStore((s) => s.adminName);
  const logout = useAdminStore((s) => s.logout);

  const setMobileOpen = useAdminUIStore((s) => s.setMobileSidebarOpen);
  const setCommandPaletteOpen = useAdminUIStore((s) => s.setCommandPaletteOpen);

  const mode = useThemeStore((s) => s.mode);
  const toggleTheme = useThemeStore((s) => s.toggle);

  const unreadCount = useNotificationsStore((s) => s.items.filter((n) => !n.read).length);

  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleLogout = () => {
    logout();
    router.push(`/${locale}/admin/login`);
  };

  return (
    <header className="h-16 bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center gap-3 px-4 shrink-0 sticky top-0 z-40 backdrop-blur-md bg-white/95 dark:bg-[#1A1A1E]/95">
      {/* Mobile menu toggle */}
      <button
        onClick={() => setMobileOpen(true)}
        className="lg:hidden w-9 h-9 rounded-lg flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
        aria-label="Open menu"
      >
        <Menu size={20} />
      </button>

      {/* Search / Command Palette trigger */}
      <button
        onClick={() => setCommandPaletteOpen(true)}
        className="flex items-center gap-2 h-9 px-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-transparent hover:border-[#EF4056] text-[#A1A3A8] text-[12px] transition-colors group flex-1 max-w-sm"
      >
        <Search size={14} className="shrink-0" />
        <span className="truncate flex-1 text-start">
          {isFa ? "جستجو یا پرش سریع..." : "Search or jump to..."}
        </span>
        <kbd className="hidden md:inline-flex items-center gap-0.5 text-[10px] font-mono bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] px-1.5 py-0.5 rounded shrink-0">
          <Command size={10} />K
        </kbd>
      </button>

      <div className="flex-1" />

      {/* View store */}
      <Link
        href={`/${locale}`}
        target="_blank"
        className="hidden md:flex items-center gap-1.5 h-9 px-3 rounded-lg text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
      >
        <ExternalLink size={14} />
        <span>{isFa ? "مشاهده فروشگاه" : "View store"}</span>
      </Link>

      {/* Theme toggle */}
      <button
        onClick={toggleTheme}
        aria-label="Toggle theme"
        className="w-9 h-9 rounded-lg flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
      >
        {mounted && (mode === "dark" ? <Sun size={16} /> : <Moon size={16} />)}
      </button>

      {/* Notifications */}
      <Link
        href={`/${locale}/admin/orders`}
        className="relative w-9 h-9 rounded-lg flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
        aria-label="Notifications"
      >
        <Bell size={16} />
        {mounted && unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-4 h-4 rounded-full bg-[#EF4056] text-white text-[9px] font-bold flex items-center justify-center">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </Link>

      {/* Divider */}
      <div className="w-px h-6 bg-[#E0E0E2] dark:bg-[#2A2A2E]" />

      {/* User menu */}
      <div className="relative">
        <button
          onClick={() => setUserMenuOpen((v) => !v)}
          className="flex items-center gap-2 h-9 pl-1 pr-2 rounded-lg hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
        >
          <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#EF4056] to-[#d63850] flex items-center justify-center text-white text-[11px] font-bold shrink-0">
            {adminName?.[0] ?? "A"}
          </div>
          <span className="hidden md:block text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
            {adminName ?? "Admin"}
          </span>
          <ChevronDown size={12} className="text-[#A1A3A8] hidden md:block" />
        </button>

        <AnimatePresence>
          {userMenuOpen && (
            <>
              <div
                className="fixed inset-0 z-[50]"
                onClick={() => setUserMenuOpen(false)}
              />
              <motion.div
                initial={{ opacity: 0, y: -8, scale: 0.96 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -8, scale: 0.96 }}
                transition={{ duration: 0.15 }}
                className={`absolute top-full mt-2 w-56 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl shadow-2xl overflow-hidden z-[60] ${
                  isFa ? "left-0" : "right-0"
                }`}
              >
                <div className="p-3 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
                  <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                    {adminName ?? "Admin"}
                  </div>
                  <div className="text-[10px] text-[#A1A3A8]">
                    {isFa ? "مدیر سیستم" : "Administrator"}
                  </div>
                </div>
                <div className="p-1.5">
                  <Link
                    href={`/${locale}/admin/settings`}
                    onClick={() => setUserMenuOpen(false)}
                    className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
                  >
                    <UserIcon size={14} />
                    {isFa ? "پروفایل" : "Profile"}
                  </Link>
                  <Link
                    href={`/${locale}/admin/settings`}
                    onClick={() => setUserMenuOpen(false)}
                    className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
                  >
                    <SettingsIcon size={14} />
                    {isFa ? "تنظیمات" : "Settings"}
                  </Link>
                  <div className="my-1 border-t border-[#E0E0E2] dark:border-[#2A2A2E]" />
                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-[12px] text-red-500 hover:bg-red-500/10 transition-colors"
                  >
                    <LogOut size={14} />
                    {isFa ? "خروج از حساب" : "Logout"}
                  </button>
                </div>
              </motion.div>
            </>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
}
"""))

# ============================================================
# components/admin/layout/AdminBreadcrumb.tsx
# ============================================================
files.append(("components/admin/layout/AdminBreadcrumb.tsx", """"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronLeft, ChevronRight, Home } from "lucide-react";

interface AdminBreadcrumbProps {
  locale: string;
}

const SEGMENT_LABELS: Record<string, { fa: string; en: string }> = {
  admin: { fa: "پنل مدیریت", en: "Admin" },
  analytics: { fa: "آنالیتیکس", en: "Analytics" },
  products: { fa: "محصولات", en: "Products" },
  categories: { fa: "دسته‌بندی‌ها", en: "Categories" },
  orders: { fa: "سفارشات", en: "Orders" },
  users: { fa: "کاربران", en: "Users" },
  discounts: { fa: "تخفیف‌ها", en: "Discounts" },
  reviews: { fa: "نظرات", en: "Reviews" },
  reports: { fa: "گزارشات", en: "Reports" },
  settings: { fa: "تنظیمات", en: "Settings" },
  new: { fa: "جدید", en: "New" },
  edit: { fa: "ویرایش", en: "Edit" },
};

export default function AdminBreadcrumb({ locale }: AdminBreadcrumbProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();

  // Split pathname and remove locale
  const segments = pathname
    .split("/")
    .filter(Boolean)
    .filter((s) => s !== locale);

  const breadcrumbs = segments.map((segment, idx) => {
    const href = "/" + segments.slice(0, idx + 1).join("/");
    const label = SEGMENT_LABELS[segment];
    const isLast = idx === segments.length - 1;

    // Skip numeric segments (IDs) — replace with generic label
    const isNumeric = /^\\d+$/.test(segment) || segment.startsWith("SP-");

    return {
      href: `/${locale}${href}`,
      labelFa: isNumeric ? `#${segment}` : (label?.fa ?? segment),
      labelEn: isNumeric ? `#${segment}` : (label?.en ?? segment),
      isLast,
    };
  });

  if (breadcrumbs.length === 0) return null;

  return (
    <nav
      aria-label="Breadcrumb"
      className="flex items-center gap-1.5 text-[12px] text-[#62666D] dark:text-[#A1A3A8] flex-wrap"
    >
      <Link
        href={`/${locale}/admin`}
        className="flex items-center gap-1 hover:text-[#EF4056] transition-colors"
      >
        <Home size={12} />
        <span>{isFa ? "پنل" : "Admin"}</span>
      </Link>

      {breadcrumbs.slice(1).map((crumb, i) => (
        <div key={i} className="flex items-center gap-1.5">
          {isFa ? (
            <ChevronLeft size={12} className="text-[#A1A3A8]" />
          ) : (
            <ChevronRight size={12} className="text-[#A1A3A8]" />
          )}
          {crumb.isLast ? (
            <span className="font-medium text-[#3F4064] dark:text-[#E5E5EA]">
              {isFa ? crumb.labelFa : crumb.labelEn}
            </span>
          ) : (
            <Link
              href={crumb.href}
              className="hover:text-[#EF4056] transition-colors"
            >
              {isFa ? crumb.labelFa : crumb.labelEn}
            </Link>
          )}
        </div>
      ))}
    </nav>
  );
}
"""))

# ============================================================
# components/admin/layout/CommandPalette.tsx
# ============================================================
files.append(("components/admin/layout/CommandPalette.tsx", """"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  ArrowRight,
  ArrowLeft,
  CornerDownLeft,
  X,
  Sparkles,
} from "lucide-react";
import { useAdminUIStore } from "@/lib/stores";
import { FLAT_ADMIN_NAV } from "@/lib/admin-nav";

interface CommandPaletteProps {
  locale: string;
}

export default function CommandPalette({ locale }: CommandPaletteProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const open = useAdminUIStore((s) => s.commandPaletteOpen);
  const setOpen = useAdminUIStore((s) => s.setCommandPaletteOpen);

  const [query, setQuery] = useState("");
  const [highlighted, setHighlighted] = useState(0);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return FLAT_ADMIN_NAV;
    return FLAT_ADMIN_NAV.filter(
      (item) =>
        item.labelFa.toLowerCase().includes(q) ||
        item.labelEn.toLowerCase().includes(q) ||
        item.href.toLowerCase().includes(q)
    );
  }, [query]);

  // Reset on open
  useEffect(() => {
    if (open) {
      setQuery("");
      setHighlighted(0);
    }
  }, [open]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen(!open);
        return;
      }
      if (!open) return;

      if (e.key === "Escape") {
        e.preventDefault();
        setOpen(false);
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        setHighlighted((prev) => (prev + 1) % Math.max(1, filtered.length));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setHighlighted((prev) =>
          prev <= 0 ? Math.max(0, filtered.length - 1) : prev - 1
        );
      } else if (e.key === "Enter" && filtered[highlighted]) {
        e.preventDefault();
        router.push(`/${locale}${filtered[highlighted].href}`);
        setOpen(false);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, filtered, highlighted, router, locale, setOpen]);

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[200]"
            onClick={() => setOpen(false)}
          />
          <div className="fixed inset-0 z-[201] flex items-start justify-center pt-[15vh] px-4 pointer-events-none">
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.96 }}
              transition={{ duration: 0.15 }}
              className="w-full max-w-xl bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-2xl shadow-2xl overflow-hidden pointer-events-auto"
            >
              {/* Search input */}
              <div className="flex items-center gap-3 px-4 h-14 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
                <Search size={18} className="text-[#A1A3A8] shrink-0" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setHighlighted(0);
                  }}
                  placeholder={
                    isFa
                      ? "جستجو در پنل یا پرش به صفحه..."
                      : "Search or jump to..."
                  }
                  className="flex-1 bg-transparent text-[14px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none"
                  autoFocus
                />
                <button
                  onClick={() => setOpen(false)}
                  className="w-7 h-7 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
                  aria-label="Close"
                >
                  <X size={14} />
                </button>
              </div>

              {/* Results */}
              <div className="max-h-[400px] overflow-y-auto p-2">
                {filtered.length === 0 ? (
                  <div className="py-12 text-center">
                    <div className="w-12 h-12 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
                      <Sparkles size={20} className="text-[#A1A3A8]" />
                    </div>
                    <div className="text-[13px] font-medium text-[#3F4064] dark:text-[#E5E5EA] mb-1">
                      {isFa ? "نتیجه‌ای یافت نشد" : "No results found"}
                    </div>
                    <div className="text-[11px] text-[#A1A3A8]">
                      {isFa
                        ? "عبارت دیگری را امتحان کنید"
                        : "Try a different keyword"}
                    </div>
                  </div>
                ) : (
                  <ul className="list-none m-0 p-0 space-y-0.5">
                    {filtered.map((item, idx) => {
                      const Icon = item.icon;
                      const isHighlighted = idx === highlighted;
                      return (
                        <li key={item.id}>
                          <button
                            onMouseEnter={() => setHighlighted(idx)}
                            onClick={() => {
                              router.push(`/${locale}${item.href}`);
                              setOpen(false);
                            }}
                            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-start transition-colors ${
                              isHighlighted
                                ? "bg-[#EF4056] text-white"
                                : "text-[#3F4064] dark:text-[#E5E5EA] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
                            }`}
                          >
                            <Icon
                              size={16}
                              className={
                                isHighlighted
                                  ? "text-white"
                                  : "text-[#62666D] dark:text-[#A1A3A8]"
                              }
                            />
                            <div className="flex-1 min-w-0">
                              <div className="text-[13px] font-medium truncate">
                                {isFa ? item.labelFa : item.labelEn}
                              </div>
                              <div
                                className={`text-[10px] truncate ${
                                  isHighlighted
                                    ? "text-white/70"
                                    : "text-[#A1A3A8]"
                                }`}
                              >
                                /{locale}
                                {item.href}
                              </div>
                            </div>
                            {isHighlighted &&
                              (isFa ? (
                                <ArrowLeft size={14} className="text-white" />
                              ) : (
                                <ArrowRight size={14} className="text-white" />
                              ))}
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </div>

              {/* Footer */}
              <div className="flex items-center justify-between gap-2 px-3 py-2.5 border-t border-[#E0E0E2] dark:border-[#2A2A2E] bg-[#FAFAFA] dark:bg-[#0F0F12]">
                <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8]">
                  <span className="flex items-center gap-1">
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] font-mono text-[9px]">
                      ↑
                    </kbd>
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] font-mono text-[9px]">
                      ↓
                    </kbd>
                    {isFa ? "پیمایش" : "Navigate"}
                  </span>
                  <span className="flex items-center gap-1">
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E]">
                      <CornerDownLeft size={9} />
                    </kbd>
                    {isFa ? "انتخاب" : "Select"}
                  </span>
                  <span className="flex items-center gap-1">
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] font-mono text-[9px]">
                      Esc
                    </kbd>
                    {isFa ? "بستن" : "Close"}
                  </span>
                </div>
                <div className="text-[10px] text-[#A1A3A8] font-mono">
                  {filtered.length} {isFa ? "نتیجه" : "results"}
                </div>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
"""))

# ============================================================
# components/admin/layout/index.ts
# ============================================================
files.append(("components/admin/layout/index.ts", """// components/admin/layout/index.ts
export { default as AdminSidebar } from "./AdminSidebar";
export { default as AdminTopbar } from "./AdminTopbar";
export { default as AdminBreadcrumb } from "./AdminBreadcrumb";
export { default as CommandPalette } from "./CommandPalette";
"""))

# ============================================================
# app/[locale]/admin/layout.tsx — rewritten
# ============================================================
files.append(("app/[locale]/admin/layout.tsx", """import AdminGuard from "@/components/admin/AdminGuard";
import { AdminSidebar, AdminTopbar, CommandPalette } from "@/components/admin/layout";

export default async function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const isLoginPage = false; // handled by AdminGuard redirect

  return (
    <AdminGuard locale={locale}>
      <div className="min-h-screen flex bg-[#F5F5F5] dark:bg-[#0F0F12]">
        <AdminSidebar locale={locale} />

        <div className="flex-1 flex flex-col min-w-0">
          <AdminTopbar locale={locale} />
          <main className="flex-1 p-4 md:p-6">{children}</main>
        </div>

        <CommandPalette locale={locale} />
      </div>
    </AdminGuard>
  );
}
"""))

# ============================================================
# app/[locale]/admin/login/layout.tsx — bypass admin layout
# ============================================================
files.append(("app/[locale]/admin/login/layout.tsx", """export default function AdminLoginLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <>{children}</>;
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 2: Layout")
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
        print("\nNew features:")
        print("  - Collapsible sidebar (toggle button)")
        print("  - Sub-menu support")
        print("  - Mobile drawer with spring animation")
        print("  - Command palette (Ctrl+K)")
        print("  - User dropdown menu")
        print("  - Theme toggle in topbar")
        print("  - Breadcrumb component")
        print("  - Online indicator")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Test:")
        print("     - Ctrl+K → Command palette")
        print("     - Sidebar toggle button")
        print("     - Mobile (resize browser)")
        print("\nNext: Admin Step 3 (Dashboard + Charts)")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()