# 05_header.py
# ساخت هدر Digikala-style
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/stores/cart.ts (Zustand store - needed by Header badge)
# ============================================================
files.append(("lib/stores/cart.ts", """// lib/stores/cart.ts
"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product } from "@/lib/types";

export interface CartLine {
  productId: number;
  quantity: number;
}

interface CartState {
  items: CartLine[];
  addItem: (productId: number, quantity?: number) => void;
  removeItem: (productId: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clear: () => void;
  getQuantity: (productId: number) => number;
  getTotalItems: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (productId, quantity = 1) => {
        set((state) => {
          const existing = state.items.find((i) => i.productId === productId);
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.productId === productId
                  ? { ...i, quantity: i.quantity + quantity }
                  : i
              ),
            };
          }
          return { items: [...state.items, { productId, quantity }] };
        });
      },

      removeItem: (productId) => {
        set((state) => ({
          items: state.items.filter((i) => i.productId !== productId),
        }));
      },

      updateQuantity: (productId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(productId);
          return;
        }
        set((state) => ({
          items: state.items.map((i) =>
            i.productId === productId ? { ...i, quantity } : i
          ),
        }));
      },

      clear: () => set({ items: [] }),

      getQuantity: (productId) => {
        const item = get().items.find((i) => i.productId === productId);
        return item?.quantity ?? 0;
      },

      getTotalItems: () => {
        return get().items.reduce((sum, i) => sum + i.quantity, 0);
      },
    }),
    { name: "sourcepixcel-cart" }
  )
);
"""))

# ============================================================
# lib/stores/wishlist.ts
# ============================================================
files.append(("lib/stores/wishlist.ts", """// lib/stores/wishlist.ts
"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface WishlistState {
  ids: number[];
  toggle: (productId: number) => void;
  has: (productId: number) => boolean;
  remove: (productId: number) => void;
  clear: () => void;
}

export const useWishlistStore = create<WishlistState>()(
  persist(
    (set, get) => ({
      ids: [],

      toggle: (productId) => {
        set((state) => ({
          ids: state.ids.includes(productId)
            ? state.ids.filter((id) => id !== productId)
            : [...state.ids, productId],
        }));
      },

      has: (productId) => get().ids.includes(productId),

      remove: (productId) => {
        set((state) => ({ ids: state.ids.filter((id) => id !== productId) }));
      },

      clear: () => set({ ids: [] }),
    }),
    { name: "sourcepixcel-wishlist" }
  )
);
"""))

# ============================================================
# lib/stores/index.ts
# ============================================================
files.append(("lib/stores/index.ts", """// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
"""))

