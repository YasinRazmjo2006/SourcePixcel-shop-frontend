"use client";

import { useState } from "react";
import { Star, Send, X, CheckCircle2 } from "lucide-react";
import type { Locale, ReviewDraft } from "@/lib/types";
import { useReviewsStore, useToastStore } from "@/lib/stores";

interface ReviewFormProps {
  productId: number;
  locale: Locale;
  onCancel?: () => void;
}

export default function ReviewForm({
  productId,
  locale,
  onCancel,
}: ReviewFormProps) {
  const isFa = locale === "fa";
  const addReview = useReviewsStore((s) => s.addReview);
  const pushToast = useToastStore((s) => s.push);

  const [authorName, setAuthorName] = useState("");
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [errors, setErrors] = useState<Record<string, string | undefined>>({});

  const t = {
    title: isFa ? "ثبت نظر" : "Write a Review",
    authorName: isFa ? "نام شما" : "Your Name",
    rating: isFa ? "امتیاز شما" : "Your Rating",
    reviewTitle: isFa ? "عنوان نظر" : "Review Title",
    reviewBody: isFa ? "متن نظر" : "Review Body",
    submit: isFa ? "ثبت نظر" : "Submit Review",
    cancel: isFa ? "انصراف" : "Cancel",
    required: isFa ? "الزامی" : "Required",
    selectRating: isFa ? "لطفاً امتیاز دهید" : "Please select a rating",
    success: isFa ? "نظر شما ثبت شد" : "Review submitted",
    thanks: isFa ? "ممنون از بازخورد شما" : "Thanks for your feedback",
    namePlaceholder: isFa ? "مثال: علی محمدی" : "e.g. John Doe",
    titlePlaceholder: isFa
      ? "خلاصه‌ای از نظر خود بنویسید"
      : "Summarize your review",
    bodyPlaceholder: isFa
      ? "تجربه خود از این محصول را بنویسید..."
      : "Share your experience with this product...",
  };

  const validate = (): boolean => {
    const e: Record<string, string | undefined> = {};
    if (!authorName.trim()) e.authorName = t.required;
    if (rating === 0) e.rating = t.selectRating;
    if (!title.trim()) e.title = t.required;
    if (!body.trim() || body.trim().length < 10) {
      e.body = isFa
        ? "متن نظر باید حداقل ۱۰ کاراکتر باشد"
        : "Review must be at least 10 characters";
    }
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    const draft: ReviewDraft = {
      productId,
      authorName,
      rating,
      title,
      body,
    };

    addReview(draft);
    pushToast({
      type: "success",
      titleFa: t.success,
      titleEn: t.success,
      messageFa: t.thanks,
      messageEn: t.thanks,
    });

    // Reset
    setAuthorName("");
    setRating(0);
    setTitle("");
    setBody("");
    setErrors({});
    onCancel?.();
  };

  const inputClass = (field: string) =>
    `w-full h-10 px-3 rounded-lg border text-[13px] text-[#3F4064] dark:text-[#E5E5EA] bg-white dark:bg-[#1A1A1E] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] dark:border-[#2A2A2E] focus:border-[#EF4056]"
    }`;

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-[#FAFAFA] dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-5"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {t.title}
        </h3>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#E0E0E2] dark:hover:bg-[#2A2A2E] transition-colors"
          >
            <X size={16} />
          </button>
        )}
      </div>

      <div className="space-y-4">
        {/* Name */}
        <div>
          <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.authorName} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={authorName}
            onChange={(e) => {
              setAuthorName(e.target.value);
              setErrors((p) => ({ ...p, authorName: undefined }));
            }}
            placeholder={t.namePlaceholder}
            className={inputClass("authorName")}
          />
          {errors.authorName && (
            <p className="text-[11px] text-[#EF4444] mt-1">
              {errors.authorName}
            </p>
          )}
        </div>

        {/* Rating */}
        <div>
          <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.rating} <span className="text-[#EF4056]">*</span>
          </label>
          <div className="flex items-center gap-1">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => {
                  setRating(star);
                  setErrors((p) => ({ ...p, rating: undefined }));
                }}
                onMouseEnter={() => setHoverRating(star)}
                onMouseLeave={() => setHoverRating(0)}
                className="transition-transform hover:scale-110"
                aria-label={`Rating ${star}`}
              >
                <Star
                  size={28}
                  className={
                    star <= (hoverRating || rating)
                      ? "fill-[#F9A825] text-[#F9A825]"
                      : "text-[#E0E0E2] dark:text-[#3A3A40]"
                  }
                />
              </button>
            ))}
            {rating > 0 && (
              <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] mr-2">
                {rating} / 5
              </span>
            )}
          </div>
          {errors.rating && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.rating}</p>
          )}
        </div>

        {/* Title */}
        <div>
          <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.reviewTitle} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value);
              setErrors((p) => ({ ...p, title: undefined }));
            }}
            placeholder={t.titlePlaceholder}
            maxLength={80}
            className={inputClass("title")}
          />
          <div className="flex items-center justify-between mt-1">
            {errors.title ? (
              <p className="text-[11px] text-[#EF4444]">{errors.title}</p>
            ) : (
              <span />
            )}
            <span className="text-[10px] text-[#A1A3A8]">
              {title.length}/80
            </span>
          </div>
        </div>

        {/* Body */}
        <div>
          <label className="block text-[12px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.reviewBody} <span className="text-[#EF4056]">*</span>
          </label>
          <textarea
            value={body}
            onChange={(e) => {
              setBody(e.target.value);
              setErrors((p) => ({ ...p, body: undefined }));
            }}
            placeholder={t.bodyPlaceholder}
            rows={5}
            maxLength={1000}
            className={`w-full px-3 py-2 rounded-lg border text-[13px] text-[#3F4064] dark:text-[#E5E5EA] bg-white dark:bg-[#1A1A1E] placeholder:text-[#A1A3A8] focus:outline-none transition-colors resize-none ${
              errors.body
                ? "border-[#EF4444] focus:border-[#EF4444]"
                : "border-[#E0E0E2] dark:border-[#2A2A2E] focus:border-[#EF4056]"
            }`}
          />
          <div className="flex items-center justify-between mt-1">
            {errors.body ? (
              <p className="text-[11px] text-[#EF4444]">{errors.body}</p>
            ) : (
              <span />
            )}
            <span className="text-[10px] text-[#A1A3A8]">
              {body.length}/1000
            </span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-end gap-3 mt-5 pt-4 border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="h-10 px-5 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
          >
            {t.cancel}
          </button>
        )}
        <button
          type="submit"
          className="h-10 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Send size={15} />
          {t.submit}
        </button>
      </div>
    </form>
  );
}
