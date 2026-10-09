"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import type { Locale } from "@/lib/types";

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  locale: Locale;
}

export default function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  locale,
}: PaginationProps) {
  const isFa = locale === "fa";

  if (totalPages <= 1) return null;

  const pages: (number | "...")[] = [];
  const showEllipsis = totalPages > 7;

  if (!showEllipsis) {
    for (let i = 1; i <= totalPages; i++) pages.push(i);
  } else {
    pages.push(1);
    if (currentPage > 3) pages.push("...");
    const start = Math.max(2, currentPage - 1);
    const end = Math.min(totalPages - 1, currentPage + 1);
    for (let i = start; i <= end; i++) pages.push(i);
    if (currentPage < totalPages - 2) pages.push("...");
    pages.push(totalPages);
  }

  const fmt = (n: number) =>
    isFa ? n.toLocaleString("fa-IR") : n.toString();

  return (
    <div className="flex items-center justify-center gap-1 mt-6">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
        className="w-9 h-9 rounded-lg border border-[#E0E0E2] bg-white flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {isFa ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {pages.map((p, i) =>
        p === "..." ? (
          <span
            key={`ellipsis-${i}`}
            className="w-9 h-9 flex items-center justify-center text-[#A1A3A8]"
          >
            ...
          </span>
        ) : (
          <button
            key={p}
            onClick={() => onPageChange(p)}
            className={`w-9 h-9 rounded-lg border text-[13px] font-medium transition-colors ${
              p === currentPage
                ? "bg-[#EF4056] text-white border-[#EF4056]"
                : "bg-white text-[#3F4064] border-[#E0E0E2] hover:border-[#EF4056] hover:text-[#EF4056]"
            }`}
          >
            {fmt(p)}
          </button>
        )
      )}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Next page"
        className="w-9 h-9 rounded-lg border border-[#E0E0E2] bg-white flex items-center justify-center text-[#62666D] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {isFa ? <ChevronLeft size={16} /> : <ChevronRight size={16} />}
      </button>
    </div>
  );
}
