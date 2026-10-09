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
