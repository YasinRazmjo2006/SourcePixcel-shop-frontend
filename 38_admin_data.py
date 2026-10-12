# 38_admin_data.py
# Step 1: Admin Data Layer — types, generators, analytics, activities
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/types/admin.ts
# ============================================================
files.append(("lib/types/admin.ts", """// lib/types/admin.ts

// ═══════════════════════════════════════════════════════════════
// ADMIN USER
// ═══════════════════════════════════════════════════════════════

export type AdminUserRole = "customer" | "admin" | "moderator" | "editor";

export interface AdminUser {
  id: number;
  fullName: string;
  firstName: string;
  lastName: string;
  email: string;
  mobile: string;
  avatar: string;
  role: AdminUserRole;
  isActive: boolean;
  isVerified: boolean;
  isBanned: boolean;
  city: string;
  joinDate: string;
  lastLogin: string;
  ordersCount: number;
  totalSpent: number;
  reviewsCount: number;
}

// ═══════════════════════════════════════════════════════════════
// ADMIN ORDER
// ═══════════════════════════════════════════════════════════════

export type AdminOrderStatus =
  | "pending"
  | "processing"
  | "shipped"
  | "delivered"
  | "cancelled"
  | "refunded";

export type PaymentMethod = "zarinpal" | "idpay" | "nextpay" | "cod";

export type ShippingMethod = "post" | "tipax" | "pickup";

export interface AdminOrderItem {
  productId: number;
  titleFa: string;
  titleEn: string;
  image: string;
  price: number;
  quantity: number;
}

export interface AdminOrder {
  id: string;
  userId: number;
  customerName: string;
  customerMobile: string;
  items: AdminOrderItem[];
  itemsCount: number;
  subtotal: number;
  discount: number;
  shipping: number;
  total: number;
  status: AdminOrderStatus;
  paymentMethod: PaymentMethod;
  shippingMethod: ShippingMethod;
  city: string;
  address: string;
  createdAt: string;
  updatedAt: string;
  trackingCode?: string;
}

// ═══════════════════════════════════════════════════════════════
// ANALYTICS
// ═══════════════════════════════════════════════════════════════

export interface SalesDataPoint {
  month: string;
  monthFa: string;
  sales: number;
  orders: number;
  visitors: number;
}

export interface CategorySalesData {
  categoryId: string;
  nameFa: string;
  nameEn: string;
  sales: number;
  orders: number;
  color: string;
}

export interface DailyVisitors {
  date: string;
  visitors: number;
  pageViews: number;
  newUsers: number;
}

export interface HourlyActivity {
  hour: number;
  activity: number;
}

export interface FunnelStep {
  step: string;
  stepFa: string;
  value: number;
  percentage: number;
}

export interface AnalyticsOverview {
  totalRevenue: number;
  totalOrders: number;
  totalUsers: number;
  totalProducts: number;
  revenueChange: number;
  ordersChange: number;
  usersChange: number;
  productsChange: number;
  conversionRate: number;
  averageOrderValue: number;
}

// ═══════════════════════════════════════════════════════════════
// ACTIVITIES
// ═══════════════════════════════════════════════════════════════

export type ActivityType =
  | "order"
  | "user"
  | "product"
  | "review"
  | "system"
  | "payment";

export interface AdminActivity {
  id: string;
  type: ActivityType;
  titleFa: string;
  titleEn: string;
  descriptionFa: string;
  descriptionEn: string;
  timestamp: number;
  user?: {
    name: string;
    avatar?: string;
  };
  amount?: number;
  link?: string;
}

// ═══════════════════════════════════════════════════════════════
// TOP PRODUCTS
// ═══════════════════════════════════════════════════════════════

export interface TopProduct {
  id: number;
  titleFa: string;
  titleEn: string;
  image: string;
  price: number;
  sales: number;
  revenue: number;
  rating: number;
}

// ═══════════════════════════════════════════════════════════════
// DATE RANGE
// ═══════════════════════════════════════════════════════════════

export type DateRangePreset =
  | "today"
  | "yesterday"
  | "last7days"
  | "last30days"
  | "last90days"
  | "thisMonth"
  | "lastMonth"
  | "thisYear"
  | "custom";

export interface DateRange {
  from: Date;
  to: Date;
  preset: DateRangePreset;
}
"""))

