"use client";

import { useEffect, useState } from "react";
import { CheckCircle2, XCircle, Info, AlertTriangle, X } from "lucide-react";
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
      {toasts.map((toast) => {
        const Icon = ICONS[toast.type];
        return (
          <div
            key={toast.id}
            className={`${COLORS[toast.type]} rounded-lg shadow-lg p-3 flex items-start gap-3 pointer-events-auto animate-in fade-in slide-in-from-top-2 duration-200`}
          >
            <Icon size={18} className="shrink-0 mt-0.5" />
            <div className="flex-1 text-[13px]">
              <div className="font-bold">{toast.titleFa}</div>
              {toast.messageFa && (
                <div className="text-[12px] opacity-90 mt-0.5">
                  {toast.messageFa}
                </div>
              )}
            </div>
            <button
              onClick={() => remove(toast.id)}
              aria-label="Close"
              className="shrink-0 opacity-70 hover:opacity-100 transition-opacity"
            >
              <X size={16} />
            </button>
          </div>
        );
      })}
    </div>
  );
}
