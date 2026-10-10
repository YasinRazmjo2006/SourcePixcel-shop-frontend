"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
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
  GitCompareArrows,
  Search,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore, useWishlistStore, useCompareStore } from "@/lib/stores";
import ThemeToggle from "@/components/common/ThemeToggle";
import { SearchAutocomplete } from "@/components/search";
import { NotificationBell } from "@/components/notifications";

const ICON_MAP: Record<
  string,
  React.ComponentType<{
    size?: number;
    className?: string;
    "aria-hidden"?: boolean | "true" | "false";
  }>
> = {
  Smartphone, Laptop, Tablet, Headphones, Camera, Watch,
  Gamepad2, Cable, Shirt, Footprints, Home, BookOpen,
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
  const compareCount = useCompareStore((s) => s.ids.length);

  useEffect(() => { setMounted(true); }, []);
  useEffect(() => {
    setMobileOpen(false);
    setOpenCategory(null);
  }, [pathname]);

  // Close mobile menu on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMobileOpen(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
    search: isFa ? "جستجو" : "Search",
    menu: isFa ? "منو" : "Menu",
    closeMenu: isFa ? "بستن منو" : "Close menu",
    cartItems: isFa ? "کالا در سبد" : "items in cart",
    wishlistItems: isFa ? "کالا در علاقه‌مندی" : "items in wishlist",
    compareItems: isFa ? "کالا در مقایسه" : "items in compare",
    notifications: isFa ? "اعلان‌ها" : "Notifications",
  };

  const swapLocale = (newLocale: Locale) => {
    const rest = pathname.replace(/^\/(fa|en)/, "");
    return `/${newLocale}${rest}`;
  };

  return (
    <>
      {/* Top thin bar */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="max-w-[1400px] mx-auto px-4 h-10 flex items-center justify-between text-[12px]">
          <div className="flex items-center gap-4">
            <Link
              href={swapLocale(isFa ? "en" : "fa")}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
              aria-label={isFa ? "Switch to English" : "تغییر به فارسی"}
            >
              {isFa ? "English" : "فارسی"}
            </Link>
            <ThemeToggle locale={locale} />
          </div>
          <div className="flex items-center gap-4">
            <Link
              href={`/${locale}/auth/login`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors"
            >
              {t.login}
            </Link>
            <span className="text-[#E0E0E2] dark:text-[#2A2A2E]" aria-hidden="true">
              |
            </span>
            <NotificationBell locale={locale} variant="top" />
            <Link
              href={`/${locale}/compare`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
              aria-label={`${t.compareItems}: ${compareCount}`}
            >
              <GitCompareArrows size={14} aria-hidden="true" />
              {mounted && compareCount > 0 && (
                <span
                  className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center"
                  aria-hidden="true"
                >
                  {compareCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/account/wishlist`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
              aria-label={`${t.wishlistItems}: ${wishlistCount}`}
            >
              <Heart size={14} aria-hidden="true" />
              {mounted && wishlistCount > 0 && (
                <span
                  className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center"
                  aria-hidden="true"
                >
                  {wishlistCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/cart`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
              aria-label={`${t.cartItems}: ${totalItems}`}
            >
              <ShoppingCart size={14} aria-hidden="true" />
              {mounted && totalItems > 0 && (
                <span
                  className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center"
                  aria-hidden="true"
                >
                  {totalItems}
                </span>
              )}
            </Link>
          </div>
        </div>
      </div>

      {/* Main header */}
      <header className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          <button
            className="lg:hidden text-[#3F4064] dark:text-[#E5E5EA]"
            onClick={() => setMobileOpen(true)}
            aria-label={t.menu}
            aria-expanded={mobileOpen}
            aria-controls="mobile-menu"
          >
            <Menu size={24} aria-hidden="true" />
          </button>

          <Link
            href={`/${locale}`}
            className="text-[#EF4056] font-bold text-xl shrink-0"
            aria-label="SourcePixcel — Home"
          >
            SourcePixcel
          </Link>

          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <SearchAutocomplete locale={locale} />
          </div>

          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} aria-hidden="true" />
            <span>{t.account}</span>
          </Link>

          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2] dark:bg-[#2A2A2E]" aria-hidden="true" />

          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors relative"
            aria-label={`${t.cart}: ${totalItems} ${t.cartItems}`}
          >
            <ShoppingCart size={20} aria-hidden="true" />
            <span>{t.cart}</span>
            {mounted && totalItems > 0 && (
              <span className="bg-[#EF4056] text-white text-[10px] rounded-full w-5 h-5 flex items-center justify-center font-bold" aria-hidden="true">
                {totalItems}
              </span>
            )}
          </Link>
        </div>

        {/* Mega menu */}
        <nav
          className="hidden lg:block border-t border-[#E0E0E2] dark:border-[#2A2A2E]"
          aria-label={isFa ? "منوی اصلی" : "Main navigation"}
        >
          <div className="max-w-[1400px] mx-auto px-4">
            <ul className="flex items-center gap-1 h-12 list-none m-0 p-0">
              {categories.map((cat) => {
                const Icon = ICON_MAP[cat.icon] ?? Cable;
                const isOpen = openCategory === cat.id;
                return (
                  <li
                    key={cat.id}
                    className="relative"
                    onMouseEnter={() => setOpenCategory(cat.id)}
                    onMouseLeave={() => setOpenCategory(null)}
                  >
                    <Link
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                      aria-haspopup={cat.subcategories.length > 0}
                      aria-expanded={isOpen}
                    >
                      <Icon size={16} aria-hidden="true" />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      {cat.subcategories.length > 0 && (
                        <ChevronDown size={12} className="opacity-50" aria-hidden="true" />
                      )}
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        <ul className="list-none m-0 p-0">
                          {cat.subcategories.map((sub) => (
                            <li key={sub.id}>
                              <Link
                                href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                                className="block px-4 py-2 text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
                              >
                                {isFa ? sub.nameFa : sub.nameEn}
                              </Link>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        </nav>
      </header>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-[100] lg:hidden"
          role="dialog"
          aria-modal="true"
          aria-label={t.menu}
          id="mobile-menu"
        >
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
            aria-hidden="true"
          />
          <div
            className="absolute top-0 bottom-0 bg-white dark:bg-[#1A1A1E] w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button
                onClick={() => setMobileOpen(false)}
                aria-label={t.closeMenu}
              >
                <X size={24} className="text-[#3F4064] dark:text-[#E5E5EA]" aria-hidden="true" />
              </button>
            </div>

            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <span className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
                  {isFa ? "حالت تاریک" : "Dark mode"}
                </span>
                <ThemeToggle locale={locale} />
              </div>

              <div className="mb-4">
                <SearchAutocomplete locale={locale} onClose={() => setMobileOpen(false)} />
              </div>

              <div className="mb-4">
                <Link
                  href={`/${locale}/auth/login`}
                  className="block text-center bg-[#EF4056] text-white rounded-lg py-2 text-sm font-medium"
                >
                  {t.login}
                </Link>
              </div>

              <nav className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] pt-4" aria-label={t.allCategories}>
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                <ul className="list-none m-0 p-0">
                  {categories.map((cat) => {
                    const Icon = ICON_MAP[cat.icon] ?? Cable;
                    return (
                      <li key={cat.id}>
                        <Link
                          href={`/${locale}/category/${cat.slug}`}
                          className="flex items-center gap-3 py-2 text-sm text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056]"
                        >
                          <Icon size={18} aria-hidden="true" />
                          <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </nav>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
