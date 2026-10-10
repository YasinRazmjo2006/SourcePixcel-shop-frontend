import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";
import JsonLd from "@/components/common/JsonLd";
import { buildFullMetadata, faqSchema } from "@/lib/seo";

interface PageProps {
  params: Promise<{ locale: string }>;
}

const FAQ_ITEMS = [
  {
    fa: {
      q: "چطور می‌توانم سفارش خود را پیگیری کنم؟",
      a: "پس از ثبت سفارش، کد پیگیری از طریق پیامک برای شما ارسال می‌شود. می‌توانید از بخش «سفارشات من» در پنل کاربری نیز وضعیت سفارش را مشاهده کنید.",
    },
    en: {
      q: "How can I track my order?",
      a: "After placing an order, a tracking code is sent to you via SMS. You can also check your order status in the 'My Orders' section of your account.",
    },
  },
  {
    fa: {
      q: "شرایط بازگشت کالا چیست؟",
      a: "شما تا ۷ روز پس از دریافت کالا، در صورت عدم رضایت یا وجود مشکل، می‌توانید درخواست بازگشت ثبت کنید. کالا باید در بسته‌بندی اصلی و بدون آسیب باشد.",
    },
    en: {
      q: "What is the return policy?",
      a: "You can request a return within 7 days of receiving the product if you're not satisfied or if there's an issue. The product must be in its original packaging without damage.",
    },
  },
  {
    fa: {
      q: "هزینه ارسال چگونه محاسبه می‌شود؟",
      a: "هزینه ارسال بر اساس روش انتخابی و مقصد محاسبه می‌شود. برای سفارشات بالای ۵ میلیون تومان، ارسال رایگان است.",
    },
    en: {
      q: "How is the shipping cost calculated?",
      a: "Shipping cost depends on your selected method and destination. Orders above 5 million Toman qualify for free shipping.",
    },
  },
  {
    fa: {
      q: "آیا امکان پرداخت در محل وجود دارد؟",
      a: "در حال حاضر فقط پرداخت آنلاین از طریق درگاه‌های معتبر (زرین‌پال) پذیرفته می‌شود.",
    },
    en: {
      q: "Is cash on delivery available?",
      a: "Currently, only online payment through trusted gateways (Zarinpal) is accepted.",
    },
  },
  {
    fa: {
      q: "چگونه می‌توانم رمز عبور خود را بازیابی کنم؟",
      a: "از صفحه ورود، روی «رمز عبور را فراموش کرده‌اید؟» کلیک کنید و شماره موبایل خود را وارد کنید. کد بازیابی برای شما ارسال می‌شود.",
    },
    en: {
      q: "How can I recover my password?",
      a: "From the login page, click 'Forgot password?' and enter your mobile number. A reset code will be sent to you.",
    },
  },
];

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return buildFullMetadata({
    locale: typedLocale,
    titleFa: "سوالات متداول",
    titleEn: "Frequently Asked Questions",
    descriptionFa:
      "پاسخ سوالات رایج درباره خرید، ارسال، بازگشت کالا و پرداخت در SourcePixcel.",
    descriptionEn:
      "Answers to common questions about shopping, shipping, returns, and payment at SourcePixcel.",
    path: "/faq",
  });
}

export default async function FAQPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  const schema = faqSchema(
    FAQ_ITEMS.map((item) => ({
      question: isFa ? item.fa.q : item.en.q,
      answer: isFa ? item.fa.a : item.en.a,
    }))
  );

  return (
    <>
      <JsonLd data={schema} />
      <StaticPage
        locale={typedLocale}
        titleFa="سوالات متداول"
        titleEn="Frequently Asked Questions"
        breadcrumbFa="سوالات متداول"
        breadcrumbEn="FAQ"
      >
        <div className="not-prose space-y-3">
          {FAQ_ITEMS.map((item, i) => {
            const data = isFa ? item.fa : item.en;
            return (
              <details
                key={i}
                className="group border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg overflow-hidden"
              >
                <summary className="cursor-pointer p-4 text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] flex items-center justify-between">
                  <span>{data.q}</span>
                  <span className="text-[#EF4056] text-[16px] group-open:rotate-45 transition-transform">
                    +
                  </span>
                </summary>
                <div className="px-4 pb-4 text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6 border-t border-[#F5F5F5] dark:border-[#2A2A2E] pt-3">
                  {data.a}
                </div>
              </details>
            );
          })}
        </div>
      </StaticPage>
    </>
  );
}
