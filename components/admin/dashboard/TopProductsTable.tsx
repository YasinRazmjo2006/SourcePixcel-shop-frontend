import Link from "next/link";
import AdminImage from "@/components/admin/common/AdminImage";
import { Trophy, Star, ArrowLeft, ArrowRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { topProducts } from "@/lib/data";
import { formatCompact } from "@/lib/utils";
import ChartCard from "../charts/ChartCard";

interface TopProductsTableProps { locale: Locale; }

export default function TopProductsTable({ locale }: TopProductsTableProps) {
  const isFa = locale === "fa";
  return (
    <ChartCard
      titleFa="پرفروش‌ترین محصولات"
      titleEn="Top Products"
      subtitleFa="بر اساس درآمد"
      subtitleEn="By revenue"
      icon={Trophy}
      delay={0.3}
      action={
        <Link href={`/${locale}/admin/products`} className="text-[11px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors shrink-0">
          {isFa ? "همه" : "All"}
          {isFa ? <ArrowLeft size={12} /> : <ArrowRight size={12} />}
        </Link>
      }
    >
      <div className="space-y-3">
        {topProducts.map((product, i) => (
          <div key={product.id} className="flex items-center gap-3 group hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 -mx-2 px-2 py-1.5 rounded-lg transition-colors">
            <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-bold shrink-0 ${i === 0 ? "bg-gradient-to-br from-amber-400 to-amber-600 text-white" : i === 1 ? "bg-gradient-to-br from-slate-300 to-slate-500 text-white" : i === 2 ? "bg-gradient-to-br from-orange-400 to-orange-600 text-white" : "bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8]"}`}>
              {isFa ? (i + 1).toLocaleString("fa-IR") : i + 1}
            </div>
            <AdminImage
              src={product.image}
              alt={isFa ? product.titleFa : product.titleEn}
              size={44}
            />
            <div className="flex-1 min-w-0">
              <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] truncate">{isFa ? product.titleFa : product.titleEn}</div>
              <div className="flex items-center gap-2 mt-0.5">
                <span className="flex items-center gap-0.5 text-[10px] text-amber-500">
                  <Star size={9} className="fill-current" />
                  {product.rating}
                </span>
                <span className="text-[10px] text-[#A1A3A8]">{product.sales.toLocaleString(isFa ? "fa-IR" : "en-US")} {isFa ? "فروش" : "sold"}</span>
              </div>
            </div>
            <div className="text-end shrink-0">
              <div className="text-[12px] font-bold text-[#EF4056] tabular-nums">{formatCompact(product.revenue, locale)}</div>
              <div className="text-[9px] text-[#A1A3A8]">{isFa ? "تومان" : "Toman"}</div>
            </div>
          </div>
        ))}
      </div>
    </ChartCard>
  );
}
