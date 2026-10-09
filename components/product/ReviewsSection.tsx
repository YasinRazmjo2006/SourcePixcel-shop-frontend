"use client";

import { useMemo, useState, useEffect } from "react";
import { Star, SlidersHorizontal, PenLine, ChevronDown } from "lucide-react";
import type { Locale, Review } from "@/lib/types";
import { getReviewsForProduct } from "@/lib/data";
import { useReviewsStore } from "@/lib/stores";
import RatingStars from "./RatingStars";
import ReviewCard from "./ReviewCard";
import ReviewForm from "./ReviewForm";

type SortOption = "newest" | "helpful" | "highest" | "lowest";
type FilterOption = "all" | 5 | 4 | 3 | 2 | 1;

interface ReviewsSectionProps {
  productId: number;
  locale: Locale;
}

export default function ReviewsSection({
  productId,
  locale,
}: ReviewsSectionProps) {
  const isFa = locale === "fa";
  const [showForm, setShowForm] = useState(false);
  const [sort, setSort] = useState<SortOption>("newest");
  const [filter, setFilter] = useState<FilterOption>("all");
  const [showAll, setShowAll] = useState(false);
  const [mounted, setMounted] = useState(false);

  const userReviews = useReviewsStore((s) => s.userReviews);
  const helpfulVotes = useReviewsStore((s) => s.helpfulVotes);

  useEffect(() => {
    setMounted(true);
  }, []);

  const allReviews = useMemo(() => {
    const base = getReviewsForProduct(productId);
    const user = userReviews.filter((r) => r.productId === productId);
    return [...user, ...base];
  }, [productId, userReviews]);

  // Statistics
  const stats = useMemo(() => {
    const total = allReviews.length;
    if (total === 0) {
      return {
        average: 0,
        total: 0,
        breakdown: [0, 0, 0, 0, 0],
      };
    }
    const sum = allReviews.reduce((s, r) => s + r.rating, 0);
    const breakdown = [5, 4, 3, 2, 1].map(
      (star) => allReviews.filter((r) => r.rating === star).length
    );
    return {
      average: sum / total,
      total,
      breakdown,
    };
  }, [allReviews]);

  // Filter + sort
  const filteredReviews = useMemo(() => {
    let result = [...allReviews];

    if (filter !== "all") {
      result = result.filter((r) => r.rating === filter);
    }

    switch (sort) {
      case "helpful":
        result.sort((a, b) => b.helpful - a.helpful);
        break;
      case "highest":
        result.sort((a, b) => b.rating - a.rating);
        break;
      case "lowest":
        result.sort((a, b) => a.rating - b.rating);
        break;
      case "newest":
      default:
        // Already newest first
        break;
    }

    return result;
  }, [allReviews, filter, sort]);

  const displayedReviews = showAll
    ? filteredReviews
    : filteredReviews.slice(0, 4);

  const t = {
    title: isFa ? "نظرات کاربران" : "Customer Reviews",
    average: isFa ? "میانگین امتیاز" : "Average Rating",
    from: isFa ? "از" : "from",
    reviews: isFa ? "نظر" : "reviews",
    writeReview: isFa ? "ثبت نظر" : "Write a Review",
    sortBy: isFa ? "مرتب‌سازی:" : "Sort by:",
    newest: isFa ? "جدیدترین" : "Newest",
    helpful: isFa ? "مفیدترین" : "Most Helpful",
    highest: isFa ? "بالاترین امتیاز" : "Highest Rating",
    lowest: isFa ? "پایین‌ترین امتیاز" : "Lowest Rating",
    filter: isFa ? "فیلتر:" : "Filter:",
    all: isFa ? "همه" : "All",
    showMore: isFa ? "نمایش نظرات بیشتر" : "Show more reviews",
    noReviews: isFa ? "هنوز نظری ثبت نشده" : "No reviews yet",
    beFirst: isFa
      ? "اولین نفری باشید که نظر می‌دهد"
      : "Be the first to write a review",
  };

  return (
    <div className="space-y-4">
      {/* Rating summary */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Average */}
          <div className="text-center md:text-start md:border-l md:border-[#E0E0E2] md:dark:border-[#2A2A2E] md:pl-6 rtl:md:border-l-0 rtl:md:border-r rtl:md:pl-0 rtl:md:pr-6">
            <div className="text-[52px] font-bold text-[#3F4064] dark:text-[#E5E5EA] leading-none mb-2">
              {stats.average.toFixed(1)}
            </div>
            <div className="flex items-center justify-center md:justify-start mb-2">
              <RatingStars rating={stats.average} size={16} />
            </div>
            <div className="text-[11px] text-[#A1A3A8]">
              {t.from} {stats.total.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
              {t.reviews}
            </div>
          </div>

          {/* Breakdown */}
          <div className="md:col-span-2 space-y-2">
            {[5, 4, 3, 2, 1].map((star, idx) => {
              const count = stats.breakdown[idx];
              const percent = stats.total > 0 ? (count / stats.total) * 100 : 0;
              return (
                <button
                  key={star}
                  onClick={() =>
                    setFilter(filter === star ? "all" : (star as FilterOption))
                  }
                  className={`w-full flex items-center gap-3 group transition-opacity ${
                    filter !== "all" && filter !== star
                      ? "opacity-40"
                      : "opacity-100"
                  }`}
                >
                  <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] w-10 flex items-center gap-1 shrink-0">
                    {isFa ? star.toLocaleString("fa-IR") : star}
                    <Star size={11} className="fill-[#F9A825] text-[#F9A825]" />
                  </span>
                  <div className="flex-1 h-2 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-full overflow-hidden">
                    <div
                      className="h-full bg-[#F9A825] rounded-full transition-all duration-500"
                      style={{ width: `${percent}%` }}
                    />
                  </div>
                  <span className="text-[11px] text-[#A1A3A8] w-14 text-left tabular-nums">
                    {count.toLocaleString(isFa ? "fa-IR" : "en-US")}{" "}
                    ({percent.toFixed(0)}%)
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Write review button */}
        {!showForm && (
          <div className="mt-5 pt-5 border-t border-[#E0E0E2] dark:border-[#2A2A2E] flex justify-center">
            <button
              onClick={() => setShowForm(true)}
              className="h-11 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] transition-colors flex items-center gap-2"
            >
              <PenLine size={16} />
              {t.writeReview}
            </button>
          </div>
        )}
      </div>

      {/* Write form */}
      {showForm && (
        <ReviewForm
          productId={productId}
          locale={locale}
          onCancel={() => setShowForm(false)}
        />
      )}

      {/* Reviews list */}
      {stats.total > 0 && (
        <>
          {/* Toolbar */}
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-3 flex items-center justify-between gap-3 flex-wrap">
            <div className="flex items-center gap-2">
              <SlidersHorizontal size={14} className="text-[#A1A3A8]" />
              <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                {t.filter}
              </span>
              <div className="flex items-center gap-1 flex-wrap">
                <button
                  onClick={() => setFilter("all")}
                  className={`text-[11px] px-2.5 py-1 rounded-lg transition-colors ${
                    filter === "all"
                      ? "bg-[#EF4056] text-white"
                      : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8]"
                  }`}
                >
                  {t.all}
                </button>
                {[5, 4, 3, 2, 1].map((star) => (
                  <button
                    key={star}
                    onClick={() => setFilter(star as FilterOption)}
                    className={`text-[11px] px-2.5 py-1 rounded-lg transition-colors flex items-center gap-1 ${
                      filter === star
                        ? "bg-[#EF4056] text-white"
                        : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8]"
                    }`}
                  >
                    {isFa ? star.toLocaleString("fa-IR") : star}
                    <Star size={10} className="fill-current" />
                  </button>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                {t.sortBy}
              </span>
              <select
                value={sort}
                onChange={(e) => setSort(e.target.value as SortOption)}
                className="h-8 px-2 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] bg-white dark:bg-[#1A1A1E] focus:outline-none focus:border-[#EF4056]"
              >
                <option value="newest">{t.newest}</option>
                <option value="helpful">{t.helpful}</option>
                <option value="highest">{t.highest}</option>
                <option value="lowest">{t.lowest}</option>
              </select>
            </div>
          </div>

          {/* Reviews */}
          {filteredReviews.length === 0 ? (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center">
              <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8]">
                {isFa
                  ? "نظری با این فیلتر پیدا نشد"
                  : "No reviews match this filter"}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {displayedReviews.map((review) => (
                <ReviewCard key={review.id} review={review} locale={locale} />
              ))}

              {!showAll && filteredReviews.length > 4 && (
                <button
                  onClick={() => setShowAll(true)}
                  className="w-full h-11 rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] bg-white dark:bg-[#1A1A1E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center justify-center gap-2"
                >
                  {t.showMore} (
                  {(filteredReviews.length - 4).toLocaleString(
                    isFa ? "fa-IR" : "en-US"
                  )}
                  )
                  <ChevronDown size={14} />
                </button>
              )}
            </div>
          )}
        </>
      )}

      {/* No reviews */}
      {mounted && stats.total === 0 && !showForm && (
        <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center">
          <div className="w-14 h-14 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
            <PenLine size={24} className="text-[#A1A3A8]" />
          </div>
          <h3 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {t.noReviews}
          </h3>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.beFirst}
          </p>
        </div>
      )}
    </div>
  );
}
