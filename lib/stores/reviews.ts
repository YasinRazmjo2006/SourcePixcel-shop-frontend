"use client";

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
