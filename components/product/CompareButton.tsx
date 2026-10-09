"use client";

import { GitCompareArrows } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useCompareStore, COMPARE_MAX } from "@/lib/stores";

interface CompareButtonProps {
  productId: number;
  locale: Locale;
  size?: "sm" | "md";
  variant?: "icon" | "full";
}

export default function CompareButton({
  productId,
  locale,
  size = "md",
  variant = "icon",
}: CompareButtonProps) {
  const isFa = locale === "fa";
  const toggle = useCompareStore((s) => s.toggle);
  const isInCompare = useCompareStore((s) => s.ids.includes(productId));
  const isFull = useCompareStore((s) => s.ids.length >= COMPARE_MAX && !isInCompare);

  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (isFull) return;
    toggle(productId);
  };

  const iconSize = size === "sm" ? 14 : 16;

  if (variant === "full") {
    return (
      <button
        onClick={handleClick}
        disabled={isFull}
        className={`h-10 px-4 rounded-lg border text-[12px] font-medium flex items-center justify-center gap-2 transition-colors ${
          isInCompare
            ? "bg-[#EF4056]/5 border-[#EF4056] text-[#EF4056]"
            : isFull
            ? "bg-[#F5F5F5] border-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
            : "bg-white border-[#E0E0E2] text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056]"
        }`}
      >
        <GitCompareArrows size={iconSize} />
        {isInCompare
          ? isFa
            ? "در مقایسه"
            : "In compare"
          : isFa
          ? "افزودن به مقایسه"
          : "Compare"}
      </button>
    );
  }

  return (
    <button
      onClick={handleClick}
      disabled={isFull}
      aria-label={isFa ? "افزودن به مقایسه" : "Add to compare"}
      title={
        isFull
          ? isFa
            ? `حداکثر ${COMPARE_MAX} محصول`
            : `Max ${COMPARE_MAX} products`
          : isFa
          ? "افزودن به مقایسه"
          : "Add to compare"
      }
      className={`w-7 h-7 rounded-full flex items-center justify-center transition-all ${
        isInCompare
          ? "bg-[#EF4056] text-white"
          : isFull
          ? "bg-[#E0E0E2] text-[#A1A3A8] cursor-not-allowed"
          : "bg-white/90 backdrop-blur text-[#62666D] hover:text-[#EF4056]"
      }`}
    >
      <GitCompareArrows size={iconSize} />
    </button>
  );
}
