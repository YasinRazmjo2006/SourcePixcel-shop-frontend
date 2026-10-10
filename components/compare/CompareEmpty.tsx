import type { Locale } from "@/lib/types";
import { EmptyState } from "@/components/common";

interface CompareEmptyProps {
  locale: Locale;
}

export default function CompareEmpty({ locale }: CompareEmptyProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
      <EmptyState
        locale={locale}
        type="compare"
        titleFa="لیست مقایسه خالی است"
        titleEn="Compare list is empty"
        messageFa="برای مقایسه، روی آیکون مقایسه در کارت محصولات کلیک کنید. می‌توانید تا ۴ محصول را همزمان مقایسه کنید."
        messageEn="Click the compare icon on product cards to add them. You can compare up to 4 products at once."
        actionLabelFa="مشاهده محصولات"
        actionLabelEn="Browse products"
        actionHref={`/${locale}`}
      />
    </div>
  );
}
