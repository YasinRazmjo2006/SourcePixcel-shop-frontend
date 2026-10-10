import { notFound } from "next/navigation";
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
