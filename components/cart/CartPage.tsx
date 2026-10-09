"use client";

import { useMemo, useState, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { Breadcrumb, EmptyState } from "@/components/common";
import EmptyCart from "./EmptyCart";
import CartLine from "./CartLine";
import CartSummary from "./CartSummary";

interface CartPageProps {
  locale: Locale;
}

export default function CartPage({ locale }: CartPageProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);

  const items = useCartStore((s) => s.items);
  const clear = useCartStore((s) => s.clear);

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
    const shipping = finalTotal > 5_000_000 || finalTotal === 0 ? 0 : 45_000;
    const total = finalTotal + shipping;
    return { subtotal, totalDiscount, shipping, total };
  }, [lines]);

  const handleCheckout = () => {
    if (typeof window !== "undefined") {
      window.location.href = `/${locale}/checkout`;
    }
  };

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8">
        <div className="bg-white rounded-lg border border-[#E0E0E2] p-8 text-center text-[#A1A3A8]">
          {isFa ? "در حال بارگذاری..." : "Loading..."}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "سبد خرید", labelEn: "Cart" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">
        {isFa ? "سبد خرید" : "Shopping Cart"}
      </h1>

      {lines.length === 0 ? (
        <EmptyCart locale={locale} />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Lines */}
          <div className="lg:col-span-2 space-y-3">
            {lines.map((line) => (
              <CartLine
                key={line.product.id}
                product={line.product}
                quantity={line.quantity}
                locale={locale}
              />
            ))}

            <button
              onClick={clear}
              className="text-[12px] text-[#EF4056] hover:underline"
            >
              {isFa ? "حذف همه محصولات" : "Clear cart"}
            </button>
          </div>

          {/* Summary */}
          <div className="lg:col-span-1">
            <CartSummary
              locale={locale}
              subtotal={totals.subtotal}
              totalDiscount={totals.totalDiscount}
              shipping={totals.shipping}
              total={totals.total}
              onCheckout={handleCheckout}
            />
          </div>
        </div>
      )}
    </div>
  );
}
