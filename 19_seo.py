# 19_seo.py
# بهینه‌سازی SEO
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/utils/seo.ts
# ============================================================
files.append(("lib/utils/seo.ts", """import type { Metadata } from "next";
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
"""))

# ============================================================
# lib/utils/index.ts (updated)
# ============================================================
files.append(("lib/utils/index.ts", """// lib/utils/index.ts
export {
  formatPrice,
  formatPriceWithCurrency,
  calcFinalPrice,
  formatDiscount,
  formatRating,
  formatReviewCount,
  truncate,
  getProductTitle,
  getCategoryName,
  getBrandName,
  formatDate,
  localePath,
  cn,
  getStockLabel,
  scrollToTop,
} from "./format";

export {
  isValidIranianMobile,
  normalizeMobile,
  formatMobileDisplay,
  isValidEmail,
  isValidIranianNationalId,
  isValidIranianPostalCode,
  getPasswordStrength,
  isValidPassword,
} from "./validators";

export {
  buildMetadata,
  buildProductSchema,
  buildOrganizationSchema,
  buildWebSiteSchema,
  buildBreadcrumbSchema,
  SITE_NAME_EXPORT,
  SITE_URL_EXPORT,
} from "./seo";
"""))

# ============================================================
# components/common/JsonLd.tsx
# ============================================================
files.append(("components/common/JsonLd.tsx", """interface JsonLdProps {
  data: Record<string, unknown> | Record<string, unknown>[];
}

export default function JsonLd({ data }: JsonLdProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}
"""))

# ============================================================
# components/common/index.ts (updated)
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
export { default as StaticPage } from "./StaticPage";
export { default as ThemeProvider } from "./ThemeProvider";
export { default as ThemeToggle } from "./ThemeToggle";
export { default as JsonLd } from "./JsonLd";
"""))

# ============================================================
# app/sitemap.ts
# ============================================================
files.append(("app/sitemap.ts", """import type { MetadataRoute } from "next";
import { categories, products, blogPosts } from "@/lib/data";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://sourcepixcel.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const locales = ["fa", "en"] as const;

  const staticPages = [
    "",
    "/categories",
    "/cart",
    "/search",
    "/about",
    "/contact",
    "/faq",
    "/terms",
    "/privacy",
    "/blog",
    "/compare",
    "/auth/login",
    "/auth/register",
  ];

  const entries: MetadataRoute.Sitemap = [];

  // Static pages
  for (const locale of locales) {
    for (const page of staticPages) {
      entries.push({
        url: `${SITE_URL}/${locale}${page}`,
        lastModified: new Date(),
        changeFrequency: "weekly",
        priority: page === "" ? 1 : 0.7,
      });
    }
  }

  // Category pages
  for (const locale of locales) {
    for (const cat of categories) {
      entries.push({
        url: `${SITE_URL}/${locale}/category/${cat.slug}`,
        lastModified: new Date(),
        changeFrequency: "weekly",
        priority: 0.8,
      });
    }
  }

  // Product pages
  for (const locale of locales) {
    for (const p of products) {
      entries.push({
        url: `${SITE_URL}/${locale}/product/${p.slug}`,
        lastModified: new Date(),
        changeFrequency: "daily",
        priority: 0.9,
      });
    }
  }

  // Blog pages
  for (const locale of locales) {
    for (const post of blogPosts) {
      entries.push({
        url: `${SITE_URL}/${locale}/blog/${post.slug}`,
        lastModified: new Date(),
        changeFrequency: "monthly",
        priority: 0.6,
      });
    }
  }

  return entries;
}
"""))

# ============================================================
# app/robots.ts
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
        disallow: ["/api/", "/admin/", "/checkout", "/account/"],
      },
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
"""))

# ============================================================
# app/manifest.ts (PWA manifest)
# ============================================================
files.append(("app/manifest.ts", """import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "SourcePixcel",
    short_name: "SourcePixcel",
    description:
      "Bilingual (Persian/English) e-commerce store by SourcePixcel",
    start_url: "/fa",
    display: "standalone",
    background_color: "#F5F5F5",
    theme_color: "#EF4056",
    orientation: "portrait",
    lang: "fa",
    dir: "rtl",
    icons: [
      {
        src: "/favicon.svg",
        sizes: "any",
        type: "image/svg+xml",
        purpose: "any",
      },
    ],
  };
}
"""))

