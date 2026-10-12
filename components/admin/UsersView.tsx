"use client";

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
