# 23_reviews.py
# سیستم نظرات و امتیاز
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/types/review.ts
# ============================================================
files.append(("lib/types/review.ts", """// lib/types/review.ts
export interface Review {
  id: string;
  productId: number;
  authorName: string;
  authorInitial: string;
  rating: number;
  title: string;
  body: string;
  date: string;
  helpful: number;
  notHelpful: number;
  verified: boolean;
  adminResponse?: {
    body: string;
    date: string;
  };
}

export interface ReviewDraft {
  productId: number;
  authorName: string;
  rating: number;
  title: string;
  body: string;
}
"""))

# ============================================================
# lib/types/index.ts (updated)
# ============================================================
files.append(("lib/types/index.ts", """// lib/types/index.ts
export type {
  Subcategory,
  Category,
  Brand,
  Product,
  CartItem,
  WishlistItem,
  CompareItem,
  FilterState,
  SortOption,
  Locale,
} from "./product";

export type { BlogPost } from "./blog";
export type { Review, ReviewDraft } from "./review";
"""))

# ============================================================
# lib/stores/reviews.ts
# ============================================================
files.append(("lib/stores/reviews.ts", """"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Review, ReviewDraft } from "@/lib/types";

interface ReviewsState {
  userReviews: Review[];
  helpfulVotes: Record<string, "up" | "down">;
  addReview: (draft: ReviewDraft) => void;
  voteHelpful: (reviewId: string, vote: "up" | "down") => void;
  getUserReviews: (productId: number) => Review[];
}

export const useReviewsStore = create<ReviewsState>()(
  persist(
    (set, get) => ({
      userReviews: [],
      helpfulVotes: {},

      addReview: (draft) => {
        const id = `rev-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        const review: Review = {
          id,
          productId: draft.productId,
          authorName: draft.authorName.trim(),
          authorInitial: draft.authorName.trim()[0] || "?",
          rating: draft.rating,
          title: draft.title.trim(),
          body: draft.body.trim(),
          date: new Date().toISOString(),
          helpful: 0,
          notHelpful: 0,
          verified: true,
        };
        set((state) => ({ userReviews: [review, ...state.userReviews] }));
      },

      voteHelpful: (reviewId, vote) => {
        set((state) => ({
          helpfulVotes: { ...state.helpfulVotes, [reviewId]: vote },
        }));
      },

      getUserReviews: (productId) =>
        get().userReviews.filter((r) => r.productId === productId),
    }),
    { name: "sourcepixcel-reviews" }
  )
);
"""))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", """// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
"""))

# ============================================================
# lib/data/mock-reviews.ts
# ============================================================
files.append(("lib/data/mock-reviews.ts", """// lib/data/mock-reviews.ts
import type { Review } from "@/lib/types";

export const mockReviews: Review[] = [
  {
    id: "rev-1",
    productId: 1,
    authorName: "علی محمدی",
    authorInitial: "ع",
    rating: 5,
    title: "کیفیت فوق‌العاده",
    body: "دوربین این گوشی واقعاً بی‌نظیره. توی نور کم هم عکس‌های عالی می‌گیره. باتری هم تا آخر روز دووم میاره. کاملاً راضی هستم و به همه پیشنهاد می‌کنم.",
    date: "1403/06/15",
    helpful: 42,
    notHelpful: 3,
    verified: true,
    adminResponse: {
      body: "ممنون از نظر مثبت شما. خوشحالیم که راضی هستید.",
      date: "1403/06/16",
    },
  },
  {
    id: "rev-2",
    productId: 1,
    authorName: "سارا احمدی",
    authorInitial: "س",
    rating: 4,
    title: "خوب ولی گرون",
    body: "به طور کلی گوشی خوبیه ولی قیمتش یه کم بالاست. طراحی و صفحه‌نمایشش عالیه. فقط ای کاش باتریش کمی قوی‌تر بود.",
    date: "1403/06/08",
    helpful: 28,
    notHelpful: 5,
    verified: true,
  },
  {
    id: "rev-3",
    productId: 1,
    authorName: "رضا کریمی",
    authorInitial: "ر",
    rating: 5,
    title: "ارسال سریع و بسته‌بندی عالی",
    body: "بسته‌بندی خیلی حرفه‌ای بود. گوشی کاملاً سالم و اورجینال رسید. پشتیبانی هم خیلی سریع جواب داد. ممنون SourcePixcel.",
    date: "1403/05/25",
    helpful: 35,
    notHelpful: 1,
    verified: true,
  },
  {
    id: "rev-4",
    productId: 1,
    authorName: "مریم رضایی",
    authorInitial: "م",
    rating: 3,
    title: "متوسط",
    body: "انتظار بیشتری داشتم. دوربین خوبه ولی رابط کاربری یکم پیچیده‌ست. برای این قیمت می‌شد بهتر باشه.",
    date: "1403/05/18",
    helpful: 12,
    notHelpful: 8,
    verified: false,
  },
  {
    id: "rev-5",
    productId: 2,
    authorName: "حسین نوری",
    authorInitial: "ح",
    rating: 5,
    title: "بهترین خریدم",
    body: "iPhone 15 Pro Max واقعاً ارزشش رو داره. دوربین، سرعت، کیفیت ساخت، همه چیز عالیه. هیچ ایرادی نمی‌تونم بگیرم.",
    date: "1403/06/20",
    helpful: 56,
    notHelpful: 2,
    verified: true,
  },
  {
    id: "rev-6",
    productId: 2,
    authorName: "نازنین صادقی",
    authorInitial: "ن",
    rating: 4,
    title: "خوب",
    body: "کیفیت ساخت عالیه. فقط به نظرم نسبت به نسخه قبلی تغییرات زیادی نداشته. ولی در کل راضی هستم.",
    date: "1403/06/05",
    helpful: 18,
    notHelpful: 4,
    verified: true,
  },
];