# ============================================================
# app/[locale]/page.tsx (with metadata + schemas)
# ============================================================
files.append(("app/[locale]/page.tsx", """import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import {
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
} from "@/lib/data";
import {
  HeroSlider,
  ServiceBadges,
  CategoryCircles,
  AmazingOffer,
  ProductSection,
  BrandLogos,
} from "@/components/home";
import JsonLd from "@/components/common/JsonLd";
import {
  buildMetadata,
  buildOrganizationSchema,
  buildWebSiteSchema,
} from "@/lib/utils";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return buildMetadata({
    locale: typedLocale,
    titleFa: "SourcePixcel | فروشگاه آنلاین مدرن",
    titleEn: "SourcePixcel | Modern Online Store",
    descriptionFa:
      "فروشگاه اینترنتی SourcePixcel — خرید آنلاین موبایل، لپ‌تاپ، لوازم خانگی، پوشاک و لوازم جانبی با ارسال سریع و ضمانت اصالت.",
    descriptionEn:
      "SourcePixcel online store — shop mobile phones, laptops, home appliances, fashion, and accessories with fast shipping and authenticity guarantee.",
    path: "",
  });
}

export default async function HomePage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  const featured = getFeaturedProducts();
  const newProducts = getNewProducts();
  const discounted = getDiscountedProducts();

  return (
    <>
      <JsonLd
        data={[buildOrganizationSchema(), buildWebSiteSchema()]}
      />
      <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
        <HeroSlider locale={typedLocale} />
        <ServiceBadges locale={typedLocale} />
        <CategoryCircles locale={typedLocale} />
        <AmazingOffer locale={typedLocale} />

        {featured.length > 0 && (
          <ProductSection
            titleFa="پیشنهاد ویژه"
            titleEn="Featured Products"
            products={featured}
            locale={typedLocale}
            seeAllHref="/search?featured=1"
          />
        )}

        {newProducts.length > 0 && (
          <ProductSection
            titleFa="جدیدترین‌ها"
            titleEn="New Arrivals"
            products={newProducts}
            locale={typedLocale}
            seeAllHref="/search?new=1"
          />
        )}

        {discounted.length > 4 && (
          <ProductSection
            titleFa="تخفیف‌دارها"
            titleEn="Discounted"
            products={discounted.slice(0, 10)}
            locale={typedLocale}
            seeAllHref="/search?discount=1"
          />
        )}

        <BrandLogos locale={typedLocale} />
      </div>
    </>
  );
}
"""))

