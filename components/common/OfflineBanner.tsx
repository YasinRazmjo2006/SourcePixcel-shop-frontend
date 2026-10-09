"use client";

import { useEffect, useState } from "react";
import { WifiOff, Wifi } from "lucide-react";
import type { Locale } from "@/lib/types";

interface OfflineBannerProps {
  locale: Locale;
}

export default function OfflineBanner({ locale }: OfflineBannerProps) {
  const isFa = locale === "fa";
  const [isOnline, setIsOnline] = useState(true);
  const [showBack, setShowBack] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    setIsOnline(navigator.onLine);

    const handleOnline = () => {
      setIsOnline(true);
      setShowBack(true);
      setTimeout(() => setShowBack(false), 3000);
    };
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  if (!mounted) return null;
  if (isOnline && !showBack) return null;

  if (isOnline && showBack) {
    return (
      <div className="fixed top-16 left-1/2 -translate-x-1/2 z-[80] bg-[#22C55E] text-white text-[12px] font-medium px-4 py-2 rounded-full shadow-lg flex items-center gap-2 animate-in fade-in slide-in-from-top-2 duration-300">
        <Wifi size={14} />
        {isFa ? "اتصال اینترنت برقرار شد" : "You are back online"}
      </div>
    );
  }

  return (
    <div className="fixed top-16 left-1/2 -translate-x-1/2 z-[80] bg-[#EF4444] text-white text-[12px] font-medium px-4 py-2 rounded-full shadow-lg flex items-center gap-2">
      <WifiOff size={14} />
      {isFa
        ? "اتصال اینترنت قطع است"
        : "You are offline"}
    </div>
  );
}
