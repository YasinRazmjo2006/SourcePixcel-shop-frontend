"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Command, X, Keyboard } from "lucide-react";
import type { Locale } from "@/lib/types";

interface KeyboardShortcutsProps {
  locale: Locale;
}

interface Shortcut {
  keys: string[];
  labelFa: string;
  labelEn: string;
}

export default function KeyboardShortcuts({ locale }: KeyboardShortcutsProps) {
  const isFa = locale === "fa";
  const router = useRouter();
  const [showHelp, setShowHelp] = useState(false);

  const shortcuts: Shortcut[] = [
    {
      keys: ["Ctrl", "K"],
      labelFa: "جستجو",
      labelEn: "Search",
    },
    {
      keys: ["Ctrl", "H"],
      labelFa: "صفحه اصلی",
      labelEn: "Home",
    },
    {
      keys: ["Ctrl", "C"],
      labelFa: "سبد خرید",
      labelEn: "Cart",
    },
    {
      keys: ["Ctrl", "W"],
      labelFa: "علاقه‌مندی‌ها",
      labelEn: "Wishlist",
    },
    {
      keys: ["Ctrl", "A"],
      labelFa: "حساب کاربری",
      labelEn: "Account",
    },
    {
      keys: ["Ctrl", "P"],
      labelFa: "پنل ادمین",
      labelEn: "Admin Panel",
    },
    {
      keys: ["Shift", "?"],
      labelFa: "راهنمای میانبرها",
      labelEn: "Show this help",
    },
    {
      keys: ["Esc"],
      labelFa: "بستن پنجره‌ها",
      labelEn: "Close dialogs",
    },
  ];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInput =
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable;

      // Ctrl+K → focus search
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        const searchInput = document.querySelector<HTMLInputElement>(
          'input[type="text"][placeholder*="جستجو"], input[type="text"][placeholder*="Search"]'
        );
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        } else {
          router.push(`/${locale}/search`);
        }
        return;
      }

      // Ctrl+H → home
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "h") {
        e.preventDefault();
        router.push(`/${locale}`);
        return;
      }

      // Ctrl+C → cart (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "c") {
        // Don't prevent default if there's a text selection
        if (!window.getSelection()?.toString()) {
          e.preventDefault();
          router.push(`/${locale}/cart`);
        }
        return;
      }

      // Ctrl+W → wishlist (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "w") {
        e.preventDefault();
        router.push(`/${locale}/account/wishlist`);
        return;
      }

      // Ctrl+A → account (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "a") {
        e.preventDefault();
        router.push(`/${locale}/account`);
        return;
      }

      // Ctrl+P → admin panel (only if not in input)
      if (!isInput && (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "p") {
        e.preventDefault();
        router.push(`/${locale}/admin`);
        return;
      }

      // Shift+? → help
      if (e.shiftKey && e.key === "?") {
        if (!isInput) {
          e.preventDefault();
          setShowHelp((v) => !v);
        }
        return;
      }

      // Esc → close help
      if (e.key === "Escape" && showHelp) {
        setShowHelp(false);
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [router, locale, showHelp]);

  if (!showHelp) return null;

  return (
    <div className="fixed inset-0 z-[200] flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={() => setShowHelp(false)}
      />
      <div className="relative bg-white dark:bg-[#1A1A1E] rounded-2xl border border-[#E0E0E2] dark:border-[#2A2A2E] shadow-2xl w-full max-w-lg max-h-[85vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-[#EF4056]/10 flex items-center justify-center">
              <Keyboard size={18} className="text-[#EF4056]" />
            </div>
            <div>
              <h2 className="text-[14px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {isFa ? "میانبرهای کیبورد" : "Keyboard Shortcuts"}
              </h2>
              <p className="text-[10px] text-[#A1A3A8]">
                {isFa
                  ? "برای جابجایی سریع‌تر در سایت"
                  : "Move faster around the site"}
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowHelp(false)}
            aria-label="Close"
            className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* List */}
        <div className="p-4 max-h-[60vh] overflow-y-auto">
          <div className="space-y-2">
            {shortcuts.map((sc, i) => (
              <div
                key={i}
                className="flex items-center justify-between gap-3 py-2.5 px-3 rounded-lg hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E] transition-colors"
              >
                <span className="text-[12px] text-[#3F4064] dark:text-[#E5E5EA]">
                  {isFa ? sc.labelFa : sc.labelEn}
                </span>
                <div className="flex items-center gap-1">
                  {sc.keys.map((key, j) => (
                    <span key={j}>
                      <kbd className="inline-flex items-center justify-center min-w-[28px] h-7 px-2 rounded-md bg-[#F5F5F5] dark:bg-[#2A2A2E] border border-[#E0E0E2] dark:border-[#3A3A40] text-[10px] font-mono font-bold text-[#3F4064] dark:text-[#E5E5EA] shadow-sm">
                        {key}
                      </kbd>
                      {j < sc.keys.length - 1 && (
                        <span className="text-[#A1A3A8] text-[10px] mx-1">
                          +
                        </span>
                      )}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="p-3 border-t border-[#E0E0E2] dark:border-[#2A2A2E] bg-[#FAFAFA] dark:bg-[#0F0F12]">
          <div className="flex items-center justify-center gap-2 text-[10px] text-[#A1A3A8]">
            <Command size={12} />
            <span>
              {isFa
                ? "برای بستن این پنجره، Esc را بزنید"
                : "Press Esc to close this dialog"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