# ============================================================
# lib/data/admin-generators.ts — seeded random helpers
# ============================================================
files.append(("lib/data/admin-generators.ts", """// lib/data/admin-generators.ts
// Seeded random generator — deterministic mock data

// Mulberry32 PRNG — fast, deterministic
function createRandom(seed: number) {
  let state = seed;
  return function random(): number {
    state |= 0;
    state = (state + 0x6d2b79f5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function seededRandom(seed: number) {
  return createRandom(seed);
}

export function pick<T>(arr: T[], rand: () => number): T {
  return arr[Math.floor(rand() * arr.length)];
}

export function pickMany<T>(arr: T[], count: number, rand: () => number): T[] {
  const shuffled = [...arr].sort(() => rand() - 0.5);
  return shuffled.slice(0, count);
}

export function intBetween(min: number, max: number, rand: () => number): number {
  return Math.floor(rand() * (max - min + 1)) + min;
}

export function floatBetween(min: number, max: number, rand: () => number, decimals = 2): number {
  const value = rand() * (max - min) + min;
  return Number(value.toFixed(decimals));
}

export function weightedPick<T>(
  items: { value: T; weight: number }[],
  rand: () => number
): T {
  const totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
  let random = rand() * totalWeight;
  for (const item of items) {
    random -= item.weight;
    if (random <= 0) return item.value;
  }
  return items[items.length - 1].value;
}

// ═══════════════════════════════════════════════════════════════
// PERSIAN DATA
// ═══════════════════════════════════════════════════════════════

export const PERSIAN_FIRST_NAMES = [
  "علی", "محمد", "رضا", "حسین", "امیر", "مهدی", "سعید", "حسن", "مجید", "کاظم",
  "سارا", "مریم", "زهرا", "فاطمه", "نرگس", "الهام", "شیما", "نیلوفر", "پریسا", "نازنین",
  "احمد", "یاسر", "پویا", "آرش", "کاوه", "بهرام", "داریوش", "کوروش", "سیاوش", "فریدون",
  "مینا", "لیلا", "سحر", "پگاه", "ترانه", "بهاره", "شقایق", "هستی", "نازنین", "سمیرا",
  "بهنام", "بهزاد", "بابک", "پیمان", "جمشید", "رامین", "سامان", "ساسان", "سینا", "فرشاد",
];

export const PERSIAN_LAST_NAMES = [
  "محمدی", "احمدی", "رضایی", "حسینی", "کریمی", "نوری", "رحیمی", "صادقی", "موسوی", "هاشمی",
  "علی‌پور", "مرادی", "جعفری", "قاسمی", "کاظمی", "بهرامی", "زمانی", "عباسی", "یوسفی", "امینی",
  "شریفی", "سلطانی", "باقری", "نجفی", "طاهری", "فرهادی", "زارعی", "بیات", "صالحی", "خانی",
  "ملکی", "شاهینی", "خسروی", "پناهی", "افشار", "ایرانی", "بابایی", "تقوی", "ثابتی", "جوادی",
];

export const PERSIAN_CITIES = [
  "تهران", "مشهد", "اصفهان", "کرج", "شیراز", "تبریز", "قم", "اهواز", "کرمانشاه", "ارومیه",
  "رشت", "زاهدان", "همدان", "کرمان", "یزد", "اردبیل", "بندرعباس", "اراک", "اسلام‌شهر", "زنجان",
  "ساری", "قزوین", "بوشهر", "سنندج", "گرگان", "خرم‌آباد", "بابل", "آمل", "نجف‌آباد", "سبزوار",
];

export const PERSIAN_STREETS = [
  "خیابان ولیعصر", "خیابان انقلاب", "بلوار کشاورز", "خیابان آزادی", "خیابان فردوسی",
  "بلوار میرداماد", "خیابان شریعتی", "بلوار صادقیه", "خیابان جمهوری", "بلوار نیایش",
  "خیابان مطهری", "بلوار ستارخان", "خیابان طالقانی", "بلوار پاسداران", "خیابان بهشتی",
];
"""))

