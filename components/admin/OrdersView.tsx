"use client";

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
