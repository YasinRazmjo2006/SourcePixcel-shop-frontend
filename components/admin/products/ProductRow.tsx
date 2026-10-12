"use client";

import AdminImage from "@/components/admin/common/AdminImage";
import { Edit, Trash2, Eye, Star, Package } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { getCategoryById, getBrandById } from "@/lib/data";
import { formatPrice } from "@/lib/utils";

interface ProductRowProps {
  locale: Locale;
  product: Product;
  isSelected: boolean;
  onToggleSelect: () => void;
  onEdit: () => void;
  onDelete: () => void;
  onView: () => void;
}

export default function ProductRow({
  locale,
  product,
  isSelected,
  onToggleSelect,
  onEdit,
  onDelete,
  onView,
}: ProductRowProps) {
  const isFa = locale === "fa";
  const category = getCategoryById(product.category);
  const brand = getBrandById(product.brand);

  return (
    <tr className={`hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors ${isSelected ? "bg-[#EF4056]/5" : ""}`}>
      <td className="p-3 w-10">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={onToggleSelect}
          className="w-4 h-4 accent-[#EF4056] cursor-pointer"
        />
      </td>
      <td className="p-3">
        <div className="flex items-center gap-3">
          <AdminImage
            src={product.image}
            alt={isFa ? product.titleFa : product.titleEn}
            size={48}
          />
          <div className="min-w-0">
            <div className="text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] line-clamp-1 max-w-[220px]">
              {isFa ? product.titleFa : product.titleEn}
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-[10px] text-[#A1A3A8]" dir="ltr">
                SP-{product.id.toString().padStart(5, "0")}
              </span>
              <span className="flex items-center gap-0.5 text-[10px] text-amber-500">
                <Star size={9} className="fill-current" />
                {product.rating}
              </span>
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
          {formatPrice(product.finalPrice, locale)}
        </div>
        {product.discountPercent > 0 && (
          <div className="text-[10px] text-[#EF4056]">
            {product.discountPercent}% {isFa ? "تخفیف" : "off"}
          </div>
        )}
      </td>
      <td className="p-3">
        <span
          className={`text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap inline-flex items-center gap-1 ${
            product.inStock
              ? "bg-[#22C55E]/10 text-[#22C55E]"
              : "bg-[#EF4444]/10 text-[#EF4444]"
          }`}
        >
          <Package size={10} />
          {product.inStock
            ? isFa
              ? "موجود"
              : "In Stock"
            : isFa
            ? "ناموجود"
            : "Out of Stock"}
        </span>
      </td>
      <td className="p-3">
        <div className="flex items-center gap-1">
          <button
            onClick={onView}
            title={isFa ? "مشاهده" : "View"}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-[#00BFFF] hover:bg-[#00BFFF]/10 transition-colors"
          >
            <Eye size={14} />
          </button>
          <button
            onClick={onEdit}
            title={isFa ? "ویرایش" : "Edit"}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-[#F59E0B] hover:bg-[#F59E0B]/10 transition-colors"
          >
            <Edit size={14} />
          </button>
          <button
            onClick={onDelete}
            title={isFa ? "حذف" : "Delete"}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-[#EF4444] hover:bg-[#EF4444]/10 transition-colors"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </td>
    </tr>
  );
}
