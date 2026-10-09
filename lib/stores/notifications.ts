"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AppNotification } from "@/lib/types";

const SEED: AppNotification[] = [
  {
    id: "notif-1",
    type: "order",
    titleFa: "سفارش شما ارسال شد",
    titleEn: "Your order has been shipped",
    bodyFa: "سفارش SP-20240002 با موفقیت ارسال شد. کد پیگیری: 123456789",
    bodyEn: "Order SP-20240002 has been shipped. Tracking: 123456789",
    dateFa: "۲ ساعت پیش",
    dateEn: "2 hours ago",
    read: false,
    href: "/account/orders",
  },
  {
    id: "notif-2",
    type: "promo",
    titleFa: "تخفیف ۴۰٪ روی موبایل‌ها",
    titleEn: "40% off on mobile phones",
    bodyFa: "جشنواره ویژه موبایل تا پایان هفته. با کد SOURCE10 تخفیف بیشتری بگیرید.",
    bodyEn: "Special mobile festival until the end of the week. Use code SOURCE10 for extra discount.",
    dateFa: "۵ ساعت پیش",
    dateEn: "5 hours ago",
    read: false,
    href: "/category/mobile",
  },
  {
    id: "notif-3",
    type: "message",
    titleFa: "پاسخ به نظر شما",
    titleEn: "Reply to your review",
    bodyFa: "تیم پشتیبانی به نظر شما درباره Samsung Galaxy S24 Ultra پاسخ داد.",
    bodyEn: "Support team replied to your review on Samsung Galaxy S24 Ultra.",
    dateFa: "دیروز",
    dateEn: "Yesterday",
    read: false,
  },
  {
    id: "notif-4",
    type: "system",
    titleFa: "به‌روزرسانی اپلیکیشن",
    titleEn: "App update available",
    bodyFa: "نسخه جدید SourcePixcel با امکانات بیشتر منتشر شد.",
    bodyEn: "New version of SourcePixcel is available with more features.",
    dateFa: "۲ روز پیش",
    dateEn: "2 days ago",
    read: true,
  },
  {
    id: "notif-5",
    type: "promo",
    titleFa: "پیشنهاد شگفت‌انگیز جدید",
    titleEn: "New amazing offer",
    bodyFa: "محصولات جدید با تخفیف تا ۳۰٪ به فروشگاه اضافه شدند.",
    bodyEn: "New products with up to 30% off have been added to the store.",
    dateFa: "۳ روز پیش",
    dateEn: "3 days ago",
    read: true,
    href: "/search?discount=1",
  },
];

interface NotificationsState {
  items: AppNotification[];
  markAsRead: (id: string) => void;
  markAllAsRead: () => void;
  remove: (id: string) => void;
  clearAll: () => void;
  getUnreadCount: () => number;
  reset: () => void;
}

export const useNotificationsStore = create<NotificationsState>()(
  persist(
    (set, get) => ({
      items: SEED,

      markAsRead: (id) => {
        set((state) => ({
          items: state.items.map((n) =>
            n.id === id ? { ...n, read: true } : n
          ),
        }));
      },

      markAllAsRead: () => {
        set((state) => ({
          items: state.items.map((n) => ({ ...n, read: true })),
        }));
      },

      remove: (id) => {
        set((state) => ({
          items: state.items.filter((n) => n.id !== id),
        }));
      },

      clearAll: () => set({ items: [] }),

      getUnreadCount: () => get().items.filter((n) => !n.read).length,

      reset: () => set({ items: SEED }),
    }),
    { name: "sourcepixcel-notifications" }
  )
);
