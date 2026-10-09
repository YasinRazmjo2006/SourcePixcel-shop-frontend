"use client";

import { useState } from "react";
import { Menu } from "lucide-react";
import AdminSidebar from "@/components/admin/AdminSidebar";
import AdminGuard from "@/components/admin/AdminGuard";

export default function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const [mobileOpen, setMobileOpen] = useState(false);

  // Note: params is a Promise in Next.js 15, but client components
  // can't await it. We'll use a workaround by reading from pathname.
  // For simplicity, we'll get locale from window.location on client.
  const [locale, setLocale] = useState("fa");

  // Read locale on mount
  if (typeof window !== "undefined") {
    const match = window.location.pathname.match(/^\/(fa|en)/);
    const detected = match?.[1] ?? "fa";
    if (detected !== locale) {
      setLocale(detected);
    }
  }

  return (
    <AdminGuard locale={locale}>
      <div className="min-h-screen flex bg-[#F5F5F5] dark:bg-[#0F0F12]">
        {/* Mobile menu button */}
        <button
          onClick={() => setMobileOpen(true)}
          className="lg:hidden fixed top-4 right-4 z-[90] w-10 h-10 rounded-lg bg-[#EF4056] text-white flex items-center justify-center shadow-lg"
          aria-label="Open menu"
        >
          <Menu size={20} />
        </button>

        <AdminSidebar
          locale={locale}
          mobileOpen={mobileOpen}
          onClose={() => setMobileOpen(false)}
        />

        <main className="flex-1 min-w-0 p-4 md:p-6">{children}</main>
      </div>
    </AdminGuard>
  );
}
