import { notFound } from "next/navigation";
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