# ============================================================
# components/layout/Header.tsx
# ============================================================
files.append(("components/layout/Header.tsx", """"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Search,
  ShoppingCart,
  Heart,
  User,
  Menu,
  X,
  ChevronDown,
  Smartphone,
  Laptop,
  Tablet,
  Headphones,
  Camera,
  Watch,
  Gamepad2,
  Cable,
  Shirt,
  Footprints,
  Home,
  BookOpen,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore } from "@/lib/stores";
import { useWishlistStore } from "@/lib/stores";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
  Smartphone,
  Laptop,
  Tablet,
  Headphones,
  Camera,
  Watch,
  Gamepad2,
  Cable,
  Shirt,
  Footprints,
  Home,
  BookOpen,
};

interface HeaderProps {
  locale: Locale;
}

export default function Header({ locale }: HeaderProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openCategory, setOpenCategory] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  const totalItems = useCartStore((s) => s.items.reduce((sum, i) => sum + i.quantity, 0));
  const wishlistCount = useWishlistStore((s) => s.ids.length);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    setMobileOpen(false);
    setOpenCategory(null);
  }, [pathname]);

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    searchPlaceholder: isFa ? "جستجو در SourcePixcel" : "Search in SourcePixcel",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    wishlist: isFa ? "علاقه‌مندی‌ها" : "Wishlist",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
  };

  const swapLocale = (newLocale: Locale) => {
    if (typeof window === "undefined") return;
    const rest = pathname.replace(/^\\/(fa|en)/, "");
    return `/${newLocale}${rest}`;
  };

  return (
    <>
      {/* ── Top thin bar ─────────────────────────────────────────────── */}
      <div className="bg-white border-b border-[#E0E0E2]">
        <div className="max-w-[1400px] mx-auto px-4 h-10 flex items-center justify-between text-[12px]">
          <div className="flex items-center gap-4">
            <Link
              href={swapLocale(isFa ? "en" : "fa")}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors"
            >
              {isFa ? "English" : "فارسی"}
            </Link>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href={`/${locale}/auth/login`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors"
            >
              {t.login}
            </Link>
            <span className="text-[#E0E0E2]">|</span>
            <Link
              href={`/${locale}/wishlist`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <Heart size={14} />
              {mounted && wishlistCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {wishlistCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/cart`}
              className="text-[#62666D] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <ShoppingCart size={14} />
              {mounted && totalItems > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* ── Main header row ──────────────────────────────────────────── */}
      <div className="bg-white border-b border-[#E0E0E2] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          {/* Mobile menu button */}
          <button
            className="lg:hidden text-[#3F4064]"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>

          {/* Logo */}
          <Link
            href={`/${locale}`}
            className="text-[#EF4056] font-bold text-xl shrink-0"
          >
            SourcePixcel
          </Link>

          {/* Search bar */}
          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <div className="relative">
              <input
                type="text"
                placeholder={t.searchPlaceholder}
                className="w-full h-10 pr-10 pl-4 rounded-lg bg-[#F5F5F5] border border-[#E0E0E2] text-sm text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] transition-colors"
                style={{ paddingRight: isFa ? 40 : 16, paddingLeft: isFa ? 16 : 40 }}
              />
              <Search
                size={18}
                className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
                style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
              />
            </div>
          </div>

          {/* Account */}
          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} />
            <span>{t.account}</span>
          </Link>

          {/* Divider */}
          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2]" />

          {/* Cart button */}
          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] text-sm hover:text-[#EF4056] transition-colors relative"
          >
            <ShoppingCart size={20} />
            <span>{t.cart}</span>
            {mounted && totalItems > 0 && (
              <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* ── Mega menu bar ──────────────────────────────────────────── */}
        <div className="hidden lg:block border-t border-[#E0E0E2]">
          <div className="max-w-[1400px] mx-auto px-4">
            <nav className="flex items-center gap-1 h-12">
              {categories.map((cat) => {
                const Icon = ICON_MAP[cat.icon] ?? Cable;
                const isOpen = openCategory === cat.id;
                return (
                  <div
                    key={cat.id}
                    className="relative"
                    onMouseEnter={() => setOpenCategory(cat.id)}
                    onMouseLeave={() => setOpenCategory(null)}
                  >
                    <Link
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                    >
                      <Icon size={16} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      <ChevronDown size={12} className="opacity-50" />
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white border border-[#E0E0E2] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        {cat.subcategories.map((sub) => (
                          <Link
                            key={sub.id}
                            href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                            className="block px-4 py-2 text-[13px] text-[#62666D] hover:bg-[#F5F5F5] hover:text-[#EF4056] transition-colors"
                          >
                            {isFa ? sub.nameFa : sub.nameEn}
                          </Link>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </nav>
          </div>
        </div>
      </div>

      {/* ── Mobile drawer ─────────────────────────────────────────────── */}
      {mobileOpen && (
        <div className="fixed inset-0 z-[100] lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
          />
          <div
            className="absolute top-0 bottom-0 bg-white w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button
                onClick={() => setMobileOpen(false)}
                aria-label="Close menu"
                className="text-[#3F4064]"
              >
                <X size={24} />
              </button>
            </div>

            <div className="p-4">
              <div className="relative mb-4">
                <input
                  type="text"
                  placeholder={t.searchPlaceholder}
                  className="w-full h-10 px-4 rounded-lg bg-[#F5F5F5] border border-[#E0E0E2] text-sm"
                />
              </div>

              <div className="mb-4">
                <Link
                  href={`/${locale}/auth/login`}
                  className="block text-center bg-[#EF4056] text-white rounded-lg py-2 text-sm font-medium"
                >
                  {t.login}
                </Link>
              </div>

              <div className="border-t border-[#E0E0E2] pt-4">
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                {categories.map((cat) => {
                  const Icon = ICON_MAP[cat.icon] ?? Cable;
                  return (
                    <Link
                      key={cat.id}
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-3 py-2 text-sm text-[#3F4064] hover:text-[#EF4056]"
                    >
                      <Icon size={18} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
"""))

# ============================================================
# app/[locale]/layout.tsx (updated to use Header)
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import type { Locale } from "@/lib/types";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const isFa = locale === "fa";
  const dir = isFa ? "rtl" : "ltr";

  return (
    <div
      dir={dir}
      lang={locale}
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      <Header locale={locale as Locale} />

      <main style={{ flex: 1 }}>{children}</main>

      <footer
        style={{
          background: "#FFFFFF",
          borderTop: "1px solid #E0E0E2",
          padding: "24px",
          textAlign: "center",
          color: "#62666D",
          fontSize: 13,
        }}
      >
        © {new Date().getFullYear()} SourcePixcel —{" "}
        {isFa ? "تمامی حقوق محفوظ است." : "All rights reserved."}
      </footer>
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 05: Header")
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
        print("\nIMPORTANT: We added zustand. Install it with:")
        print("  npm install zustand --registry=https://mirror-npm.runflare.com")
        print("\nThen run: npm run dev")
        print("Next: run 06_footer.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()