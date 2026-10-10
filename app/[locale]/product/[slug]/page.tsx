import { notFound } from "next/navigation";
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
