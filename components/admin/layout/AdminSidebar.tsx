"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronDown,
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
      {/* ═══ Header ═══ */}
      <div
        className={`h-16 flex items-center border-b border-[#2A2A2E] relative shrink-0 ${
          collapsed ? "justify-center px-2" : "justify-between px-3"
        }`}
      >
        {/* Logo — shown when expanded */}
        {!collapsed && (
          <Link
            href={`/${locale}/admin`}
            className="flex items-center gap-2 overflow-hidden"
            onClick={() => setMobileOpen(false)}
          >
            <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[#EF4056] to-[#d63850] flex items-center justify-center shrink-0 shadow-lg">
              <span className="text-white font-black text-[16px]">S</span>
            </div>
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
          </Link>
        )}

        {/* Collapse button — shown when expanded */}
        {!collapsed && !mobileOpen && (
          <button
            onClick={toggleSidebar}
            className="hidden lg:flex w-8 h-8 items-center justify-center rounded-lg text-white/50 hover:text-white hover:bg-white/5 transition-colors"
            aria-label="Collapse sidebar"
            title={isFa ? "جمع کردن" : "Collapse"}
          >
            <PanelLeftClose size={16} />
          </button>
        )}

        {/* Expand button — shown when collapsed */}
        {collapsed && (
          <button
            onClick={toggleSidebar}
            className="hidden lg:flex w-10 h-10 items-center justify-center rounded-lg bg-gradient-to-br from-[#EF4056] to-[#d63850] text-white shadow-lg hover:scale-105 transition-transform"
            aria-label="Expand sidebar"
            title={isFa ? "باز کردن" : "Expand"}
          >
            <PanelLeftOpen size={18} />
          </button>
        )}

        {/* Mobile close button */}
        {mobileOpen && (
          <button
            onClick={() => setMobileOpen(false)}
            className="text-white/60 hover:text-white lg:hidden"
            aria-label="Close menu"
          >
            <X size={20} />
          </button>
        )}
      </div>

      {/* ═══ User card ═══ */}
      {!collapsed && (
        <div className="p-3 border-b border-[#2A2A2E] shrink-0">
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

      {/* ═══ Navigation ═══ */}
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto overflow-x-hidden">
        {ADMIN_NAV.map((navItem) => (
          <NavItem
            key={navItem.id}
            item={navItem}
            locale={locale}
            collapsed={collapsed}
            isActive={isActive}
            expanded={!!expanded[navItem.id]}
            onToggleExpand={() => toggleExpand(navItem.id)}
            onNavigate={() => setMobileOpen(false)}
          />
        ))}
      </nav>

      {/* ═══ Footer ═══ */}
      <div className="p-3 border-t border-[#2A2A2E] space-y-1 shrink-0">
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
                const childIsActive = isActive(child.href, child.exact);
                return (
                  <li key={child.id}>
                    <Link
                      href={`/${locale}${child.href}`}
                      onClick={onNavigate}
                      className={`flex items-center gap-2 px-3 py-2 rounded-lg text-[12px] transition-colors ${
                        childIsActive
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
      {!collapsed &&
        item.badge !== undefined &&
        typeof item.badge === "number" &&
        item.badge > 0 && (
          <span
            className={`text-[10px] rounded-full min-w-[20px] h-5 px-1.5 flex items-center justify-center font-bold shrink-0 ${
              active ? "bg-white text-[#EF4056]" : "bg-[#EF4056] text-white"
            }`}
          >
            {item.badge}
          </span>
        )}
    </Link>
  );
}