import Link from "next/link";
import { Home, Search, ArrowRight, ArrowLeft } from "lucide-react";

export default async function LocaleNotFound({
  params,
}: {
  params?: Promise<{ locale: string }>;
}) {
  const locale = params ? (await params).locale : "fa";
  const isFa = locale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-16 md:py-24 text-center">
      <h1 className="text-[100px] md:text-[140px] font-bold text-[#EF4056] leading-none mb-4 select-none">
        404
      </h1>
      <h2 className="text-[22px] md:text-[26px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
        {isFa ? "صفحه‌ای که دنبالش هستید پیدا نشد" : "Page not found"}
      </h2>
      <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-8 max-w-md mx-auto leading-7">
        {isFa
          ? "ممکن است آدرس اشتباه باشد یا صفحه حذف شده باشد. می‌توانید از جستجو استفاده کنید یا به خانه برگردید."
          : "The address might be incorrect, or the page may have been removed. Try searching or go back to home."}
      </p>
      <div className="flex items-center justify-center gap-3 flex-wrap">
        <Link
          href={`/${locale}`}
          className="h-11 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors inline-flex items-center gap-2"
        >
          {isFa ? <ArrowRight size={16} /> : <ArrowLeft size={16} />}
          {isFa ? "بازگشت به خانه" : "Back to Home"}
        </Link>
        <Link
          href={`/${locale}/search`}
          className="h-11 px-6 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] font-medium text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors inline-flex items-center gap-2"
        >
          <Search size={16} />
          {isFa ? "جستجو در فروشگاه" : "Search"}
        </Link>
      </div>

      <div className="mt-12 text-[12px] text-[#A1A3A8]">
        {isFa
          ? "اگر فکر می‌کنید این یک خطاست، با پشتیبانی تماس بگیرید."
          : "If you think this is an error, please contact support."}
      </div>
    </div>
  );
}
