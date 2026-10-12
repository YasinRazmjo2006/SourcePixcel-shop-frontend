// lib/types/admin.ts

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
