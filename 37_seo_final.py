# 37_seo_final.py
# SEO نهایی: metadata، schema، OG، sitemap، robots
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/seo.ts — ابزارهای جامع SEO
# ============================================================
files.append(("lib/seo.ts", """import type { Metadata } from "next";

const SITE_NAME = "SourcePixcel";
const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://sourcepixcel.vercel.app";
const SITE_DESCRIPTION_FA =
  "فروشگاه اینترنتی SourcePixcel — خرید آنلاین موبایل، لپ‌تاپ، لوازم خانگی، پوشاک و لوازم جانبی با ارسال سریع و ضمانت اصالت.";
const SITE_DESCRIPTION_EN =
  "SourcePixcel online store — shop mobile phones, laptops, home appliances, fashion, and accessories with fast shipping and authenticity guarantee.";
const DEFAULT_OG_IMAGE = `${SITE_URL}/og-image.png`;
const TWITTER_HANDLE = "@sourcepixcel";

export const SEO = {
  SITE_NAME,
  SITE_URL,
  SITE_DESCRIPTION_FA,
  SITE_DESCRIPTION_EN,
  DEFAULT_OG_IMAGE,
  TWITTER_HANDLE,
};

// ═══════════════════════════════════════════════════════════════
// BUILD METADATA — full featured
// ═══════════════════════════════════════════════════════════════

interface BuildMetadataOptions {
  locale: "fa" | "en";
  titleFa?: string;
  titleEn?: string;
  descriptionFa?: string;
  descriptionEn?: string;
  path?: string;
  image?: string;
  type?: "website" | "article" | "product";
  publishedTime?: string;
  authors?: string[];
  noIndex?: boolean;
}

export function buildFullMetadata({
  locale,
  titleFa,
  titleEn,
  descriptionFa,
  descriptionEn,
  path = "",
  image,
  type = "website",
  publishedTime,
  authors,
  noIndex = false,
}: BuildMetadataOptions): Metadata {
  const isFa = locale === "fa";

  const title = isFa ? titleFa : titleEn;
  const description = isFa
    ? descriptionFa || SITE_DESCRIPTION_FA
    : descriptionEn || SITE_DESCRIPTION_EN;

  const canonicalUrl = `${SITE_URL}/${locale}${path}`;
  const ogImage = image || DEFAULT_OG_IMAGE;

  return {
    metadataBase: new URL(SITE_URL),
    title: {
      default: `${SITE_NAME} — ${
        isFa ? "فروشگاه آنلاین مدرن" : "Modern Online Store"
      }`,
      template: `%s | ${SITE_NAME}`,
    },
    description,
    applicationName: SITE_NAME,
    authors: authors ? authors.map((name) => ({ name })) : [{ name: SITE_NAME }],
    generator: "Next.js",
    keywords: isFa
      ? [
          "فروشگاه آنلاین",
          "خرید اینترنتی",
          "موبایل",
          "لپ تاپ",
          "لوازم خانگی",
          "پوشاک",
          "لوازم جانبی",
          "سورس پیکسل",
        ]
      : [
          "online store",
          "e-commerce",
          "mobile phones",
          "laptops",
          "home appliances",
          "fashion",
          "accessories",
          "SourcePixcel",
        ],
    referrer: "origin-when-cross-origin",
    creator: SITE_NAME,
    publisher: SITE_NAME,

    // Canonical + alternate
    alternates: {
      canonical: canonicalUrl,
      languages: {
        "fa-IR": `${SITE_URL}/fa${path}`,
        "en-US": `${SITE_URL}/en${path}`,
        "x-default": `${SITE_URL}/fa${path}`,
      },
    },

    // Robots
    robots: noIndex
      ? {
          index: false,
          follow: false,
        }
      : {
          index: true,
          follow: true,
          nocache: false,
          googleBot: {
            index: true,
            follow: true,
            noimageindex: false,
            "max-video-preview": -1,
            "max-image-preview": "large",
            "max-snippet": -1,
          },
        },

    // Open Graph
    openGraph: {
      type: type === "product" ? "website" : type,
      siteName: SITE_NAME,
      title: title || SITE_NAME,
      description,
      url: canonicalUrl,
      locale: isFa ? "fa_IR" : "en_US",
      alternateLocale: isFa ? "en_US" : "fa_IR",
      images: [
        {
          url: ogImage,
          width: 1200,
          height: 630,
          alt: title || SITE_NAME,
        },
      ],
      ...(publishedTime && { publishedTime }),
      ...(authors && { authors }),
    },

    // Twitter
    twitter: {
      card: "summary_large_image",
      site: TWITTER_HANDLE,
      creator: TWITTER_HANDLE,
      title: title || SITE_NAME,
      description,
      images: [ogImage],
    },

    // Other
    formatDetection: {
      email: false,
      address: false,
      telephone: false,
    },

    // Icons
    icons: {
      icon: [
        { url: "/favicon.svg", type: "image/svg+xml" },
        { url: "/favicon.ico", sizes: "any" },
      ],
      apple: [{ url: "/apple-icon.png", sizes: "180x180" }],
    },

    // Manifest
    manifest: "/manifest.webmanifest",

    // Verification
    verification: {
      google: process.env.NEXT_PUBLIC_GOOGLE_VERIFICATION,
      yandex: process.env.NEXT_PUBLIC_YANDEX_VERIFICATION,
    },
  };
}

// ═══════════════════════════════════════════════════════════════
// JSON-LD SCHEMAS
// ═══════════════════════════════════════════════════════════════

export function organizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": `${SITE_URL}#organization`,
    name: SITE_NAME,
    url: SITE_URL,
    logo: {
      "@type": "ImageObject",
      url: `${SITE_URL}/favicon.svg`,
      width: 512,
      height: 512,
    },
    image: DEFAULT_OG_IMAGE,
    description: SITE_DESCRIPTION_EN,
    sameAs: [
      "https://instagram.com/sourcepixcel",
      "https://twitter.com/sourcepixcel",
      "https://linkedin.com/company/sourcepixcel",
      "https://youtube.com/@sourcepixcel",
    ],
    contactPoint: [
      {
        "@type": "ContactPoint",
        telephone: "+98-21-12345678",
        contactType: "customer support",
        availableLanguage: ["Persian", "English"],
        areaServed: "IR",
      },
    ],
    address: {
      "@type": "PostalAddress",
      streetAddress: "Valiasr St., No. 123",
      addressLocality: "Tehran",
      addressCountry: "IR",
    },
  };
}

export function webSiteSchema(locale: "fa" | "en") {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": `${SITE_URL}#website`,
    url: SITE_URL,
    name: SITE_NAME,
    description: SITE_DESCRIPTION_EN,
    inLanguage: locale === "fa" ? "fa-IR" : "en-US",
    publisher: { "@id": `${SITE_URL}#organization` },
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${SITE_URL}/${locale}/search?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  };
}

export function productSchema(params: {
  name: string;
  description: string;
  image: string | string[];
  sku: string;
  mpn?: string;
  brand: string;
  price: number;
  currency?: string;
  inStock: boolean;
  url: string;
  rating?: number;
  reviewCount?: number;
  condition?: string;
  category?: string;
  locale: "fa" | "en";
}) {
  const {
    name,
    description,
    image,
    sku,
    mpn,
    brand,
    price,
    currency = "IRR",
    inStock,
    url,
    rating,
    reviewCount,
    condition = "NewCondition",
    category,
    locale,
  } = params;

  const schema: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "Product",
    "@id": url,
    name,
    description,
    image: Array.isArray(image) ? image : [image],
    sku,
    mpn: mpn || sku,
    brand: {
      "@type": "Brand",
      name: brand,
    },
    category,
    inLanguage: locale === "fa" ? "fa-IR" : "en-US",
    offers: {
      "@type": "Offer",
      url,
      priceCurrency: currency,
      price: price.toString(),
      priceValidUntil: new Date(
        Date.now() + 365 * 24 * 60 * 60 * 1000
      ).toISOString(),
      itemCondition: `https://schema.org/${condition}`,
      availability: inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
      seller: {
        "@type": "Organization",
        name: SITE_NAME,
      },
      hasMerchantReturnPolicy: {
        "@type": "MerchantReturnPolicy",
        applicableCountry: "IR",
        returnPolicyCategory:
          "https://schema.org/MerchantReturnFiniteReturnWindow",
        merchantReturnDays: 7,
        returnMethod: "https://schema.org/ReturnByMail",
        returnFees: "https://schema.org/FreeReturn",
      },
      shippingDetails: {
        "@type": "OfferShippingDetails",
        shippingRate: {
          "@type": "MonetaryAmount",
          value: "0",
          currency: "IRR",
        },
        shippingDestination: {
          "@type": "DefinedRegion",
          addressCountry: "IR",
        },
      },
    },
  };

  if (rating && reviewCount) {
    schema.aggregateRating = {
      "@type": "AggregateRating",
      ratingValue: rating.toString(),
      reviewCount: reviewCount.toString(),
      bestRating: "5",
      worstRating: "1",
    };
  }

  return schema;
}

export function articleSchema(params: {
  headline: string;
  description: string;
  image: string;
  author: string;
  publishedTime: string;
  modifiedTime?: string;
  url: string;
  category: string;
  keywords?: string[];
  locale: "fa" | "en";
}) {
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: params.headline,
    description: params.description,
    image: params.image,
    author: {
      "@type": "Person",
      name: params.author,
    },
    publisher: {
      "@type": "Organization",
      name: SITE_NAME,
      logo: {
        "@type": "ImageObject",
        url: `${SITE_URL}/favicon.svg`,
      },
    },
    datePublished: params.publishedTime,
    dateModified: params.modifiedTime || params.publishedTime,
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": params.url,
    },
    articleSection: params.category,
    keywords: params.keywords?.join(", "),
    inLanguage: params.locale === "fa" ? "fa-IR" : "en-US",
  };
}

export function breadcrumbSchema(
  items: { name: string; url: string }[]
) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export function faqSchema(
  items: { question: string; answer: string }[]
) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: items.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: item.answer,
      },
    })),
  };
}

export function reviewSchema(params: {
  itemName: string;
  itemType: string;
  reviews: {
    author: string;
    rating: number;
    text: string;
    datePublished: string;
  }[];
  aggregateRating?: {
    ratingValue: number;
    reviewCount: number;
  };
}) {
  const schema: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": params.itemType,
    name: params.itemName,
    review: params.reviews.map((r) => ({
      "@type": "Review",
      author: {
        "@type": "Person",
        name: r.author,
      },
      reviewRating: {
        "@type": "Rating",
        ratingValue: r.rating.toString(),
        bestRating: "5",
        worstRating: "1",
      },
      reviewBody: r.text,
      datePublished: r.datePublished,
    })),
  };

  if (params.aggregateRating) {
    schema.aggregateRating = {
      "@type": "AggregateRating",
      ratingValue: params.aggregateRating.ratingValue.toString(),
      reviewCount: params.aggregateRating.reviewCount.toString(),
      bestRating: "5",
      worstRating: "1",
    };
  }

  return schema;
}

export function siteNavigationSchema(locale: "fa" | "en") {
  return {
    "@context": "https://schema.org",
    "@type": "SiteNavigationElement",
    name: [
      locale === "fa" ? "خانه" : "Home",
      locale === "fa" ? "دسته‌بندی‌ها" : "Categories",
      locale === "fa" ? "وبلاگ" : "Blog",
      locale === "fa" ? "تماس با ما" : "Contact",
    ],
    url: [
      `${SITE_URL}/${locale}`,
      `${SITE_URL}/${locale}/categories`,
      `${SITE_URL}/${locale}/blog`,
      `${SITE_URL}/${locale}/contact`,
    ],
  };
}

// ═══════════════════════════════════════════════════════════════
// PRECONNECT HINTS
// ═══════════════════════════════════════════════════════════════

export function preconnectDomains(): string[] {
  return [
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
    "https://picsum.photos",
    "https://loremflickr.com",
  ];
}
"""))

