import { MapPin, Truck } from "lucide-react";
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
