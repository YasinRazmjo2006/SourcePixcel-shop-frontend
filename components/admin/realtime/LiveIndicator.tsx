"use client";

import { motion } from "framer-motion";
import { Wifi, WifiOff } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useLiveActivityStore } from "@/lib/stores";

interface LiveIndicatorProps {
  locale: Locale;
}

export default function LiveIndicator({ locale }: LiveIndicatorProps) {
  const isFa = locale === "fa";
  const isConnected = useLiveActivityStore((s) => s.isConnected);

  return (
    <div
      className={`inline-flex items-center gap-1.5 h-7 px-2.5 rounded-full text-[10px] font-bold transition-colors ${
        isConnected
          ? "bg-[#22C55E]/10 text-[#22C55E]"
          : "bg-[#EF4444]/10 text-[#EF4444]"
      }`}
    >
      {isConnected ? (
        <>
          <motion.span
            animate={{ scale: [1, 1.3, 1], opacity: [1, 0.5, 1] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="w-1.5 h-1.5 rounded-full bg-[#22C55E]"
          />
          <Wifi size={11} />
          <span>{isFa ? "زنده" : "LIVE"}</span>
        </>
      ) : (
        <>
          <WifiOff size={11} />
          <span>{isFa ? "قطع" : "OFFLINE"}</span>
        </>
      )}
    </div>
  );
}