export const getReviewsByProduct = (productId: number): Review[] => {
  return mockReviews.filter((r) => r.productId === productId);
};

// Generic fallback reviews for products without specific reviews
export const getGenericReviews = (): Review[] => {
  return [
    {
      id: "rev-generic-1",
      productId: 0,
      authorName: "کاربر SourcePixcel",
      authorInitial: "ک",
      rating: 5,
      title: "کیفیت عالی",
      body: "محصول با کیفیت و مطابق توضیحات بود. ارسال سریع انجام شد و بسته‌بندی عالی بود. حتماً دوباره خرید می‌کنم.",
      date: "1403/06/10",
      helpful: 24,
      notHelpful: 2,
      verified: true,
    },
    {
      id: "rev-generic-2",
      productId: 0,
      authorName: "محمد رحیمی",
      authorInitial: "م",
      rating: 4,
      title: "خوب و مقرون به صرفه",
      body: "نسبت به قیمتش کیفیت خوبی داره. فقط کمی زودتر از انتظارم رسید که باعث شد کمی گیج بشم. در کل راضی هستم.",
      date: "1403/06/02",
      helpful: 15,
      notHelpful: 3,
      verified: true,
    },
    {
      id: "rev-generic-3",
      productId: 0,
      authorName: "فاطمه حسینی",
      authorInitial: "ف",
      rating: 5,
      title: "پیشنهاد می‌کنم",
      body: "از خریدم کاملاً راضی هستم. محصول اورجینال و باکیفیت. پشتیبانی SourcePixcel هم عالی بود.",
      date: "1403/05/22",
      helpful: 31,
      notHelpful: 1,
      verified: true,
    },
  ];
};

export const getReviewsForProduct = (productId: number): Review[] => {
  const specific = getReviewsByProduct(productId);
  if (specific.length > 0) return specific;
  // Return generic reviews with adjusted productId
  return getGenericReviews().map((r) => ({ ...r, productId }));
};
"""))

# ============================================================
# lib/data/index.ts (updated)
# ============================================================
files.append(("lib/data/index.ts", """// lib/data/index.ts
export {
  categories,
  brands,
  products,
  getProductBySlug,
  getProductsByCategory,
  getProductsByBrand,
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
  getCategoryById,
  getBrandById,
  getProductsBySubcategory,
} from "./products";

export {
  mockOrders,
  getOrderById,
} from "./mock-orders";
export type { MockOrder, OrderItem } from "./mock-orders";

export {
  blogPosts,
  getBlogPostBySlug,
  getRecentBlogPosts,
  getRelatedBlogPosts,
} from "./mock-blog";
export type { BlogPost } from "./mock-blog";

export {
  mockReviews,
  getReviewsByProduct,
  getGenericReviews,
  getReviewsForProduct,
} from "./mock-reviews";

export { getProductImage } from "./product-images";
"""))

# ============================================================
# components/product/ReviewForm.tsx
# ============================================================
files.append(("components/product/ReviewForm.tsx", """"use client";

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
"""))

# ============================================================
# components/product/ReviewCard.tsx
# ============================================================
files.append(("components/product/ReviewCard.tsx", """"use client";

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
"""))

# ============================================================
# components/product/ReviewsSection.tsx
# ============================================================
files.append(("components/product/ReviewsSection.tsx", """"use client";

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
"""))

# ============================================================
# components/product/index.ts (updated)
# ============================================================
files.append(("components/product/index.ts", """// components/product/index.ts
export { default as ProductCard } from "./ProductCard";
export { default as RatingStars } from "./RatingStars";
export { default as PriceTag } from "./PriceTag";
export { default as ProductFilters } from "./ProductFilters";
export { default as ProductSort } from "./ProductSort";
export { default as ProductGallery } from "./ProductGallery";
export { default as ProductDetail } from "./ProductDetail";
export { default as ProductTabs } from "./ProductTabs";
export { default as QuantitySelector } from "./QuantitySelector";
export { default as RelatedProducts } from "./RelatedProducts";
export { default as CompareButton } from "./CompareButton";
export { default as ReviewForm } from "./ReviewForm";
export { default as ReviewCard } from "./ReviewCard";
export { default as ReviewsSection } from "./ReviewsSection";
export type { FilterValues } from "./ProductFilters";
"""))

# ============================================================
# components/product/ProductTabs.tsx (updated to use ReviewsSection)
# ============================================================
files.append(("components/product/ProductTabs.tsx", """"use client";

