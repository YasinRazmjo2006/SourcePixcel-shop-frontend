import type { Metadata } from "next";
import type { Locale } from "@/lib/types";

const SITE_NAME = "SourcePixcel";
const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://sourcepixcel.vercel.app";

interface SeoOptions {
  titleFa: string;
  titleEn: string;
  descriptionFa: string;
  descriptionEn: string;
  path?: string;
  locale: Locale;
  image?: string;
  type?: "website" | "article" | "product";
}

export function buildMetadata(options: SeoOptions): Metadata {
  const {
    titleFa,
    titleEn,
    descriptionFa,
    descriptionEn,
    path = "",
    locale,
    image,
    type = "website",
  } = options;

  const isFa = locale === "fa";
  const title = isFa ? titleFa : titleEn;
  const description = isFa ? descriptionFa : descriptionEn;
  const canonicalUrl = `${SITE_URL}/${locale}${path}`;

  return {
    title,
    description,
    metadataBase: new URL(SITE_URL),
    alternates: {
      canonical: canonicalUrl,
      languages: {
        "fa-IR": `${SITE_URL}/fa${path}`,
        "en-US": `${SITE_URL}/en${path}`,
      },
    },
    openGraph: {
      title,
      description,
      url: canonicalUrl,
      siteName: SITE_NAME,
      locale: isFa ? "fa_IR" : "en_US",
      type: type === "product" ? "website" : type,
      images: image
        ? [{ url: image, width: 1200, height: 630, alt: title }]
        : undefined,
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: image ? [image] : undefined,
    },
    robots: {
      index: true,
      follow: true,
      googleBot: {
        index: true,
        follow: true,
        "max-image-preview": "large",
        "max-snippet": -1,
      },
    },
  };
}

export const SITE_NAME_EXPORT = SITE_NAME;
export const SITE_URL_EXPORT = SITE_URL;

export function buildProductSchema(params: {
  name: string;
  description: string;
  image: string;
  sku: string;
  price: number;
  currency?: string;
  inStock: boolean;
  rating?: number;
  reviewCount?: number;
  brand?: string;
  url: string;
}) {
  const {
    name,
    description,
    image,
    sku,
    price,
    currency = "IRR",
    inStock,
    rating,
    reviewCount,
    brand,
    url,
  } = params;

  const schema: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "Product",
    name,
    description,
    image,
    sku,
    brand: brand ? { "@type": "Brand", name: brand } : undefined,
    offers: {
      "@type": "Offer",
      url,
      priceCurrency: currency,
      price: price.toString(),
      availability: inStock
        ? "https://schema.org/InStock"
        : "https://schema.org/OutOfStock",
    },
  };

  if (rating && reviewCount) {
    schema.aggregateRating = {
      "@type": "AggregateRating",
      ratingValue: rating.toString(),
      reviewCount: reviewCount.toString(),
    };
  }

  return schema;
}

export function buildOrganizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: SITE_NAME,
    url: SITE_URL,
    logo: `${SITE_URL}/favicon.svg`,
    sameAs: [
      "https://instagram.com/sourcepixcel",
      "https://twitter.com/sourcepixcel",
    ],
  };
}

export function buildWebSiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: SITE_NAME,
    url: SITE_URL,
    potentialAction: {
      "@type": "SearchAction",
      target: `${SITE_URL}/fa/search?q={search_term_string}`,
      "query-input": "required name=search_term_string",
    },
  };
}

export function buildBreadcrumbSchema(
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
