"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

interface ErrorBoundaryProps {
  locale?: string;
  children: React.ReactNode;
}

export default function ErrorBoundary({
  locale = "fa",
  children,
}: ErrorBoundaryProps) {
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const isFa = locale === "fa";

  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      setHasError(true);
      setErrorMessage(event.error?.message ?? "Unknown error");
    };
    window.addEventListener("error", handleError);
    return () => window.removeEventListener("error", handleError);
  }, []);

  if (hasError) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center px-4 text-center">
        <div className="w-20 h-20 rounded-full bg-[#EF4444]/10 flex items-center justify-center mb-4">
          <AlertTriangle size={40} className="text-[#EF4444]" />
        </div>
        <h1 className="text-[20px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2">
          {isFa ? "مشکلی پیش آمد" : "Something went wrong"}
        </h1>
        <p className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md">
          {isFa
            ? "متأسفانه خطایی رخ داد. لطفاً صفحه را دوباره بارگذاری کنید."
            : "An unexpected error occurred. Please reload the page."}
        </p>
        <div className="flex items-center gap-3">
          <button
            onClick={() => window.location.reload()}
            className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] flex items-center gap-2"
          >
            <RefreshCw size={16} />
            {isFa ? "بارگذاری مجدد" : "Reload"}
          </button>
          <Link
            href={`/${locale}`}
            className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] dark:text-[#E5E5EA] hover:border-[#EF4056] hover:text-[#EF4056] flex items-center gap-2"
          >
            <Home size={16} />
            {isFa ? "بازگشت به خانه" : "Home"}
          </Link>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
