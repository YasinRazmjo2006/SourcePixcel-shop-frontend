"use client";

import { useEffect } from "react";
import { motion } from "framer-motion";
import { RefreshCw, Home, AlertTriangle } from "lucide-react";
import Link from "next/link";
import { RippleButton } from "@/components/ui";

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
      <div className="relative mb-6 inline-block">
        <motion.div
          animate={{ scale: [1, 1.15, 1], opacity: [0.15, 0.05, 0.15] }}
          transition={{ duration: 3, repeat: Infinity }}
          className="absolute inset-0 rounded-full bg-[#EF4444]"
          style={{ width: 120, height: 120 }}
        />
        <motion.div
          initial={{ scale: 0, rotate: -10 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
          className="relative w-[120px] h-[120px] rounded-full bg-[#EF4444]/10 flex items-center justify-center"
        >
          <motion.div
            animate={{ rotate: [0, -5, 5, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <AlertTriangle size={52} className="text-[#EF4444]" />
          </motion.div>
        </motion.div>
      </div>

      <motion.h1
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="text-[22px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2"
      >
        خطایی رخ داد
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md mx-auto leading-6"
      >
        متأسفانه در بارگذاری این صفحه مشکلی پیش آمد. لطفاً دوباره تلاش کنید یا به
        صفحه اصلی بازگردید.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        className="flex items-center justify-center gap-3 flex-wrap"
      >
        <RippleButton onClick={reset} variant="primary" size="md">
          <RefreshCw size={16} />
          تلاش مجدد
        </RippleButton>

        <Link href="/fa">
          <RippleButton variant="ghost" size="md">
            <Home size={16} />
            بازگشت به خانه
          </RippleButton>
        </Link>
      </motion.div>
    </div>
  );
}