# ============================================================
# lib/data/mock-admin-users.ts
# ============================================================
files.append(("lib/data/mock-admin-users.ts", """// lib/data/mock-admin-users.ts
import type { AdminUser, AdminUserRole } from "@/lib/types";
import {
  seededRandom,
  pick,
  intBetween,
  floatBetween,
  weightedPick,
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
  PERSIAN_CITIES,
} from "./admin-generators";

const USER_SEED = 42;
const USER_COUNT = 1000;

// ═══════════════════════════════════════════════════════════════
// USER GENERATION
// ═══════════════════════════════════════════════════════════════

function generateUser(id: number, rand: () => number): AdminUser {
  const firstName = pick(PERSIAN_FIRST_NAMES, rand);
  const lastName = pick(PERSIAN_LAST_NAMES, rand);
  const fullName = `${firstName} ${lastName}`;

  const email = `user${id}@${pick(["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"], rand)}`;
  const mobile = `09${intBetween(100000000, 999999999, rand)}`;

  const role = weightedPick<AdminUserRole>(
    [
      { value: "customer", weight: 92 },
      { value: "admin", weight: 3 },
      { value: "moderator", weight: 2 },
      { value: "editor", weight: 3 },
    ],
    rand
  );

  const joinDaysAgo = intBetween(1, 730, rand);
  const joinDate = new Date(Date.now() - joinDaysAgo * 86400000);

  const lastLoginDaysAgo = intBetween(0, Math.min(joinDaysAgo, 60), rand);
  const lastLogin = new Date(Date.now() - lastLoginDaysAgo * 86400000);

  const ordersCount = intBetween(0, 50, rand);
  const totalSpent = ordersCount * intBetween(500_000, 50_000_000, rand);
  const reviewsCount = intBetween(0, 15, rand);

  return {
    id,
    fullName,
    firstName,
    lastName,
    email,
    mobile,
    avatar: `https://i.pravatar.cc/150?u=${id}`,
    role,
    isActive: rand() > 0.1,
    isVerified: rand() > 0.2,
    isBanned: rand() > 0.97,
    city: pick(PERSIAN_CITIES, rand),
    joinDate: joinDate.toISOString(),
    lastLogin: lastLogin.toISOString(),
    ordersCount,
    totalSpent,
    reviewsCount,
  };
}

// Generate all users once
const rand = seededRandom(USER_SEED);
export const adminUsers: AdminUser[] = Array.from({ length: USER_COUNT }, (_, i) =>
  generateUser(i + 1, rand)
);

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

export function getAdminUserById(id: number): AdminUser | undefined {
  return adminUsers.find((u) => u.id === id);
}

export function getAdminUserStats() {
  const total = adminUsers.length;
  const active = adminUsers.filter((u) => u.isActive).length;
  const verified = adminUsers.filter((u) => u.isVerified).length;
  const banned = adminUsers.filter((u) => u.isBanned).length;
  const admins = adminUsers.filter((u) => u.role === "admin").length;
  const totalSpent = adminUsers.reduce((sum, u) => sum + u.totalSpent, 0);
  const totalOrders = adminUsers.reduce((sum, u) => sum + u.ordersCount, 0);

  return {
    total,
    active,
    verified,
    banned,
    admins,
    totalSpent,
    totalOrders,
    averageOrderValue: totalOrders > 0 ? Math.round(totalSpent / totalOrders) : 0,
  };
}

export const ADMIN_USERS_TOTAL = USER_COUNT;
"""))

