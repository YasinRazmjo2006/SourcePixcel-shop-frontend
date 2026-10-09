# 12_checkout.py
# ساخت صفحه تسویه حساب چند مرحله‌ای
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/checkout/StepIndicator.tsx
# ============================================================
files.append(("components/checkout/StepIndicator.tsx", """import { Check } from "lucide-react";
import type { Locale } from "@/lib/types";

interface StepIndicatorProps {
  currentStep: number;
  steps: { fa: string; en: string }[];
  locale: Locale;
}

export default function StepIndicator({
  currentStep,
  steps,
  locale,
}: StepIndicatorProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 mb-4">
      <div className="flex items-center justify-between max-w-2xl mx-auto">
        {steps.map((step, i) => {
          const stepNum = i + 1;
          const isActive = stepNum === currentStep;
          const isDone = stepNum < currentStep;

          return (
            <div key={i} className="flex items-center flex-1">
              <div className="flex flex-col items-center gap-2 shrink-0">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-[12px] font-bold transition-colors ${
                    isDone
                      ? "bg-[#22C55E] text-white"
                      : isActive
                      ? "bg-[#EF4056] text-white"
                      : "bg-[#F5F5F5] text-[#A1A3A8]"
                  }`}
                >
                  {isDone ? (
                    <Check size={14} />
                  ) : isFa ? (
                    stepNum.toLocaleString("fa-IR")
                  ) : (
                    stepNum
                  )}
                </div>
                <span
                  className={`text-[11px] text-center whitespace-nowrap ${
                    isActive
                      ? "text-[#EF4056] font-medium"
                      : isDone
                      ? "text-[#22C55E]"
                      : "text-[#A1A3A8]"
                  }`}
                >
                  {isFa ? step.fa : step.en}
                </span>
              </div>

              {i < steps.length - 1 && (
                <div
                  className={`flex-1 h-[2px] mx-2 mb-6 transition-colors ${
                    isDone ? "bg-[#22C55E]" : "bg-[#E0E0E2]"
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/checkout/ShippingForm.tsx
# ============================================================
files.append(("components/checkout/ShippingForm.tsx", """"use client";

import { useState } from "react";
import type { Locale } from "@/lib/types";
import { iranProvinces, getCitiesByProvince } from "@/lib/data/iran-provinces";
import { isValidIranianMobile, isValidIranianPostalCode } from "@/lib/utils";

export interface ShippingData {
  fullName: string;
  mobile: string;
  province: string;
  city: string;
  postalCode: string;
  address: string;
}

interface ShippingFormProps {
  locale: Locale;
  initialData: ShippingData;
  onSubmit: (data: ShippingData) => void;
}

const EMPTY: ShippingData = {
  fullName: "",
  mobile: "",
  province: "",
  city: "",
  postalCode: "",
  address: "",
};

export default function ShippingForm({
  locale,
  initialData,
  onSubmit,
}: ShippingFormProps) {
  const isFa = locale === "fa";
  const [data, setData] = useState<ShippingData>(initialData || EMPTY);
  const [errors, setErrors] = useState<Partial<Record<keyof ShippingData, string>>>({});

  const t = {
    fullName: isFa ? "نام و نام خانوادگی" : "Full Name",
    mobile: isFa ? "شماره موبایل" : "Mobile Number",
    province: isFa ? "استان" : "Province",
    city: isFa ? "شهر" : "City",
    postalCode: isFa ? "کد پستی" : "Postal Code",
    address: isFa ? "آدرس کامل" : "Full Address",
    select: isFa ? "انتخاب کنید" : "Select",
    next: isFa ? "ادامه" : "Continue",
    required: isFa ? "این فیلد الزامی است" : "This field is required",
    invalidMobile: isFa ? "شماره موبایل نامعتبر است" : "Invalid mobile number",
    invalidPostal: isFa ? "کد پستی نامعتبر است" : "Invalid postal code",
  };

  const cities = data.province ? getCitiesByProvince(data.province) : [];

  const update = <K extends keyof ShippingData>(
    key: K,
    value: ShippingData[K]
  ) => {
    setData((prev) => ({ ...prev, [key]: value }));
    setErrors((prev) => ({ ...prev, [key]: undefined }));
  };

  const validate = (): boolean => {
    const errs: Partial<Record<keyof ShippingData, string>> = {};
    if (!data.fullName.trim()) errs.fullName = t.required;
    if (!data.mobile.trim()) errs.mobile = t.required;
    else if (!isValidIranianMobile(data.mobile)) errs.mobile = t.invalidMobile;
    if (!data.province) errs.province = t.required;
    if (!data.city) errs.city = t.required;
    if (!data.postalCode.trim()) errs.postalCode = t.required;
    else if (!isValidIranianPostalCode(data.postalCode))
      errs.postalCode = t.invalidPostal;
    if (!data.address.trim()) errs.address = t.required;
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) onSubmit(data);
  };

  const inputClass = (field: keyof ShippingData) =>
    `w-full h-10 px-3 rounded-lg border text-[13px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] focus:border-[#EF4056]"
    }`;

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg border border-[#E0E0E2] p-5">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-5">
        {isFa ? "اطلاعات ارسال" : "Shipping Information"}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Full name */}
        <div className="md:col-span-2">
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.fullName} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={data.fullName}
            onChange={(e) => update("fullName", e.target.value)}
            className={inputClass("fullName")}
            placeholder={isFa ? "مثال: علی محمدی" : "e.g. John Doe"}
          />
          {errors.fullName && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.fullName}</p>
          )}
        </div>

        {/* Mobile */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.mobile} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="tel"
            value={data.mobile}
            onChange={(e) => update("mobile", e.target.value)}
            className={inputClass("mobile")}
            placeholder="09123456789"
            dir="ltr"
          />
          {errors.mobile && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.mobile}</p>
          )}
        </div>

        {/* Postal code */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.postalCode} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={data.postalCode}
            onChange={(e) => update("postalCode", e.target.value)}
            className={inputClass("postalCode")}
            placeholder="1234567890"
            dir="ltr"
          />
          {errors.postalCode && (
            <p className="text-[11px] text-[#EF4444] mt-1">
              {errors.postalCode}
            </p>
          )}
        </div>

        {/* Province */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.province} <span className="text-[#EF4056]">*</span>
          </label>
          <select
            value={data.province}
            onChange={(e) => {
              update("province", e.target.value);
              update("city", "");
            }}
            className={inputClass("province")}
          >
            <option value="">{t.select}</option>
            {iranProvinces.map((p) => (
              <option key={p.id} value={p.id}>
                {isFa ? p.nameFa : p.nameEn}
              </option>
            ))}
          </select>
          {errors.province && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.province}</p>
          )}
        </div>

        {/* City */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.city} <span className="text-[#EF4056]">*</span>
          </label>
          <select
            value={data.city}
            onChange={(e) => update("city", e.target.value)}
            disabled={!data.province}
            className={`${inputClass("city")} disabled:bg-[#F5F5F5] disabled:cursor-not-allowed`}
          >
            <option value="">{t.select}</option>
            {cities.map((c) => (
              <option key={c.id} value={c.id}>
                {isFa ? c.nameFa : c.nameEn}
              </option>
            ))}
          </select>
          {errors.city && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.city}</p>
          )}
        </div>

        {/* Address */}
        <div className="md:col-span-2">
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.address} <span className="text-[#EF4056]">*</span>
          </label>
          <textarea
            rows={3}
            value={data.address}
            onChange={(e) => update("address", e.target.value)}
            className={`${inputClass("address")} h-auto py-2 resize-none`}
            placeholder={
              isFa
                ? "خیابان، کوچه، پلاک، واحد..."
                : "Street, alley, number, unit..."
            }
          />
          {errors.address && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.address}</p>
          )}
        </div>
      </div>

      <div className="flex justify-end mt-6">
        <button
          type="submit"
          className="h-10 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors"
        >
          {t.next}
        </button>
      </div>
    </form>
  );
}
"""))

# ============================================================
# components/checkout/ShippingMethod.tsx
# ============================================================
files.append(("components/checkout/ShippingMethod.tsx", """"use client";

