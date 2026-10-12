"use client";

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