# ============================================================
# app/[locale]/layout.tsx — بهبود SEO
# ============================================================
files.append(("app/[locale]/layout.tsx", """import type { Metadata } from "next";
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
"""))

# ============================================================
# app/[locale]/product/[slug]/page.tsx — بهبود SEO محصول
# ============================================================
files.append(("app/[locale]/product/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import {
  products,
  getProductBySlug,
  getProductsByCategory,
  getCategoryById,
  getBrandById,
  getReviewsForProduct,
} from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";
import JsonLd from "@/components/common/JsonLd";
import {
  ProductDetail,
  ProductTabs,
  RelatedProducts,
} from "@/components/product";
import {
  buildFullMetadata,
  productSchema,
  breadcrumbSchema,
  reviewSchema,
  SEO,
} from "@/lib/seo";

interface PageProps {
  params: Promise<{ locale: string; slug: string }>;
}

export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    products.map((p) => ({ locale, slug: p.slug }))
  );
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;
  const product = getProductBySlug(slug);
  if (!product) {
    return { title: "Product not found" };
  }

  const brand = getBrandById(product.brand);
  const category = getCategoryById(product.category);
  const isFa = typedLocale === "fa";

  const title = isFa ? product.titleFa : product.titleEn;
  const brandName = brand ? (isFa ? brand.nameFa : brand.nameEn) : "";
  const categoryName = category ? (isFa ? category.nameFa : category.nameEn) : "";

  const descriptionFa = `خرید ${product.titleFa} با بهترین قیمت و ارسال سریع از SourcePixcel. ${brandName} ${categoryName} با ضمانت اصالت و ۷ روز مهلت بازگشت.`;
  const descriptionEn = `Buy ${product.titleEn} at the best price with fast shipping from SourcePixcel. ${brandName} ${categoryName} with authenticity guarantee and 7-day return.`;

  return buildFullMetadata({
    locale: typedLocale,
    titleFa: `${product.titleFa} | ${brandName}`,
    titleEn: `${product.titleEn} | ${brandName}`,
    descriptionFa,
    descriptionEn,
    path: `/product/${slug}`,
    image: product.image,
    type: "product",
  });
}

