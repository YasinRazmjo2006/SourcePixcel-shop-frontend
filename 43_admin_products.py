# 43_admin_products.py
# Step 6: Products Management (CRUD + Filters + Bulk Actions)
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# lib/stores/admin-products.ts
# ============================================================
files.append(("lib/stores/admin-products.ts", '''"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { Product } from "@/lib/types";
import { products as initialProducts } from "@/lib/data";

interface AdminProductsState {
  products: Product[];
  addProduct: (product: Product) => void;
  updateProduct: (id: number, updates: Partial<Product>) => void;
  deleteProduct: (id: number) => void;
  deleteProducts: (ids: number[]) => void;
  toggleStock: (id: number) => void;
  reset: () => void;
}

export const useAdminProductsStore = create<AdminProductsState>()(
  persist(
    (set) => ({
      products: initialProducts,

      addProduct: (product) =>
        set((state) => ({
          products: [product, ...state.products],
        })),

      updateProduct: (id, updates) =>
        set((state) => ({
          products: state.products.map((p) =>
            p.id === id ? { ...p, ...updates } : p
          ),
        })),

      deleteProduct: (id) =>
        set((state) => ({
          products: state.products.filter((p) => p.id !== id),
        })),

      deleteProducts: (ids) =>
        set((state) => ({
          products: state.products.filter((p) => !ids.includes(p.id)),
        })),

      toggleStock: (id) =>
        set((state) => ({
          products: state.products.map((p) =>
            p.id === id ? { ...p, inStock: !p.inStock } : p
          ),
        })),

      reset: () => set({ products: initialProducts }),
    }),
    { name: "sourcepixcel-admin-products" }
  )
);
'''))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", '''// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export { useAdminStore } from "./admin";
export { useAdminUIStore } from "./admin-ui";
export { useAdminProductsStore } from "./admin-products";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
'''))

# ============================================================
# components/admin/products/ProductFormDrawer.tsx
# ============================================================
files.append(("components/admin/products/ProductFormDrawer.tsx", '''"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Save, Upload, ImageIcon } from "lucide-react";
import type { Locale, Product } from "@/lib/types";
import { categories, brands } from "@/lib/data";

interface ProductFormDrawerProps {
  locale: Locale;
  product: Product | null;
  open: boolean;
  onClose: () => void;
  onSave: (product: Product) => void;
}

interface FormState {
  titleFa: string;
  titleEn: string;
  slug: string;
  description: string;
  price: string;
  discountPercent: string;
  stock: string;
  category: string;
  brand: string;
  image: string;
  inStock: boolean;
}

const EMPTY: FormState = {
  titleFa: "",
  titleEn: "",
  slug: "",
  description: "",
  price: "",
  discountPercent: "0",
  stock: "0",
  category: "mobile",
  brand: "samsung",
  image: "/images/products/product-1.svg",
  inStock: true,
};

