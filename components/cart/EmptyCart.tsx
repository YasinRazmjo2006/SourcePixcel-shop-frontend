import type { Locale } from "@/lib/types";
import { EmptyState } from "@/components/common";

interface EmptyCartProps {
  locale: Locale;
}

export default function EmptyCart({ locale }: EmptyCartProps) {
  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
      <EmptyState
        locale={locale}
        type="cart"
        titleFa="سبد خرید شما خالی است"
        titleEn="Your cart is empty"
        messageFa="می‌توانید از دسته‌بندی‌های مختلف، محصولات مورد نظر خود را اضافه کنید و از تخفیف‌های ویژه بهره‌مند شوید."
        messageEn="You can browse various categories, add products to your cart, and enjoy special discounts."
        actionLabelFa="شروع خرید"
        actionLabelEn="Start shopping"
        actionHref={`/${locale}`}
      />
    </div>
  );
}
