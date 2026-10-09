import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function TermsPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="شرایط و قوانین"
      titleEn="Terms and Conditions"
      breadcrumbFa="شرایط و قوانین"
      breadcrumbEn="Terms"
    >
      {isFa ? (
        <>
          <p>
            استفاده از خدمات SourcePixcel به معنای پذیرش کامل قوانین و مقررات
            زیر است. لطفاً پیش از ثبت سفارش، این شرایط را به دقت مطالعه کنید.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۱. ثبت سفارش
          </h2>
          <p>
            کلیه سفارشات پس از تایید نهایی و پرداخت موفق، وارد مرحله پردازش
            می‌شوند. SourcePixcel مجاز است در صورت بروز مشکل در موجودی یا قیمت،
            سفارش را لغو و مبلغ را بازگرداند.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۲. قیمت‌ها و پرداخت
          </h2>
          <p>
            کلیه قیمت‌ها به تومان و شامل مالیات بر ارزش افزوده است. پرداخت از
            طریق درگاه‌های امن انجام می‌شود و SourcePixcel مسئولیتی در قبال
            اطلاعات کارت بانکی کاربران ندارد.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۳. ارسال و تحویل
          </h2>
          <p>
            زمان ارسال بر اساس روش انتخابی و مقصد متفاوت است. SourcePixcel
            تلاش می‌کند سفارشات را در سریع‌ترین زمان ارسال کند، اما در شرایط
            خاص (تعطیلات، حوادث غیرمترقبه) ممکن است تاخیر رخ دهد.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۴. بازگشت کالا
          </h2>
          <p>
            در صورت مغایرت کالا با توضیحات یا وجود ایراد فنی، تا ۷ روز پس از
            دریافت، امکان بازگشت وجود دارد. کالا باید در بسته‌بندی اصلی و سالم
            باشد.
          </p>
        </>
      ) : (
        <>
          <p>
            Using SourcePixcel services means full acceptance of the following
            terms and conditions. Please read them carefully before placing an
            order.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            1. Ordering
          </h2>
          <p>
            All orders enter the processing stage after final confirmation and
            successful payment. SourcePixcel may cancel an order and refund the
            amount if there's an issue with stock or pricing.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            2. Prices and Payment
          </h2>
          <p>
            All prices are in Toman and include VAT. Payments are made through
            secure gateways, and SourcePixcel is not responsible for users'
            banking card information.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            3. Shipping and Delivery
          </h2>
          <p>
            Delivery time varies based on the selected method and destination.
            SourcePixcel aims to ship orders as quickly as possible, but delays
            may occur under special circumstances.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            4. Returns
          </h2>
          <p>
            In case of a product mismatch or technical defect, a return can be
            requested within 7 days of receipt. The product must be in its
            original packaging and undamaged.
          </p>
        </>
      )}
    </StaticPage>
  );
}
