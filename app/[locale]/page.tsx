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
  BlogPreview,
  Newsletter,
} from "@/components/home";
import {
  StatsCounter,
  TrustBadges,
  Guarantees,
  PaymentMethods,
  Testimonials,
} from "@/components/trust";
import JsonLd from "@/components/common/JsonLd";
import LazySection from "@/components/common/LazySection";
import { Container } from "@/components/ui";
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
      <Container className="py-4 space-y-4 md:space-y-5">
        {/* Above the fold — always render */}
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

        {/* Below the fold — lazy load */}
        <LazySection minHeight={300}>
          <BrandLogos locale={typedLocale} />
        </LazySection>

        {discounted.length > 0 && (
          <LazySection minHeight={400}>
            <ProductSection
              titleFa="تخفیف‌دارها"
              titleEn="Discounted"
              products={discounted}
              locale={typedLocale}
              seeAllHref="/search?discount=1"
            />
          </LazySection>
        )}

        <LazySection minHeight={250}>
          <Guarantees locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={150}>
          <StatsCounter locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={250}>
          <TrustBadges locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={150}>
          <PaymentMethods locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={350}>
          <Testimonials locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={350}>
          <BlogPreview locale={typedLocale} />
        </LazySection>

        <LazySection minHeight={200}>
          <Newsletter locale={typedLocale} />
        </LazySection>
      </Container>
    </>
  );
}