export default function ProductFormDrawer({
  locale,
  product,
  open,
  onClose,
  onSave,
}: ProductFormDrawerProps) {
  const isFa = locale === "fa";
  const [form, setForm] = useState<FormState>(EMPTY);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const isEdit = !!product;

  useEffect(() => {
    if (product) {
      setForm({
        titleFa: product.titleFa,
        titleEn: product.titleEn,
        slug: product.slug,
        description: "",
        price: String(product.price),
        discountPercent: String(product.discountPercent),
        stock: String(product.reviewCount),
        category: product.category,
        brand: product.brand,
        image: product.image,
        inStock: product.inStock,
      });
    } else {
      setForm(EMPTY);
    }
    setErrors({});
  }, [product, open]);

  const update = (key: keyof FormState, value: string | boolean) => {
    setForm((prev) => ({ ...prev, [key]: value }));
    setErrors((prev) => {
      const n = { ...prev };
      delete n[key];
      return n;
    });
  };

  const validate = () => {
    const e: Record<string, string> = {};
    if (!form.titleFa.trim()) e.titleFa = isFa ? "الزامی" : "Required";
    if (!form.titleEn.trim()) e.titleEn = isFa ? "الزامی" : "Required";
    if (!form.slug.trim()) e.slug = isFa ? "الزامی" : "Required";
    if (!form.price || Number(form.price) <= 0) e.price = isFa ? "قیمت معتبر وارد کنید" : "Invalid price";
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleSave = () => {
    if (!validate()) return;

    const price = Number(form.price);
    const discountPercent = Number(form.discountPercent);
    const finalPrice = Math.round(price * (1 - discountPercent / 100));

    const newProduct: Product = {
      id: product?.id ?? Date.now(),
      slug: form.slug,
      titleFa: form.titleFa,
      titleEn: form.titleEn,
      brand: form.brand,
      category: form.category,
      subcategory: product?.subcategory ?? "general",
      price,
      discountPercent,
      finalPrice,
      rating: product?.rating ?? 5,
      reviewCount: product?.reviewCount ?? 0,
      image: form.image,
      inStock: form.inStock,
      tags: product?.tags ?? [],
    };

    onSave(newProduct);
    onClose();
  };

  const inputClass = (key: string) =>
    `w-full h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border text-[12px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[key]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] dark:border-[#2A2A2E] focus:border-[#EF4056]"
    }`;

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[150]"
            onClick={onClose}
          />

          <motion.aside
            initial={{ x: isFa ? "100%" : "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: isFa ? "100%" : "-100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed top-0 bottom-0 w-full max-w-lg bg-white dark:bg-[#1A1A1E] shadow-2xl z-[151] overflow-y-auto"
            style={{ [isFa ? "right" : "left"]: 0 }}
          >
            {/* Header */}
            <div className="sticky top-0 bg-white dark:bg-[#1A1A1E] border-b border-[#E0E0E2] dark:border-[#2A2A2E] p-4 flex items-center justify-between z-10">
              <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {isEdit
                  ? isFa
                    ? "ویرایش محصول"
                    : "Edit Product"
                  : isFa
                  ? "محصول جدید"
                  : "New Product"}
              </h2>
              <button
                onClick={onClose}
                aria-label="Close"
                className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              >
                <X size={18} />
              </button>
            </div>

            <div className="p-4 space-y-4">
              {/* Image preview */}
              <div className="bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-xl p-4 flex items-center gap-3">
                <div className="w-20 h-20 rounded-lg bg-white dark:bg-[#1A1A1E] flex items-center justify-center overflow-hidden shrink-0 relative">
                  {form.image ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img src={form.image} alt="preview" className="w-full h-full object-cover" />
                  ) : (
                    <ImageIcon size={24} className="text-[#A1A3A8]" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-2">
                    {isFa ? "تصویر محصول" : "Product Image"}
                  </div>
                  <button className="h-8 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[11px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors flex items-center gap-1.5">
                    <Upload size={12} />
                    {isFa ? "آپلود" : "Upload"}
                  </button>
                </div>
              </div>

              {/* Titles */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "عنوان فارسی" : "Persian Title"} *
                  </label>
                  <input
                    type="text"
                    value={form.titleFa}
                    onChange={(e) => update("titleFa", e.target.value)}
                    className={inputClass("titleFa")}
                  />
                  {errors.titleFa && (
                    <p className="text-[10px] text-[#EF4444] mt-1">{errors.titleFa}</p>
                  )}
                </div>
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "عنوان انگلیسی" : "English Title"} *
                  </label>
                  <input
                    type="text"
                    value={form.titleEn}
                    onChange={(e) => update("titleEn", e.target.value)}
                    className={inputClass("titleEn")}
                  />
                  {errors.titleEn && (
                    <p className="text-[10px] text-[#EF4444] mt-1">{errors.titleEn}</p>
                  )}
                </div>
              </div>

              {/* Slug */}
              <div>
                <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                  {isFa ? "نامک (Slug)" : "Slug"} *
                </label>
                <input
                  type="text"
                  value={form.slug}
                  onChange={(e) => update("slug", e.target.value)}
                  dir="ltr"
                  className={inputClass("slug")}
                />
                {errors.slug && (
                  <p className="text-[10px] text-[#EF4444] mt-1">{errors.slug}</p>
                )}
              </div>

              {/* Category + Brand */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "دسته‌بندی" : "Category"}
                  </label>
                  <select
                    value={form.category}
                    onChange={(e) => update("category", e.target.value)}
                    className={inputClass("category")}
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>
                        {isFa ? c.nameFa : c.nameEn}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "برند" : "Brand"}
                  </label>
                  <select
                    value={form.brand}
                    onChange={(e) => update("brand", e.target.value)}
                    className={inputClass("brand")}
                  >
                    {brands.slice(0, 30).map((b) => (
                      <option key={b.id} value={b.id}>
                        {isFa ? b.nameFa : b.nameEn}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Price + Discount + Stock */}
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "قیمت (تومان)" : "Price (T)"} *
                  </label>
                  <input
                    type="number"
                    value={form.price}
                    onChange={(e) => update("price", e.target.value)}
                    dir="ltr"
                    className={inputClass("price")}
                  />
                  {errors.price && (
                    <p className="text-[10px] text-[#EF4444] mt-1">{errors.price}</p>
                  )}
                </div>
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "تخفیف ٪" : "Discount %"}
                  </label>
                  <input
                    type="number"
                    value={form.discountPercent}
                    onChange={(e) => update("discountPercent", e.target.value)}
                    dir="ltr"
                    className={inputClass("discountPercent")}
                    min="0"
                    max="100"
                  />
                </div>
                <div>
                  <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                    {isFa ? "موجودی" : "Stock"}
                  </label>
                  <input
                    type="number"
                    value={form.stock}
                    onChange={(e) => update("stock", e.target.value)}
                    dir="ltr"
                    className={inputClass("stock")}
                  />
                </div>
              </div>

              {/* In Stock toggle */}
              <label className="flex items-center justify-between p-3 bg-[#F5F5F5] dark:bg-[#2A2A2E] rounded-lg cursor-pointer">
                <span className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA]">
                  {isFa ? "موجود در انبار" : "In Stock"}
                </span>
                <input
                  type="checkbox"
                  checked={form.inStock}
                  onChange={(e) => update("inStock", e.target.checked)}
                  className="w-4 h-4 accent-[#22C55E] cursor-pointer"
                />
              </label>
            </div>

            {/* Footer */}
            <div className="sticky bottom-0 bg-white dark:bg-[#1A1A1E] border-t border-[#E0E0E2] dark:border-[#2A2A2E] p-4 flex items-center gap-2">
              <button
                onClick={onClose}
                className="flex-1 h-10 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
              >
                {isFa ? "انصراف" : "Cancel"}
              </button>
              <button
                onClick={handleSave}
                className="flex-1 h-10 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center justify-center gap-2"
              >
                <Save size={14} />
                {isEdit ? (isFa ? "ذخیره" : "Save") : isFa ? "ایجاد" : "Create"}
              </button>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
'''))

# ============================================================
# components/admin/products/ProductRow.tsx
# ============================================================
files.append(("components/admin/products/ProductRow.tsx", '''"use client";

import Image from "next/image";
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
          <div className="w-12 h-12 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0">
            <Image
              src={product.image}
              alt={isFa ? product.titleFa : product.titleEn}
              fill
              sizes="48px"
              className="object-cover"
            />
          </div>
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
'''))

# ============================================================
# components/admin/products/DeleteConfirmDialog.tsx
# ============================================================
files.append(("components/admin/products/DeleteConfirmDialog.tsx", '''"use client";

import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, X } from "lucide-react";
import type { Locale } from "@/lib/types";

interface DeleteConfirmDialogProps {
  locale: Locale;
  open: boolean;
  count: number;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function DeleteConfirmDialog({
  locale,
  open,
  count,
  onConfirm,
  onCancel,
}: DeleteConfirmDialogProps) {
  const isFa = locale === "fa";

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[200]"
            onClick={onCancel}
          />
          <div className="fixed inset-0 z-[201] flex items-center justify-center p-4 pointer-events-none">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -8 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -8 }}
              transition={{ duration: 0.15 }}
              className="w-full max-w-sm bg-white dark:bg-[#1A1A1E] rounded-2xl border border-[#E0E0E2] dark:border-[#2A2A2E] shadow-2xl pointer-events-auto"
            >
              <div className="p-5 text-center">
                <div className="w-14 h-14 rounded-full bg-[#EF4444]/10 flex items-center justify-center mx-auto mb-3">
                  <AlertTriangle size={28} className="text-[#EF4444]" />
                </div>
                <h3 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
                  {isFa ? "تایید حذف" : "Confirm Delete"}
                </h3>
                <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8] leading-6 mb-5">
                  {isFa
                    ? `آیا از حذف ${count} محصول مطمئن هستید؟ این عمل قابل بازگشت نیست.`
                    : `Are you sure you want to delete ${count} product(s)? This action cannot be undone.`}
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={onCancel}
                    className="flex-1 h-10 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors"
                  >
                    {isFa ? "انصراف" : "Cancel"}
                  </button>
                  <button
                    onClick={onConfirm}
                    className="flex-1 h-10 rounded-lg bg-[#EF4444] text-white text-[12px] font-medium hover:bg-[#d63030] transition-colors"
                  >
                    {isFa ? "حذف" : "Delete"}
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
'''))

# ============================================================
# components/admin/products/index.ts
# ============================================================
files.append(("components/admin/products/index.ts", '''// components/admin/products/index.ts
export { default as ProductFormDrawer } from "./ProductFormDrawer";
export { default as ProductRow } from "./ProductRow";
export { default as DeleteConfirmDialog } from "./DeleteConfirmDialog";
'''))

# ============================================================
# components/admin/ProductsView.tsx
# ============================================================
files.append(("components/admin/ProductsView.tsx", '''"use client";

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
'''))

# ============================================================
# app/[locale]/admin/products/page.tsx (updated)
# ============================================================
files.append(("app/[locale]/admin/products/page.tsx", '''import ProductsView from "@/components/admin/ProductsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminProductsPage({ params }: PageProps) {
  const { locale } = await params;
  return <ProductsView locale={locale as "fa" | "en"} />;
}
'''))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", '''// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as DashboardView } from "./DashboardView";
export { default as AnalyticsView } from "./AnalyticsView";
export { default as UsersView } from "./UsersView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as AdminLoginForm } from "./AdminLoginForm";

// Layout
export * from "./layout";

// Dashboard
export * from "./dashboard";

// Analytics
export * from "./analytics";

// Users
export * from "./users";

// Products
export * from "./products";

// Charts
export * from "./charts";
'''))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 6: Products Management")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")
    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/products")

if __name__ == "__main__":
    main()