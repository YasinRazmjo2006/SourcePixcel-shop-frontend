"use client";

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
