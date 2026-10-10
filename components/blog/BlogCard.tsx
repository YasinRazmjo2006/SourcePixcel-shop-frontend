import Link from "next/link";
import { Calendar, Clock, User } from "lucide-react";
import type { BlogPost, Locale } from "@/lib/types";
import { SmartImage } from "@/components/common";

interface BlogCardProps {
  post: BlogPost;
  locale: Locale;
  featured?: boolean;
}

export default function BlogCard({ post, locale, featured = false }: BlogCardProps) {
  const isFa = locale === "fa";

  const title = isFa ? post.titleFa : post.titleEn;
  const excerpt = isFa ? post.excerptFa : post.excerptEn;
  const category = isFa ? post.categoryFa : post.categoryEn;
  const author = isFa ? post.authorFa : post.authorEn;
  const date = isFa ? post.dateFa : post.dateEn;
  const readTime = isFa ? post.readTimeFa : post.readTimeEn;

  return (
    <Link
      href={`/${locale}/blog/${post.slug}`}
      className="group bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden hover:shadow-lg transition-shadow flex flex-col"
    >
      <div className={`relative ${featured ? "aspect-[16/7]" : "aspect-video"} overflow-hidden`}>
        <SmartImage
          src={post.cover}
          alt={title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <span className="absolute top-3 bg-[#EF4056] text-white text-[10px] font-medium px-2 py-1 rounded z-10"
          style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
        >
          {category}
        </span>
      </div>

      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-[14px] md:text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-6 mb-2 line-clamp-2 group-hover:text-[#EF4056] transition-colors">
          {title}
        </h3>

        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6 line-clamp-2 mb-3 flex-1">
          {excerpt}
        </p>

        <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8] pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex-wrap">
          <span className="flex items-center gap-1">
            <User size={11} />
            {author}
          </span>
          <span className="flex items-center gap-1">
            <Calendar size={11} />
            {date}
          </span>
          <span className="flex items-center gap-1">
            <Clock size={11} />
            {readTime}
          </span>
        </div>
      </div>
    </Link>
  );
}
