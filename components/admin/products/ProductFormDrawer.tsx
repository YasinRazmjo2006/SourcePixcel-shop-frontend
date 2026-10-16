"use client";

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
  image: withBasePath("/images/products/product-1.svg"),
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
import { withBasePath } from "@/lib/utils/paths";
