import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";
import { buildFullMetadata } from "@/lib/seo";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return buildFullMetadata({
    locale: typedLocale,
    titleFa: "درباره ما",
    titleEn: "About Us",
    descriptionFa:
      "درباره SourcePixcel — فروشگاه اینترنتی مدرن با هدف ارائه بهترین تجربه خرید آنلاین برای کاربران ایرانی.",
    descriptionEn:
      "About SourcePixcel — a modern online store with the goal of providing the best online shopping experience for Iranian users.",
    path: "/about",
  });
}

export default async function AboutPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="درباره ما"
      titleEn="About Us"
      breadcrumbFa="درباره ما"
      breadcrumbEn="About"
    >
      {isFa ? (
        <>
          <p>
            <strong>SourcePixcel</strong> یک فروشگاه اینترنتی مدرن است که با هدف
            ارائه بهترین تجربه خرید آنلاین برای کاربران ایرانی طراحی شده است. ما
            با تمرکز بر کیفیت، اصالت کالا و خدمات مشتریان، تلاش می‌کنیم تا
            خرید آنلاین را برای شما ساده‌تر، سریع‌تر و مطمئن‌تر کنیم.
          </p>
          <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mt-6 mb-2">
            چرا SourcePixcel؟
          </h2>
          <ul className="list-disc pr-5 space-y-1">
            <li>ارسال سریع به سراسر کشور</li>
            <li>ضمانت اصالت و سلامت کالا</li>
            <li>۷ روز مهلت بازگشت بدون قید و شرط</li>
            <li>پشتیبانی ۲۴ ساعته در ۷ روز هفته</li>
            <li>پرداخت امن از طریق درگاه‌های معتبر</li>
          </ul>
          <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mt-6 mb-2">
            چشم‌انداز ما
          </h2>
          <p>
            ما می‌خواهیم به بزرگ‌ترین و معتبرترین فروشگاه آنلاین ایران تبدیل
            شویم و تجربه‌ای بی‌نظیر برای میلیون‌ها کاربر ایرانی فراهم کنیم.
          </p>
        </>
      ) : (
        <>
          <p>
            <strong>SourcePixcel</strong> is a modern online store designed to
            provide the best online shopping experience for Iranian users. With
            a focus on quality, authenticity, and customer service, we strive
            to make online shopping simpler, faster, and safer.
          </p>
          <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mt-6 mb-2">
            Why SourcePixcel?
          </h2>
          <ul className="list-disc pl-5 space-y-1">
            <li>Fast shipping across the country</li>
            <li>Authenticity and health guarantee</li>
            <li>7-day no-questions-asked return</li>
            <li>24/7 support, 7 days a week</li>
            <li>Secure payment through trusted gateways</li>
          </ul>
          <h2 className="text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mt-6 mb-2">
            Our Vision
          </h2>
          <p>
            We aim to become the largest and most trusted online store in Iran,
            providing an unmatched experience for millions of Iranian users.
          </p>
        </>
      )}
    </StaticPage>
  );
}
