"use client";

import { ThumbsUp, ThumbsDown, ShieldCheck, MessageSquare } from "lucide-react";
import type { Locale, Review } from "@/lib/types";
import { useReviewsStore } from "@/lib/stores";
import RatingStars from "./RatingStars";

interface ReviewCardProps {
  review: Review;
  locale: Locale;
}

export default function ReviewCard({ review, locale }: ReviewCardProps) {
  const isFa = locale === "fa";
  const voteHelpful = useReviewsStore((s) => s.voteHelpful);
  const helpfulVotes = useReviewsStore((s) => s.helpfulVotes);
  const userVote = helpfulVotes[review.id];

  const handleVote = (vote: "up" | "down") => {
    if (userVote) return;
    voteHelpful(review.id, vote);
  };

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[#EF4056]/10 flex items-center justify-center text-[14px] font-bold text-[#EF4056] shrink-0">
            {review.authorInitial}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {review.authorName}
              </span>
              {review.verified && (
                <span className="text-[10px] text-[#22C55E] flex items-center gap-0.5">
                  <ShieldCheck size={11} />
                  {isFa ? "خرید تاییدشده" : "Verified"}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2 mt-1">
              <RatingStars rating={review.rating} size={11} />
              <span className="text-[10px] text-[#A1A3A8]">
                {review.date}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Title */}
      {review.title && (
        <h4 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
          {review.title}
        </h4>
      )}

      {/* Body */}
      <p className="text-[12px] md:text-[13px] text-[#62666D] dark:text-[#A1A3A8] leading-7 mb-4">
        {review.body}
      </p>

      {/* Admin response */}
      {review.adminResponse && (
        <div className="bg-[#00BFFF]/5 border border-[#00BFFF]/20 rounded-lg p-3 mb-4">
          <div className="flex items-center gap-2 mb-1">
            <MessageSquare size={12} className="text-[#00BFFF]" />
            <span className="text-[11px] font-bold text-[#00BFFF]">
              {isFa ? "پاسخ SourcePixcel" : "SourcePixcel Response"}
            </span>
          </div>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6">
            {review.adminResponse.body}
          </p>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-4 pt-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
        <span className="text-[11px] text-[#A1A3A8]">
          {isFa ? "این نظر برای شما مفید بود؟" : "Was this helpful?"}
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => handleVote("up")}
            disabled={!!userVote}
            className={`flex items-center gap-1.5 text-[11px] px-2.5 py-1 rounded-lg transition-colors ${
              userVote === "up"
                ? "bg-[#22C55E]/10 text-[#22C55E]"
                : userVote === "down"
                ? "text-[#A1A3A8] cursor-not-allowed"
                : "text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
            }`}
          >
            <ThumbsUp size={12} />
            <span>{review.helpful + (userVote === "up" ? 1 : 0)}</span>
          </button>
          <button
            onClick={() => handleVote("down")}
            disabled={!!userVote}
            className={`flex items-center gap-1.5 text-[11px] px-2.5 py-1 rounded-lg transition-colors ${
              userVote === "down"
                ? "bg-[#EF4444]/10 text-[#EF4444]"
                : userVote === "up"
                ? "text-[#A1A3A8] cursor-not-allowed"
                : "text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
            }`}
          >
            <ThumbsDown size={12} />
            <span>{review.notHelpful + (userVote === "down" ? 1 : 0)}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
