// lib/types/product.ts

// ─── Subcategory ──────────────────────────────────────────────────────────────
export interface Subcategory {
  id: string;
  nameFa: string;
  nameEn: string;
}

// ─── Category ─────────────────────────────────────────────────────────────────
export interface Category {
  id: string;
  nameFa: string;
  nameEn: string;
  slug: string;
  icon: string;
  subcategories: Subcategory[];
}

// ─── Brand ────────────────────────────────────────────────────────────────────
export interface Brand {
  id: string;
  nameFa: string;
  nameEn: string;
  categories: string[];
}

// ─── Product ──────────────────────────────────────────────────────────────────
export interface Product {
  id: number;
  slug: string;
  titleFa: string;
  titleEn: string;
  brand: string;
  category: string;
  subcategory: string;
  price: number;
  discountPercent: number;
  finalPrice: number;
  rating: number;
  reviewCount: number;
  image: string;
  inStock: boolean;
  tags: string[];
  isNew?: boolean;
  isFeatured?: boolean;
}

// ─── Cart Item ────────────────────────────────────────────────────────────────
export interface CartItem {
  productId: number;
  quantity: number;
}

// ─── Wishlist Item ────────────────────────────────────────────────────────────
export interface WishlistItem {
  productId: number;
  addedAt: number;
}

// ─── Compare Item ─────────────────────────────────────────────────────────────
export interface CompareItem {
  productId: number;
  addedAt: number;
}

// ─── Filter State ─────────────────────────────────────────────────────────────
export interface FilterState {
  category?: string;
  brands: string[];
  minPrice: number;
  maxPrice: number;
  inStockOnly: boolean;
  discountedOnly: boolean;
  minRating: number;
}

// ─── Sort Option ──────────────────────────────────────────────────────────────
export type SortOption =
  | "popular"
  | "newest"
  | "price-asc"
  | "price-desc"
  | "rating";

// ─── Locale ───────────────────────────────────────────────────────────────────
export type Locale = "fa" | "en";