import { useState } from "react";
import type { Locale, Product } from "@/lib/types";
import ReviewsSection from "./ReviewsSection";

interface ProductTabsProps {
  product: Product;
  locale: Locale;
}

export default function ProductTabs({ product, locale }: ProductTabsProps) {
  const isFa = locale === "fa";
  const [activeTab, setActiveTab] = useState<"specs" | "description" | "reviews">(
    "specs"
  );

  const tabs = [
    { id: "specs", fa: "مشخصات", en: "Specifications" },
    { id: "description", fa: "توضیحات", en: "Description" },
    { id: "reviews", fa: "نظرات", en: "Reviews" },
  ] as const;

  const specs = [
    { labelFa: "برند", labelEn: "Brand", valueFa: product.brand, valueEn: product.brand },
    { labelFa: "دسته‌بندی", labelEn: "Category", valueFa: product.category, valueEn: product.category },
    { labelFa: "امتیاز", labelEn: "Rating", valueFa: product.rating.toFixed(1), valueEn: product.rating.toFixed(1) },
    { labelFa: "تعداد نظرات", labelEn: "Review count", valueFa: product.reviewCount.toLocaleString("fa-IR"), valueEn: product.reviewCount.toLocaleString("en-US") },
    { labelFa: "وضعیت", labelEn: "Status", valueFa: product.inStock ? "موجود" : "ناموجود", valueEn: product.inStock ? "In stock" : "Out of stock" },
    { labelFa: "کد محصول", labelEn: "SKU", valueFa: `SP-${product.id.toString().padStart(5, "0")}`, valueEn: `SP-${product.id.toString().padStart(5, "0")}` },
  ];

  const description = isFa
    ? `${product.titleFa} یکی از بهترین محصولات موجود در دسته ${product.category} است. این محصول با کیفیت ساخت بالا و طراحی مدرن، تجربه‌ای بی‌نظیر را برای شما فراهم می‌کند. تمامی محصولات SourcePixcel دارای ضمانت اصالت و ۷ روز مهلت بازگشت هستند.`
    : `${product.titleEn} is one of the best products in the ${product.category} category. With high build quality and modern design, it provides an unparalleled experience. All SourcePixcel products come with authenticity guarantee and 7-day return policy.`;

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E]">
      {/* Tab headers */}
      <div className="flex border-b border-[#E0E0E2] dark:border-[#2A2A2E] overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-5 py-3 text-[13px] font-medium whitespace-nowrap transition-colors border-b-2 ${
              activeTab === tab.id
                ? "text-[#EF4056] border-[#EF4056]"
                : "text-[#62666D] dark:text-[#A1A3A8] border-transparent hover:text-[#3F4064] dark:hover:text-[#E5E5EA]"
            }`}
          >
            {isFa ? tab.fa : tab.en}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="p-4 md:p-5">
        {activeTab === "specs" && (
          <div className="space-y-0">
            {specs.map((spec, i) => (
              <div
                key={i}
                className={`flex items-start py-3 gap-4 ${
                  i % 2 === 0
                    ? "bg-[#FAFAFA] dark:bg-[#0F0F12]"
                    : "bg-white dark:bg-[#1A1A1E]"
                } rounded px-3`}
              >
                <span className="text-[12px] text-[#A1A3A8] w-32 shrink-0">
                  {isFa ? spec.labelFa : spec.labelEn}
                </span>
                <span className="text-[13px] text-[#3F4064] dark:text-[#E5E5EA] flex-1">
                  {isFa ? spec.valueFa : spec.valueEn}
                </span>
              </div>
            ))}
          </div>
        )}

        {activeTab === "description" && (
          <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] leading-7 whitespace-pre-line">
            {description}
          </p>
        )}

        {activeTab === "reviews" && (
          <ReviewsSection productId={product.id} locale={locale} />
        )}
      </div>
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 23: Reviews System")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("Now run:")
        print("  Remove-Item -Recurse -Force .next")
        print("  npm run dev")
        print("\nTest: http://localhost:3000/fa/product/samsung-galaxy-s24-ultra")
        print("  → Click the 'Reviews' tab")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()