import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";
import { Phone, Mail, MapPin, Clock } from "lucide-react";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ContactPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  const items = [
    {
      icon: Phone,
      fa: { label: "تلفن پشتیبانی", value: "021-12345678" },
      en: { label: "Support Phone", value: "021-12345678" },
    },
    {
      icon: Mail,
      fa: { label: "ایمیل", value: "support@sourcepixcel.com" },
      en: { label: "Email", value: "support@sourcepixcel.com" },
    },
    {
      icon: MapPin,
      fa: { label: "آدرس", value: "تهران، خیابان ولیعصر، پلاک ۱۲۳" },
      en: { label: "Address", value: "Tehran, Valiasr St., No. 123" },
    },
    {
      icon: Clock,
      fa: { label: "ساعات پاسخگویی", value: "۲۴ ساعته، ۷ روز هفته" },
      en: { label: "Hours", value: "24/7" },
    },
  ];

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="تماس با ما"
      titleEn="Contact Us"
      breadcrumbFa="تماس با ما"
      breadcrumbEn="Contact"
    >
      <p>
        {isFa
          ? "تیم پشتیبانی SourcePixcel به صورت شبانه‌روزی آماده پاسخگویی به سوالات و مشکلات شماست."
          : "SourcePixcel support team is available 24/7 to answer your questions and help with any issues."}
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 not-prose mt-4">
        {items.map((item, i) => {
          const Icon = item.icon;
          const data = isFa ? item.fa : item.en;
          return (
            <div
              key={i}
              className="flex items-start gap-3 p-4 rounded-lg border border-[#E0E0E2] bg-[#FAFAFA]"
            >
              <div className="w-10 h-10 rounded-lg bg-white border border-[#E0E0E2] flex items-center justify-center shrink-0">
                <Icon size={18} className="text-[#EF4056]" />
              </div>
              <div>
                <div className="text-[11px] text-[#A1A3A8] mb-1">
                  {data.label}
                </div>
                <div className="text-[13px] text-[#3F4064] font-medium" dir={i < 2 ? "ltr" : "auto"}>
                  {data.value}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </StaticPage>
  );
}
