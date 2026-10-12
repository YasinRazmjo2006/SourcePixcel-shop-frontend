"use client";

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
