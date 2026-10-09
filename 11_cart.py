# 11_cart.py
# ساخت صفحه سبد خرید
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/cart/EmptyCart.tsx
# ============================================================
files.append(("components/cart/EmptyCart.tsx", """import Link from "next/link";
import { ShoppingBag } from "lucide-react";
import type { Locale } from "@/lib/types";

interface EmptyCartProps {
  locale: Locale;
}

export default function EmptyCart({ locale }: EmptyCartProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] py-16 px-4 flex flex-col items-center text-center">
      <div className="w-24 h-24 rounded-full bg-[#F5F5F5] flex items-center justify-center mb-5">
        <ShoppingBag size={44} className="text-[#A1A3A8]" />
      </div>
      <h2 className="text-[18px] font-bold text-[#3F4064] mb-2">
        {isFa ? "سبد خرید شما خالی است" : "Your cart is empty"}
      </h2>
      <p className="text-[13px] text-[#62666D] mb-6 max-w-md">
        {isFa
          ? "می‌توانید از دسته‌بندی‌های مختلف، محصولات مورد نظر خود را اضافه کنید."
          : "You can add products from various categories to your cart."}
      </p>
      <Link
        href={`/${locale}`}
        className="bg-[#EF4056] text-white text-[13px] font-medium px-6 py-2.5 rounded-lg hover:bg-[#d63850] transition-colors"
      >
        {isFa ? "شروع خرید" : "Start shopping"}
      </Link>
    </div>
  );
}
"""))

