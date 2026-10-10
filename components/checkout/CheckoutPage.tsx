"use client";

import { useState, useMemo, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { Breadcrumb, EmptyState } from "@/components/common";
import { PaymentMethods, TrustBadges } from "@/components/trust";
import StepIndicator from "./StepIndicator";
import ShippingForm, { type ShippingData } from "./ShippingForm";
import ShippingMethod from "./ShippingMethod";
import OrderReview from "./OrderReview";
import ZarinpalGateway from "@/components/payment/ZarinpalGateway";
import PaymentCallback from "@/components/payment/PaymentCallback";

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
  const [showGateway, setShowGateway] = useState(false);
  const [paymentResult, setPaymentResult] = useState<{
    status: "success" | "failed" | "cancelled";
    authority: string;
  } | null>(null);

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

  const [orderNumber] = useState(
    () => `SP-${Date.now().toString().slice(-8)}`
  );

  const handlePay = () => {
    setShowGateway(true);
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleGatewaySuccess = (refId: string) => {
    const authority = sessionStorage.getItem("sourcepixcel-txn-authority") || "";
    clearCart();
    setShowGateway(false);
    setPaymentResult({ status: "success", authority });
  };

  const handleGatewayCancel = () => {
    setShowGateway(false);
    setPaymentResult({ status: "cancelled", authority: "" });
  };

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  if (paymentResult) {
    return (
      <PaymentCallback
        locale={locale}
        authority={paymentResult.authority}
        status={paymentResult.status}
      />
    );
  }

  if (showGateway) {
    return (
      <ZarinpalGateway
        locale={locale}
        amount={totals.total}
        orderNumber={orderNumber}
        onSuccess={handleGatewaySuccess}
        onCancel={handleGatewayCancel}
      />
    );
  }

  if (lines.length === 0) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-4">
        <Breadcrumb
          locale={locale}
          items={[{ labelFa: "تسویه حساب", labelEn: "Checkout" }]}
        />
        <EmptyState
          locale={locale}
          type="cart"
          titleFa="سبد خرید خالی است"
          titleEn="Your cart is empty"
          messageFa="برای تسویه حساب ابتدا محصولی به سبد خرید اضافه کنید."
          messageEn="Add a product to your cart before checking out."
          actionLabelFa="شروع خرید"
          actionLabelEn="Start shopping"
          actionHref={`/${locale}`}
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

      <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
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
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
              <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-5">
                {isFa ? "پرداخت" : "Payment"}
              </h2>

              <div className="bg-[#FAFAFA] dark:bg-[#0F0F12] rounded-xl p-4 mb-4 border border-[#E0E0E2] dark:border-[#2A2A2E]">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                    {isFa ? "مبلغ قابل پرداخت" : "Amount to Pay"}
                  </span>
                  <span className="text-[18px] font-bold text-[#EF4056]">
                    {totals.total.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
                    <span className="text-[11px] text-[#62666D] font-normal">
                      {isFa ? "تومان" : "T"}
                    </span>
                  </span>
                </div>
                <div className="text-[11px] text-[#A1A3A8] text-center">
                  {isFa
                    ? "پس از کلیک روی پرداخت، به درگاه زرین‌پال منتقل می‌شوید."
                    : "After clicking pay, you will be redirected to Zarinpal."}
                </div>
              </div>

              <div className="border-2 border-dashed border-[#E0E0E2] dark:border-[#2A2A2E] rounded-xl p-5 bg-[#F9A825]/5 mb-5">
                <div className="flex items-center justify-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#F9A825] to-[#FFB300] flex items-center justify-center text-white text-[22px] font-bold">
                    Z
                  </div>
                  <div className="text-center">
                    <div className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                      {isFa ? "درگاه پرداخت زرین‌پال" : "Zarinpal Payment Gateway"}
                    </div>
                    <div className="text-[11px] text-[#A1A3A8]">
                      {isFa ? "محیط آزمایشی (Sandbox)" : "Sandbox Environment"}
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep(2)}
                  className="h-11 px-5 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                >
                  {isFa ? "بازگشت" : "Back"}
                </button>
                <button
                  onClick={handlePay}
                  className="flex-1 h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors"
                >
                  {isFa ? "پرداخت و اتمام خرید" : "Pay & Complete Order"}
                </button>
              </div>
            </div>
          )}

          {/* Payment methods + Trust badges in checkout */}
          <PaymentMethods locale={locale} />
        </div>

        <div className="lg:col-span-1 space-y-4">
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
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5 text-[12px] text-[#A1A3A8] text-center">
              {isFa
                ? "اطلاعات سفارش پس از تکمیل فرم نمایش داده می‌شود."
                : "Order details will appear after completing the form."}
            </div>
          )}

          <TrustBadges locale={locale} variant="compact" />
        </div>
      </div>
    </div>
  );
}
