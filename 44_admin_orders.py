# 44_admin_orders.py
# Step 7: Orders Management
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# lib/stores/admin-orders.ts
# ============================================================
files.append(("lib/stores/admin-orders.ts", '''"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { AdminOrder, AdminOrderStatus } from "@/lib/types";
import { adminOrders as initialOrders } from "@/lib/data";

interface AdminOrdersState {
  orders: AdminOrder[];
  updateStatus: (id: string, status: AdminOrderStatus) => void;
  addTrackingCode: (id: string, code: string) => void;
  deleteOrder: (id: string) => void;
  reset: () => void;
}

export const useAdminOrdersStore = create<AdminOrdersState>()(
  persist(
    (set) => ({
      orders: initialOrders,

      updateStatus: (id, status) =>
        set((state) => ({
          orders: state.orders.map((o) =>
            o.id === id
              ? { ...o, status, updatedAt: new Date().toISOString() }
              : o
          ),
        })),

      addTrackingCode: (id, code) =>
        set((state) => ({
          orders: state.orders.map((o) =>
            o.id === id ? { ...o, trackingCode: code } : o
          ),
        })),

      deleteOrder: (id) =>
        set((state) => ({
          orders: state.orders.filter((o) => o.id !== id),
        })),

      reset: () => set({ orders: initialOrders }),
    }),
    { name: "sourcepixcel-admin-orders" }
  )
);
'''))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", '''// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export { useAdminStore } from "./admin";
export { useAdminUIStore } from "./admin-ui";
export { useAdminProductsStore } from "./admin-products";
export { useAdminOrdersStore } from "./admin-orders";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
'''))

# ============================================================
# components/admin/orders/OrderStatusBadge.tsx
# ============================================================
files.append(("components/admin/orders/OrderStatusBadge.tsx", '''"use client";

import type { Locale, AdminOrderStatus } from "@/lib/types";

interface OrderStatusBadgeProps {
  status: AdminOrderStatus;
  locale: Locale;
}

const CONFIG: Record<
  AdminOrderStatus,
  { bg: string; fa: string; en: string }
> = {
  pending: { bg: "#F59E0B", fa: "در انتظار", en: "Pending" },
  processing: { bg: "#00BFFF", fa: "در حال پردازش", en: "Processing" },
  shipped: { bg: "#8B5CF6", fa: "ارسال شده", en: "Shipped" },
  delivered: { bg: "#22C55E", fa: "تحویل شده", en: "Delivered" },
  cancelled: { bg: "#EF4444", fa: "لغو شده", en: "Cancelled" },
  refunded: { bg: "#94A3B8", fa: "مرجوع", en: "Refunded" },
};

export default function OrderStatusBadge({
  status,
  locale,
}: OrderStatusBadgeProps) {
  const isFa = locale === "fa";
  const c = CONFIG[status];

  return (
    <span
      className="text-[10px] px-2 py-1 rounded-full font-medium whitespace-nowrap inline-block"
      style={{ backgroundColor: `${c.bg}15`, color: c.bg }}
    >
      {isFa ? c.fa : c.en}
    </span>
  );
}
'''))

# ============================================================
# components/admin/orders/OrderFilters.tsx
# ============================================================
files.append(("components/admin/orders/OrderFilters.tsx", '''"use client";

import { Search, X } from "lucide-react";
import type { Locale, AdminOrderStatus, PaymentMethod } from "@/lib/types";

export interface OrderFilterValues {
  query: string;
  status: AdminOrderStatus | "all";
  payment: PaymentMethod | "all";
  sortBy: "newest" | "oldest" | "highest" | "lowest";
}

interface OrderFiltersProps {
  locale: Locale;
  values: OrderFilterValues;
  onChange: (values: OrderFilterValues) => void;
  resultCount: number;
}

