"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import {
  ArrowRight,
  MapPin,
  Package,
  Truck,
  CheckCircle2,
  Receipt,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import type { MockOrder } from "@/lib/data";
import { products as allProducts } from "@/lib/data";
import { formatPrice } from "@/lib/utils";
import OrderStatusBadge from "./OrderStatusBadge";
import InvoiceView from "./InvoiceView";

interface OrderDetailViewProps {
  locale: Locale;
  order: MockOrder;
}

export default function OrderDetailView({
  locale,
  order,
}: OrderDetailViewProps) {
  const isFa = locale === "fa";
  const [showInvoice, setShowInvoice] = useState(false);

  const lines = order.items
    .map((item) => {
      const product = allProducts.find((p) => p.id === item.productId);
      return product ? { ...item, product } : null;
    })
    .filter((x): x is typeof x & { product: NonNullable<typeof x>["product"] } => x !== null);

  const steps = [
    { id: "pending", icon: Package, fa: "ثبت شده", en: "Placed" },
    { id: "processing", icon: Package, fa: "در حال پردازش", en: "Processing" },
    { id: "shipped", icon: Truck, fa: "ارسال شده", en: "Shipped" },
    { id: "delivered", icon: CheckCircle2, fa: "تحویل داده شده", en: "Delivered" },
  ];

  const statusIndex = steps.findIndex((s) => s.id === order.status);

  if (showInvoice) {
    return (
      <InvoiceView
        locale={locale}
        order={order}
        onBack={() => setShowInvoice(false)}
      />
    );
  }

  return (
    <div className="space-y-4">
      {/* Back + invoice button */}
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <Link
          href={`/${locale}/account/orders`}
          className="inline-flex items-center gap-2 text-[12px] text-[#00BFFF] hover:text-[#EF4056] transition-colors"
        >
          <ArrowRight
            size={14}
            className={isFa ? "" : "rotate-180"}
          />
          {isFa ? "بازگشت به سفارشات" : "Back to orders"}
        </Link>

        <button
          onClick={() => setShowInvoice(true)}
          className="h-9 px-4 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-2"
        >
          <Receipt size={14} />
          {isFa ? "مشاهده فاکتور" : "View Invoice"}
        </button>
      </div>

      {/* Header */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
          <div>
            <div className="text-[11px] text-[#A1A3A8] mb-1">
              {isFa ? "شماره سفارش" : "Order Number"}
            </div>
            <div className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA]" dir="ltr">
              {order.id}
            </div>
          </div>
          <OrderStatusBadge status={order.status} locale={locale} />
        </div>

        {/* Progress */}
        <div className="flex items-center justify-between max-w-2xl mx-auto mt-6">
          {steps.map((step, i) => {
            const Icon = step.icon;
            const done = i <= statusIndex;
            const active = i === statusIndex;
            return (
              <div key={step.id} className="flex items-center flex-1">
                <div className="flex flex-col items-center gap-2 shrink-0">
                  <div
                    className={`w-9 h-9 rounded-full flex items-center justify-center transition-colors ${
                      done
                        ? active
                          ? "bg-[#EF4056] text-white"
                          : "bg-[#22C55E] text-white"
                        : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#A1A3A8]"
                    }`}
                  >
                    <Icon size={16} />
                  </div>
                  <span
                    className={`text-[10px] text-center whitespace-nowrap ${
                      done ? "text-[#3F4064] dark:text-[#E5E5EA] font-medium" : "text-[#A1A3A8]"
                    }`}
                  >
                    {isFa ? step.fa : step.en}
                  </span>
                </div>
                {i < steps.length - 1 && (
                  <div
                    className={`flex-1 h-[2px] mx-2 mb-6 ${
                      i < statusIndex ? "bg-[#22C55E]" : "bg-[#E0E0E2] dark:bg-[#2A2A2E]"
                    }`}
                  />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Items */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
          {isFa ? "محصولات سفارش" : "Order Items"}
        </h3>
        <div className="space-y-3">
          {lines.map((line, i) => (
            <div
              key={i}
              className="flex items-center gap-3 pb-3 border-b border-[#F5F5F5] dark:border-[#2A2A2E] last:border-0 last:pb-0"
            >
              <Link
                href={`/${locale}/product/${line.product.slug}`}
                className="w-14 h-14 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0"
              >
                <Image
                  src={line.product.image}
                  alt={isFa ? line.product.titleFa : line.product.titleEn}
                  fill
                  sizes="56px"
                  className="object-cover"
                />
              </Link>
              <div className="flex-1 min-w-0">
                <Link
                  href={`/${locale}/product/${line.product.slug}`}
                  className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 hover:text-[#EF4056]"
                >
                  {isFa ? line.product.titleFa : line.product.titleEn}
                </Link>
                <div className="text-[11px] text-[#A1A3A8] mt-1">
                  {isFa
                    ? `${line.quantity.toLocaleString("fa-IR")} عدد`
                    : `${line.quantity} pcs`}
                </div>
              </div>
              <div className="text-left shrink-0">
                <div className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                  {formatPrice(line.priceAtPurchase * line.quantity, locale)}
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] mt-4 pt-4 flex justify-between items-center">
          <span className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {isFa ? "مجموع" : "Total"}
          </span>
          <div className="flex items-center gap-1">
            <span className="text-[18px] font-bold text-[#EF4056]">
              {formatPrice(order.total, locale)}
            </span>
            <span className="text-[11px] text-[#62666D]">
              {isFa ? "تومان" : "Toman"}
            </span>
          </div>
        </div>
      </div>

      {/* Shipping */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3 flex items-center gap-2">
          <MapPin size={16} className="text-[#EF4056]" />
          {isFa ? "آدرس ارسال" : "Shipping Address"}
        </h3>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6">
          {order.shippingAddress}
        </p>
      </div>
    </div>
  );
}