# ============================================================
# components/cart/CartLine.tsx
# ============================================================
files.append(("components/cart/CartLine.tsx", """"use client";

import Link from "next/link";
import Image from "next/image";
import { Trash2, Plus, Minus, Heart, Store } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { useCartStore, useWishlistStore } from "@/lib/stores";
import { formatPrice } from "@/lib/utils";
import { getBrandById } from "@/lib/data";

interface CartLineProps {
  product: Product;
  quantity: number;
  locale: Locale;
}

export default function CartLine({ product, quantity, locale }: CartLineProps) {
  const isFa = locale === "fa";
  const updateQuantity = useCartStore((s) => s.updateQuantity);
  const removeItem = useCartStore((s) => s.removeItem);
  const toggleWishlist = useWishlistStore((s) => s.toggle);

  const brand = getBrandById(product.brand);
  const title = isFa ? product.titleFa : product.titleEn;
  const lineTotal = product.finalPrice * quantity;
  const lineOriginal = product.price * quantity;

  const dec = () => updateQuantity(product.id, quantity - 1);
  const inc = () => updateQuantity(product.id, quantity + 1);
  const remove = () => removeItem(product.id);

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 flex gap-4">
      {/* Image */}
      <Link
        href={`/${locale}/product/${product.slug}`}
        className="w-20 h-20 md:w-28 md:h-28 shrink-0 rounded-lg bg-[#F5F5F5] overflow-hidden relative"
      >
        <Image
          src={product.image}
          alt={title}
          fill
          sizes="120px"
          className="object-cover"
        />
      </Link>

      {/* Info */}
      <div className="flex-1 min-w-0 flex flex-col">
        <div className="flex items-start justify-between gap-3">
          <Link
            href={`/${locale}/product/${product.slug}`}
            className="text-[13px] md:text-[14px] text-[#3F4064] leading-5 line-clamp-2 hover:text-[#EF4056] transition-colors"
          >
            {title}
          </Link>

          <button
            onClick={remove}
            aria-label={isFa ? "حذف" : "Remove"}
            className="text-[#A1A3A8] hover:text-[#EF4444] transition-colors shrink-0"
          >
            <Trash2 size={16} />
          </button>
        </div>

        {/* Brand */}
        {brand && (
          <div className="flex items-center gap-1 text-[11px] text-[#A1A3A8] mt-1">
            <Store size={11} />
            <span>{isFa ? brand.nameFa : brand.nameEn}</span>
          </div>
        )}

        {/* Actions row */}
        <div className="flex items-end justify-between gap-3 mt-auto pt-3">
          {/* Quantity */}
          <div className="flex items-center gap-2 border border-[#E0E0E2] rounded-lg">
            <button
              onClick={inc}
              aria-label="Increase"
              className="w-7 h-7 flex items-center justify-center text-[#EF4056] hover:bg-[#F5F5F5] rounded-r-lg transition-colors"
            >
              <Plus size={14} />
            </button>
            <span className="w-6 text-center text-[13px] font-bold text-[#3F4064] tabular-nums">
              {isFa ? quantity.toLocaleString("fa-IR") : quantity}
            </span>
            <button
              onClick={dec}
              aria-label="Decrease"
              className="w-7 h-7 flex items-center justify-center text-[#EF4056] hover:bg-[#F5F5F5] rounded-l-lg transition-colors"
            >
              <Minus size={14} />
            </button>
          </div>

          {/* Price */}
          <div className="text-right">
            {product.discountPercent > 0 && (
              <div className="text-[11px] text-[#A1A3A8] line-through">
                {formatPrice(lineOriginal, locale)}
              </div>
            )}
            <div className="flex items-center gap-1">
              <span className="text-[14px] md:text-[15px] font-bold text-[#3F4064]">
                {formatPrice(lineTotal, locale)}
              </span>
              <span className="text-[10px] text-[#62666D]">
                {isFa ? "تومان" : "Toman"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/cart/CartSummary.tsx
# ============================================================
files.append(("components/cart/CartSummary.tsx", """"use client";

import { useState } from "react";
import { Tag, Check, X } from "lucide-react";
import type { Locale } from "@/lib/types";
import { formatPrice } from "@/lib/utils";

interface CartSummaryProps {
  locale: Locale;
  subtotal: number;
  totalDiscount: number;
  shipping: number;
  total: number;
  onCheckout: () => void;
}

export default function CartSummary({
  locale,
  subtotal,
  totalDiscount,
  shipping,
  total,
  onCheckout,
}: CartSummaryProps) {
  const isFa = locale === "fa";
  const [coupon, setCoupon] = useState("");
  const [couponStatus, setCouponStatus] = useState<"idle" | "ok" | "error">(
    "idle"
  );

  const t = {
    summary: isFa ? "خلاصه سفارش" : "Order Summary",
    subtotal: isFa ? "جمع کل کالاها" : "Subtotal",
    discount: isFa ? "تخفیف" : "Discount",
    shipping: isFa ? "هزینه ارسال" : "Shipping",
    total: isFa ? "مبلغ قابل پرداخت" : "Total",
    free: isFa ? "رایگان" : "Free",
    couponPlaceholder: isFa ? "کد تخفیف" : "Coupon code",
    apply: isFa ? "اعمال" : "Apply",
    checkout: isFa ? "ادامه فرآیند خرید" : "Proceed to Checkout",
    couponOk: isFa ? "کد تخفیف معتبر است" : "Coupon applied",
    couponError: isFa ? "کد تخفیف نامعتبر است" : "Invalid coupon",
  };

  const handleApplyCoupon = () => {
    if (coupon.trim().toUpperCase() === "SOURCE10") {
      setCouponStatus("ok");
    } else {
      setCouponStatus("error");
    }
  };

  const removeCoupon = () => {
    setCoupon("");
    setCouponStatus("idle");
  };

  return (
    <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 sticky top-24">
      <h2 className="text-[15px] font-bold text-[#3F4064] mb-4">
        {t.summary}
      </h2>

      {/* Coupon */}
      <div className="mb-4">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Tag
              size={14}
              className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
              style={{ [isFa ? "right" : "left"]: 10 } as React.CSSProperties}
            />
            <input
              type="text"
              value={coupon}
              onChange={(e) => {
                setCoupon(e.target.value);
                setCouponStatus("idle");
              }}
              placeholder={t.couponPlaceholder}
              className="w-full h-9 rounded-lg border border-[#E0E0E2] text-[12px] focus:outline-none focus:border-[#EF4056]"
              style={{
                paddingRight: isFa ? 32 : 12,
                paddingLeft: isFa ? 12 : 32,
              }}
            />
          </div>
          {couponStatus === "ok" ? (
            <button
              onClick={removeCoupon}
              className="h-9 px-3 rounded-lg bg-[#22C55E]/10 text-[#22C55E] text-[12px] font-medium flex items-center gap-1"
            >
              <Check size={14} />
            </button>
          ) : (
            <button
              onClick={handleApplyCoupon}
              disabled={!coupon.trim()}
              className="h-9 px-3 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {t.apply}
            </button>
          )}
        </div>
        {couponStatus === "ok" && (
          <p className="text-[11px] text-[#22C55E] mt-2 flex items-center gap-1">
            <Check size={12} /> {t.couponOk}
          </p>
        )}
        {couponStatus === "error" && (
          <p className="text-[11px] text-[#EF4444] mt-2 flex items-center gap-1">
            <X size={12} /> {t.couponError}
          </p>
        )}
      </div>

      {/* Divider */}
      <div className="border-t border-[#E0E0E2] pt-4 space-y-3">
        <div className="flex items-center justify-between text-[13px]">
          <span className="text-[#62666D]">{t.subtotal}</span>
          <span className="text-[#3F4064] font-medium">
            {formatPrice(subtotal, locale)}{" "}
            <span className="text-[10px] text-[#A1A3A8]">
              {isFa ? "تومان" : "T"}
            </span>
          </span>
        </div>

        {totalDiscount > 0 && (
          <div className="flex items-center justify-between text-[13px]">
            <span className="text-[#62666D]">{t.discount}</span>
            <span className="text-[#EF4056] font-medium">
              -{formatPrice(totalDiscount, locale)}{" "}
              <span className="text-[10px]">
                {isFa ? "تومان" : "T"}
              </span>
            </span>
          </div>
        )}

        <div className="flex items-center justify-between text-[13px]">
          <span className="text-[#62666D]">{t.shipping}</span>
          <span
            className={
              shipping === 0
                ? "text-[#22C55E] font-medium"
                : "text-[#3F4064] font-medium"
            }
          >
            {shipping === 0
              ? t.free
              : `${formatPrice(shipping, locale)} ${
                  isFa ? "تومان" : "T"
                }`}
          </span>
        </div>
      </div>

      {/* Divider */}
      <div className="border-t border-[#E0E0E2] my-4" />

      {/* Total */}
      <div className="flex items-center justify-between mb-4">
        <span className="text-[14px] font-bold text-[#3F4064]">{t.total}</span>
        <div className="flex items-center gap-1">
          <span className="text-[18px] font-bold text-[#EF4056]">
            {formatPrice(total, locale)}
          </span>
          <span className="text-[11px] text-[#62666D]">
            {isFa ? "تومان" : "Toman"}
          </span>
        </div>
      </div>

      {/* Checkout button */}
      <button
        onClick={onCheckout}
        className="w-full h-11 rounded-lg bg-[#EF4056] text-white text-[14px] font-bold hover:bg-[#d63850] transition-colors"
      >
        {t.checkout}
      </button>

      {/* Hint */}
      <p className="text-[11px] text-[#A1A3A8] text-center mt-3">
        {isFa
          ? "با کد SOURCE10 از ۱۰٪ تخفیف بهره‌مند شوید"
          : "Use code SOURCE10 for 10% off"}
      </p>
    </div>
  );
}
"""))

# ============================================================
# components/cart/CartPage.tsx
# ============================================================
files.append(("components/cart/CartPage.tsx", """"use client";

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
"""))

# ============================================================
# components/cart/index.ts
# ============================================================
files.append(("components/cart/index.ts", """// components/cart/index.ts
export { default as CartPage } from "./CartPage";
export { default as CartLine } from "./CartLine";
export { default as CartSummary } from "./CartSummary";
export { default as EmptyCart } from "./EmptyCart";
"""))

# ============================================================
# app/[locale]/cart/page.tsx
# ============================================================
files.append(("app/[locale]/cart/page.tsx", """import type { Locale } from "@/lib/types";
import { CartPage } from "@/components/cart";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CartRoute({ params }: PageProps) {
  const { locale } = await params;
  return <CartPage locale={locale as Locale} />;
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 11: Cart")
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
        print("Open: http://localhost:3000/fa/cart")
        print("\nNext: run 12_checkout.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()