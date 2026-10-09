import type { Metadata } from "next";
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
  Testimonials,
  BlogPreview,
  Newsletter,
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

const HOME_SECTION_SIZE = 5;

export default async function HomePage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  const featured = getFeaturedProducts().slice(0, HOME_SECTION_SIZE);
  const newProducts = getNewProducts().slice(0, HOME_SECTION_SIZE);
  const discounted = getDiscountedProducts().slice(0, HOME_SECTION_SIZE);

  return (
    <>
      <JsonLd data={[buildOrganizationSchema(), buildWebSiteSchema()]} />
      <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
        {/* 1. Hero Slider */}
        <HeroSlider locale={typedLocale} />

        {/* 2. Service Badges */}
        <ServiceBadges locale={typedLocale} />

        {/* 3. Categories */}
        <CategoryCircles locale={typedLocale} />

        {/* 4. Amazing Offer */}
        <AmazingOffer locale={typedLocale} />

        {/* 5. Featured */}
        {featured.length > 0 && (
          <ProductSection
            titleFa="پیشنهاد ویژه"
            titleEn="Featured Products"
            products={featured}
            locale={typedLocale}
            seeAllHref="/search?featured=1"
          />
        )}

        {/* 6. New Arrivals */}
        {newProducts.length > 0 && (
          <ProductSection
            titleFa="جدیدترین‌ها"
            titleEn="New Arrivals"
            products={newProducts}
            locale={typedLocale}
            seeAllHref="/search?new=1"
          />
        )}

        {/* 7. Brands */}
        <BrandLogos locale={typedLocale} />

        {/* 8. Discounted */}
        {discounted.length > 0 && (
          <ProductSection
            titleFa="تخفیف‌دارها"
            titleEn="Discounted"
            products={discounted}
            locale={typedLocale}
            seeAllHref="/search?discount=1"
          />
        )}

        {/* 9. Testimonials */}
        <Testimonials locale={typedLocale} />

        {/* 10. Blog */}
        <BlogPreview locale={typedLocale} />

        {/* 11. Newsletter */}
        <Newsletter locale={typedLocale} />
      </div>
    </>
  );
}