# ============================================================
# lib/data/mock-admin-orders.ts
# ============================================================
files.append(("lib/data/mock-admin-orders.ts", """// lib/data/mock-admin-orders.ts
import type {
  AdminOrder,
  AdminOrderStatus,
  PaymentMethod,
  ShippingMethod,
} from "@/lib/types";
import { products } from "./products";
import {
  seededRandom,
  pick,
  pickMany,
  intBetween,
  weightedPick,
  PERSIAN_CITIES,
  PERSIAN_STREETS,
} from "./admin-generators";
import { adminUsers } from "./mock-admin-users";

const ORDER_SEED = 1234;
const ORDER_COUNT = 5000;

// ═══════════════════════════════════════════════════════════════
// ORDER GENERATION
// ═══════════════════════════════════════════════════════════════

function generateOrder(index: number, rand: () => number): AdminOrder {
  const user = adminUsers[intBetween(0, adminUsers.length - 1, rand)];

  const itemsCount = weightedPick(
    [
      { value: 1, weight: 40 },
      { value: 2, weight: 30 },
      { value: 3, weight: 20 },
      { value: 4, weight: 8 },
      { value: 5, weight: 2 },
    ],
    rand
  );

  const selectedProducts = pickMany(products, itemsCount, rand);

  const items = selectedProducts.map((p) => ({
    productId: p.id,
    titleFa: p.titleFa,
    titleEn: p.titleEn,
    image: p.image,
    price: p.finalPrice,
    quantity: intBetween(1, 3, rand),
  }));

  const subtotal = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const discount = rand() > 0.7 ? Math.round(subtotal * 0.1) : 0;
  const shipping = subtotal > 5_000_000 ? 0 : 45_000;
  const total = subtotal - discount + shipping;

  const status = weightedPick<AdminOrderStatus>(
    [
      { value: "delivered", weight: 55 },
      { value: "shipped", weight: 15 },
      { value: "processing", weight: 15 },
      { value: "pending", weight: 8 },
      { value: "cancelled", weight: 4 },
      { value: "refunded", weight: 3 },
    ],
    rand
  );

  const paymentMethod = weightedPick<PaymentMethod>(
    [
      { value: "zarinpal", weight: 70 },
      { value: "idpay", weight: 15 },
      { value: "nextpay", weight: 10 },
      { value: "cod", weight: 5 },
    ],
    rand
  );

  const shippingMethod = weightedPick<ShippingMethod>(
    [
      { value: "post", weight: 60 },
      { value: "tipax", weight: 30 },
      { value: "pickup", weight: 10 },
    ],
    rand
  );

  const daysAgo = intBetween(0, 365, rand);
  const createdAt = new Date(Date.now() - daysAgo * 86400000);
  const updatedAt = new Date(createdAt.getTime() + intBetween(0, 10, rand) * 86400000);

  const city = user.city || pick(PERSIAN_CITIES, rand);
  const street = pick(PERSIAN_STREETS, rand);
  const address = `${city}، ${street}، پلاک ${intBetween(1, 500, rand)}، واحد ${intBetween(1, 20, rand)}`;

  return {
    id: `SP-${String(100000 + index).padStart(6, "0")}`,
    userId: user.id,
    customerName: user.fullName,
    customerMobile: user.mobile,
    items,
    itemsCount: items.reduce((sum, i) => sum + i.quantity, 0),
    subtotal,
    discount,
    shipping,
    total,
    status,
    paymentMethod,
    shippingMethod,
    city,
    address,
    createdAt: createdAt.toISOString(),
    updatedAt: updatedAt.toISOString(),
    trackingCode:
      status === "shipped" || status === "delivered"
        ? `TRK${intBetween(100000000, 999999999, rand)}`
        : undefined,
  };
}

// Generate all orders once
const rand = seededRandom(ORDER_SEED);
export const adminOrders: AdminOrder[] = Array.from({ length: ORDER_COUNT }, (_, i) =>
  generateOrder(i, rand)
);

// Sort by createdAt descending
adminOrders.sort(
  (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
);

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

export function getAdminOrderById(id: string): AdminOrder | undefined {
  return adminOrders.find((o) => o.id === id);
}

export function getAdminOrderStats() {
  const total = adminOrders.length;
  const byStatus: Record<AdminOrderStatus, number> = {
    pending: 0,
    processing: 0,
    shipped: 0,
    delivered: 0,
    cancelled: 0,
    refunded: 0,
  };

  let totalRevenue = 0;
  for (const order of adminOrders) {
    byStatus[order.status]++;
    if (order.status !== "cancelled" && order.status !== "refunded") {
      totalRevenue += order.total;
    }
  }

  return {
    total,
    byStatus,
    totalRevenue,
    averageOrderValue: total > 0 ? Math.round(totalRevenue / total) : 0,
  };
}

export const ADMIN_ORDERS_TOTAL = ORDER_COUNT;
"""))

