"use client";

import { useState, useEffect } from "react";
import type { Locale, Product } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import { useCompareStore } from "@/lib/stores";
import { Breadcrumb } from "@/components/common";
import CompareEmpty from "./CompareEmpty";
import CompareTable from "./CompareTable";

interface ComparePageProps {
  locale: Locale;
}

export default function ComparePage({ locale }: ComparePageProps) {
  const isFa = locale === "fa";
  const [mounted, setMounted] = useState(false);
  const ids = useCompareStore((s) => s.ids);

  useEffect(() => {
    setMounted(true);
  }, []);

  const items: Product[] = ids
    .map((id) => allProducts.find((p) => p.id === id))
    .filter((p): p is Product => p !== undefined);

  if (!mounted) {
    return (
      <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
        {isFa ? "در حال بارگذاری..." : "Loading..."}
      </div>
    );
  }

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "مقایسه محصولات", labelEn: "Compare" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">
        {isFa ? "مقایسه محصولات" : "Compare Products"}
      </h1>

      {items.length === 0 ? (
        <CompareEmpty locale={locale} />
      ) : (
        <CompareTable locale={locale} products={items} />
      )}
    </div>
  );
}
