import type { Locale } from "@/lib/types";
import Breadcrumb from "./Breadcrumb";

interface StaticPageProps {
  locale: Locale;
  titleFa: string;
  titleEn: string;
  breadcrumbFa: string;
  breadcrumbEn: string;
  children: React.ReactNode;
}

export default function StaticPage({
  locale,
  titleFa,
  titleEn,
  breadcrumbFa,
  breadcrumbEn,
  children,
}: StaticPageProps) {
  const isFa = locale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: breadcrumbFa, labelEn: breadcrumbEn }]}
      />

      <div className="bg-white rounded-lg border border-[#E0E0E2] p-6 md:p-8">
        <h1 className="text-[22px] font-bold text-[#3F4064] mb-6">
          {isFa ? titleFa : titleEn}
        </h1>
        <div className="prose prose-sm max-w-none text-[13px] text-[#62666D] leading-7 space-y-4">
          {children}
        </div>
      </div>
    </div>
  );
}
