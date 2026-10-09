"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { Locale } from "@/lib/types";
import { useAuthStore } from "@/lib/stores";

interface AccountGuardProps {
  locale: Locale;
  children: React.ReactNode;
}

export default function AccountGuard({ locale, children }: AccountGuardProps) {
  const router = useRouter();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isAuthenticated) {
      router.replace(`/${locale}/auth/login`);
    }
  }, [mounted, isAuthenticated, router, locale]);

  if (!mounted) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Loading...
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Redirecting to login...
      </div>
    );
  }

  return <>{children}</>;
}
