"use client";

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
