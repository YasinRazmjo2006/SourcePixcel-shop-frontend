import type { Locale } from "@/lib/types";
import { blogPosts } from "@/lib/data";
import { BlogList } from "@/components/blog";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export const metadata = {
  title: "Blog — SourcePixcel",
  description: "Read the latest articles and guides on SourcePixcel blog.",
};

export default async function BlogPage({ params }: PageProps) {
  const { locale } = await params;
  return <BlogList locale={locale as Locale} posts={blogPosts} />;
}
