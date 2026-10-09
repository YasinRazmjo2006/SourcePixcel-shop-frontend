// lib/types/review.ts
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
