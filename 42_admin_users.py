# 42_admin_users.py
# Step 5: Users Management
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# lib/hooks/use-virtual-rows.ts
# ============================================================
files.append(("lib/hooks/use-virtual-rows.ts", '''"use client";

import { useCallback, useRef, useState, useEffect } from "react";

export function useVirtualRows(
  rowCount: number,
  rowHeight: number,
  containerHeight: number,
  overscan = 5
) {
  const [scrollTop, setScrollTop] = useState(0);

  const startIndex = Math.max(0, Math.floor(scrollTop / rowHeight) - overscan);
  const endIndex = Math.min(
    rowCount - 1,
    Math.floor((scrollTop + containerHeight) / rowHeight) + overscan
  );

  const totalHeight = rowCount * rowHeight;

  const handleScroll = useCallback((e: React.UIEvent<HTMLElement>) => {
    setScrollTop(e.currentTarget.scrollTop);
  }, []);

  return {
    startIndex,
    endIndex,
    totalHeight,
    handleScroll,
    offsetY: startIndex * rowHeight,
  };
}
'''))

# ============================================================
# components/admin/users/UserFilters.tsx
# ============================================================
files.append(("components/admin/users/UserFilters.tsx", '''"use client";

import { Search, X } from "lucide-react";
import type { Locale, AdminUserRole } from "@/lib/types";

export interface UserFilterValues {
  query: string;
  role: AdminUserRole | "all";
  status: "all" | "active" | "inactive" | "banned" | "verified";
  sortBy: "newest" | "oldest" | "name" | "spent";
}

interface UserFiltersProps {
  locale: Locale;
  values: UserFilterValues;
  onChange: (values: UserFilterValues) => void;
  resultCount: number;
}

export default function UserFilters({
  locale,
  values,
  onChange,
  resultCount,
}: UserFiltersProps) {
  const isFa = locale === "fa";

  const t = {
    search: isFa ? "جستجو در نام، ایمیل، موبایل..." : "Search name, email, mobile...",
    allRoles: isFa ? "همه نقش‌ها" : "All Roles",
    customer: isFa ? "مشتری" : "Customer",
    admin: isFa ? "مدیر" : "Admin",
    moderator: isFa ? "ناظر" : "Moderator",
    editor: isFa ? "نویسنده" : "Editor",
    allStatus: isFa ? "همه وضعیت‌ها" : "All Status",
    active: isFa ? "فعال" : "Active",
    inactive: isFa ? "غیرفعال" : "Inactive",
    banned: isFa ? "مسدود" : "Banned",
    verified: isFa ? "تایید شده" : "Verified",
    newest: isFa ? "جدیدترین" : "Newest",
    oldest: isFa ? "قدیمی‌ترین" : "Oldest",
    name: isFa ? "نام" : "Name",
    spent: isFa ? "بیشترین خرید" : "Most Spent",
    results: isFa ? "نتیجه" : "results",
    clear: isFa ? "پاک کردن" : "Clear",
  };

  const hasFilters =
    values.query ||
    values.role !== "all" ||
    values.status !== "all";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-3 md:p-4 space-y-3">
      <div className="flex flex-col md:flex-row gap-2 md:gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <input
            type="text"
            value={values.query}
            onChange={(e) => onChange({ ...values, query: e.target.value })}
            placeholder={t.search}
            className="w-full h-10 pr-9 pl-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-transparent focus:border-[#EF4056] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors"
            style={{ paddingRight: isFa ? 36 : 12, paddingLeft: isFa ? 12 : 36 }}
          />
          <Search
            size={14}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "right" : "left"]: 12 }}
          />
        </div>

        {/* Role */}
        <select
          value={values.role}
          onChange={(e) =>
            onChange({ ...values, role: e.target.value as UserFilterValues["role"] })
          }
          className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
        >
          <option value="all">{t.allRoles}</option>
          <option value="customer">{t.customer}</option>
          <option value="admin">{t.admin}</option>
          <option value="moderator">{t.moderator}</option>
          <option value="editor">{t.editor}</option>
        </select>

        {/* Status */}
        <select
          value={values.status}
          onChange={(e) =>
            onChange({ ...values, status: e.target.value as UserFilterValues["status"] })
          }
          className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
        >
          <option value="all">{t.allStatus}</option>
          <option value="active">{t.active}</option>
          <option value="inactive">{t.inactive}</option>
          <option value="banned">{t.banned}</option>
          <option value="verified">{t.verified}</option>
        </select>

        {/* Sort */}
        <select
          value={values.sortBy}
          onChange={(e) =>
            onChange({ ...values, sortBy: e.target.value as UserFilterValues["sortBy"] })
          }
          className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
        >
          <option value="newest">{t.newest}</option>
          <option value="oldest">{t.oldest}</option>
          <option value="name">{t.name}</option>
          <option value="spent">{t.spent}</option>
        </select>
      </div>

      {/* Results + Clear */}
      <div className="flex items-center justify-between">
        <div className="text-[11px] text-[#A1A3A8]">
          {resultCount.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.results}
        </div>
        {hasFilters && (
          <button
            onClick={() =>
              onChange({ query: "", role: "all", status: "all", sortBy: "newest" })
            }
            className="text-[11px] text-[#EF4056] hover:underline flex items-center gap-1"
          >
            <X size={11} />
            {t.clear}
          </button>
        )}
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/users/UserStatusBadge.tsx
# ============================================================
files.append(("components/admin/users/UserStatusBadge.tsx", '''"use client";

import type { Locale, AdminUserRole, AdminUser } from "@/lib/types";

interface UserStatusBadgeProps {
  locale: Locale;
  user: AdminUser;
}

export function UserRoleBadge({ role, locale }: { role: AdminUserRole; locale: Locale }) {
  const isFa = locale === "fa";

  const config: Record<AdminUserRole, { fa: string; en: string; bg: string; text: string }> = {
    customer: { fa: "مشتری", en: "Customer", bg: "#94A3B8", text: "#94A3B8" },
    admin: { fa: "مدیر", en: "Admin", bg: "#EF4056", text: "#EF4056" },
    moderator: { fa: "ناظر", en: "Moderator", bg: "#8B5CF6", text: "#8B5CF6" },
    editor: { fa: "نویسنده", en: "Editor", bg: "#00BFFF", text: "#00BFFF" },
  };

  const c = config[role];
  return (
    <span
      className="text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap"
      style={{ backgroundColor: `${c.bg}15`, color: c.text }}
    >
      {isFa ? c.fa : c.en}
    </span>
  );
}

export default function UserStatusBadge({ locale, user }: UserStatusBadgeProps) {
  const isFa = locale === "fa";

  if (user.isBanned) {
    return (
      <span className="text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap bg-[#EF4444]/10 text-[#EF4444]">
        {isFa ? "مسدود" : "Banned"}
      </span>
    );
  }

  if (!user.isActive) {
    return (
      <span className="text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap bg-[#94A3B8]/10 text-[#94A3B8]">
        {isFa ? "غیرفعال" : "Inactive"}
      </span>
    );
  }

  return (
    <span className="text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap bg-[#22C55E]/10 text-[#22C55E]">
      {isFa ? "فعال" : "Active"}
    </span>
  );
}
'''))

# ============================================================
# components/admin/users/UserDetailDrawer.tsx
# ============================================================
files.append(("components/admin/users/UserDetailDrawer.tsx", '''"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Mail,
  Phone,
  MapPin,
  Calendar,
  ShoppingBag,
  DollarSign,
  Star,
  Ban,
  CheckCircle,
  ShieldCheck,
} from "lucide-react";
import type { Locale, AdminUser } from "@/lib/types";
import { formatPrice, formatDate } from "@/lib/utils";
import { UserRoleBadge } from "./UserStatusBadge";

interface UserDetailDrawerProps {
  locale: Locale;
  user: AdminUser | null;
  onClose: () => void;
}

export default function UserDetailDrawer({
  locale,
  user,
  onClose,
}: UserDetailDrawerProps) {
  const isFa = locale === "fa";

  const t = {
    title: isFa ? "جزئیات کاربر" : "User Details",
    email: isFa ? "ایمیل" : "Email",
    mobile: isFa ? "موبایل" : "Mobile",
    city: isFa ? "شهر" : "City",
    joinDate: isFa ? "تاریخ عضویت" : "Join Date",
    lastLogin: isFa ? "آخرین ورود" : "Last Login",
    orders: isFa ? "سفارشات" : "Orders",
    totalSpent: isFa ? "مجموع خرید" : "Total Spent",
    reviews: isFa ? "نظرات" : "Reviews",
    role: isFa ? "نقش" : "Role",
    status: isFa ? "وضعیت" : "Status",
    ban: isFa ? "مسدود کردن" : "Ban User",
    unban: isFa ? "رفع مسدودیت" : "Unban User",
    verify: isFa ? "تایید" : "Verify",
    active: isFa ? "فعال" : "Active",
    inactive: isFa ? "غیرفعال" : "Inactive",
    banned: isFa ? "مسدود" : "Banned",
    verified: isFa ? "تایید شده" : "Verified",
    notVerified: isFa ? "تایید نشده" : "Not Verified",
  };

  return (
    <AnimatePresence>
      {user && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[150]"
            onClick={onClose}
          />

          {/* Drawer */}
          <motion.aside
            initial={{ x: isFa ? "100%" : "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: isFa ? "100%" : "-100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed top-0 bottom-0 w-full max-w-md bg-white dark:bg-[#1A1A1E] shadow-2xl z-[151] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 }}
          >
            {/* Header */}
            <div className="sticky top-0 bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] p-4 flex items-center justify-between z-10">
              <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.title}
              </h2>
              <button
                onClick={onClose}
                aria-label="Close"
                className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-4 space-y-5">
              {/* Profile */}
              <div className="flex items-center gap-3">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-[#EF4056] to-[#d63850] flex items-center justify-center text-white font-bold text-[20px] shrink-0 overflow-hidden">
                  {user.avatar ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={user.avatar}
                      alt={user.fullName}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    user.fullName[0]
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] truncate">
                    {user.fullName}
                  </div>
                  <div className="flex items-center gap-2 mt-1.5 flex-wrap">
                    <UserRoleBadge role={user.role} locale={locale} />
                    {user.isVerified && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full font-medium bg-[#22C55E]/10 text-[#22C55E] flex items-center gap-0.5">
                        <ShieldCheck size={10} />
                        {t.verified}
                      </span>
                    )}
                    {user.isBanned && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full font-medium bg-[#EF4444]/10 text-[#EF4444] flex items-center gap-0.5">
                        <Ban size={10} />
                        {t.banned}
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-3 gap-2">
                <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg p-2.5 text-center">
                  <ShoppingBag size={14} className="text-[#EF4056] mx-auto mb-1" />
                  <div className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {user.ordersCount.toLocaleString(isFa ? "fa-IR" : "en-US")}
                  </div>
                  <div className="text-[9px] text-[#A1A3A8]">{t.orders}</div>
                </div>
                <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg p-2.5 text-center">
                  <DollarSign size={14} className="text-[#22C55E] mx-auto mb-1" />
                  <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {formatPrice(user.totalSpent, locale)}
                  </div>
                  <div className="text-[9px] text-[#A1A3A8]">{t.totalSpent}</div>
                </div>
                <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg p-2.5 text-center">
                  <Star size={14} className="text-[#F59E0B] mx-auto mb-1" />
                  <div className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {user.reviewsCount.toLocaleString(isFa ? "fa-IR" : "en-US")}
                  </div>
                  <div className="text-[9px] text-[#A1A3A8]">{t.reviews}</div>
                </div>
              </div>

              {/* Details */}
              <div className="space-y-2.5">
                <div className="flex items-center gap-2 text-[12px]">
                  <Mail size={14} className="text-[#A1A3A8] shrink-0" />
                  <span className="text-[#62666D] dark:text-[#A1A3A8] shrink-0">{t.email}:</span>
                  <span className="text-[#3F4064] dark:text-[#E5E5EA] truncate" dir="ltr">{user.email}</span>
                </div>
                <div className="flex items-center gap-2 text-[12px]">
                  <Phone size={14} className="text-[#A1A3A8] shrink-0" />
                  <span className="text-[#62666D] dark:text-[#A1A3A8] shrink-0">{t.mobile}:</span>
                  <span className="text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">{user.mobile}</span>
                </div>
                <div className="flex items-center gap-2 text-[12px]">
                  <MapPin size={14} className="text-[#A1A3A8] shrink-0" />
                  <span className="text-[#62666D] dark:text-[#A1A3A8] shrink-0">{t.city}:</span>
                  <span className="text-[#3F4064] dark:text-[#E5E5EA]">{user.city}</span>
                </div>
                <div className="flex items-center gap-2 text-[12px]">
                  <Calendar size={14} className="text-[#A1A3A8] shrink-0" />
                  <span className="text-[#62666D] dark:text-[#A1A3A8] shrink-0">{t.joinDate}:</span>
                  <span className="text-[#3F4064] dark:text-[#E5E5EA]">
                    {formatDate(user.joinDate, locale)}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-[12px]">
                  <Calendar size={14} className="text-[#A1A3A8] shrink-0" />
                  <span className="text-[#62666D] dark:text-[#A1A3A8] shrink-0">{t.lastLogin}:</span>
                  <span className="text-[#3F4064] dark:text-[#E5E5EA]">
                    {formatDate(user.lastLogin, locale)}
                  </span>
                </div>
              </div>

              {/* Actions */}
              <div className="pt-4 border-t border-[#E0E0E2] dark:border-[#2A2A2E] space-y-2">
                <button
                  className={`w-full h-10 rounded-lg text-[12px] font-medium transition-colors flex items-center justify-center gap-2 ${
                    user.isBanned
                      ? "bg-[#22C55E] text-white hover:bg-[#1da34d]"
                      : "bg-[#EF4444]/10 text-[#EF4444] hover:bg-[#EF4444]/20"
                  }`}
                >
                  {user.isBanned ? (
                    <>
                      <CheckCircle size={14} />
                      {t.unban}
                    </>
                  ) : (
                    <>
                      <Ban size={14} />
                      {t.ban}
                    </>
                  )}
                </button>
                {!user.isVerified && (
                  <button className="w-full h-10 rounded-lg bg-[#22C55E]/10 text-[#22C55E] hover:bg-[#22C55E]/20 text-[12px] font-medium transition-colors flex items-center justify-center gap-2">
                    <ShieldCheck size={14} />
                    {t.verify}
                  </button>
                )}
              </div>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
'''))

# ============================================================
# components/admin/users/UsersTable.tsx
# ============================================================
files.append(("components/admin/users/UsersTable.tsx", '''"use client";

import { useMemo, useRef } from "react";
import type { Locale, AdminUser } from "@/lib/types";
import { formatPrice, formatDate } from "@/lib/utils";
import { UserRoleBadge } from "./UserStatusBadge";
import UserStatusBadge from "./UserStatusBadge";

interface UsersTableProps {
  locale: Locale;
  users: AdminUser[];
  onUserClick: (user: AdminUser) => void;
  selectedIds: number[];
  onToggleSelect: (id: number) => void;
  onToggleSelectAll: () => void;
}

const ROW_HEIGHT = 60;

export default function UsersTable({
  locale,
  users,
  onUserClick,
  selectedIds,
  onToggleSelect,
  onToggleSelectAll,
}: UsersTableProps) {
  const isFa = locale === "fa";
  const containerRef = useRef<HTMLDivElement>(null);

  const allSelected = users.length > 0 && selectedIds.length === users.length;
  const someSelected = selectedIds.length > 0 && !allSelected;

  const t = {
    user: isFa ? "کاربر" : "User",
    contact: isFa ? "تماس" : "Contact",
    city: isFa ? "شهر" : "City",
    orders: isFa ? "سفارشات" : "Orders",
    spent: isFa ? "خرید کل" : "Total Spent",
    joinDate: isFa ? "عضویت" : "Joined",
    empty: isFa ? "کاربری یافت نشد" : "No users found",
  };

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
      {/* Header */}
      <div className="grid grid-cols-[40px_1.5fr_1.5fr_1fr_80px_120px_100px] gap-3 px-4 py-3 bg-[#F5F5F5] dark:bg-[#0F0F12] border-b border-[#E0E0E2] dark:border-[#2A2A2E] text-[10px] font-bold text-[#62666D] dark:text-[#A1A3A8] uppercase">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={allSelected}
            ref={(el) => {
              if (el) el.indeterminate = someSelected;
            }}
            onChange={onToggleSelectAll}
            className="w-4 h-4 accent-[#EF4056] cursor-pointer"
          />
        </div>
        <div>{t.user}</div>
        <div className="hidden md:block">{t.contact}</div>
        <div className="hidden lg:block">{t.city}</div>
        <div className="text-center">{t.orders}</div>
        <div className="text-end">{t.spent}</div>
        <div className="hidden md:block text-end">{t.joinDate}</div>
      </div>

      {/* Body */}
      <div className="max-h-[600px] overflow-y-auto">
        {users.length === 0 ? (
          <div className="py-16 text-center">
            <div className="text-[13px] text-[#A1A3A8]">{t.empty}</div>
          </div>
        ) : (
          users.map((user, i) => {
            const isSelected = selectedIds.includes(user.id);
            return (
              <div
                key={user.id}
                className={`grid grid-cols-[40px_1.5fr_1.5fr_1fr_80px_120px_100px] gap-3 px-4 py-3 items-center border-b border-[#F5F5F5] dark:border-[#2A2A2E] last:border-0 hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors cursor-pointer ${
                  isSelected ? "bg-[#EF4056]/5" : ""
                }`}
                style={{ minHeight: ROW_HEIGHT }}
                onClick={() => onUserClick(user)}
              >
                {/* Checkbox */}
                <div className="flex items-center" onClick={(e) => e.stopPropagation()}>
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => onToggleSelect(user.id)}
                    className="w-4 h-4 accent-[#EF4056] cursor-pointer"
                  />
                </div>

                {/* User */}
                <div className="flex items-center gap-2.5 min-w-0">
                  <div className="w-9 h-9 rounded-full bg-gradient-to-br from-[#EF4056] to-[#d63850] flex items-center justify-center text-white font-bold text-[12px] shrink-0 overflow-hidden">
                    {user.avatar ? (
                      // eslint-disable-next-line @next/next/no-img-element
                      <img
                        src={user.avatar}
                        alt={user.fullName}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      user.fullName[0]
                    )}
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] truncate">
                      {user.fullName}
                    </div>
                    <div className="flex items-center gap-1.5 mt-0.5">
                      <UserRoleBadge role={user.role} locale={locale} />
                      <UserStatusBadge locale={locale} user={user} />
                    </div>
                  </div>
                </div>

                {/* Contact */}
                <div className="hidden md:block min-w-0">
                  <div className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] truncate" dir="ltr">
                    {user.email}
                  </div>
                  <div className="text-[10px] text-[#A1A3A8] mt-0.5" dir="ltr">
                    {user.mobile}
                  </div>
                </div>

                {/* City */}
                <div className="hidden lg:block text-[11px] text-[#62666D] dark:text-[#A1A3A8] truncate">
                  {user.city}
                </div>

                {/* Orders */}
                <div className="text-center text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                  {user.ordersCount.toLocaleString(isFa ? "fa-IR" : "en-US")}
                </div>

                {/* Spent */}
                <div className="text-end text-[11px] font-bold text-[#EF4056] tabular-nums">
                  {formatPrice(user.totalSpent, locale)}
                </div>

                {/* Join Date */}
                <div className="hidden md:block text-end text-[10px] text-[#A1A3A8]">
                  {formatDate(user.joinDate, locale)}
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/users/index.ts
# ============================================================
files.append(("components/admin/users/index.ts", '''// components/admin/users/index.ts
export { default as UserFilters } from "./UserFilters";
export type { UserFilterValues } from "./UserFilters";
export { default as UserDetailDrawer } from "./UserDetailDrawer";
export { default as UsersTable } from "./UsersTable";
export { UserRoleBadge } from "./UserStatusBadge";
export { default as UserStatusBadge } from "./UserStatusBadge";
'''))

# ============================================================
# components/admin/UsersView.tsx
# ============================================================
files.append(("components/admin/UsersView.tsx", '''"use client";

import { useMemo, useState } from "react";
import { Users as UsersIcon, Download, Trash2, Ban } from "lucide-react";
import type { Locale, AdminUser } from "@/lib/types";
import { adminUsers } from "@/lib/data";
import UserFilters, { type UserFilterValues } from "./users/UserFilters";
import UsersTable from "./users/UsersTable";
import UserDetailDrawer from "./users/UserDetailDrawer";

interface UsersViewProps {
  locale: Locale;
}

const ITEMS_PER_PAGE = 30;

export default function UsersView({ locale }: UsersViewProps) {
  const isFa = locale === "fa";

  const [filters, setFilters] = useState<UserFilterValues>({
    query: "",
    role: "all",
    status: "all",
    sortBy: "newest",
  });

  const [page, setPage] = useState(1);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [selectedUser, setSelectedUser] = useState<AdminUser | null>(null);

  const filtered = useMemo(() => {
    let result = [...adminUsers];
    const q = filters.query.toLowerCase().trim();

    if (q) {
      result = result.filter(
        (u) =>
          u.fullName.toLowerCase().includes(q) ||
          u.email.toLowerCase().includes(q) ||
          u.mobile.includes(q)
      );
    }

    if (filters.role !== "all") {
      result = result.filter((u) => u.role === filters.role);
    }

    if (filters.status === "active") result = result.filter((u) => u.isActive && !u.isBanned);
    else if (filters.status === "inactive") result = result.filter((u) => !u.isActive);
    else if (filters.status === "banned") result = result.filter((u) => u.isBanned);
    else if (filters.status === "verified") result = result.filter((u) => u.isVerified);

    switch (filters.sortBy) {
      case "oldest":
        result.sort((a, b) => new Date(a.joinDate).getTime() - new Date(b.joinDate).getTime());
        break;
      case "name":
        result.sort((a, b) => a.fullName.localeCompare(b.fullName, "fa"));
        break;
      case "spent":
        result.sort((a, b) => b.totalSpent - a.totalSpent);
        break;
      case "newest":
      default:
        result.sort((a, b) => new Date(b.joinDate).getTime() - new Date(a.joinDate).getTime());
    }

    return result;
  }, [filters]);

  const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
  const paginated = filtered.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  const toggleSelect = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === paginated.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(paginated.map((u) => u.id));
    }
  };

  const t = {
    title: isFa ? "مدیریت کاربران" : "Users Management",
    subtitle: isFa
      ? `${filtered.length.toLocaleString("fa-IR")} کاربر`
      : `${filtered.length.toLocaleString("en-US")} users`,
    selected: isFa ? "انتخاب شده" : "selected",
    export: isFa ? "دانلود CSV" : "Export CSV",
    ban: isFa ? "مسدود کردن" : "Ban",
    delete: isFa ? "حذف" : "Delete",
    page: isFa ? "صفحه" : "Page",
    of: isFa ? "از" : "of",
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-[#EF4056]/10 flex items-center justify-center shrink-0">
            <UsersIcon size={20} className="text-[#EF4056]" />
          </div>
          <div>
            <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-0.5">
              {t.title}
            </h1>
            <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
              {t.subtitle}
            </p>
          </div>
        </div>

        <button className="h-10 px-4 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2">
          <Download size={14} />
          {t.export}
        </button>
      </div>

      {/* Filters */}
      <UserFilters
        locale={locale}
        values={filters}
        onChange={(v) => {
          setFilters(v);
          setPage(1);
        }}
        resultCount={filtered.length}
      />

      {/* Bulk actions */}
      {selectedIds.length > 0 && (
        <div className="bg-[#EF4056]/5 border border-[#EF4056]/20 rounded-lg p-3 flex items-center justify-between">
          <div className="text-[12px] text-[#EF4056] font-medium">
            {selectedIds.length.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.selected}
          </div>
          <div className="flex items-center gap-2">
            <button className="h-8 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors flex items-center gap-1.5">
              <Ban size={12} />
              {t.ban}
            </button>
            <button className="h-8 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors flex items-center gap-1.5">
              <Trash2 size={12} />
              {t.delete}
            </button>
          </div>
        </div>
      )}

      {/* Table */}
      <UsersTable
        locale={locale}
        users={paginated}
        onUserClick={setSelectedUser}
        selectedIds={selectedIds}
        onToggleSelect={toggleSelect}
        onToggleSelectAll={toggleSelectAll}
      />

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="text-[11px] text-[#A1A3A8]">
            {t.page} {page.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.of}{" "}
            {totalPages.toLocaleString(isFa ? "fa-IR" : "en-US")}
          </div>
          <div className="flex items-center gap-1">
            {Array.from({ length: Math.min(7, totalPages) }, (_, i) => {
              let pageNum = i + 1;
              if (totalPages > 7 && page > 4) {
                pageNum = page - 3 + i;
                if (pageNum > totalPages) pageNum = totalPages - 6 + i;
              }
              if (pageNum < 1 || pageNum > totalPages) return null;
              return (
                <button
                  key={pageNum}
                  onClick={() => {
                    setPage(pageNum);
                    window.scrollTo({ top: 0, behavior: "smooth" });
                  }}
                  className={`w-8 h-8 rounded-lg text-[11px] font-medium transition-colors ${
                    pageNum === page
                      ? "bg-[#EF4056] text-white"
                      : "bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056]"
                  }`}
                >
                  {pageNum.toLocaleString(isFa ? "fa-IR" : "en-US")}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Detail Drawer */}
      <UserDetailDrawer
        locale={locale}
        user={selectedUser}
        onClose={() => setSelectedUser(null)}
      />
    </div>
  );
}
'''))

# ============================================================
# app/[locale]/admin/users/page.tsx
# ============================================================
files.append(("app/[locale]/admin/users/page.tsx", '''import UsersView from "@/components/admin/UsersView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminUsersPage({ params }: PageProps) {
  const { locale } = await params;
  return <UsersView locale={locale as "fa" | "en"} />;
}
'''))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", '''// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as DashboardView } from "./DashboardView";
export { default as AnalyticsView } from "./AnalyticsView";
export { default as UsersView } from "./UsersView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as AdminLoginForm } from "./AdminLoginForm";

// Layout
export * from "./layout";

// Dashboard
export * from "./dashboard";

// Analytics
export * from "./analytics";

// Users
export * from "./users";

// Charts
export * from "./charts";
'''))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 5: Users Management")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")
    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/users")

if __name__ == "__main__":
    main()