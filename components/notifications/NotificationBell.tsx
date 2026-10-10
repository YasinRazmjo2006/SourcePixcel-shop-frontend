"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  Bell,
  Package,
  Tag,
  Info,
  MessageSquare,
  Check,
  Trash2,
  X,
} from "lucide-react";
import type { Locale, NotificationType } from "@/lib/types";
import { useNotificationsStore } from "@/lib/stores";

interface NotificationBellProps {
  locale: Locale;
  variant?: "top" | "header";
}

const TYPE_ICONS: Record<
  NotificationType,
  React.ComponentType<{ size?: number; "aria-hidden"?: boolean }>
> = {
  order: Package,
  promo: Tag,
  system: Info,
  message: MessageSquare,
};

const TYPE_COLORS: Record<NotificationType, string> = {
  order: "#22C55E",
  promo: "#EF4056",
  system: "#00BFFF",
  message: "#8B5CF6",
};

export default function NotificationBell({
  locale,
  variant = "top",
}: NotificationBellProps) {
  const isFa = locale === "fa";
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  const items = useNotificationsStore((s) => s.items);
  const markAsRead = useNotificationsStore((s) => s.markAsRead);
  const markAllAsRead = useNotificationsStore((s) => s.markAllAsRead);
  const remove = useNotificationsStore((s) => s.remove);
  const clearAll = useNotificationsStore((s) => s.clearAll);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        wrapperRef.current &&
        !wrapperRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () =>
      document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const unreadCount = items.filter((n) => !n.read).length;
  const iconSize = variant === "top" ? 14 : 20;

  return (
    <div ref={wrapperRef} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-label={isFa ? "اعلان‌ها" : "Notifications"}
        className={
          variant === "top"
            ? "text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors relative"
            : "text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors flex items-center gap-2 relative"
        }
      >
        <Bell size={iconSize} aria-hidden={true} />
        {variant === "header" && (
          <span>{isFa ? "اعلان‌ها" : "Notifications"}</span>
        )}
        {mounted && unreadCount > 0 && (
          <span
            className={
              variant === "top"
                ? "absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center font-bold animate-pulse"
                : "bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold animate-pulse"
            }
          >
            {unreadCount}
          </span>
        )}
      </button>

      {open && (
        <div
          className="absolute top-full mt-2 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl shadow-2xl overflow-hidden z-[60] w-80 md:w-96 left-0 md:left-auto md:right-0"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-3 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
            <div className="flex items-center gap-2">
              <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {isFa ? "اعلان‌ها" : "Notifications"}
              </h3>
              {unreadCount > 0 && (
                <span className="text-[10px] bg-[#EF4056] text-white px-1.5 py-0.5 rounded-full font-bold">
                  {unreadCount}
                </span>
              )}
            </div>
            <div className="flex items-center gap-1">
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="text-[10px] text-[#00BFFF] hover:underline flex items-center gap-1"
                >
                  <Check size={11} aria-hidden={true} />
                  {isFa ? "خواندن همه" : "Read all"}
                </button>
              )}
              <button
                onClick={() => setOpen(false)}
                className="w-6 h-6 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
                aria-label="Close"
              >
                <X size={14} aria-hidden={true} />
              </button>
            </div>
          </div>

          {/* List */}
          <div className="max-h-[400px] overflow-y-auto">
            {items.length === 0 ? (
              <div className="p-8 text-center">
                <div className="w-14 h-14 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
                  <Bell size={24} className="text-[#A1A3A8]" aria-hidden={true} />
                </div>
                <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  {isFa ? "اعلان جدیدی ندارید" : "No notifications yet"}
                </p>
              </div>
            ) : (
              items.map((notif) => {
                const Icon = TYPE_ICONS[notif.type];
                const color = TYPE_COLORS[notif.type];

                const content = (
                  <>
                    <div
                      className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
                      style={{ backgroundColor: `${color}15` }}
                    >
                      <Icon size={16} aria-hidden={true} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <h4
                          className={`text-[12px] leading-5 line-clamp-1 ${
                            !notif.read
                              ? "font-bold text-[#3F4064] dark:text-[#E5E5EA]"
                              : "font-medium text-[#62666D] dark:text-[#A1A3A8]"
                          }`}
                        >
                          {isFa ? notif.titleFa : notif.titleEn}
                        </h4>
                        {!notif.read && (
                          <div className="w-2 h-2 rounded-full bg-[#EF4056] shrink-0 mt-1.5" />
                        )}
                      </div>
                      <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] leading-5 line-clamp-2 mt-0.5">
                        {isFa ? notif.bodyFa : notif.bodyEn}
                      </p>
                      <span className="text-[10px] text-[#A1A3A8] mt-1 block">
                        {isFa ? notif.dateFa : notif.dateEn}
                      </span>
                    </div>
                    <button
                      onClick={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        remove(notif.id);
                      }}
                      aria-label="Remove"
                      className="w-6 h-6 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#EF4444]/10 hover:text-[#EF4444] opacity-0 group-hover:opacity-100 transition-all shrink-0"
                    >
                      <Trash2 size={12} aria-hidden={true} />
                    </button>
                  </>
                );

                const itemClassName = `flex items-start gap-3 p-3 border-b border-[#F5F5F5] dark:border-[#2A2A2E] last:border-0 hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors cursor-pointer relative group ${
                  !notif.read ? "bg-[#EF4056]/[0.03]" : ""
                }`;

                if (notif.href) {
                  return (
                    <Link
                      key={notif.id}
                      href={`/${locale}${notif.href}`}
                      onClick={() => {
                        markAsRead(notif.id);
                        setOpen(false);
                      }}
                      className={itemClassName}
                    >
                      {content}
                    </Link>
                  );
                }

                return (
                  <div
                    key={notif.id}
                    onClick={() => markAsRead(notif.id)}
                    className={itemClassName}
                  >
                    {content}
                  </div>
                );
              })
            )}
          </div>

          {/* Footer */}
          {items.length > 0 && (
            <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] p-2">
              <button
                onClick={clearAll}
                className="w-full text-[11px] text-[#EF4444] hover:bg-[#EF4444]/5 rounded-lg py-2 transition-colors flex items-center justify-center gap-1"
              >
                <Trash2 size={12} aria-hidden={true} />
                {isFa ? "پاک کردن همه" : "Clear all"}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}