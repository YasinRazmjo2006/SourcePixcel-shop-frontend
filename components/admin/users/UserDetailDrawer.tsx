"use client";

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
