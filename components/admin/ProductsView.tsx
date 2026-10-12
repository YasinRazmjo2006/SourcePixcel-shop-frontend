"use client";

import { useState, useMemo, useEffect } from "react";
import Link from "next/link";
import {
  Search,
  Plus,
  Trash2,
  Download,
  Upload,
  X,
  Check,
} from "lucide-react";
import type { Locale, Product, SortOption } from "@/lib/types";
import { useAdminProductsStore, useToastStore } from "@/lib/stores";
import { getCategoryById } from "@/lib/data";
import { categories } from "@/lib/data";
import ProductRow from "./products/ProductRow";
import ProductFormDrawer from "./products/ProductFormDrawer";
import DeleteConfirmDialog from "./products/DeleteConfirmDialog";

interface ProductsViewProps {
  locale: Locale;
}

const ITEMS_PER_PAGE = 20;

export default function ProductsView({ locale }: ProductsViewProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const products = useAdminProductsStore((s) => s.products);
  const addProduct = useAdminProductsStore((s) => s.addProduct);
  const updateProduct = useAdminProductsStore((s) => s.updateProduct);
  const deleteProducts = useAdminProductsStore((s) => s.deleteProducts);
  const [mounted, setMounted] = useState(false);

  const [query, setQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [stockFilter, setStockFilter] = useState<"all" | "in" | "out">("all");
  const [sort, setSort] = useState<SortOption>("popular");
  const [page, setPage] = useState(1);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [editing, setEditing] = useState<Product | null>(null);
  const [formOpen, setFormOpen] = useState(false);
  const [deleteOpen, setDeleteOpen] = useState(false);

  useEffect(() => setMounted(true), []);

  const filtered = useMemo(() => {
    let result = [...products];
    const q = query.toLowerCase().trim();
    if (q) {
      result = result.filter(
        (p) =>
          p.titleFa.toLowerCase().includes(q) ||
          p.titleEn.toLowerCase().includes(q) ||
          p.brand.toLowerCase().includes(q) ||
          p.slug.toLowerCase().includes(q)
      );
    }
    if (categoryFilter !== "all") {
      result = result.filter((p) => p.category === categoryFilter);
    }
    if (stockFilter === "in") result = result.filter((p) => p.inStock);
    if (stockFilter === "out") result = result.filter((p) => !p.inStock);

    switch (sort) {
      case "newest":
        result.sort((a, b) => b.id - a.id);
        break;
      case "price-asc":
        result.sort((a, b) => a.finalPrice - b.finalPrice);
        break;
      case "price-desc":
        result.sort((a, b) => b.finalPrice - a.finalPrice);
        break;
      case "rating":
        result.sort((a, b) => b.rating - a.rating);
        break;
      default:
        result.sort((a, b) => b.reviewCount - a.reviewCount);
    }
    return result;
  }, [products, query, categoryFilter, stockFilter, sort]);

  const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
  const paginated = filtered.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  useEffect(() => {
    setPage(1);
  }, [query, categoryFilter, stockFilter, sort]);

  const allSelected = paginated.length > 0 && selectedIds.length === paginated.length;
  const someSelected = selectedIds.length > 0 && !allSelected;

  const toggleSelect = (id: number) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (allSelected) {
      setSelectedIds([]);
    } else {
      setSelectedIds(paginated.map((p) => p.id));
    }
  };

  const handleAdd = () => {
    setEditing(null);
    setFormOpen(true);
  };

  const handleEdit = (product: Product) => {
    setEditing(product);
    setFormOpen(true);
  };

  const handleSave = (product: Product) => {
    if (editing) {
      updateProduct(product.id, product);
      pushToast({
        type: "success",
        titleFa: "محصول به‌روزرسانی شد",
        titleEn: "Product updated",
      });
    } else {
      addProduct(product);
      pushToast({
        type: "success",
        titleFa: "محصول ایجاد شد",
        titleEn: "Product created",
      });
    }
  };

  const handleDeleteSingle = (id: number) => {
    setSelectedIds([id]);
    setDeleteOpen(true);
  };

  const confirmDelete = () => {
    deleteProducts(selectedIds);
    pushToast({
      type: "success",
      titleFa: `${selectedIds.length} محصول حذف شد`,
      titleEn: `${selectedIds.length} product(s) deleted`,
    });
    setSelectedIds([]);
    setDeleteOpen(false);
  };

  const t = {
    title: isFa ? "مدیریت محصولات" : "Products Management",
    subtitle: isFa
      ? `${filtered.length.toLocaleString("fa-IR")} محصول`
      : `${filtered.length} products`,
    search: isFa ? "جستجوی محصول..." : "Search product...",
    add: isFa ? "محصول جدید" : "New Product",
    export: isFa ? "خروجی" : "Export",
    import: isFa ? "ورود" : "Import",
    allCategories: isFa ? "همه دسته‌ها" : "All Categories",
    allStock: isFa ? "همه وضعیت‌ها" : "All Status",
    inStock: isFa ? "موجود" : "In Stock",
    outStock: isFa ? "ناموجود" : "Out of Stock",
    selected: isFa ? "انتخاب شده" : "selected",
    delete: isFa ? "حذف" : "Delete",
    clear: isFa ? "لغو انتخاب" : "Clear Selection",
    product: isFa ? "محصول" : "Product",
    category: isFa ? "دسته" : "Category",
    brand: isFa ? "برند" : "Brand",
    price: isFa ? "قیمت" : "Price",
    stock: isFa ? "وضعیت" : "Stock",
    actions: isFa ? "عملیات" : "Actions",
    empty: isFa ? "محصولی یافت نشد" : "No products found",
    page: isFa ? "صفحه" : "Page",
    of: isFa ? "از" : "of",
  };

  if (!mounted) {
    return (
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div>
          <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
            {t.title}
          </h1>
          <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
            {t.subtitle}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-1.5">
            <Upload size={14} />
            <span className="hidden md:inline">{t.import}</span>
          </button>
          <button className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-1.5">
            <Download size={14} />
            <span className="hidden md:inline">{t.export}</span>
          </button>
          <button
            onClick={handleAdd}
            className="h-10 px-4 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
          >
            <Plus size={14} />
            {t.add}
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-3 md:p-4 space-y-3">
        <div className="flex flex-col md:flex-row gap-2 md:gap-3">
          <div className="relative flex-1">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={t.search}
              className="w-full h-10 pr-9 pl-3 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-transparent focus:border-[#EF4056] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors"
              style={{ paddingRight: isFa ? 36 : 12, paddingLeft: isFa ? 12 : 36 }}
            />
            <Search
              size={14}
              className="absolute top-1/2 -translate-y-1/2 text-[#A1A3A8]"
              style={{ [isFa ? "right" : "left"]: 12 }}
            />
          </div>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
          >
            <option value="all">{t.allCategories}</option>
            {categories.map((c) => (
              <option key={c.id} value={c.id}>
                {isFa ? c.nameFa : c.nameEn}
              </option>
            ))}
          </select>
          <select
            value={stockFilter}
            onChange={(e) => setStockFilter(e.target.value as "all" | "in" | "out")}
            className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
          >
            <option value="all">{t.allStock}</option>
            <option value="in">{t.inStock}</option>
            <option value="out">{t.outStock}</option>
          </select>
          <select
            value={sort}
            onChange={(e) => setSort(e.target.value as SortOption)}
            className="h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056]"
          >
            <option value="popular">{isFa ? "محبوب‌ترین" : "Popular"}</option>
            <option value="newest">{isFa ? "جدیدترین" : "Newest"}</option>
            <option value="price-asc">{isFa ? "ارزان‌ترین" : "Price: Low"}</option>
            <option value="price-desc">{isFa ? "گران‌ترین" : "Price: High"}</option>
            <option value="rating">{isFa ? "بیشترین امتیاز" : "Rating"}</option>
          </select>
        </div>
      </div>

      {/* Bulk Actions */}
      {selectedIds.length > 0 && (
        <div className="bg-[#EF4056]/5 border border-[#EF4056]/20 rounded-lg p-3 flex items-center justify-between flex-wrap gap-2">
          <div className="text-[12px] text-[#EF4056] font-medium">
            {selectedIds.length.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.selected}
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSelectedIds([])}
              className="h-8 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] text-[#62666D] hover:border-[#EF4056] transition-colors flex items-center gap-1.5"
            >
              <X size={12} />
              {t.clear}
            </button>
            <button
              onClick={() => setDeleteOpen(true)}
              className="h-8 px-3 rounded-lg bg-[#EF4444] text-white text-[11px] font-medium hover:bg-[#d63030] transition-colors flex items-center gap-1.5"
            >
              <Trash2 size={12} />
              {t.delete} ({selectedIds.length})
            </button>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[800px]">
            <thead className="bg-[#F5F5F5] dark:bg-[#0F0F12] text-[10px] text-[#62666D] dark:text-[#A1A3A8] uppercase">
              <tr>
                <th className="p-3 w-10">
                  <input
                    type="checkbox"
                    checked={allSelected}
                    ref={(el) => {
                      if (el) el.indeterminate = someSelected;
                    }}
                    onChange={toggleSelectAll}
                    className="w-4 h-4 accent-[#EF4056] cursor-pointer"
                  />
                </th>
                <th className="text-start p-3 font-medium">{t.product}</th>
                <th className="text-start p-3 font-medium">{t.category}</th>
                <th className="text-start p-3 font-medium">{t.brand}</th>
                <th className="text-start p-3 font-medium">{t.price}</th>
                <th className="text-start p-3 font-medium">{t.stock}</th>
                <th className="text-start p-3 font-medium">{t.actions}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]">
              {paginated.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-16 text-center text-[13px] text-[#A1A3A8]">
                    {t.empty}
                  </td>
                </tr>
              ) : (
                paginated.map((product) => (
                  <ProductRow
                    key={product.id}
                    locale={locale}
                    product={product}
                    isSelected={selectedIds.includes(product.id)}
                    onToggleSelect={() => toggleSelect(product.id)}
                    onEdit={() => handleEdit(product)}
                    onDelete={() => handleDeleteSingle(product.id)}
                    onView={() => {
                      window.open(`/${locale}/product/${product.slug}`, "_blank");
                    }}
                  />
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-3 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex-wrap gap-3">
            <span className="text-[11px] text-[#A1A3A8]">
              {t.page} {page.toLocaleString(isFa ? "fa-IR" : "en-US")} {t.of}{" "}
              {totalPages.toLocaleString(isFa ? "fa-IR" : "en-US")}
            </span>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page === 1}
                className="w-8 h-8 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? "قبلی" : "Prev"}
              </button>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page === totalPages}
                className="w-8 h-8 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-center text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {isFa ? "بعدی" : "Next"}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Form Drawer */}
      <ProductFormDrawer
        locale={locale}
        product={editing}
        open={formOpen}
        onClose={() => {
          setFormOpen(false);
          setEditing(null);
        }}
        onSave={handleSave}
      />

      {/* Delete Confirm */}
      <DeleteConfirmDialog
        locale={locale}
        open={deleteOpen}
        count={selectedIds.length}
        onConfirm={confirmDelete}
        onCancel={() => setDeleteOpen(false)}
      />
    </div>
  );
}
