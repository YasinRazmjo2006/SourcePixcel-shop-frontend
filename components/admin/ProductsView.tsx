"use client";

import { useState, useMemo } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Search,
  Plus,
  Edit,
  Trash2,
  Eye,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import { products as allProducts, getCategoryById, getBrandById } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface ProductsViewProps {
  locale: string;
}

const PER_PAGE = 10;

export default function ProductsView({ locale }: ProductsViewProps) {
  const isFa = locale === "fa";
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const q = query.toLowerCase().trim();
    if (!q) return allProducts;
    return allProducts.filter(
      (p) =>
        p.titleFa.toLowerCase().includes(q) ||
        p.titleEn.toLowerCase().includes(q) ||
        p.brand.toLowerCase().includes(q)
    );
  }, [query]);

  const totalPages = Math.ceil(filtered.length / PER_PAGE);
  const paginated = filtered.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const t = {
    title: isFa ? "مدیریت محصولات" : "Products Management",
    subtitle: isFa
      ? `${filtered.length} محصول موجود`
      : `${filtered.length} products`,
    searchPlaceholder: isFa ? "جستجوی محصول..." : "Search product...",
    addNew: isFa ? "افزودن محصول" : "Add Product",
    product: isFa ? "محصول" : "Product",
    category: isFa ? "دسته" : "Category",
    brand: isFa ? "برند" : "Brand",
    price: isFa ? "قیمت" : "Price",
    stock: isFa ? "موجودی" : "Stock",
    actions: isFa ? "عملیات" : "Actions",
    inStock: isFa ? "موجود" : "In stock",
    outOfStock: isFa ? "ناموجود" : "Out",
    edit: isFa ? "ویرایش" : "Edit",
    delete: isFa ? "حذف" : "Delete",
    view: isFa ? "مشاهده" : "View",
    confirmDelete: isFa
      ? "آیا مطمئن هستید؟"
      : "Are you sure?",
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h1 className="text-[20px] md:text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {t.title}
          </h1>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.subtitle}
          </p>
        </div>
        <button className="h-10 px-4 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2">
          <Plus size={16} />
          {t.addNew}
        </button>
      </div>

      {/* Search */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-3">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setPage(1);
            }}
            placeholder={t.searchPlaceholder}
            className="w-full h-10 pr-10 pl-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-transparent focus:border-[#EF4056] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors"
            style={{
              paddingRight: isFa ? 40 : 12,
              paddingLeft: isFa ? 12 : 40,
            }}
          />
          <Search
            size={16}
            className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
            style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
          />
        </div>
      </div>

      {/* Table */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[11px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="text-right p-3 font-medium">{t.product}</th>
                <th className="text-right p-3 font-medium">{t.category}</th>
                <th className="text-right p-3 font-medium">{t.brand}</th>
                <th className="text-right p-3 font-medium">{t.price}</th>
                <th className="text-right p-3 font-medium">{t.stock}</th>
                <th className="text-right p-3 font-medium">{t.actions}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {paginated.map((p) => {
                const category = getCategoryById(p.category);
                const brand = getBrandById(p.brand);
                return (
                  <tr
                    key={p.id}
                    className="hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors"
                  >
                    <td className="p-3">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
                          <Image
                            src={p.image}
                            alt={isFa ? p.titleFa : p.titleEn}
                            fill
                            sizes="48px"
                            className="object-cover"
                          />
                        </div>
                        <div className="min-w-0">
                          <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 max-w-[220px]">
                            {isFa ? p.titleFa : p.titleEn}
                          </div>
                          <div className="text-[10px] text-[#A1A3A8]" dir="ltr">
                            SP-{p.id.toString().padStart(5, "0")}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {category ? (isFa ? category.nameFa : category.nameEn) : "—"}
                    </td>
                    <td className="p-3 text-[11px] text-[#62666D] dark:text-[#A1A3A8]">
                      {brand ? (isFa ? brand.nameFa : brand.nameEn) : "—"}
                    </td>
                    <td className="p-3">
                      <div className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                        {formatPrice(p.finalPrice, isFa ? "fa" : "en")}
                      </div>
                      {p.discountPercent > 0 && (
                        <div className="text-[10px] text-[#EF4056]">
                          {p.discountPercent}% {isFa ? "تخفیف" : "off"}
                        </div>
                      )}
                    </td>
                    <td className="p-3">
                      <span
                        className={`text-[10px] px-2 py-1 rounded-full font-medium ${
                          p.inStock
                            ? "bg-[#22C55E]/10 text-[#22C55E]"
                            : "bg-[#EF4444]/10 text-[#EF4444]"
                        }`}
                      >
                        {p.inStock ? t.inStock : t.outOfStock}
                      </span>
                    </td>
                    <td className="p-3">
                      <div className="flex items-center gap-1">
                        <Link
                          href={`/${locale}/product/${p.slug}`}
                          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
                          title={t.view}
                        >
                          <Eye size={14} />
                        </Link>
                        <button
                          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#F59E0B] hover:bg-[#F59E0B]/10 transition-colors"
                          title={t.edit}
                        >
                          <Edit size={14} />
                        </button>
                        <button
                          className="w-7 h-7 rounded-lg flex items-center justify-center text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors"
                          title={t.delete}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex-wrap gap-3">
            <span className="text-[11px] text-[#A1A3A8]">
              {isFa
                ? `صفحه ${page.toLocaleString("fa-IR")} از ${totalPages.toLocaleString("fa-IR")}`
                : `Page ${page} of ${totalPages}`}
            </span>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="w-8 h-8 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="w-8 h-8 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? <ChevronLeft size={14} /> : <ChevronRight size={14} />}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