export default async function ProductPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const product = getProductBySlug(slug);
  if (!product) notFound();

  const category = getCategoryById(product.category);
  const brand = getBrandById(product.brand);
  const isFa = typedLocale === "fa";

  const related = getProductsByCategory(product.category)
    .filter((p) => p.id !== product.id)
    .slice(0, 5);

  const breadcrumbItems = [
    {
      labelFa: "دسته‌بندی‌ها",
      labelEn: "Categories",
      href: `/${typedLocale}/categories`,
    },
  ];

  if (category) {
    breadcrumbItems.push({
      labelFa: category.nameFa,
      labelEn: category.nameEn,
      href: `/${typedLocale}/category/${category.slug}`,
    });
  }

  breadcrumbItems.push({
    labelFa: product.titleFa,
    labelEn: product.titleEn,
  });

  // JSON-LD Schemas
  const productUrl = `${SEO.SITE_URL}/${typedLocale}/product/${slug}`;
  const reviews = getReviewsForProduct(product.id);

  const pSchema = productSchema({
    name: isFa ? product.titleFa : product.titleEn,
    description: isFa
      ? `خرید ${product.titleFa} با ضمانت اصالت و ارسال سریع`
      : `Buy ${product.titleEn} with authenticity guarantee and fast shipping`,
    image: product.image,
    sku: `SP-${product.id.toString().padStart(5, "0")}`,
    brand: brand ? (isFa ? brand.nameFa : brand.nameEn) : "SourcePixcel",
    price: product.finalPrice,
    currency: "IRR",
    inStock: product.inStock,
    url: productUrl,
    rating: product.rating,
    reviewCount: product.reviewCount,
    category: category ? (isFa ? category.nameFa : category.nameEn) : undefined,
    locale: typedLocale,
  });

  const bSchema = breadcrumbSchema([
    { name: isFa ? "خانه" : "Home", url: `${SEO.SITE_URL}/${typedLocale}` },
    ...(category
      ? [
          {
            name: isFa ? category.nameFa : category.nameEn,
            url: `${SEO.SITE_URL}/${typedLocale}/category/${category.slug}`,
          },
        ]
      : []),
    {
      name: isFa ? product.titleFa : product.titleEn,
      url: productUrl,
    },
  ]);

  const rSchema = reviewSchema({
    itemName: isFa ? product.titleFa : product.titleEn,
    itemType: "Product",
    reviews: reviews.slice(0, 5).map((r) => ({
      author: r.authorName,
      rating: r.rating,
      text: r.body,
      datePublished: r.date,
    })),
    aggregateRating: {
      ratingValue: product.rating,
      reviewCount: product.reviewCount,
    },
  });

  return (
    <>
      <JsonLd data={[pSchema, bSchema, rSchema]} />
      <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
        <Breadcrumb locale={typedLocale} items={breadcrumbItems} />
        <ProductDetail product={product} locale={typedLocale} />
        <ProductTabs product={product} locale={typedLocale} />
        <RelatedProducts products={related} locale={typedLocale} />
      </div>
    </>
  );
}
"""))

# ============================================================
# app/[locale]/category/[slug]/page.tsx — بهبود SEO دسته
# ============================================================
files.append(("app/[locale]/category/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import { categories, brands, products } from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";
import JsonLd from "@/components/common/JsonLd";
import { CategoryPage } from "@/components/category";
import { buildFullMetadata, breadcrumbSchema, SEO } from "@/lib/seo";

interface PageProps {
  params: Promise<{ locale: string; slug: string }>;
}

export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    categories.map((cat) => ({ locale, slug: cat.slug }))
  );
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;
  const category = categories.find((c) => c.slug === slug);
  if (!category) return { title: "Category not found" };

  const subcats = category.subcategories.map((s) => s.nameEn).join(", ");

  return buildFullMetadata({
    locale: typedLocale,
    titleFa: `خرید ${category.nameFa} | بهترین قیمت`,
    titleEn: `Buy ${category.nameEn} | Best Price`,
    descriptionFa: `خرید آنلاین ${category.nameFa} با بهترین قیمت و ارسال سریع. انواع ${category.subcategories
      .map((s) => s.nameFa)
      .join("، ")} با ضمانت اصالت از SourcePixcel.`,
    descriptionEn: `Buy ${category.nameEn} online with the best price and fast shipping. All ${subcats} with authenticity guarantee from SourcePixcel.`,
    path: `/category/${slug}`,
  });
}

export default async function CategoryListingPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const category = categories.find((c) => c.slug === slug);
  if (!category) notFound();

  const isFa = typedLocale === "fa";

  const bSchema = breadcrumbSchema([
    { name: isFa ? "خانه" : "Home", url: `${SEO.SITE_URL}/${typedLocale}` },
    {
      name: isFa ? "دسته‌بندی‌ها" : "Categories",
      url: `${SEO.SITE_URL}/${typedLocale}/categories`,
    },
    {
      name: isFa ? category.nameFa : category.nameEn,
      url: `${SEO.SITE_URL}/${typedLocale}/category/${slug}`,
    },
  ]);

  return (
    <>
      <JsonLd data={bSchema} />
      <div className="max-w-[1400px] mx-auto px-4">
        <Breadcrumb
          locale={typedLocale}
          items={[
            {
              labelFa: "دسته‌بندی‌ها",
              labelEn: "Categories",
              href: `/${typedLocale}/categories`,
            },
            {
              labelFa: category.nameFa,
              labelEn: category.nameEn,
            },
          ]}
        />

        <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
          {isFa ? category.nameFa : category.nameEn}
        </h1>

        <CategoryPage
          locale={typedLocale}
          categories={categories}
          brands={brands}
          products={products}
          initialCategoryId={category.id}
        />
      </div>
    </>
  );
}
"""))

