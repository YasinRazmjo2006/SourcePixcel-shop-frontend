# 02_types.py
# ساخت تایپ‌های TypeScript پروژه SourcePixcel
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/types/product.ts
# ============================================================
files.append(("lib/types/product.ts", """// lib/types/product.ts

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
"""))

# ============================================================
# lib/types/index.ts (barrel export)
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
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 02: Types")
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
        print("Next: run 03_data.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()