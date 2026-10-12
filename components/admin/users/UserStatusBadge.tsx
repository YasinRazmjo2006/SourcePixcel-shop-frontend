"use client";

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
