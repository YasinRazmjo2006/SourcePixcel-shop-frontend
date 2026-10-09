import Link from "next/link";
import type { Locale } from "@/lib/types";
import { categories } from "@/lib/data";
import Breadcrumb from "@/components/common/Breadcrumb";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CategoriesPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={typedLocale}
        items={[{ labelFa: "دسته‌بندی‌ها", labelEn: "Categories" }]}
      />

      <h1 className="text-[22px] font-bold text-[#3F4064] mb-6">
        {isFa ? "همه دسته‌بندی‌ها" : "All Categories"}
      </h1>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {categories.map((cat) => (
          <Link
            key={cat.id}
            href={`/${typedLocale}/category/${cat.slug}`}
            className="bg-white rounded-lg border border-[#E0E0E2] p-4 hover:shadow-md transition-shadow"
          >
            <h3 className="text-[14px] font-bold text-[#3F4064] mb-3">
              {isFa ? cat.nameFa : cat.nameEn}
            </h3>
            <ul className="space-y-1">
              {cat.subcategories.map((sub) => (
                <li
                  key={sub.id}
                  className="text-[12px] text-[#62666D] hover:text-[#EF4056] transition-colors"
                >
                  {isFa ? sub.nameFa : sub.nameEn}
                </li>
              ))}
            </ul>
          </Link>
        ))}
      </div>
    </div>
  );
}
