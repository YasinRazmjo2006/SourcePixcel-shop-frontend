"use client";

import { useEffect } from "react";
import Link from "next/link";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Page error:", error);
  }, [error]);

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-16 text-center">
      <div className="w-20 h-20 rounded-full bg-[#EF4444]/10 flex items-center justify-center mx-auto mb-4">
        <AlertTriangle size={40} className="text-[#EF4444]" />
      </div>
      <h1 className="text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
        خطایی رخ داد
      </h1>
      <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md mx-auto">
        متأسفانه در بارگذاری این صفحه مشکلی پیش آمد. لطفاً دوباره تلاش کنید.
      </p>
      <div className="flex items-center justify-center gap-3 flex-wrap">
        <button
          onClick={reset}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] flex items-center gap-2"
        >
          <RefreshCw size={16} />
          تلاش مجدد
        </button>
        <Link
          href="/fa"
          className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] flex items-center gap-2"
        >
          <Home size={16} />
          بازگشت به خانه
        </Link>
      </div>
    </div>
  );
}
