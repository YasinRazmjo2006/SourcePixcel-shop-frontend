"use client";

import { useState, useMemo, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import {
  FileText,
  Plus,
  Download,
  Users as UsersIcon,
  ShoppingCart,
  Package,
  DollarSign,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import {
  useAdminReportsStore,
  useAdminOrdersStore,
  useAdminProductsStore,
  useToastStore,
} from "@/lib/stores";
import { adminUsers } from "@/lib/data";
import {
  formatPrice,
  formatDate,
  exportToCSV,
  exportToExcel,
  exportToPDF,
  type CsvColumn,
} from "@/lib/utils";
import type { ReportType, ReportFormat } from "@/lib/stores";
import ReportCard from "./reports/ReportCard";
import ReportBuilder from "./reports/ReportBuilder";
import ExportButtons from "./reports/ExportButtons";

interface ReportsViewProps {
  locale: Locale;
}

export default function ReportsView({ locale }: ReportsViewProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const savedReports = useAdminReportsStore((s) => s.savedReports);
  const addReport = useAdminReportsStore((s) => s.addReport);
  const removeReport = useAdminReportsStore((s) => s.removeReport);

  const orders = useAdminOrdersStore((s) => s.orders);
  const products = useAdminProductsStore((s) => s.products);

  const [mounted, setMounted] = useState(false);
  const [builderOpen, setBuilderOpen] = useState(false);
  const [activeType, setActiveType] = useState<ReportType>("orders");

  useEffect(() => setMounted(true), []);

  // Build current data based on type
  const currentData = useMemo(() => {
    if (activeType === "orders") return orders.slice(0, 100);
    if (activeType === "users") return adminUsers.slice(0, 100);
    if (activeType === "products") return products.slice(0, 100);
    return orders.slice(0, 100);
  }, [activeType, orders, products]);

  const columns: CsvColumn<Record<string, unknown>>[] = useMemo(() => {
    if (activeType === "orders") {
      return [
        { key: "id", label: isFa ? "شماره سفارش" : "Order ID" },
        { key: "customerName", label: isFa ? "مشتری" : "Customer" },
        { key: "customerMobile", label: isFa ? "موبایل" : "Mobile" },
        { key: "itemsCount", label: isFa ? "تعداد اقلام" : "Items" },
        {
          key: "total",
          label: isFa ? "مبلغ کل (تومان)" : "Total (T)",
          formatter: (v) => formatPrice(Number(v), locale),
        },
        { key: "status", label: isFa ? "وضعیت" : "Status" },
        {
          key: "createdAt",
          label: isFa ? "تاریخ" : "Date",
          formatter: (v) => formatDate(String(v), locale),
        },
      ];
    }
    if (activeType === "users") {
      return [
        { key: "id", label: "ID" },
        { key: "fullName", label: isFa ? "نام" : "Name" },
        { key: "email", label: isFa ? "ایمیل" : "Email" },
        { key: "mobile", label: isFa ? "موبایل" : "Mobile" },
        { key: "role", label: isFa ? "نقش" : "Role" },
        { key: "city", label: isFa ? "شهر" : "City" },
        { key: "ordersCount", label: isFa ? "تعداد سفارش" : "Orders" },
        {
          key: "totalSpent",
          label: isFa ? "مجموع خرید" : "Total Spent",
          formatter: (v) => formatPrice(Number(v), locale),
        },
      ];
    }
    if (activeType === "products") {
      return [
        { key: "id", label: "ID" },
        {
          key: "titleFa",
          label: isFa ? "عنوان" : "Title",
          formatter: (_v, row) =>
            isFa
              ? String(row.titleFa ?? "")
              : String(row.titleEn ?? ""),
        },
        { key: "brand", label: isFa ? "برند" : "Brand" },
        { key: "category", label: isFa ? "دسته" : "Category" },
        {
          key: "price",
          label: isFa ? "قیمت (تومان)" : "Price (T)",
          formatter: (v) => formatPrice(Number(v), locale),
        },
        {
          key: "finalPrice",
          label: isFa ? "قیمت نهایی" : "Final Price",
          formatter: (v) => formatPrice(Number(v), locale),
        },
        { key: "inStock", label: isFa ? "موجود" : "In Stock" },
      ];
    }
    return [];
  }, [activeType, locale, isFa]);

  const handleExport = (format: ReportFormat) => {
    const filename = `${activeType}-report-${Date.now()}`;
    const title = isFa
      ? `گزارش ${activeType === "orders" ? "سفارشات" : activeType === "users" ? "کاربران" : "محصولات"}`
      : `${activeType} Report`;

    try {
      if (format === "csv") {
        exportToCSV(currentData, columns, filename);
      } else if (format === "excel") {
        exportToExcel(currentData, columns, filename, activeType);
      } else {
        exportToPDF({
          title,
          subtitle: isFa
            ? `${currentData.length} رکورد`
            : `${currentData.length} records`,
          data: currentData,
          columns,
          filename,
          locale,
        });
      }

      pushToast({
        type: "success",
        titleFa: "گزارش دانلود شد",
        titleEn: "Report downloaded",
        messageFa: filename,
        messageEn: filename,
      });
    } catch (error) {
      pushToast({
        type: "error",
        titleFa: "خطا در دانلود",
        titleEn: "Download error",
      });
    }
  };

  const handleSaveReport = (data: {
    name: string;
    type: ReportType;
    format: ReportFormat;
    schedule?: "daily" | "weekly" | "monthly";
  }) => {
    addReport(data);
    setBuilderOpen(false);
    pushToast({
      type: "success",
      titleFa: "گزارش ذخیره شد",
      titleEn: "Report saved",
    });
  };

  const t = {
    title: isFa ? "گزارشات" : "Reports",
    subtitle: isFa
      ? "ساخت، مدیریت و دانلود گزارش‌های سفارشی"
      : "Create, manage and download custom reports",
    newReport: isFa ? "گزارش جدید" : "New Report",
    quickExport: isFa ? "خروجی سریع" : "Quick Export",
    savedReports: isFa ? "گزارش‌های ذخیره شده" : "Saved Reports",
    emptyReports: isFa
      ? "هنوز گزارشی ذخیره نکرده‌اید"
      : "You haven't saved any reports yet",
    orders: isFa ? "سفارشات" : "Orders",
    users: isFa ? "کاربران" : "Users",
    products: isFa ? "محصولات" : "Products",
    sales: isFa ? "فروش" : "Sales",
    records: isFa ? "رکورد" : "records",
  };

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  const quickExportTypes: Array<{
    value: ReportType;
    icon: typeof ShoppingCart;
    label: string;
    color: string;
  }> = [
    { value: "orders", icon: ShoppingCart, label: t.orders, color: "#EF4056" },
    { value: "users", icon: UsersIcon, label: t.users, color: "#00BFFF" },
    { value: "products", icon: Package, label: t.products, color: "#8B5CF6" },
    { value: "sales", icon: DollarSign, label: t.sales, color: "#22C55E" },
  ];

  return (
    <div className="space-y-4 md:space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {t.title}
          </h1>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.subtitle}
          </p>
        </div>
        <button
          onClick={() => setBuilderOpen((v) => !v)}
          className="h-10 px-4 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Plus size={14} />
          {t.newReport}
        </button>
      </div>

      {/* Builder */}
      <AnimatePresence>
        {builderOpen && (
          <ReportBuilder
            locale={locale}
            onSave={handleSaveReport}
            onCancel={() => setBuilderOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Quick Export */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-5">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center">
            <Download size={16} className="text-[#EF4056]" />
          </div>
          <div>
            <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
              {t.quickExport}
            </h2>
            <p className="text-[10px] text-[#A1A3A8]">
              {currentData.length.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
              {t.records}
            </p>
          </div>
        </div>

        {/* Type selector */}
        <div className="flex flex-wrap gap-2 mb-4">
          {quickExportTypes.map((tp) => {
            const Icon = tp.icon;
            return (
              <button
                key={tp.value}
                onClick={() => setActiveType(tp.value)}
                className={`h-9 px-3 rounded-lg text-[11px] font-medium transition-all flex items-center gap-1.5 ${
                  activeType === tp.value
                    ? "text-white shadow-sm"
                    : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#3A3A40]"
                }`}
                style={
                  activeType === tp.value
                    ? { backgroundColor: tp.color }
                    : undefined
                }
              >
                <Icon size={13} />
                {tp.label}
              </button>
            );
          })}
        </div>

        {/* Export buttons */}
        <div className="pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
          <ExportButtons
            locale={locale}
            onExport={handleExport}
            disabled={currentData.length === 0}
          />
        </div>
      </div>

      {/* Saved Reports */}
      <div>
        <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
          <FileText size={16} className="text-[#EF4056]" />
          {t.savedReports}
          <span className="text-[11px] text-[#A1A3A8] font-normal">
            ({savedReports.length.toLocaleString(isFa ? "fa-IR" : "en-US")})
          </span>
        </h2>

        {savedReports.length === 0 ? (
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-12 text-center">
            <div className="w-14 h-14 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
              <FileText size={24} className="text-[#A1A3A8]" />
            </div>
            <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8]">
              {t.emptyReports}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
            {savedReports.map((report, i) => (
              <ReportCard
                key={report.id}
                locale={locale}
                report={report}
                delay={i * 0.05}
                onDownload={() => {
                  setActiveType(report.type);
                  setTimeout(() => handleExport(report.format), 100);
                }}
                onDelete={() => {
                  removeReport(report.id);
                  pushToast({
                    type: "info",
                    titleFa: "گزارش حذف شد",
                    titleEn: "Report deleted",
                  });
                }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
