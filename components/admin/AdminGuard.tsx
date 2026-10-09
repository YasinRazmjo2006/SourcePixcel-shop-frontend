"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useAdminStore } from "@/lib/stores";

interface AdminGuardProps {
  locale: string;
  children: React.ReactNode;
}

export default function AdminGuard({ locale, children }: AdminGuardProps) {
  const router = useRouter();
  const pathname = usePathname();
  const isAdmin = useAdminStore((s) => s.isAdmin);
  const [mounted, setMounted] = useState(false);

  const isLoginPage = pathname.includes("/admin/login");

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isAdmin && !isLoginPage) {
      router.replace(`/${locale}/admin/login`);
    }
  }, [mounted, isAdmin, isLoginPage, router, locale]);

  if (!mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Loading...
      </div>
    );
  }

  if (!isAdmin && !isLoginPage) {
    return (
      <div className="min-h-screen flex items-center justify-center text-[#A1A3A8] text-[13px]">
        Redirecting to login...
      </div>
    );
  }

  return <>{children}</>;
}
