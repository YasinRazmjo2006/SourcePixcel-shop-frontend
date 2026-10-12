"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  ArrowRight,
  ArrowLeft,
  CornerDownLeft,
  X,
  Sparkles,
} from "lucide-react";
import { useAdminUIStore } from "@/lib/stores";
import { FLAT_ADMIN_NAV } from "@/lib/admin-nav";

interface CommandPaletteProps {
  locale: string;
}

export default function CommandPalette({ locale }: CommandPaletteProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const open = useAdminUIStore((s) => s.commandPaletteOpen);
  const setOpen = useAdminUIStore((s) => s.setCommandPaletteOpen);

  const [query, setQuery] = useState("");
  const [highlighted, setHighlighted] = useState(0);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return FLAT_ADMIN_NAV;
    return FLAT_ADMIN_NAV.filter(
      (item) =>
        item.labelFa.toLowerCase().includes(q) ||
        item.labelEn.toLowerCase().includes(q) ||
        item.href.toLowerCase().includes(q)
    );
  }, [query]);

  // Reset on open
  useEffect(() => {
    if (open) {
      setQuery("");
      setHighlighted(0);
    }
  }, [open]);

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen(!open);
        return;
      }
      if (!open) return;

      if (e.key === "Escape") {
        e.preventDefault();
        setOpen(false);
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        setHighlighted((prev) => (prev + 1) % Math.max(1, filtered.length));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setHighlighted((prev) =>
          prev <= 0 ? Math.max(0, filtered.length - 1) : prev - 1
        );
      } else if (e.key === "Enter" && filtered[highlighted]) {
        e.preventDefault();
        router.push(`/${locale}${filtered[highlighted].href}`);
        setOpen(false);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, filtered, highlighted, router, locale, setOpen]);

  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[200]"
            onClick={() => setOpen(false)}
          />
          <div className="fixed inset-0 z-[201] flex items-start justify-center pt-[15vh] px-4 pointer-events-none">
            <motion.div
              initial={{ opacity: 0, y: -20, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.96 }}
              transition={{ duration: 0.15 }}
              className="w-full max-w-xl bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] rounded-2xl shadow-2xl overflow-hidden pointer-events-auto"
            >
              {/* Search input */}
              <div className="flex items-center gap-3 px-4 h-14 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
                <Search size={18} className="text-[#A1A3A8] shrink-0" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setHighlighted(0);
                  }}
                  placeholder={
                    isFa
                      ? "جستجو در پنل یا پرش به صفحه..."
                      : "Search or jump to..."
                  }
                  className="flex-1 bg-transparent text-[14px] text-[#3F4064] dark:text-[#E5E5EA] placeholder:text-[#A1A3A8] focus:outline-none"
                  autoFocus
                />
                <button
                  onClick={() => setOpen(false)}
                  className="w-7 h-7 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
                  aria-label="Close"
                >
                  <X size={14} />
                </button>
              </div>

              {/* Results */}
              <div className="max-h-[400px] overflow-y-auto p-2">
                {filtered.length === 0 ? (
                  <div className="py-12 text-center">
                    <div className="w-12 h-12 rounded-full bg-[#F5F5F5] dark:bg-[#2A2A2E] flex items-center justify-center mx-auto mb-3">
                      <Sparkles size={20} className="text-[#A1A3A8]" />
                    </div>
                    <div className="text-[13px] font-medium text-[#3F4064] dark:text-[#E5E5EA] mb-1">
                      {isFa ? "نتیجه‌ای یافت نشد" : "No results found"}
                    </div>
                    <div className="text-[11px] text-[#A1A3A8]">
                      {isFa
                        ? "عبارت دیگری را امتحان کنید"
                        : "Try a different keyword"}
                    </div>
                  </div>
                ) : (
                  <ul className="list-none m-0 p-0 space-y-0.5">
                    {filtered.map((item, idx) => {
                      const Icon = item.icon;
                      const isHighlighted = idx === highlighted;
                      return (
                        <li key={item.id}>
                          <button
                            onMouseEnter={() => setHighlighted(idx)}
                            onClick={() => {
                              router.push(`/${locale}${item.href}`);
                              setOpen(false);
                            }}
                            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-start transition-colors ${
                              isHighlighted
                                ? "bg-[#EF4056] text-white"
                                : "text-[#3F4064] dark:text-[#E5E5EA] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
                            }`}
                          >
                            <Icon
                              size={16}
                              className={
                                isHighlighted
                                  ? "text-white"
                                  : "text-[#62666D] dark:text-[#A1A3A8]"
                              }
                            />
                            <div className="flex-1 min-w-0">
                              <div className="text-[13px] font-medium truncate">
                                {isFa ? item.labelFa : item.labelEn}
                              </div>
                              <div
                                className={`text-[10px] truncate ${
                                  isHighlighted
                                    ? "text-white/70"
                                    : "text-[#A1A3A8]"
                                }`}
                              >
                                /{locale}
                                {item.href}
                              </div>
                            </div>
                            {isHighlighted &&
                              (isFa ? (
                                <ArrowLeft size={14} className="text-white" />
                              ) : (
                                <ArrowRight size={14} className="text-white" />
                              ))}
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                )}
              </div>

              {/* Footer */}
              <div className="flex items-center justify-between gap-2 px-3 py-2.5 border-t border-[#E0E0E2] dark:border-[#2A2A2E] bg-[#FAFAFA] dark:bg-[#0F0F12]">
                <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8]">
                  <span className="flex items-center gap-1">
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] font-mono text-[9px]">
                      ↑
                    </kbd>
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] font-mono text-[9px]">
                      ↓
                    </kbd>
                    {isFa ? "پیمایش" : "Navigate"}
                  </span>
                  <span className="flex items-center gap-1">
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E]">
                      <CornerDownLeft size={9} />
                    </kbd>
                    {isFa ? "انتخاب" : "Select"}
                  </span>
                  <span className="flex items-center gap-1">
                    <kbd className="inline-flex items-center justify-center min-w-[20px] h-5 px-1 rounded bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] font-mono text-[9px]">
                      Esc
                    </kbd>
                    {isFa ? "بستن" : "Close"}
                  </span>
                </div>
                <div className="text-[10px] text-[#A1A3A8] font-mono">
                  {filtered.length} {isFa ? "نتیجه" : "results"}
                </div>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