import { useState } from "react";
import { Truck, Zap, Package } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

export interface ShippingOption {
  id: string;
  nameFa: string;
  nameEn: string;
  descFa: string;
  descEn: string;
  price: number;
  icon: "truck" | "zap" | "package";
}

interface ShippingMethodProps {
  locale: Locale;
  selected: string | null;
  onSelect: (id: string) => void;
  onNext: () => void;
  onBack: () => void;
  subtotal: number;
}

export default function ShippingMethod({
  locale,
  selected,
  onSelect,
  onNext,
  onBack,
  subtotal,
}: ShippingMethodProps) {
  const isFa = locale === "fa";

  const FREE_THRESHOLD = 5_000_000;

  const options: ShippingOption[] = [
    {
      id: "post",
      nameFa: "پست پیشتاز",
      nameEn: "Express Post",
      descFa: "۳ تا ۵ روز کاری",
      descEn: "3 to 5 business days",
      price: subtotal >= FREE_THRESHOLD ? 0 : 45_000,
      icon: "truck",
    },
    {
      id: "tipax",
      nameFa: "تیپاکس",
      nameEn: "Tipax",
      descFa: "۱ تا ۲ روز کاری",
      descEn: "1 to 2 business days",
      price: subtotal >= FREE_THRESHOLD ? 0 : 85_000,
      icon: "zap",
    },
    {
      id: "pickup",
      nameFa: "تحویل حضوری",
      nameEn: "Store Pickup",
      descFa: "دریافت از فروشگاه",
      descEn: "Pick up from store",
      price: 0,
      icon: "package",
    },
  ];

  const IconMap = { truck: Truck, zap: Zap, package: Package };

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-5">
        {isFa ? "روش ارسال" : "Shipping Method"}
      </h2>

      {subtotal >= FREE_THRESHOLD && (
        <div className="bg-[#22C55E]/5 border border-[#22C55E]/20 rounded-lg p-3 mb-4 text-[12px] text-[#22C55E]">
          {isFa
            ? "🎉 ارسال شما رایگان است (خرید بالای ۵ میلیون تومان)"
            : "🎉 You have free shipping (orders above 5M Toman)"}
        </div>
      )}

      <div className="space-y-3">
        {options.map((opt) => {
          const Icon = IconMap[opt.icon];
          const isSelected = selected === opt.id;
          return (
            <button
              key={opt.id}
              type="button"
              onClick={() => onSelect(opt.id)}
              className={`w-full flex items-center gap-4 p-4 rounded-lg border-2 text-right transition-colors ${
                isSelected
                  ? "border-[#EF4056] bg-[#EF4056]/5"
                  : "border-[#E0E0E2] hover:border-[#A1A3A8]"
              }`}
            >
              <div
                className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                  isSelected
                    ? "bg-[#EF4056] text-white"
                    : "bg-[#F5F5F5] text-[#62666D]"
                }`}
              >
                <Icon size={20} />
              </div>

              <div className="flex-1 text-right">
                <div className="text-[13px] font-bold text-[#3F4064]">
                  {isFa ? opt.nameFa : opt.nameEn}
                </div>
                <div className="text-[11px] text-[#A1A3A8] mt-0.5">
                  {isFa ? opt.descFa : opt.descEn}
                </div>
              </div>

              <div className="text-left shrink-0">
                <div
                  className={`text-[13px] font-bold ${
                    opt.price === 0 ? "text-[#22C55E]" : "text-[#3F4064]"
                  }`}
                >
                  {opt.price === 0
                    ? isFa
                      ? "رایگان"
                      : "Free"
                    : `${formatPrice(opt.price, locale)} ${
                        isFa ? "تومان" : "T"
                      }`}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      <div className="flex justify-between mt-6">
        <button
          type="button"
          onClick={onBack}
          className="h-10 px-6 rounded-lg border border-[#E0E0E2] text-[13px] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
        >
          {isFa ? "بازگشت" : "Back"}
        </button>
        <button
          type="button"
          onClick={onNext}
          disabled={!selected}
          className="h-10 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {isFa ? "ادامه" : "Continue"}
        </button>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/checkout/PaymentStep.tsx
# ============================================================
files.append(("components/checkout/PaymentStep.tsx", """"use client";

import { useState } from "react";
import { CreditCard, ShieldCheck, Loader2 } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

interface PaymentStepProps {
  locale: Locale;
  total: number;
  onBack: () => void;
  onPay: () => void;
}

export default function PaymentStep({
  locale,
  total,
  onBack,
  onPay,
}: PaymentStepProps) {
  const isFa = locale === "fa";
  const [processing, setProcessing] = useState(false);

  const handlePay = () => {
    setProcessing(true);
    setTimeout(() => {
      onPay();
    }, 1500);
  };

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-5">
        {isFa ? "پرداخت" : "Payment"}
      </h2>

      {/* Simulated gateway */}
      <div className="border-2 border-dashed border-[#E0E0E2] rounded-lg p-6 mb-5 bg-[#FAFAFA]">
        <div className="flex flex-col items-center text-center">
          <div className="w-14 h-14 rounded-full bg-[#EF4056]/10 flex items-center justify-center mb-3">
            <CreditCard size={28} className="text-[#EF4056]" />
          </div>
          <h3 className="text-[14px] font-bold text-[#3F4064] mb-1">
            {isFa ? "درگاه پرداخت زرین‌پال" : "Zarinpal Payment Gateway"}
          </h3>
          <p className="text-[12px] text-[#A1A3A8] mb-4">
            {isFa
              ? "این یک محیط آزمایشی است. پرداخت واقعی انجام نمی‌شود."
              : "This is a test environment. No real payment will be made."}
          </p>

          <div className="bg-white rounded-lg border border-[#E0E0E2] w-full max-w-sm p-4">
            <div className="text-[12px] text-[#62666D] mb-1">
              {isFa ? "مبلغ قابل پرداخت" : "Amount to pay"}
            </div>
            <div className="flex items-center justify-center gap-1">
              <span className="text-[24px] font-bold text-[#EF4056]">
                {formatPrice(total, locale)}
              </span>
              <span className="text-[12px] text-[#62666D]">
                {isFa ? "تومان" : "Toman"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Trust */}
      <div className="flex items-center justify-center gap-2 text-[11px] text-[#62666D] mb-5">
        <ShieldCheck size={14} className="text-[#22C55E]" />
        {isFa
          ? "پرداخت امن با رمزنگاری SSL"
          : "Secure payment with SSL encryption"}
      </div>

      <div className="flex justify-between">
        <button
          type="button"
          onClick={onBack}
          disabled={processing}
          className="h-10 px-6 rounded-lg border border-[#E0E0E2] text-[13px] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40"
        >
          {isFa ? "بازگشت" : "Back"}
        </button>
        <button
          type="button"
          onClick={handlePay}
          disabled={processing}
          className="h-10 px-6 rounded-lg bg-[#22C55E] text-white text-[13px] font-medium hover:bg-[#1da34d] transition-colors disabled:opacity-60 flex items-center gap-2 min-w-[160px] justify-center"
        >
          {processing ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              {isFa ? "در حال پردازش..." : "Processing..."}
            </>
          ) : (
            <>
              <ShieldCheck size={16} />
              {isFa ? "پرداخت" : "Pay Now"}
            </>
          )}
        </button>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/checkout/OrderSuccess.tsx
# ============================================================
files.append(("components/checkout/OrderSuccess.tsx", """import Link from "next/link";
import { CheckCircle2, Package, ArrowLeft } from "lucide-react";
import type { Locale } from "@/lib/types";

interface OrderSuccessProps {
  locale: Locale;
  orderNumber: string;
}

export default function OrderSuccess({
  locale,
  orderNumber,
}: OrderSuccessProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-8 md:p-12 text-center max-w-2xl mx-auto">
      <div className="w-20 h-20 rounded-full bg-[#22C55E]/10 flex items-center justify-center mx-auto mb-5">
        <CheckCircle2 size={48} className="text-[#22C55E]" />
      </div>

      <h1 className="text-[22px] font-bold text-[#3F4064] mb-3">
        {isFa ? "سفارش شما ثبت شد!" : "Order placed successfully!"}
      </h1>

      <p className="text-[13px] text-[#62666D] mb-6 leading-6">
        {isFa
          ? "از خرید شما سپاسگزاریم. کد پیگیری سفارش برای شما پیامک خواهد شد."
          : "Thank you for your purchase. Your order tracking code will be sent via SMS."}
      </p>

      <div className="bg-[#FAFAFA] rounded-lg p-4 mb-6 inline-block">
        <div className="text-[11px] text-[#A1A3A8] mb-1">
          {isFa ? "شماره سفارش" : "Order Number"}
        </div>
        <div className="text-[16px] font-bold text-[#3F4064]" dir="ltr">
          {orderNumber}
        </div>
      </div>

      <div className="flex items-center justify-center gap-3 flex-wrap">
        <Link
          href={`/${locale}/account/orders`}
          className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-2"
        >
          <Package size={16} />
          {isFa ? "پیگیری سفارش" : "Track Order"}
        </Link>
        <Link
          href={`/${locale}`}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <ArrowLeft size={16} />
          {isFa ? "بازگشت به فروشگاه" : "Back to Store"}
        </Link>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/checkout/OrderReview.tsx
# ============================================================
files.append(("components/checkout/OrderReview.tsx", """import { MapPin, Truck } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { formatPrice } from "@/lib/utils";
import { iranProvinces } from "@/lib/data/iran-provinces";
import type { ShippingData } from "./ShippingForm";

interface OrderReviewProps {
  locale: Locale;
  lines: { product: Product; quantity: number }[];
  shipping: ShippingData;
  shippingMethodId: string;
  subtotal: number;
  totalDiscount: number;
  shippingCost: number;
  total: number;
}

export default function OrderReview({
  locale,
  lines,
  shipping,
  shippingMethodId,
  subtotal,
  totalDiscount,
  shippingCost,
  total,
}: OrderReviewProps) {
  const isFa = locale === "fa";
  const province = iranProvinces.find((p) => p.id === shipping.province);
  const city = province?.cities.find((c) => c.id === shipping.city);

  const methodNames: Record<string, { fa: string; en: string }> = {
    post: { fa: "پست پیشتاز", en: "Express Post" },
    tipax: { fa: "تیپاکس", en: "Tipax" },
    pickup: { fa: "تحویل حضوری", en: "Store Pickup" },
  };

  const method = methodNames[shippingMethodId] ?? methodNames.post;

  return (
    <div className="space-y-4">
      {/* Shipping info */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] mb-3 flex items-center gap-2">
          <MapPin size={16} className="text-[#EF4056]" />
          {isFa ? "اطلاعات ارسال" : "Shipping Info"}
        </h3>
        <div className="space-y-1 text-[12px] text-[#62666D]">
          <div>
            <span className="text-[#A1A3A8]">
              {isFa ? "نام: " : "Name: "}
            </span>
            {shipping.fullName}
          </div>
          <div>
            <span className="text-[#A1A3A8]">
              {isFa ? "موبایل: " : "Mobile: "}
            </span>
            <span dir="ltr">{shipping.mobile}</span>
          </div>
          <div>
            <span className="text-[#A1A3A8]">
              {isFa ? "آدرس: " : "Address: "}
            </span>
            {isFa ? province?.nameFa : province?.nameEn},{" "}
            {isFa ? city?.nameFa : city?.nameEn} — {shipping.address}
          </div>
          <div>
            <span className="text-[#A1A3A8]">
              {isFa ? "کد پستی: " : "Postal: "}
            </span>
            <span dir="ltr">{shipping.postalCode}</span>
          </div>
        </div>
      </div>

      {/* Shipping method */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] mb-3 flex items-center gap-2">
          <Truck size={16} className="text-[#EF4056]" />
          {isFa ? "روش ارسال" : "Shipping Method"}
        </h3>
        <div className="text-[12px] text-[#62666D]">
          {isFa ? method.fa : method.en}
        </div>
      </div>

      {/* Order lines */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <h3 className="text-[14px] font-bold text-[#3F4064] mb-4">
          {isFa ? "محصولات" : "Items"}
        </h3>
        <div className="space-y-3">
          {lines.map(({ product, quantity }) => (
            <div
              key={product.id}
              className="flex items-center gap-3 pb-3 border-b border-[#F5F5F5] last:border-0 last:pb-0"
            >
              <div className="text-[12px] text-[#EF4056] font-bold shrink-0 w-7 text-center">
                ×{isFa ? quantity.toLocaleString("fa-IR") : quantity}
              </div>
              <div className="flex-1 text-[12px] text-[#3F4064] line-clamp-1">
                {isFa ? product.titleFa : product.titleEn}
              </div>
              <div className="text-[12px] font-bold text-[#3F4064]">
                {formatPrice(product.finalPrice * quantity, locale)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Totals */}
      <div className="bg-white rounded-lg border border-[#E0E0E2] p-5">
        <div className="space-y-2 text-[13px]">
          <div className="flex justify-between">
            <span className="text-[#62666D]">
              {isFa ? "جمع کالاها" : "Subtotal"}
            </span>
            <span>{formatPrice(subtotal, locale)}</span>
          </div>
          {totalDiscount > 0 && (
            <div className="flex justify-between">
              <span className="text-[#62666D]">
                {isFa ? "تخفیف" : "Discount"}
              </span>
              <span className="text-[#EF4056]">
                -{formatPrice(totalDiscount, locale)}
              </span>
            </div>
          )}
          <div className="flex justify-between">
            <span className="text-[#62666D]">
              {isFa ? "ارسال" : "Shipping"}
            </span>
            <span className={shippingCost === 0 ? "text-[#22C55E]" : ""}>
              {shippingCost === 0
                ? isFa
                  ? "رایگان"
                  : "Free"
                : formatPrice(shippingCost, locale)}
            </span>
          </div>
          <div className="border-t border-[#E0E0E2] pt-3 flex justify-between text-[15px] font-bold">
            <span className="text-[#3F4064]">
              {isFa ? "مبلغ نهایی" : "Total"}
            </span>
            <span className="text-[#EF4056]">
              {formatPrice(total, locale)}{" "}
              <span className="text-[11px] text-[#62666D]">
                {isFa ? "تومان" : "T"}
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/checkout/index.ts
# ============================================================
files.append(("components/checkout/index.ts", """// components/checkout/index.ts
export { default as StepIndicator } from "./StepIndicator";
export { default as ShippingForm } from "./ShippingForm";
export { default as ShippingMethod } from "./ShippingMethod";
export { default as PaymentStep } from "./PaymentStep";
export { default as OrderReview } from "./OrderReview";
export { default as OrderSuccess } from "./OrderSuccess";
export type { ShippingData } from "./ShippingForm";
"""))

# ============================================================
# components/checkout/CheckoutPage.tsx
# ============================================================
files.append(("components/checkout/CheckoutPage.tsx", """"use client";

import { useState, useMemo, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { Breadcrumb, EmptyState } from "@/components/common";
import StepIndicator from "./StepIndicator";
import ShippingForm, { type ShippingData } from "./ShippingForm";
import ShippingMethod from "./ShippingMethod";
import PaymentStep from "./PaymentStep";
import OrderReview from "./OrderReview";
import OrderSuccess from "./OrderSuccess";

interface CheckoutPageProps {
  locale: Locale;
}

const STEPS = [
  { fa: "اطلاعات ارسال", en: "Shipping" },
  { fa: "روش ارسال", en: "Method" },
  { fa: "پرداخت", en: "Payment" },
];

const EMPTY_SHIPPING: ShippingData = {
  fullName: "",
  mobile: "",
  province: "",
  city: "",
  postalCode: "",
  address: "",
};

export default function CheckoutPage({ locale }: CheckoutPageProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const [step, setStep] = useState(1);
  const [shipping, setShipping] = useState<ShippingData>(EMPTY_SHIPPING);
  const [shippingMethodId, setShippingMethodId] = useState<string | null>(null);
  const [orderNumber, setOrderNumber] = useState<string | null>(null);

  const items = useCartStore((s) => s.items);
  const clearCart = useCartStore((s) => s.clear);

  useEffect(() => {
    setMounted(true);
  }, []);

  const lines = useMemo(() => {
    return items
      .map((line) => {
        const product = allProducts.find((p) => p.id === line.productId);
        return product ? { product, quantity: line.quantity } : null;
      })
      .filter((x): x is { product: Product; quantity: number } => x !== null);
  }, [items]);

  const totals = useMemo(() => {
    const subtotal = lines.reduce(
      (sum, l) => sum + l.product.price * l.quantity,
      0
    );
    const finalTotal = lines.reduce(
      (sum, l) => sum + l.product.finalPrice * l.quantity,
      0
    );
    const totalDiscount = subtotal - finalTotal;
    const FREE = 5_000_000;

    let shippingCost = 0;
    if (shippingMethodId === "post") {
      shippingCost = finalTotal >= FREE ? 0 : 45_000;
    } else if (shippingMethodId === "tipax") {
      shippingCost = finalTotal >= FREE ? 0 : 85_000;
    } else if (shippingMethodId === "pickup") {
      shippingCost = 0;
    }

    const total = finalTotal + shippingCost;
    return { subtotal, totalDiscount, shippingCost, total };
  }, [lines, shippingMethodId]);

  const handlePay = () => {
    const num = `SP-${Date.now().toString().slice(-8)}`;
    setOrderNumber(num);
    clearCart();
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  // Success state
  if (orderNumber) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8">
        <OrderSuccess locale={locale} orderNumber={orderNumber} />
      </div>
    );
  }

  // Empty cart
  if (lines.length === 0) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-4">
        <Breadcrumb
          locale={locale}
          items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
        />
        <EmptyState
          locale={locale}
          titleFa="سبد خرید خالی است"
          titleEn="Your cart is empty"
          messageFa="برای تسویه حساب ابتدا محصولی به سبد خرید اضافه کنید."
          messageEn="Add a product to your cart before checking out."
        />
      </div>
    );
  }

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">
        {isFa ? "تسویه حساب" : "Checkout"}
      </h1>

      <StepIndicator currentStep={step} steps={STEPS} locale={locale} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-4">
          {step === 1 && (
            <ShippingForm
              locale={locale}
              initialData={shipping}
              onSubmit={(data) => {
                setShipping(data);
                setStep(2);
              }}
            />
          )}

          {step === 2 && (
            <ShippingMethod
              locale={locale}
              selected={shippingMethodId}
              onSelect={setShippingMethodId}
              onNext={() => setStep(3)}
              onBack={() => setStep(1)}
              subtotal={totals.subtotal}
            />
          )}

          {step === 3 && (
            <PaymentStep
              locale={locale}
              total={totals.total}
              onBack={() => setStep(2)}
              onPay={handlePay}
            />
          )}
        </div>

        {/* Review sidebar */}
        <div className="lg:col-span-1">
          {step >= 2 && shipping.fullName ? (
            <OrderReview
              locale={locale}
              lines={lines}
              shipping={shipping}
              shippingMethodId={shippingMethodId ?? "post"}
              subtotal={totals.subtotal}
              totalDiscount={totals.totalDiscount}
              shippingCost={totals.shippingCost}
              total={totals.total}
            />
          ) : (
            <div className="bg-white rounded-lg border border-[#E0E0E2] p-5 text-[12px] text-[#A1A3A8] text-center">
              {isFa
                ? "اطلاعات سفارش پس از تکمیل فرم نمایش داده می‌شود."
                : "Order details will appear after completing the form."}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/checkout/page.tsx
# ============================================================
files.append(("app/[locale]/checkout/page.tsx", """import type { Locale } from "@/lib/types";
import { CheckoutPage } from "@/components/checkout";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CheckoutRoute({ params }: PageProps) {
  const { locale } = await params;
  return <CheckoutPage locale={locale as Locale} />;
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 12: Checkout")
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
        print("Now run: npm run dev")
        print("Test:")
        print("  1. Add a product to cart")
        print("  2. Go to http://localhost:3000/fa/cart")
        print("  3. Click 'Proceed to Checkout'")
        print("\nNext: run 13_auth.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()