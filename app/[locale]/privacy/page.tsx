import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function PrivacyPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="حریم خصوصی"
      titleEn="Privacy Policy"
      breadcrumbFa="حریم خصوصی"
      breadcrumbEn="Privacy"
    >
      {isFa ? (
        <>
          <p>
            SourcePixcel متعهد به حفظ حریم خصوصی کاربران خود است. این سند
            نحوه جمع‌آوری، استفاده و محافظت از اطلاعات شخصی شما را توضیح می‌دهد.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            اطلاعاتی که جمع‌آوری می‌کنیم
          </h2>
          <ul className="list-disc pr-5 space-y-1">
            <li>نام و نام خانوادگی</li>
            <li>شماره موبایل و ایمیل</li>
            <li>آدرس ارسال سفارش</li>
            <li>تاریخچه سفارشات و بازدیدها</li>
          </ul>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            نحوه استفاده از اطلاعات
          </h2>
          <p>
            اطلاعات شما فقط برای پردازش سفارشات، ارسال، پشتیبانی و بهبود
            خدمات استفاده می‌شود. ما هیچ‌گاه اطلاعات شما را با اشخاص ثالث به
            اشتراک نمی‌گذاریم، مگر در چارچوب قانون.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            امنیت اطلاعات
          </h2>
          <p>
            کلیه اطلاعات از طریق پروتکل SSL رمزنگاری می‌شود و دسترسی به
            اطلاعات شما فقط برای کارکنان مجاز امکان‌پذیر است.
          </p>
        </>
      ) : (
        <>
          <p>
            SourcePixcel is committed to protecting the privacy of its users.
            This document explains how we collect, use, and protect your
            personal information.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            Information We Collect
          </h2>
          <ul className="list-disc pl-5 space-y-1">
            <li>Full name</li>
            <li>Mobile number and email</li>
            <li>Shipping address</li>
            <li>Order and browsing history</li>
          </ul>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            How We Use Information
          </h2>
          <p>
            Your information is used only to process orders, ship, provide
            support, and improve our services. We never share your information
            with third parties, except as required by law.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            Data Security
          </h2>
          <p>
            All information is encrypted via SSL, and access to your data is
            restricted to authorized personnel only.
          </p>
        </>
      )}
    </StaticPage>
  );
}