# ============================================================
# app/[locale]/product/[slug]/page.tsx (with Product Schema)
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
} from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";
import JsonLd from "@/components/common/JsonLd";
import {
  ProductDetail,
  ProductTabs,
  RelatedProducts,
} from "@/components/product";
import {
  buildMetadata,
  buildProductSchema,
  buildBreadcrumbSchema,
  SITE_URL_EXPORT,
} from "@/lib/utils";

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

  return buildMetadata({
    locale: typedLocale,
    titleFa: `${product.titleFa} | SourcePixcel`,
    titleEn: `${product.titleEn} | SourcePixcel`,
    descriptionFa: product.titleFa,
    descriptionEn: product.titleEn,
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

  const productSchema = buildProductSchema({
    name: isFa ? product.titleFa : product.titleEn,
    description: isFa ? product.titleFa : product.titleEn,
    image: product.image,
    sku: `SP-${product.id.toString().padStart(5, "0")}`,
    price: product.finalPrice,
    inStock: product.inStock,
    rating: product.rating,
    reviewCount: product.reviewCount,
    brand: brand ? (isFa ? brand.nameFa : brand.nameEn) : undefined,
    url: `${SITE_URL_EXPORT}/${typedLocale}/product/${slug}`,
  });

  const breadcrumbSchema = buildBreadcrumbSchema([
    { name: isFa ? "خانه" : "Home", url: `${SITE_URL_EXPORT}/${typedLocale}` },
    ...(category
      ? [
          {
            name: isFa ? category.nameFa : category.nameEn,
            url: `${SITE_URL_EXPORT}/${typedLocale}/category/${category.slug}`,
          },
        ]
      : []),
    {
      name: isFa ? product.titleFa : product.titleEn,
      url: `${SITE_URL_EXPORT}/${typedLocale}/product/${slug}`,
    },
  ]);

  return (
    <>
      <JsonLd data={[productSchema, breadcrumbSchema]} />
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
# app/[locale]/category/[slug]/page.tsx (with metadata)
# ============================================================
files.append(("app/[locale]/category/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Metadata } from "next";
import type { Locale } from "@/lib/types";
import { categories, brands, products } from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";
import JsonLd from "@/components/common/JsonLd";
import { CategoryPage } from "@/components/category";
import { buildMetadata, buildBreadcrumbSchema, SITE_URL_EXPORT } from "@/lib/utils";

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

  return buildMetadata({
    locale: typedLocale,
    titleFa: `${category.nameFa} | SourcePixcel`,
    titleEn: `${category.nameEn} | SourcePixcel`,
    descriptionFa: `خرید آنلاین ${category.nameFa} با بهترین قیمت و ارسال سریع از SourcePixcel.`,
    descriptionEn: `Buy ${category.nameEn} online with the best price and fast shipping from SourcePixcel.`,
    path: `/category/${slug}`,
  });
}

export default async function CategoryListingPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const category = categories.find((c) => c.slug === slug);
  if (!category) notFound();

  const isFa = typedLocale === "fa";

  const breadcrumbSchema = buildBreadcrumbSchema([
    { name: isFa ? "خانه" : "Home", url: `${SITE_URL_EXPORT}/${typedLocale}` },
    {
      name: isFa ? "دسته‌بندی‌ها" : "Categories",
      url: `${SITE_URL_EXPORT}/${typedLocale}/categories`,
    },
    {
      name: isFa ? category.nameFa : category.nameEn,
      url: `${SITE_URL_EXPORT}/${typedLocale}/category/${slug}`,
    },
  ]);

  return (
    <>
      <JsonLd data={breadcrumbSchema} />
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

        <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
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
# app/[locale]/blog/[slug]/page.tsx (with Article Schema)
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
import { buildMetadata, SITE_URL_EXPORT } from "@/lib/utils";

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

  return buildMetadata({
    locale: typedLocale,
    titleFa: `${post.titleFa} | وبلاگ SourcePixcel`,
    titleEn: `${post.titleEn} | SourcePixcel Blog`,
    descriptionFa: post.excerptFa,
    descriptionEn: post.excerptEn,
    path: `/blog/${slug}`,
    image: post.cover,
    type: "article",
  });
}

export default async function BlogPostPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const post = getBlogPostBySlug(slug);
  if (!post) notFound();

  const related = getRelatedBlogPosts(slug, 3);
  const isFa = typedLocale === "fa";

  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: isFa ? post.titleFa : post.titleEn,
    description: isFa ? post.excerptFa : post.excerptEn,
    image: post.cover,
    author: {
      "@type": "Person",
      name: isFa ? post.authorFa : post.authorEn,
    },
    publisher: {
      "@type": "Organization",
      name: "SourcePixcel",
      logo: {
        "@type": "ImageObject",
        url: `${SITE_URL_EXPORT}/favicon.svg`,
      },
    },
    url: `${SITE_URL_EXPORT}/${typedLocale}/blog/${slug}`,
    articleSection: isFa ? post.categoryFa : post.categoryEn,
    keywords: post.tags.join(", "),
  };

  return (
    <>
      <JsonLd data={articleSchema} />
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
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 19: SEO + Metadata")
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
        print("Now run: npm run dev")
        print("Test:")
        print("  Sitemap:  http://localhost:3000/sitemap.xml")
        print("  Robots:   http://localhost:3000/robots.txt")
        print("  Manifest: http://localhost:3000/manifest.webmanifest")
        print("\nNext: run 20_final.py (final touches)")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()