# ============================================================
# app/[locale]/blog/[slug]/page.tsx — بهبود SEO بلاگ
# ============================================================
files.append(("app/[locale]/blog/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import {
  blogPosts,
  getBlogPostBySlug,
  getRelatedBlogPosts,
} from "@/lib/data";
import { BlogPostDetail } from "@/components/blog";
import JsonLd from "@/components/common/JsonLd";
import { buildFullMetadata, articleSchema, SEO } from "@/lib/seo";

interface PageProps {
  params: Promise<{ locale: string; slug: string }>;
}

export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    blogPosts.map((post) => ({ locale, slug: post.slug }))
  );
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;
  const post = getBlogPostBySlug(slug);
  if (!post) return { title: "Post not found" };

  const isFa = typedLocale === "fa";

  return buildFullMetadata({
    locale: typedLocale,
    titleFa: post.titleFa,
    titleEn: post.titleEn,
    descriptionFa: post.excerptFa,
    descriptionEn: post.excerptEn,
    path: `/blog/${slug}`,
    image: post.cover,
    type: "article",
    authors: [isFa ? post.authorFa : post.authorEn],
  });
}

export default async function BlogPostPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const post = getBlogPostBySlug(slug);
  if (!post) notFound();

  const related = getRelatedBlogPosts(slug, 3);
  const isFa = typedLocale === "fa";

  const aSchema = articleSchema({
    headline: isFa ? post.titleFa : post.titleEn,
    description: isFa ? post.excerptFa : post.excerptEn,
    image: post.cover,
    author: isFa ? post.authorFa : post.authorEn,
    publishedTime: post.dateEn,
    url: `${SEO.SITE_URL}/${typedLocale}/blog/${slug}`,
    category: isFa ? post.categoryFa : post.categoryEn,
    keywords: post.tags,
    locale: typedLocale,
  });

  return (
    <>
      <JsonLd data={aSchema} />
      <BlogPostDetail
        locale={typedLocale}
        post={post}
        related={related}
      />
    </>
  );
}
"""))

# ============================================================
# app/[locale]/faq/page.tsx — با FAQ Schema
# ============================================================
files.append(("app/[locale]/faq/page.tsx", """import type { Metadata } from "next";
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
"""))

# ============================================================
# app/sitemap.ts — sitemap پیشرفته
# ============================================================
files.append(("app/sitemap.ts", """import type { MetadataRoute } from "next";
import { categories, products, blogPosts } from "@/lib/data";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://sourcepixcel.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const locales = ["fa", "en"] as const;
  const now = new Date();

  const entries: MetadataRoute.Sitemap = [];

  // Static pages
  const staticPages = [
    { path: "", priority: 1.0, freq: "daily" as const },
    { path: "/categories", priority: 0.9, freq: "weekly" as const },
    { path: "/search", priority: 0.6, freq: "weekly" as const },
    { path: "/blog", priority: 0.8, freq: "weekly" as const },
    { path: "/about", priority: 0.5, freq: "monthly" as const },
    { path: "/contact", priority: 0.5, freq: "monthly" as const },
    { path: "/faq", priority: 0.6, freq: "monthly" as const },
    { path: "/terms", priority: 0.3, freq: "yearly" as const },
    { path: "/privacy", priority: 0.3, freq: "yearly" as const },
    { path: "/auth/login", priority: 0.4, freq: "monthly" as const },
    { path: "/auth/register", priority: 0.5, freq: "monthly" as const },
  ];

  for (const locale of locales) {
    for (const page of staticPages) {
      entries.push({
        url: `${SITE_URL}/${locale}${page.path}`,
        lastModified: now,
        changeFrequency: page.freq,
        priority: page.priority,
      });
    }
  }

  // Category pages
  for (const locale of locales) {
    for (const cat of categories) {
      entries.push({
        url: `${SITE_URL}/${locale}/category/${cat.slug}`,
        lastModified: now,
        changeFrequency: "weekly",
        priority: 0.85,
      });
    }
  }

  // Product pages (high priority)
  for (const locale of locales) {
    for (const p of products) {
      entries.push({
        url: `${SITE_URL}/${locale}/product/${p.slug}`,
        lastModified: now,
        changeFrequency: "daily",
        priority: p.isFeatured ? 0.95 : 0.9,
      });
    }
  }

  // Blog posts
  for (const locale of locales) {
    for (const post of blogPosts) {
      entries.push({
        url: `${SITE_URL}/${locale}/blog/${post.slug}`,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.7,
      });
    }
  }

  return entries;
}
"""))

# ============================================================
# app/robots.ts — robots پیشرفته
# ============================================================
files.append(("app/robots.ts", """import type { MetadataRoute } from "next";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://sourcepixcel.vercel.app";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/api/",
          "/admin/",
          "/checkout",
          "/account/",
          "/*/admin/",
          "/*/checkout",
          "/*/account/",
        ],
      },
      {
        userAgent: "GPTBot",
        allow: "/",
      },
      {
        userAgent: "CCBot",
        allow: "/",
      },
      {
        userAgent: "Twitterbot",
        allow: "/",
      },
      {
        userAgent: "facebookexternalhit",
        allow: "/",
      },
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
"""))

# ============================================================
# app/opengraph-image.tsx — OG image داینامیک
# ============================================================
files.append(("app/opengraph-image.tsx", """import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "SourcePixcel — Modern Online Store";
export const size = {
  width: 1200,
  height: 630,
};
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          height: "100%",
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: "#EF4056",
          backgroundImage:
            "linear-gradient(135deg, #EF4056 0%, #d63850 100%)",
          fontFamily: "system-ui, sans-serif",
          position: "relative",
        }}
      >
        {/* Decorative circles */}
        <div
          style={{
            position: "absolute",
            top: -100,
            right: -100,
            width: 400,
            height: 400,
            borderRadius: "50%",
            background: "rgba(255, 255, 255, 0.1)",
          }}
        />
        <div
          style={{
            position: "absolute",
            bottom: -150,
            left: -150,
            width: 500,
            height: 500,
            borderRadius: "50%",
            background: "rgba(255, 255, 255, 0.05)",
          }}
        />

        {/* Logo */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 20,
            marginBottom: 40,
          }}
        >
          <div
            style={{
              width: 100,
              height: 100,
              borderRadius: 24,
              background: "white",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 64,
              fontWeight: 900,
              color: "#EF4056",
            }}
          >
            S
          </div>
          <div
            style={{
              fontSize: 80,
              fontWeight: 900,
              color: "white",
              letterSpacing: -2,
            }}
          >
            SourcePixcel
          </div>
        </div>

        {/* Subtitle */}
        <div
          style={{
            fontSize: 36,
            color: "rgba(255, 255, 255, 0.9)",
            fontWeight: 500,
            textAlign: "center",
            maxWidth: 900,
          }}
        >
          فروشگاه آنلاین مدرن | Modern Online Store
        </div>

        {/* Features */}
        <div
          style={{
            display: "flex",
            gap: 30,
            marginTop: 60,
            fontSize: 24,
            color: "rgba(255, 255, 255, 0.85)",
          }}
        >
          <div>✓ ارسال سریع</div>
          <div>✓ ضمانت اصالت</div>
          <div>✓ ۷ روز بازگشت</div>
        </div>
      </div>
    ),
    {
      ...size,
    }
  );
}
"""))

# ============================================================
# app/[locale]/about/page.tsx — با metadata
# ============================================================
files.append(("app/[locale]/about/page.tsx", """import type { Metadata } from "next";
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
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 37: SEO Final")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Test SEO:")
        print("     - http://localhost:3000/sitemap.xml")
        print("     - http://localhost:3000/robots.txt")
        print("     - http://localhost:3000/opengraph-image")
        print("     - Right-click page → View Source → check <meta> tags")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()