"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronLeft, ChevronRight, Home } from "lucide-react";

interface AdminBreadcrumbProps {
  locale: string;
}

const SEGMENT_LABELS: Record<string, { fa: string; en: string }> = {
  admin: { fa: "پنل مدیریت", en: "Admin" },
  analytics: { fa: "آنالیتیکس", en: "Analytics" },
  products: { fa: "محصولات", en: "Products" },
  categories: { fa: "دسته‌بندی‌ها", en: "Categories" },
  orders: { fa: "سفارشات", en: "Orders" },
  users: { fa: "کاربران", en: "Users" },
  discounts: { fa: "تخفیف‌ها", en: "Discounts" },
  reviews: { fa: "نظرات", en: "Reviews" },
  reports: { fa: "گزارشات", en: "Reports" },
  settings: { fa: "تنظیمات", en: "Settings" },
  new: { fa: "جدید", en: "New" },
  edit: { fa: "ویرایش", en: "Edit" },
};

export default function AdminBreadcrumb({ locale }: AdminBreadcrumbProps) {
  const isFa = locale === "fa";
  const pathname = usePathname();

  // Split pathname and remove locale
  const segments = pathname
    .split("/")
    .filter(Boolean)
    .filter((s) => s !== locale);

  const breadcrumbs = segments.map((segment, idx) => {
    const href = "/" + segments.slice(0, idx + 1).join("/");
    const label = SEGMENT_LABELS[segment];
    const isLast = idx === segments.length - 1;

    // Skip numeric segments (IDs) — replace with generic label
    const isNumeric = /^\d+$/.test(segment) || segment.startsWith("SP-");

    return {
      href: `/${locale}${href}`,
      labelFa: isNumeric ? `#${segment}` : (label?.fa ?? segment),
      labelEn: isNumeric ? `#${segment}` : (label?.en ?? segment),
      isLast,
    };
  });

  if (breadcrumbs.length === 0) return null;

  return (
    <nav
      aria-label="Breadcrumb"
      className="flex items-center gap-1.5 text-[12px] text-[#62666D] dark:text-[#A1A3A8] flex-wrap"
    >
      <Link
        href={`/${locale}/admin`}
        className="flex items-center gap-1 hover:text-[#EF4056] transition-colors"
      >
        <Home size={12} />
        <span>{isFa ? "پنل" : "Admin"}</span>
      </Link>

      {breadcrumbs.slice(1).map((crumb, i) => (
        <div key={i} className="flex items-center gap-1.5">
          {isFa ? (
            <ChevronLeft size={12} className="text-[#A1A3A8]" />
          ) : (
            <ChevronRight size={12} className="text-[#A1A3A8]" />
          )}
          {crumb.isLast ? (
            <span className="font-medium text-[#3F4064] dark:text-[#E5E5EA]">
              {isFa ? crumb.labelFa : crumb.labelEn}
            </span>
          ) : (
            <Link
              href={crumb.href}
              className="hover:text-[#EF4056] transition-colors"
            >
              {isFa ? crumb.labelFa : crumb.labelEn}
            </Link>
          )}
        </div>
      ))}
    </nav>
  );
}
