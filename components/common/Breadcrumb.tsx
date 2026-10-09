import Link from "next/link";
import { ChevronLeft, Home } from "lucide-react";
import type { Locale } from "@/lib/types";

interface BreadcrumbItem {
  labelFa: string;
  labelEn: string;
  href?: string;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  locale: Locale;
}

export default function Breadcrumb({ items, locale }: BreadcrumbProps) {
  const safeLocale = (locale || "fa") as string;
  const isFa = safeLocale === "fa";

  return (
    <nav
      aria-label="Breadcrumb"
      className="flex items-center gap-2 text-[12px] text-[#62666D] py-3 flex-wrap"
    >
      <Link
        href={`/${safeLocale}`}
        className="flex items-center gap-1 hover:text-[#EF4056] transition-colors"
      >
        <Home size={14} />
        <span>{isFa ? "خانه" : "Home"}</span>
      </Link>

      {items.map((item, i) => {
        const hasHref =
          typeof item.href === "string" && item.href.trim().length > 0;

        return (
          <div key={i} className="flex items-center gap-2">
            <ChevronLeft size={14} className={isFa ? "" : "rotate-180"} />

            {hasHref ? (
              <Link
                href={item.href as string}
                className="hover:text-[#EF4056] transition-colors"
              >
                {isFa ? item.labelFa : item.labelEn}
              </Link>
            ) : (
              <span className="text-[#3F4064] font-medium">
                {isFa ? item.labelFa : item.labelEn}
              </span>
            )}
          </div>
        );
      })}
    </nav>
  );
}