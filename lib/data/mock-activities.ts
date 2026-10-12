// lib/data/mock-activities.ts
import type { AdminActivity, ActivityType } from "@/lib/types";
import {
  seededRandom,
  pick,
  intBetween,
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
} from "./admin-generators";

// ═══════════════════════════════════════════════════════════════
// ACTIVITY TEMPLATES
// ═══════════════════════════════════════════════════════════════

interface ActivityTemplate {
  type: ActivityType;
  titleFa: string;
  titleEn: string;
  descFa: (name: string, amount?: number) => string;
  descEn: (name: string, amount?: number) => string;
  link?: string;
  withAmount?: boolean;
}

const TEMPLATES: ActivityTemplate[] = [
  {
    type: "order",
    titleFa: "سفارش جدید",
    titleEn: "New order",
    descFa: (name, amount) => `${name} یک سفارش به مبلغ ${amount?.toLocaleString("fa-IR")} تومان ثبت کرد`,
    descEn: (name, amount) => `${name} placed an order for ${amount?.toLocaleString("en-US")} Toman`,
    link: "/admin/orders",
    withAmount: true,
  },
  {
    type: "user",
    titleFa: "کاربر جدید",
    titleEn: "New user",
    descFa: (name) => `${name} حساب کاربری جدیدی ایجاد کرد`,
    descEn: (name) => `${name} created a new account`,
    link: "/admin/users",
  },
  {
    type: "review",
    titleFa: "نظر جدید",
    titleEn: "New review",
    descFa: (name) => `${name} یک نظر جدید برای محصولی ثبت کرد`,
    descEn: (name) => `${name} submitted a new product review`,
  },
  {
    type: "payment",
    titleFa: "پرداخت موفق",
    titleEn: "Payment successful",
    descFa: (name, amount) => `پرداخت ${amount?.toLocaleString("fa-IR")} تومان از ${name} دریافت شد`,
    descEn: (name, amount) => `Payment of ${amount?.toLocaleString("en-US")} Toman received from ${name}`,
    link: "/admin/orders",
    withAmount: true,
  },
  {
    type: "product",
    titleFa: "موجودی کم",
    titleEn: "Low stock",
    descFa: () => `موجودی یکی از محصولات به کمتر از ۵ عدد رسید`,
    descEn: () => `Stock for one of the products dropped below 5`,
    link: "/admin/products",
  },
  {
    type: "system",
    titleFa: "به‌روزرسانی سیستم",
    titleEn: "System update",
    descFa: () => `سیستم با موفقیت به آخرین نسخه به‌روزرسانی شد`,
    descEn: () => `System successfully updated to the latest version`,
  },
];

// ═══════════════════════════════════════════════════════════════
// GENERATE
// ═══════════════════════════════════════════════════════════════

const rand = seededRandom(2024);
const ACTIVITY_COUNT = 25;

export const adminActivities: AdminActivity[] = Array.from(
  { length: ACTIVITY_COUNT },
  (_, i) => {
    const template = pick(TEMPLATES, rand);
    const firstName = pick(PERSIAN_FIRST_NAMES, rand);
    const lastName = pick(PERSIAN_LAST_NAMES, rand);
    const fullName = `${firstName} ${lastName}`;
    const amount = template.withAmount ? intBetween(200_000, 50_000_000, rand) : undefined;

    return {
      id: `act-${i + 1}`,
      type: template.type,
      titleFa: template.titleFa,
      titleEn: template.titleEn,
      descriptionFa: template.descFa(fullName, amount),
      descriptionEn: template.descEn(fullName, amount),
      timestamp: Date.now() - intBetween(1, 1440, rand) * 60 * 1000, // last 24 hours
      user: {
        name: fullName,
      },
      amount,
      link: template.link,
    };
  }
);

// Sort by timestamp descending
adminActivities.sort((a, b) => b.timestamp - a.timestamp);

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

export function getRecentActivities(count = 10): AdminActivity[] {
  return adminActivities.slice(0, count);
}

export function getActivitiesByType(type: ActivityType): AdminActivity[] {
  return adminActivities.filter((a) => a.type === type);
}
