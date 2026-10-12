// lib/data/mock-analytics.ts
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
