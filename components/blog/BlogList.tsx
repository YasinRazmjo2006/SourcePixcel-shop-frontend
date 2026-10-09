import type { BlogPost, Locale } from "@/lib/types";
import { Breadcrumb } from "@/components/common";
import BlogCard from "./BlogCard";

interface BlogListProps {
  locale: Locale;
  posts: BlogPost[];
}

export default function BlogList({ locale, posts }: BlogListProps) {
  const isFa = locale === "fa";
  const featured = posts[0];
  const rest = posts.slice(1);

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "وبلاگ", labelEn: "Blog" }]}
      />

      <h1 className="text-[22px] font-bold text-[#3F4064] mb-6">
        {isFa ? "وبلاگ SourcePixcel" : "SourcePixcel Blog"}
      </h1>

      {/* Featured post */}
      {featured && (
        <div className="mb-8">
          <BlogCard post={featured} locale={locale} featured />
        </div>
      )}

      {/* Rest */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {rest.map((post) => (
          <BlogCard key={post.id} post={post} locale={locale} />
        ))}
      </div>
    </div>
  );
}
