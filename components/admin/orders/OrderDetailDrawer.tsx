"use client";

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
