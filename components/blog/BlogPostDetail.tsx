import Link from "next/link";
import { Calendar, Clock, User, Tag, ArrowRight, ArrowLeft } from "lucide-react";
import type { BlogPost, Locale } from "@/lib/types";
import { Breadcrumb, SmartImage } from "@/components/common";

interface BlogPostDetailProps {
  locale: Locale;
  post: BlogPost;
  related: BlogPost[];
}

export default function BlogPostDetail({
  locale,
  post,
  related,
}: BlogPostDetailProps) {
  const isFa = locale === "fa";

  const title = isFa ? post.titleFa : post.titleEn;
  const content = isFa ? post.contentFa : post.contentEn;
  const category = isFa ? post.categoryFa : post.categoryEn;
  const author = isFa ? post.authorFa : post.authorEn;
  const date = isFa ? post.dateFa : post.dateEn;
  const readTime = isFa ? post.readTimeFa : post.readTimeEn;

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[
          { labelFa: "وبلاگ", labelEn: "Blog", href: `/${locale}/blog` },
          { labelFa: post.titleFa, labelEn: post.titleEn },
        ]}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <article className="lg:col-span-2 bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
          <div className="relative aspect-video">
            <SmartImage
              src={post.cover}
              alt={title}
              fill
              sizes="(max-width: 1024px) 100vw, 66vw"
              className="object-cover"
              priority
            />
          </div>

          <div className="p-5 md:p-7">
            <div className="mb-3">
              <Link
                href={`/${locale}/blog`}
                className="inline-block bg-[#EF4056]/10 text-[#EF4056] text-[11px] font-medium px-2 py-1 rounded"
              >
                {category}
              </Link>
            </div>

            <h1 className="text-[22px] md:text-[26px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-9 mb-4">
              {title}
            </h1>

            <div className="flex items-center gap-4 text-[11px] text-[#A1A3A8] pb-4 mb-5 border-b border-[#E0E0E2] dark:border-[#2A2A2E] flex-wrap">
              <span className="flex items-center gap-1">
                <User size={12} />
                {author}
              </span>
              <span className="flex items-center gap-1">
                <Calendar size={12} />
                {date}
              </span>
              <span className="flex items-center gap-1">
                <Clock size={12} />
                {readTime}
              </span>
            </div>

            <div className="prose text-[13px] md:text-[14px] text-[#62666D] dark:text-[#A1A3A8] whitespace-pre-line">
              {content}
            </div>

            {post.tags.length > 0 && (
              <div className="flex items-center gap-2 mt-8 pt-5 border-t border-[#E0E0E2] dark:border-[#2A2A2E] flex-wrap">
                <Tag size={14} className="text-[#A1A3A8]" />
                {post.tags.map((tag, i) => (
                  <span
                    key={i}
                    className="text-[11px] bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8] px-2 py-1 rounded"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="mt-6">
              <Link
                href={`/${locale}/blog`}
                className="inline-flex items-center gap-2 text-[12px] text-[#00BFFF] hover:text-[#EF4056] transition-colors"
              >
                {isFa ? <ArrowRight size={14} /> : <ArrowLeft size={14} />}
                {isFa ? "بازگشت به وبلاگ" : "Back to blog"}
              </Link>
            </div>
          </div>
        </article>

        <aside className="lg:col-span-1">
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 sticky top-24">
            <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-4">
              {isFa ? "مطالب مرتبط" : "Related Posts"}
            </h2>
            <div className="space-y-3">
              {related.map((rp) => (
                <Link
                  key={rp.id}
                  href={`/${locale}/blog/${rp.slug}`}
                  className="flex gap-3 group"
                >
                  <div className="w-20 h-16 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
                    <SmartImage
                      src={rp.cover}
                      alt={isFa ? rp.titleFa : rp.titleEn}
                      fill
                      sizes="80px"
                      className="object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] leading-5 line-clamp-2 group-hover:text-[#EF4056] transition-colors">
                      {isFa ? rp.titleFa : rp.titleEn}
                    </h3>
                    <div className="text-[10px] text-[#A1A3A8] mt-1">
                      {isFa ? rp.dateFa : rp.dateEn}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
