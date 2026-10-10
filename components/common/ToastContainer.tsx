"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle2,
  XCircle,
  Info,
  AlertTriangle,
  X,
} from "lucide-react";
import { useToastStore, type ToastType } from "@/lib/stores";

const ICONS = {
  success: CheckCircle2,
  error: XCircle,
  info: Info,
  warning: AlertTriangle,
};

const COLORS: Record<ToastType, string> = {
  success: "bg-[#22C55E] text-white",
  error: "bg-[#EF4444] text-white",
  info: "bg-[#00BFFF] text-white",
  warning: "bg-[#F59E0B] text-white",
};

const PROGRESS_COLORS: Record<ToastType, string> = {
  success: "bg-[#16A34A]",
  error: "bg-[#DC2626]",
  info: "bg-[#0284C7]",
  warning: "bg-[#D97706]",
};

export default function ToastContainer() {
  const toasts = useToastStore((s) => s.toasts);
  const remove = useToastStore((s) => s.remove);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div className="fixed top-4 left-1/2 -translate-x-1/2 z-[200] flex flex-col gap-2 pointer-events-none w-full max-w-sm px-4">
      <AnimatePresence mode="popLayout">
        {toasts.map((toast) => {
          const Icon = ICONS[toast.type];
          const duration = toast.duration ?? 3500;

          return (
            <motion.div
              key={toast.id}
              layout
              initial={{ opacity: 0, y: -20, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{
                type: "spring",
                stiffness: 400,
                damping: 30,
              }}
              className={`${COLORS[toast.type]} rounded-lg shadow-lg pointer-events-auto overflow-hidden`}
            >
              <div className="p-3 flex items-start gap-3">
                <motion.div
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{
                    delay: 0.1,
                    type: "spring",
                    stiffness: 500,
                    damping: 25,
                  }}
                >
                  <Icon size={18} className="shrink-0 mt-0.5" />
                </motion.div>

                <div className="flex-1 text-[13px]">
                  <div className="font-bold">{toast.titleFa}</div>
                  {toast.messageFa && (
                    <div className="text-[12px] opacity-90 mt-0.5 line-clamp-2">
                      {toast.messageFa}
                    </div>
                  )}
                </div>

                <motion.button
                  whileHover={{ scale: 1.15, rotate: 90 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={() => remove(toast.id)}
                  aria-label="Close"
                  className="shrink-0 opacity-70 hover:opacity-100 transition-opacity"
                >
                  <X size={16} />
                </motion.button>
              </div>

              {/* Progress bar */}
              {duration > 0 && (
                <motion.div
                  initial={{ scaleX: 1 }}
                  animate={{ scaleX: 0 }}
                  transition={{ duration: duration / 1000, ease: "linear" }}
                  className={`h-[3px] origin-left ${PROGRESS_COLORS[toast.type]}`}
                />
              )}
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