export default function OrderFilters({
  locale,
  values,
  onChange,
  resultCount,
}: OrderFiltersProps) {
  const isFa = locale === "fa";

  const t = {
    search: isFa ? "جستجو در شماره، مشتری، موبایل..." : "Search ID, customer, mobile...",
    allStatus: isFa ? "همه وضعیت‌ها" : "All Status",
    pending: isFa ? "در انتظار" : "Pending",
    processing: isFa ? "در حال پردازش" : "Processing",
    shipped: isFa ? "ارسال شده" : "Shipped",
    delivered: isFa ? "تحویل شده" : "Delivered",
    cancelled: isFa ? "لغو شده" : "Cancelled",
    refunded: isFa ? "مرجوع" : "Refunded",
    allPayments: isFa ? "همه پرداخت‌ها" : "All Payments",
    zarinpal: "زرین‌پال",
    idpay: "IDPay",
    nextpay: "NextPay",
    cod: isFa ? "پرداخت در محل" : "Cash on Delivery",
    newest: isFa ? "جدیدترین" : "Newest",
    oldest: isFa ? "قدیمی‌ترین" : "Oldest",
    highest: isFa ? "بیشترین مبلغ" : "Highest Amount",
    lowest: isFa ? "کمترین مبلغ" : "Lowest Amount",
    results: isFa ? "سفارش" : "orders",
    clear: isFa ? "پاک کردن" : "Clear",
  };

  const hasFilters =
    values.query || values.status !== "all" || values.payment !== "all";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-3 md:p-4 space-y-3">
      <div className="flex flex-col md:flex-row gap-2 md:gap-3">
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

        <select
          value={values.status}
          onChange={(e) =>
            onChange({ ...values, status: e.target.value as OrderFilterValues["status"] })
          }
          className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
        >
          <option value="all">{t.allStatus}</option>
          <option value="pending">{t.pending}</option>
          <option value="processing">{t.processing}</option>
          <option value="shipped">{t.shipped}</option>
          <option value="delivered">{t.delivered}</option>
          <option value="cancelled">{t.cancelled}</option>
          <option value="refunded">{t.refunded}</option>
        </select>

        <select
          value={values.payment}
          onChange={(e) =>
            onChange({ ...values, payment: e.target.value as OrderFilterValues["payment"] })
          }
          className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
        >
          <option value="all">{t.allPayments}</option>
          <option value="zarinpal">{t.zarinpal}</option>
          <option value="idpay">{t.idpay}</option>
          <option value="nextpay">{t.nextpay}</option>
          <option value="cod">{t.cod}</option>
        </select>

        <select
          value={values.sortBy}
          onChange={(e) =>
            onChange({ ...values, sortBy: e.target.value as OrderFilterValues["sortBy"] })
          }
          className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
        >
          <option value="newest">{t.newest}</option>
          <option value="oldest">{t.oldest}</option>
          <option value="highest">{t.highest}</option>
          <option value="lowest">{t.lowest}</option>
        </select>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-[11px] text-[#A1A3A8]">
          {resultCount.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.results}
        </div>
        {hasFilters && (
          <button
            onClick={() =>
              onChange({ query: "", status: "all", payment: "all", sortBy: "newest" })
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
'''))

# ============================================================
# components/admin/orders/OrderDetailDrawer.tsx
# ============================================================
files.append(("components/admin/orders/OrderDetailDrawer.tsx", '''"use client";

import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";
import {
  X,
  MapPin,
  Phone,
  User,
  CreditCard,
  Truck,
  Package,
  Copy,
  Check,
  Printer,
  Send,
} from "lucide-react";
import { useState } from "react";
import type { Locale, AdminOrder, AdminOrderStatus } from "@/lib/types";
import { formatPrice, formatDate } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";

interface OrderDetailDrawerProps {
  locale: Locale;
  order: AdminOrder | null;
  onClose: () => void;
  onStatusChange: (id: string, status: AdminOrderStatus) => void;
}

const STATUS_OPTIONS: Array<{ value: AdminOrderStatus; fa: string; en: string }> = [
  { value: "pending", fa: "در انتظار", en: "Pending" },
  { value: "processing", fa: "در حال پردازش", en: "Processing" },
  { value: "shipped", fa: "ارسال شده", en: "Shipped" },
  { value: "delivered", fa: "تحویل شده", en: "Delivered" },
  { value: "cancelled", fa: "لغو شده", en: "Cancelled" },
  { value: "refunded", fa: "مرجوع", en: "Refunded" },
];

export default function OrderDetailDrawer({
  locale,
  order,
  onClose,
  onStatusChange,
}: OrderDetailDrawerProps) {
  const isFa = locale === "fa";
  const [copied, setCopied] = useState(false);

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const t = {
    title: isFa ? "جزئیات سفارش" : "Order Details",
    customer: isFa ? "مشتری" : "Customer",
    address: isFa ? "آدرس" : "Address",
    items: isFa ? "محصولات" : "Items",
    summary: isFa ? "خلاصه مالی" : "Summary",
    subtotal: isFa ? "جمع کالاها" : "Subtotal",
    discount: isFa ? "تخفیف" : "Discount",
    shipping: isFa ? "ارسال" : "Shipping",
    total: isFa ? "مبلغ کل" : "Total",
    payment: isFa ? "روش پرداخت" : "Payment Method",
    shippingMethod: isFa ? "روش ارسال" : "Shipping Method",
    changeStatus: isFa ? "تغییر وضعیت" : "Change Status",
    printInvoice: isFa ? "چاپ فاکتور" : "Print Invoice",
    sendNotification: isFa ? "ارسال اعلان" : "Send Notification",
    trackingCode: isFa ? "کد پیگیری" : "Tracking Code",
    orderDate: isFa ? "تاریخ سفارش" : "Order Date",
    noTracking: isFa ? "کد پیگیری ثبت نشده" : "No tracking code",
  };

  return (
    <AnimatePresence>
      {order && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[150]"
            onClick={onClose}
          />

          <motion.aside
            initial={{ x: isFa ? "100%" : "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: isFa ? "100%" : "-100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed top-0 bottom-0 w-full max-w-lg bg-white dark:bg-[#1A1A1E] shadow-2xl z-[151] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 }}
          >
            <div className="sticky top-0 bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] p-4 flex items-center justify-between z-10">
              <div className="flex items-center gap-2">
                <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                  {t.title}
                </h2>
                <button
                  onClick={() => handleCopy(order.id)}
                  className="w-6 h-6 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
                  title="Copy ID"
                >
                  {copied ? <Check size={12} className="text-[#22C55E]" /> : <Copy size={12} />}
                </button>
              </div>
              <button
                onClick={onClose}
                aria-label="Close"
                className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-4 space-y-5">
              {/* Order ID + Status */}
              <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-[11px] text-[#A1A3A8]">
                    {isFa ? "شماره سفارش" : "Order ID"}
                  </div>
                  <OrderStatusBadge status={order.status} locale={locale} />
                </div>
                <div className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                  {order.id}
                </div>
                <div className="text-[10px] text-[#A1A3A8] mt-1">
                  {t.orderDate}: {formatDate(order.createdAt, locale)}
                </div>
              </div>

              {/* Customer */}
              <div>
                <h3 className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
                  <User size={14} className="text-[#EF4056]" />
                  {t.customer}
                </h3>
                <div className="space-y-2 text-[12px]">
                  <div className="flex items-center gap-2">
                    <User size={12} className="text-[#A1A3A8]" />
                    <span className="text-[#62666D] dark:text-[#A1A3A8]">{order.customerName}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone size={12} className="text-[#A1A3A8]" />
                    <span className="text-[#62666D] dark:text-[#A1A3A8]" dir="ltr">
                      {order.customerMobile}
                    </span>
                  </div>
                  <div className="flex items-start gap-2">
                    <MapPin size={12} className="text-[#A1A3A8] mt-0.5 shrink-0" />
                    <span className="text-[#62666D] dark:text-[#A1A3A8] leading-5">
                      {order.address}
                    </span>
                  </div>
                </div>
              </div>

              {/* Items */}
              <div>
                <h3 className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
                  <Package size={14} className="text-[#EF4056]" />
                  {t.items} ({order.items.length})
                </h3>
                <div className="space-y-2">
                  {order.items.map((item, i) => (
                    <div
                      key={i}
                      className="flex items-center gap-3 p-2 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg"
                    >
                      <div className="w-12 h-12 rounded-lg bg-white dark:bg-[#1A1A1E] overflow-hidden relative shrink-0">
                        <Image
                          src={item.image}
                          alt={isFa ? item.titleFa : item.titleEn}
                          fill
                          sizes="48px"
                          className="object-cover"
                        />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA] truncate">
                          {isFa ? item.titleFa : item.titleEn}
                        </div>
                        <div className="text-[10px] text-[#A1A3A8] mt-0.5">
                          {item.quantity.toLocaleString(isFa ? "fa-IR" : "en-US")} ×{" "}
                          {formatPrice(item.price, locale)}
                        </div>
                      </div>
                      <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] shrink-0">
                        {formatPrice(item.price * item.quantity, locale)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Summary */}
              <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-xl p-4 space-y-2 text-[12px]">
                <div className="flex justify-between">
                  <span className="text-[#62666D] dark:text-[#A1A3A8]">{t.subtotal}</span>
                  <span className="text-[#3F4064] dark:text-[#E5E5EA] font-medium">
                    {formatPrice(order.subtotal, locale)}
                  </span>
                </div>
                {order.discount > 0 && (
                  <div className="flex justify-between">
                    <span className="text-[#62666D] dark:text-[#A1A3A8]">{t.discount}</span>
                    <span className="text-[#EF4056] font-medium">
                      -{formatPrice(order.discount, locale)}
                    </span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span className="text-[#62666D] dark:text-[#A1A3A8]">{t.shipping}</span>
                  <span
                    className={
                      order.shipping === 0
                        ? "text-[#22C55E] font-medium"
                        : "text-[#3F4064] dark:text-[#E5E5EA] font-medium"
                    }
                  >
                    {order.shipping === 0
                      ? isFa
                        ? "رایگان"
                        : "Free"
                      : formatPrice(order.shipping, locale)}
                  </span>
                </div>
                <div className="flex justify-between pt-2 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
                  <span className="font-bold text-[#3F4064] dark:text-[#E5E5EA]">{t.total}</span>
                  <span className="font-bold text-[#EF4056] text-[14px]">
                    {formatPrice(order.total, locale)}
                  </span>
                </div>
              </div>

              {/* Payment + Shipping */}
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg p-3">
                  <div className="flex items-center gap-1.5 mb-1">
                    <CreditCard size={12} className="text-[#8B5CF6]" />
                    <span className="text-[10px] text-[#A1A3A8]">{t.payment}</span>
                  </div>
                  <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
                    {order.paymentMethod}
                  </div>
                </div>
                <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg p-3">
                  <div className="flex items-center gap-1.5 mb-1">
                    <Truck size={12} className="text-[#00BFFF]" />
                    <span className="text-[10px] text-[#A1A3A8]">{t.shippingMethod}</span>
                  </div>
                  <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
                    {order.shippingMethod}
                  </div>
                </div>
              </div>

              {/* Tracking Code */}
              <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg p-3">
                <div className="text-[10px] text-[#A1A3A8] mb-1">{t.trackingCode}</div>
                <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                  {order.trackingCode || t.noTracking}
                </div>
              </div>

              {/* Change Status */}
              <div>
                <h3 className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
                  {t.changeStatus}
                </h3>
                <div className="grid grid-cols-3 gap-2">
                  {STATUS_OPTIONS.map((opt) => (
                    <button
                      key={opt.value}
                      onClick={() => onStatusChange(order.id, opt.value)}
                      className={`h-9 rounded-lg text-[11px] font-medium transition-colors ${
                        order.status === opt.value
                          ? "bg-[#EF4056] text-white"
                          : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#EF4056]/10"
                      }`}
                    >
                      {isFa ? opt.fa : opt.en}
                    </button>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="pt-4 border-t border-[#E0E0E2] dark:border-[#2A2A2E] space-y-2">
                <button className="w-full h-10 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center justify-center gap-2">
                  <Printer size={14} />
                  {t.printInvoice}
                </button>
                <button className="w-full h-10 rounded-lg bg-[#00BFFF]/10 text-[#00BFFF] hover:bg-[#00BFFF]/20 text-[12px] font-medium transition-colors flex items-center justify-center gap-2">
                  <Send size={14} />
                  {t.sendNotification}
                </button>
              </div>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
'''))

# ============================================================
# components/admin/orders/index.ts
# ============================================================
files.append(("components/admin/orders/index.ts", '''// components/admin/orders/index.ts
export { default as OrderStatusBadge } from "./OrderStatusBadge";
export { default as OrderFilters } from "./OrderFilters";
export type { OrderFilterValues } from "./OrderFilters";
export { default as OrderDetailDrawer } from "./OrderDetailDrawer";
'''))

# ============================================================
# components/admin/OrdersView.tsx (rewritten)
# ============================================================
files.append(("components/admin/OrdersView.tsx", '''"use client";

import { useState, useMemo, useEffect } from "react";
import { Eye, Download, ShoppingCart } from "lucide-react";
import type { Locale, AdminOrder, AdminOrderStatus } from "@/lib/types";
import { useAdminOrdersStore, useToastStore } from "@/lib/stores";
import { formatPrice, formatRelativeTime } from "@/lib/utils";
import OrderStatusBadge from "./orders/OrderStatusBadge";
import OrderFilters, { type OrderFilterValues } from "./orders/OrderFilters";
import OrderDetailDrawer from "./orders/OrderDetailDrawer";

interface OrdersViewProps {
  locale: Locale;
}

const ITEMS_PER_PAGE = 20;

export default function OrdersView({ locale }: OrdersViewProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const orders = useAdminOrdersStore((s) => s.orders);
  const updateStatus = useAdminOrdersStore((s) => s.updateStatus);
  const [mounted, setMounted] = useState(false);

  const [filters, setFilters] = useState<OrderFilterValues>({
    query: "",
    status: "all",
    payment: "all",
    sortBy: "newest",
  });
  const [page, setPage] = useState(1);
  const [selectedOrder, setSelectedOrder] = useState<AdminOrder | null>(null);

  useEffect(() => setMounted(true), []);

  const filtered = useMemo(() => {
    let result = [...orders];
    const q = filters.query.toLowerCase().trim();

    if (q) {
      result = result.filter(
        (o) =>
          o.id.toLowerCase().includes(q) ||
          o.customerName.toLowerCase().includes(q) ||
          o.customerMobile.includes(q)
      );
    }

    if (filters.status !== "all") {
      result = result.filter((o) => o.status === filters.status);
    }

    if (filters.payment !== "all") {
      result = result.filter((o) => o.paymentMethod === filters.payment);
    }

    switch (filters.sortBy) {
      case "oldest":
        result.sort(
          (a, b) =>
            new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
        );
        break;
      case "highest":
        result.sort((a, b) => b.total - a.total);
        break;
      case "lowest":
        result.sort((a, b) => a.total - b.total);
        break;
      case "newest":
      default:
        result.sort(
          (a, b) =>
            new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
        );
    }

    return result;
  }, [orders, filters]);

  const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
  const paginated = filtered.slice(
    (page - 1) * ITEMS_PER_PAGE,
    page * ITEMS_PER_PAGE
  );

  useEffect(() => setPage(1), [filters]);

  const handleStatusChange = (id: string, status: AdminOrderStatus) => {
    updateStatus(id, status);
    setSelectedOrder((prev) => (prev ? { ...prev, status } : prev));
    pushToast({
      type: "success",
      titleFa: "وضعیت سفارش به‌روزرسانی شد",
      titleEn: "Order status updated",
    });
  };

  const t = {
    title: isFa ? "مدیریت سفارشات" : "Orders Management",
    subtitle: isFa
      ? `${filtered.length.toLocaleString("fa-IR")} سفارش`
      : `${filtered.length.toLocaleString("en-US")} orders`,
    export: isFa ? "خروجی CSV" : "Export CSV",
    orderId: isFa ? "شماره" : "Order",
    customer: isFa ? "مشتری" : "Customer",
    items: isFa ? "محصولات" : "Items",
    total: isFa ? "مبلغ" : "Total",
    status: isFa ? "وضعیت" : "Status",
    date: isFa ? "تاریخ" : "Date",
    actions: isFa ? "عملیات" : "Actions",
    itemsCount: isFa ? "قلم" : "items",
    empty: isFa ? "سفارشی یافت نشد" : "No orders found",
    page: isFa ? "صفحه" : "Page",
    of: isFa ? "از" : "of",
  };

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-[#EF4056]/10 flex items-center justify-center shrink-0">
            <ShoppingCart size={20} className="text-[#EF4056]" />
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
      <OrderFilters
        locale={locale}
        values={filters}
        onChange={setFilters}
        resultCount={filtered.length}
      />

      {/* Table */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[800px]">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[10px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-start p-3 font-medium">{t.orderId}</th>
                <th className="text-start p-3 font-medium">{t.customer}</th>
                <th className="text-start p-3 font-medium">{t.items}</th>
                <th className="text-start p-3 font-medium">{t.total}</th>
                <th className="text-start p-3 font-medium">{t.status}</th>
                <th className="text-start p-3 font-medium">{t.date}</th>
                <th className="text-start p-3 font-medium">{t.actions}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {paginated.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-16 text-center text-[13px] text-[#A1A3A8]">
                    {t.empty}
                  </td>
                </tr>
              ) : (
                paginated.map((order) => (
                  <tr
                    key={order.id}
                    className="hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors cursor-pointer"
                    onClick={() => setSelectedOrder(order)}
                  >
                    <td className="p-3">
                      <div className="text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
                        {order.id}
                      </div>
                    </td>
                    <td className="p-3">
                      <div className="text-[11px] text-[#3F4064] dark:text-[#E5E5EA] truncate max-w-[120px]">
                        {order.customerName}
                      </div>
                      <div className="text-[10px] text-[#A1A3A8]" dir="ltr">
                        {order.customerMobile}
                      </div>
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {order.itemsCount.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.itemsCount}
                    </td>
                    <td className="p-3 text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                      {formatPrice(order.total, locale)}
                    </td>
                    <td className="p-3">
                      <OrderStatusBadge status={order.status} locale={locale} />
                    </td>
                    <td className="p-3 text-[10px] text-[#A1A3A8]">
                      {formatRelativeTime(
                        new Date(order.createdAt).getTime(),
                        locale
                      )}
                    </td>
                    <td className="p-3" onClick={(e) => e.stopPropagation()}>
                      <button
                        onClick={() => setSelectedOrder(order)}
                        className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
                      >
                        <Eye size={14} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {totalPages > 1 && (
          <div className="flex items-center justify-between p-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex-wrap gap-3">
            <span className="text-[11px] text-[#A1A3A8]">
              {t.page} {page.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.of}{" "}
              {totalPages.toLocaleString(isFa ? "fa-IR" : "en-US")}
            </span>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="h-8 px-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? "قبلی" : "Prev"}
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="h-8 px-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? "بعدی" : "Next"}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Detail Drawer */}
      <OrderDetailDrawer
        locale={locale}
        order={selectedOrder}
        onClose={() => setSelectedOrder(null)}
        onStatusChange={handleStatusChange}
      />
    </div>
  );
}
'''))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", '''// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as DashboardView } from "./DashboardView";
export { default as AnalyticsView } from "./AnalyticsView";
export { default as UsersView } from "./UsersView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as AdminLoginForm } from "./AdminLoginForm";

// Layout
export * from "./layout";

// Dashboard
export * from "./dashboard";

// Analytics
export * from "./analytics";

// Users
export * from "./users";

// Products
export * from "./products";

// Orders
export * from "./orders";

// Charts
export * from "./charts";
'''))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 7: Orders Management")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")
    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/orders")

if __name__ == "__main__":
    main()