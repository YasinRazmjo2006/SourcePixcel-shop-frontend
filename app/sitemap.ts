import type { MetadataRoute } from "next";
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
