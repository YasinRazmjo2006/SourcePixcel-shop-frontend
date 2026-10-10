import type { Metadata } from "next";

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
