import Link from "next/link";
import {
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

const ICON_MAP: Record<string, React.ComponentType<{ size?: number; className?: string; style?: React.CSSProperties }>> = {
  Smartphone, Laptop, Tablet, Headphones, Camera, Watch,
  Gamepad2, Cable, Shirt, Footprints, Home, BookOpen,
};

const CATEGORY_COLORS: Record<string, string> = {
  mobile: "#EF4056",
  laptop: "#00BFFF",
  tablet: "#8B5CF6",
  audio: "#F59E0B",
  camera: "#22C55E",
  smartwatch: "#EC4899",
  gaming: "#06B6D4",
  accessories: "#6B7280",
  clothing: "#F97316",
  shoes: "#10B981",
  home: "#6366F1",
  books: "#84CC16",
};

interface CategoryCirclesProps {
  locale: Locale;
}

export default function CategoryCircles({ locale }: CategoryCirclesProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-[15px] md:text-[16px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
          {isFa ? "دسته‌بندی‌ها" : "Shop by Category"}
        </h2>
      </div>

      <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-3">
        {categories.map((cat) => {
          const Icon = ICON_MAP[cat.icon] ?? Cable;
          const color = CATEGORY_COLORS[cat.id] ?? "#EF4056";
          return (
            <Link
              key={cat.id}
              href={`/${locale}/category/${cat.slug}`}
              className="flex flex-col items-center gap-2 group"
            >
              <div
                className="w-14 h-14 md:w-16 md:h-16 rounded-full flex items-center justify-center transition-all group-hover:scale-110 group-hover:shadow-lg"
                style={{ backgroundColor: `${color}15` }}
              >
                <Icon
                  size={26}
                  style={{ color }}
                  className="transition-transform"
                />
              </div>
              <span className="text-[10px] md:text-[11px] text-[#62666D] dark:text-[#A1A3A8] text-center leading-tight font-medium group-hover:text-[#EF4056] transition-colors">
                {isFa ? cat.nameFa : cat.nameEn}
              </span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
