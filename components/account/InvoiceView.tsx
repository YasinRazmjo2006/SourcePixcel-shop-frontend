"use client";

import Image from "next/image";
import { Printer, ArrowRight, ArrowLeft } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import type { MockOrder } from "@/lib/data";
import { products as allProducts } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface InvoiceViewProps {
  locale: Locale;
  order: MockOrder;
  onBack: () => void;
}

export default function InvoiceView({
  locale,
  order,
  onBack,
}: InvoiceViewProps) {
  const isFa = locale === "fa";

  const lines = order.items
    .map((item) => {
      const product = allProducts.find((p) => p.id === item.productId);
      return product ? { ...item, product } : null;
    })
    .filter((x): x is typeof x & { product: Product } => x !== null);

  const subtotal = lines.reduce(
    (s, l) => s + l.priceAtPurchase * l.quantity,
    0
  );
  const shipping = 45_000;

  const t = {
    invoice: isFa ? "فاکتور سفارش" : "Order Invoice",
    orderNumber: isFa ? "شماره سفارش" : "Order Number",
    date: isFa ? "تاریخ" : "Date",
    status: isFa ? "وضعیت" : "Status",
    shippingAddress: isFa ? "آدرس ارسال" : "Shipping Address",
    product: isFa ? "محصول" : "Product",
    quantity: isFa ? "تعداد" : "Qty",
    unitPrice: isFa ? "قیمت واحد" : "Unit Price",
    total: isFa ? "جمع" : "Total",
    subtotal: isFa ? "جمع کالاها" : "Subtotal",
    shippingCost: isFa ? "هزینه ارسال" : "Shipping",
    grandTotal: isFa ? "مبلغ نهایی" : "Grand Total",
    print: isFa ? "چاپ فاکتور" : "Print Invoice",
    back: isFa ? "بازگشت" : "Back",
    companyName: isFa ? "فروشگاه SourcePixcel" : "SourcePixcel Store",
    companyAddress: isFa
      ? "تهران، خیابان ولیعصر، پلاک ۱۲۳"
      : "Tehran, Valiasr St., No. 123",
    companyPhone: "021-12345678",
    companyEmail: "support@sourcepixcel.com",
    thankYou: isFa
      ? "از خرید شما سپاسگزاریم"
      : "Thank you for your purchase",
    terms: isFa
      ? "این فاکتور به عنوان رسید خرید معتبر است."
      : "This invoice is a valid purchase receipt.",
    statusLabels: {
      pending: isFa ? "در انتظار پرداخت" : "Pending",
      processing: isFa ? "در حال پردازش" : "Processing",
      shipped: isFa ? "ارسال شده" : "Shipped",
      delivered: isFa ? "تحویل داده شده" : "Delivered",
      cancelled: isFa ? "لغو شده" : "Cancelled",
    },
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <>
      {/* Action buttons (hidden in print) */}
      <div className="no-print flex items-center justify-between gap-3 mb-4 flex-wrap">
        <button
          onClick={onBack}
          className="h-10 px-4 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-2"
        >
          {isFa ? <ArrowRight size={16} /> : <ArrowLeft size={16} />}
          {t.back}
        </button>
        <button
          onClick={handlePrint}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Printer size={16} />
          {t.print}
        </button>
      </div>

      {/* Invoice */}
      <div className="print-content bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-6 md:p-8">
        {/* Header */}
        <div className="flex items-start justify-between gap-4 pb-6 border-b-2 border-[#EF4056] mb-6 flex-wrap">
          <div>
            <div className="flex items-center gap-3 mb-3">
              <div className="w-12 h-12 rounded-xl bg-[#EF4056] flex items-center justify-center text-white text-[22px] font-bold">
                S
              </div>
              <div>
                <div className="text-[18px] font-bold text-[#EF4056]">
                  SourcePixcel
                </div>
                <div className="text-[11px] text-[#A1A3A8]">
                  {t.companyAddress}
                </div>
              </div>
            </div>
            <div className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] space-y-1">
              <div>📞 {t.companyPhone}</div>
              <div>✉️ {t.companyEmail}</div>
            </div>
          </div>

          <div className="text-start">
            <div className="text-[22px] md:text-[26px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
              {t.invoice}
            </div>
            <div className="space-y-1.5 text-[12px]">
              <div className="flex items-center gap-2">
                <span className="text-[#A1A3A8]">{t.orderNumber}:</span>
                <span
                  className="font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums"
                  dir="ltr"
                >
                  {order.id}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[#A1A3A8]">{t.date}:</span>
                <span className="text-[#3F4064] dark:text-[#E5E5EA]">
                  {order.date}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[#A1A3A8]">{t.status}:</span>
                <span className="inline-block text-[10px] font-medium px-2 py-0.5 rounded-full bg-[#22C55E]/10 text-[#22C55E]">
                  {t.statusLabels[order.status]}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Shipping address */}
        <div className="mb-6">
          <h3 className="text-[12px] font-bold text-[#A1A3A8] uppercase mb-2">
            {t.shippingAddress}
          </h3>
          <p className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA] leading-6">
            {order.shippingAddress}
          </p>
        </div>

        {/* Items table */}
        <div className="overflow-x-auto mb-6">
          <table className="w-full">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[11px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-right p-3 font-medium">{t.product}</th>
                <th className="text-right p-3 font-medium w-20">{t.quantity}</th>
                <th className="text-right p-3 font-medium w-32">{t.unitPrice}</th>
                <th className="text-right p-3 font-medium w-32">{t.total}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {lines.map((line, idx) => (
                <tr key={idx}>
                  <td className="p-3">
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0 no-print">
                        <Image
                          src={line.product.image}
                          alt={
                            isFa
                              ? line.product.titleFa
                              : line.product.titleEn
                          }
                          fill
                          sizes="48px"
                          className="object-cover"
                        />
                      </div>
                      <div>
                        <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA]">
                          {isFa
                            ? line.product.titleFa
                            : line.product.titleEn}
                        </div>
                        <div
                          className="text-[10px] text-[#A1A3A8]"
                          dir="ltr"
                        >
                          SP-
                          {line.product.id.toString().padStart(5, "0")}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="p-3 text-[12px] text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {isFa
                      ? line.quantity.toLocaleString("fa-IR")
                      : line.quantity}
                  </td>
                  <td className="p-3 text-[12px] text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {formatPrice(line.priceAtPurchase, locale)}
                  </td>
                  <td className="p-3 text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                    {formatPrice(
                      line.priceAtPurchase * line.quantity,
                      locale
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Totals */}
        <div className="flex justify-end mb-6">
          <div className="w-full max-w-xs space-y-2 text-[12px]">
            <div className="flex items-center justify-between">
              <span className="text-[#62666D] dark:text-[#A1A3A8]">
                {t.subtotal}
              </span>
              <span className="text-[#3F4064] dark:text-[#E5E5EA] tabular-nums">
                {formatPrice(subtotal, locale)}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-[#62666D] dark:text-[#A1A3A8]">
                {t.shippingCost}
              </span>
              <span className="text-[#22C55E] tabular-nums">
                {formatPrice(shipping, locale)}
              </span>
            </div>
            <div className="flex items-center justify-between pt-2 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.grandTotal}
              </span>
              <span className="text-[15px] font-bold text-[#EF4056] tabular-nums">
                {formatPrice(subtotal + shipping, locale)}{" "}
                <span className="text-[10px] text-[#A1A3A8] font-normal">
                  {isFa ? "تومان" : "T"}
                </span>
              </span>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-6 border-t border-dashed border-[#E0E0E2] dark:border-[#2A2A2E]">
          <div className="text-center space-y-2">
            <div className="text-[14px] font-bold text-[#EF4056]">
              {t.thankYou}
            </div>
            <div className="text-[11px] text-[#A1A3A8]">{t.terms}</div>
            <div className="pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] text-[10px] text-[#A1A3A8]">
              {t.companyName} — {new Date().getFullYear()}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