# ============================================================
# lib/data/mock-analytics.ts
# ============================================================
files.append(("lib/data/mock-analytics.ts", """// lib/data/mock-analytics.ts
import type {
  SalesDataPoint,
  CategorySalesData,
  DailyVisitors,
  HourlyActivity,
  FunnelStep,
  AnalyticsOverview,
  TopProduct,
} from "@/lib/types";
import { products, categories } from "./products";
import {
  seededRandom,
  intBetween,
  floatBetween,
} from "./admin-generators";

// ═══════════════════════════════════════════════════════════════
// OVERVIEW STATS
// ═══════════════════════════════════════════════════════════════

export const analyticsOverview: AnalyticsOverview = {
  totalRevenue: 24_580_000_000,
  totalOrders: 12_450,
  totalUsers: 8_234,
  totalProducts: 68,
  revenueChange: 12.5,
  ordersChange: 8.3,
  usersChange: 15.2,
  productsChange: 0,
  conversionRate: 3.42,
  averageOrderValue: 1_974_000,
};

// ═══════════════════════════════════════════════════════════════
// SALES DATA — 12 MONTHS
// ═══════════════════════════════════════════════════════════════

const MONTHS_FA = [
  "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
  "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
];
const MONTHS_EN = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

const salesRand = seededRandom(999);
export const monthlySales: SalesDataPoint[] = MONTHS_FA.map((monthFa, i) => {
  const base = intBetween(1_200_000_000, 2_800_000_000, salesRand);
  return {
    month: MONTHS_EN[i],
    monthFa,
    sales: base,
    orders: intBetween(800, 1800, salesRand),
    visitors: intBetween(15_000, 45_000, salesRand),
  };
});

// ═══════════════════════════════════════════════════════════════
// CATEGORY SALES
// ═══════════════════════════════════════════════════════════════

const CATEGORY_COLORS: Record<string, string> = {
  mobile: "#EF4056",
  laptop: "#00BFFF",
  tablet: "#8B5CF6",
  audio: "#F59E0B",
  camera: "#22C55E",
  smartwatch: "#EC4899",
  gaming: "#06B6D4",
  accessories: "#6B7280",
  clothing: "#F97316",
  shoes: "#10B981",
  home: "#6366F1",
  books: "#84CC16",
};

const catRand = seededRandom(777);
export const categorySales: CategorySalesData[] = categories.map((cat) => ({
  categoryId: cat.id,
  nameFa: cat.nameFa,
  nameEn: cat.nameEn,
  sales: intBetween(500_000_000, 3_000_000_000, catRand),
  orders: intBetween(100, 1500, catRand),
  color: CATEGORY_COLORS[cat.id] ?? "#EF4056",
}));

categorySales.sort((a, b) => b.sales - a.sales);

// ═══════════════════════════════════════════════════════════════
// DAILY VISITORS — 30 DAYS
// ═══════════════════════════════════════════════════════════════

const visitorsRand = seededRandom(555);
export const dailyVisitors: DailyVisitors[] = Array.from({ length: 30 }, (_, i) => {
  const date = new Date(Date.now() - (29 - i) * 86400000);
  return {
    date: date.toISOString().slice(0, 10),
    visitors: intBetween(800, 3200, visitorsRand),
    pageViews: intBetween(3000, 12000, visitorsRand),
    newUsers: intBetween(50, 400, visitorsRand),
  };
});

// ═══════════════════════════════════════════════════════════════
// HOURLY ACTIVITY — 24 HOURS
// ═══════════════════════════════════════════════════════════════

const hourlyRand = seededRandom(333);
export const hourlyActivity: HourlyActivity[] = Array.from({ length: 24 }, (_, hour) => {
  // Peak hours: 10-14, 19-23
  let base = intBetween(20, 60, hourlyRand);
  if (hour >= 10 && hour <= 14) base += 80;
  if (hour >= 19 && hour <= 23) base += 100;
  if (hour >= 2 && hour <= 6) base = intBetween(5, 20, hourlyRand);
  return { hour, activity: base };
});

// ═══════════════════════════════════════════════════════════════
// FUNNEL
// ═══════════════════════════════════════════════════════════════

export const salesFunnel: FunnelStep[] = [
  { step: "visit", stepFa: "بازدید", value: 100000, percentage: 100 },
  { step: "product-view", stepFa: "مشاهده محصول", value: 45000, percentage: 45 },
  { step: "add-to-cart", stepFa: "افزودن به سبد", value: 12000, percentage: 12 },
  { step: "checkout", stepFa: "شروع پرداخت", value: 5500, percentage: 5.5 },
  { step: "purchase", stepFa: "خرید موفق", value: 3420, percentage: 3.42 },
];

// ═══════════════════════════════════════════════════════════════
// TOP PRODUCTS
// ═══════════════════════════════════════════════════════════════

const topRand = seededRandom(111);
export const topProducts: TopProduct[] = products
  .slice(0, 10)
  .map((p) => ({
    id: p.id,
    titleFa: p.titleFa,
    titleEn: p.titleEn,
    image: p.image,
    price: p.finalPrice,
    sales: intBetween(50, 800, topRand),
    revenue: p.finalPrice * intBetween(50, 800, topRand),
    rating: p.rating,
  }))
  .sort((a, b) => b.revenue - a.revenue)
  .slice(0, 5);
"""))

