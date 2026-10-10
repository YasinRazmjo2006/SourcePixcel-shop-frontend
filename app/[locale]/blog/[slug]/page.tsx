import { notFound } from "next/navigation";
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
