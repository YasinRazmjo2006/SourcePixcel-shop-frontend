"use client";

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