# ============================================================
# lib/data/mock-activities.ts
# ============================================================
files.append(("lib/data/mock-activities.ts", """// lib/data/mock-activities.ts
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
"""))

# ============================================================
# lib/data/index.ts (updated)
# ============================================================
files.append(("lib/data/index.ts", """// lib/data/index.ts
export {
  categories,
  brands,
  products,
  getProductBySlug,
  getProductsByCategory,
  getProductsByBrand,
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
  getCategoryById,
  getBrandById,
  getProductsBySubcategory,
} from "./products";

export {
  mockOrders,
  getOrderById,
} from "./mock-orders";
export type { MockOrder, OrderItem } from "./mock-orders";

export {
  blogPosts,
  getBlogPostBySlug,
  getRecentBlogPosts,
  getRelatedBlogPosts,
} from "./mock-blog";
export type { BlogPost } from "./mock-blog";

export {
  mockReviews,
  getReviewsByProduct,
  getGenericReviews,
  getReviewsForProduct,
} from "./mock-reviews";

export { getProductImage } from "./product-images";

// ═══════════════════════════════════════════════════════════════
// ADMIN DATA
// ═══════════════════════════════════════════════════════════════

export {
  adminUsers,
  getAdminUserById,
  getAdminUserStats,
  ADMIN_USERS_TOTAL,
} from "./mock-admin-users";

export {
  adminOrders,
  getAdminOrderById,
  getAdminOrderStats,
  ADMIN_ORDERS_TOTAL,
} from "./mock-admin-orders";

export {
  analyticsOverview,
  monthlySales,
  categorySales,
  dailyVisitors,
  hourlyActivity,
  salesFunnel,
  topProducts,
} from "./mock-analytics";

export {
  adminActivities,
  getRecentActivities,
  getActivitiesByType,
} from "./mock-activities";

export {
  seededRandom,
  pick,
  pickMany,
  intBetween,
  floatBetween,
  weightedPick,
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
  PERSIAN_CITIES,
  PERSIAN_STREETS,
} from "./admin-generators";
"""))

# ============================================================
# lib/types/index.ts (updated)
# ============================================================
files.append(("lib/types/index.ts", """// lib/types/index.ts
export type {
  Subcategory,
  Category,
  Brand,
  Product,
  CartItem,
  WishlistItem,
  CompareItem,
  FilterState,
  SortOption,
  Locale,
} from "./product";

export type { BlogPost } from "./blog";
export type { Review, ReviewDraft } from "./review";
export type { AppNotification, NotificationType } from "./notification";

// Admin types
export type {
  AdminUser,
  AdminUserRole,
  AdminOrder,
  AdminOrderStatus,
  AdminOrderItem,
  PaymentMethod,
  ShippingMethod,
  SalesDataPoint,
  CategorySalesData,
  DailyVisitors,
  HourlyActivity,
  FunnelStep,
  AnalyticsOverview,
  AdminActivity,
  ActivityType,
  TopProduct,
  DateRange,
  DateRangePreset,
} from "./admin";
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 1: Data Layer")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("\nData generated:")
        print("  - 1000 admin users")
        print("  - 5000 admin orders")
        print("  - 12 months of sales data")
        print("  - 12 categories analytics")
        print("  - 30 days of visitors")
        print("  - 24 hours of activity")
        print("  - Sales funnel")
        print("  - Top 5 products")
        print("  - 25 recent activities")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Test: http://localhost:3000/fa/admin")
        print("\nNext: Admin Step 2 (Layout)")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()