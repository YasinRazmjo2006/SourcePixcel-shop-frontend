import type { MetadataRoute } from "next";
import { categories, products, blogPosts } from "@/lib/data";

const SITE_URL =
  process.env.NEXT_PUBLIC_SITE_URL || "https://sourcepixcel.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const locales = ["fa", "en"] as const;
  const now = new Date();

  const entries: MetadataRoute.Sitemap = [];

  // Static pages
  const staticPages = [
    { path: "", priority: 1.0, freq: "daily" as const },
    { path: "/categories", priority: 0.9, freq: "weekly" as const },
    { path: "/search", priority: 0.6, freq: "weekly" as const },
    { path: "/blog", priority: 0.8, freq: "weekly" as const },
    { path: "/about", priority: 0.5, freq: "monthly" as const },
    { path: "/contact", priority: 0.5, freq: "monthly" as const },
    { path: "/faq", priority: 0.6, freq: "monthly" as const },
    { path: "/terms", priority: 0.3, freq: "yearly" as const },
    { path: "/privacy", priority: 0.3, freq: "yearly" as const },
    { path: "/auth/login", priority: 0.4, freq: "monthly" as const },
    { path: "/auth/register", priority: 0.5, freq: "monthly" as const },
  ];

  for (const locale of locales) {
    for (const page of staticPages) {
      entries.push({
        url: `${SITE_URL}/${locale}${page.path}`,
        lastModified: now,
        changeFrequency: page.freq,
        priority: page.priority,
      });
    }
  }

  // Category pages
  for (const locale of locales) {
    for (const cat of categories) {
      entries.push({
        url: `${SITE_URL}/${locale}/category/${cat.slug}`,
        lastModified: now,
        changeFrequency: "weekly",
        priority: 0.85,
      });
    }
  }

  // Product pages (high priority)
  for (const locale of locales) {
    for (const p of products) {
      entries.push({
        url: `${SITE_URL}/${locale}/product/${p.slug}`,
        lastModified: now,
        changeFrequency: "daily",
        priority: p.isFeatured ? 0.95 : 0.9,
      });
    }
  }

  // Blog posts
  for (const locale of locales) {
    for (const post of blogPosts) {
      entries.push({
        url: `${SITE_URL}/${locale}/blog/${post.slug}`,
        lastModified: now,
        changeFrequency: "monthly",
        priority: 0.7,
      });
    }
  }

  return entries;
}
