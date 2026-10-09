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
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import { useCartStore, useWishlistStore, useCompareStore } from "@/lib/stores";
import ThemeToggle from "@/components/common/ThemeToggle";
import { SearchAutocomplete } from "@/components/search";
import { NotificationBell } from "@/components/notifications";

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string }>> = {
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

  const t = {
    login: isFa ? "ورود | ثبت‌نام" : "Login | Register",
    cart: isFa ? "سبد خرید" : "Cart",
    account: isFa ? "حساب من" : "My Account",
    allCategories: isFa ? "دسته‌بندی‌ها" : "Categories",
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
            <span className="text-[#E0E0E2] dark:text-[#2A2A2E]">|</span>
            <NotificationBell locale={locale} variant="top" />
            <Link
              href={`/${locale}/compare`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
            >
              <GitCompareArrows size={14} />
              {mounted && compareCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-[#EF4056] text-white text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {compareCount}
                </span>
              )}
            </Link>
            <Link
              href={`/${locale}/account/wishlist`}
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
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
              className="text-[#62666D] dark:text-[#A1A3A8] hover:text-[#EF4056] transition-colors flex items-center gap-1 relative"
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

      {/* Main header */}
      <div className="bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] sticky top-0 z-50">
        <div className="max-w-[1400px] mx-auto px-4 h-16 flex items-center gap-4">
          <button
            className="lg:hidden text-[#3F4064] dark:text-[#E5E5EA]"
            onClick={() => setMobileOpen(true)}
            aria-label="Open menu"
          >
            <Menu size={24} />
          </button>

          <Link href={`/${locale}`} className="text-[#EF4056] font-bold text-xl shrink-0">
            SourcePixcel
          </Link>

          <div className="flex-1 max-w-2xl mx-auto hidden md:block">
            <SearchAutocomplete locale={locale} />
          </div>

          <Link
            href={`/${locale}/account`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors"
          >
            <User size={20} />
            <span>{t.account}</span>
          </Link>

          <div className="hidden lg:block w-px h-6 bg-[#E0E0E2] dark:bg-[#2A2A2E]" />

          <Link
            href={`/${locale}/cart`}
            className="hidden lg:flex items-center gap-2 text-[#3F4064] dark:text-[#E5E5EA] text-sm hover:text-[#EF4056] transition-colors relative"
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

        {/* Mega menu */}
        <div className="hidden lg:block border-t border-[#E0E0E2] dark:border-[#2A2A2E]">
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
                      className="flex items-center gap-2 px-3 py-2 text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056] transition-colors whitespace-nowrap"
                    >
                      <Icon size={16} />
                      <span>{isFa ? cat.nameFa : cat.nameEn}</span>
                      <ChevronDown size={12} className="opacity-50" />
                    </Link>

                    {isOpen && cat.subcategories.length > 0 && (
                      <div className="absolute top-full right-0 bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-lg shadow-lg py-2 min-w-[200px] z-50">
                        {cat.subcategories.map((sub) => (
                          <Link
                            key={sub.id}
                            href={`/${locale}/category/${cat.slug}?sub=${sub.id}`}
                            className="block px-4 py-2 text-[13px] text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] hover:text-[#EF4056] transition-colors"
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

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-[100] lg:hidden">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setMobileOpen(false)}
          />
          <div
            className="absolute top-0 bottom-0 bg-white dark:bg-[#1A1A1E] w-80 max-w-[85%] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 } as React.CSSProperties}
          >
            <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <span className="text-[#EF4056] font-bold text-lg">SourcePixcel</span>
              <button onClick={() => setMobileOpen(false)} aria-label="Close menu">
                <X size={24} className="text-[#3F4064] dark:text-[#E5E5EA]" />
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

              <div className="border-t border-[#E0E0E2] dark:border-[#2A2A2E] pt-4">
                <div className="text-xs font-bold text-[#A1A3A8] mb-2">
                  {t.allCategories}
                </div>
                {categories.map((cat) => {
                  const Icon = ICON_MAP[cat.icon] ?? Cable;
                  return (
                    <Link
                      key={cat.id}
                      href={`/${locale}/category/${cat.slug}`}
                      className="flex items-center gap-3 py-2 text-sm text-[#3F4064] dark:text-[#E5E5EA] hover:text-[#EF4056]"
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
