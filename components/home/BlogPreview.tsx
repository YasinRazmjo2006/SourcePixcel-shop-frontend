import Link from "next/link";
import { Calendar, Clock, ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { blogPosts } from "@/lib/data";
import { SmartImage } from "@/components/common";

interface BlogPreviewProps {
  locale: Locale;
}

export default function BlogPreview({ locale }: BlogPreviewProps) {
  const isFa = locale === "fa";
  const posts = blogPosts.slice(0, 3);

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[16px] md:text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "آخرین مطالب وبلاگ" : "Latest from the Blog"}
        </h2>
        <Link
          href={`/${locale}/blog`}
          className="text-[12px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors"
        >
          {isFa ? "مشاهده همه" : "See all"}
          {isFa ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {posts.map((post) => (
          <Link
            key={post.id}
            href={`/${locale}/blog/${post.slug}`}
            className="group bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden hover:shadow-lg transition-shadow"
          >
            <div className="relative aspect-video overflow-hidden bg-[#F5F5F5]">
              <SmartImage
                src={post.cover}
                alt={isFa ? post.titleFa : post.titleEn}
                fill
                sizes="(max-width: 768px) 100vw, 33vw"
                className="object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <span
                className="absolute top-3 bg-[#EF4056] text-white text-[10px] font-medium px-2 py-1 rounded z-10"
                style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
              >
                {isFa ? post.categoryFa : post.categoryEn}
              </span>
            </div>

            <div className="p-4">
              <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-5 line-clamp-2 mb-2 group-hover:text-[#EF4056] transition-colors min-h-[40px]">
                {isFa ? post.titleFa : post.titleEn}
              </h3>

              <p className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] line-clamp-2 mb-3 min-h-[32px]">
                {isFa ? post.excerptFa : post.excerptEn}
              </p>

              <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8] pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
                <span className="flex items-center gap-1">
                  <Calendar size={11} />
                  {isFa ? post.dateFa : post.dateEn}
                </span>
                <span className="flex items-center gap-1">
                  <Clock size={11} />
                  {isFa ? post.readTimeFa : post.readTimeEn}
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
