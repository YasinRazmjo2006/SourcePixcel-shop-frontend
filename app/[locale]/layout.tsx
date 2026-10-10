import type { Metadata } from "next";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import BottomNav from "@/components/layout/BottomNav";
import ToastContainer from "@/components/common/ToastContainer";
import KeyboardShortcuts from "@/components/common/KeyboardShortcuts";
import OfflineBanner from "@/components/common/OfflineBanner";
import FontLoader from "@/components/common/FontLoader";
import SkipLink from "@/components/a11y/SkipLink";
import ScreenReaderAnnouncer from "@/components/a11y/ScreenReaderAnnouncer";
import JsonLd from "@/components/common/JsonLd";
import type { Locale } from "@/lib/types";
import {
  buildFullMetadata,
  organizationSchema,
  webSiteSchema,
  siteNavigationSchema,
} from "@/lib/seo";

interface LayoutProps {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

export async function generateStaticParams() {
  return [{ locale: "fa" }, { locale: "en" }];
}

export async function generateMetadata({
  params,
}: LayoutProps): Promise<Metadata> {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return buildFullMetadata({
    locale: typedLocale,
    titleFa: "فروشگاه آنلاین مدرن",
    titleEn: "Modern Online Store",
    descriptionFa:
      "فروشگاه اینترنتی SourcePixcel — خرید آنلاین موبایل، لپ‌تاپ، لوازم خانگی، پوشاک و لوازم جانبی با ارسال سریع و ضمانت اصالت.",
    descriptionEn:
      "SourcePixcel online store — shop mobile phones, laptops, home appliances, fashion, and accessories with fast shipping and authenticity guarantee.",
    path: "",
  });
}

export default async function LocaleLayout({
  children,
  params,
}: LayoutProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <div
      dir={locale === "fa" ? "rtl" : "ltr"}
      lang={locale}
      className="font-sans"
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      {/* Preconnect for performance */}
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossOrigin="anonymous"
      />
      <link rel="dns-prefetch" href="https://picsum.photos" />
      <link rel="dns-prefetch" href="https://loremflickr.com" />

      {/* Global JSON-LD */}
      <JsonLd
        data={[
          organizationSchema(),
          webSiteSchema(typedLocale),
          siteNavigationSchema(typedLocale),
        ]}
      />

      <SkipLink locale={typedLocale} />
      <ScreenReaderAnnouncer />
      <FontLoader />
      <Header locale={typedLocale} />
      <main
        id="main-content"
        role="main"
        style={{ flex: 1 }}
        className="pb-16 lg:pb-0"
        tabIndex={-1}
      >
        {children}
      </main>
      <Footer locale={typedLocale} />
      <BottomNav locale={typedLocale} />
      <ToastContainer />
      <KeyboardShortcuts locale={typedLocale} />
      <OfflineBanner locale={typedLocale} />
    </div>
  );
}
