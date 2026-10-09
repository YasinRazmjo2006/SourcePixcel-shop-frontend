"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Home,
  LayoutGrid,
  ShoppingCart,
  Heart,
  User,
} from "lucide-react";
import type { Locale } from "@/lib/types";
import { useCartStore, useWishlistStore, useAuthStore } from "@/lib/stores";

interface BottomNavProps {
  locale: Locale;
}

export default function BottomNav({ locale }: BottomNavProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();
  const cartCount = useCartStore((s) =>
    s.items.reduce((sum, i) => sum + i.quantity, 0)
  );
  const wishlistCount = useWishlistStore((s) => s.ids.length);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const links = [
    {
      href: `/${locale}`,
      icon: Home,
      fa: "خانه",
      en: "Home",
      exact: true,
    },
    {
      href: `/${locale}/categories`,
      icon: LayoutGrid,
      fa: "دسته‌ها",
      en: "Categories",
    },
    {
      href: `/${locale}/cart`,
      icon: ShoppingCart,
      fa: "سبد",
      en: "Cart",
      badge: cartCount,
    },
    {
      href: `/${locale}/account/wishlist`,
      icon: Heart,
      fa: "علاقه‌مندی",
      en: "Wishlist",
      badge: wishlistCount,
    },
    {
      href: isAuthenticated ? `/${locale}/account` : `/${locale}/auth/login`,
      icon: User,
      fa: "حساب",
      en: "Account",
    },
  ];

  const isActive = (href: string, exact?: boolean) => {
    if (exact) return pathname === href;
    return pathname.startsWith(href);
  };

  return (
    <nav
      className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/95 dark:bg-[#1A1A1E]/95 backdrop-blur-md border-t border-[#E0E0E2] dark:border-[#2A2A2E]"
      style={{ paddingBottom: "env(safe-area-inset-bottom)" }}
    >
      <div className="grid grid-cols-5 h-16">
        {links.map((link) => {
          const Icon = link.icon;
          const active = isActive(link.href, link.exact);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex flex-col items-center justify-center gap-1 transition-colors relative ${
                active
                  ? "text-[#EF4056]"
                  : "text-[#62666D] dark:text-[#A1A3A8]"
              }`}
            >
              <div className="relative">
                <Icon size={22} strokeWidth={active ? 2.4 : 2} />
                {link.badge !== undefined && link.badge > 0 && (
                  <span className="absolute -top-1.5 -right-1.5 bg-[#EF4056] text-white text-[9px] rounded-full min-w-[16px] h-[16px] px-1 flex items-center justify-center font-bold">
                    {link.badge > 99 ? "99+" : link.badge}
                  </span>
                )}
              </div>
              <span
                className={`text-[10px] ${
                  active ? "font-bold" : "font-medium"
                }`}
              >
                {isFa ? link.fa : link.en}
              </span>
              {active && (
                <span className="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-[#EF4056] rounded-full" />
              )}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
