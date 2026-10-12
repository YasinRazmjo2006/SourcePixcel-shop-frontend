import AdminGuard from "@/components/admin/AdminGuard";
import { AdminSidebar, AdminTopbar, CommandPalette } from "@/components/admin/layout";

export default async function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const isLoginPage = false; // handled by AdminGuard redirect

  return (
    <AdminGuard locale={locale}>
      <div className="min-h-screen flex bg-[#F5F5F5] dark:bg-[#0F0F12]">
        <AdminSidebar locale={locale} />

        <div className="flex-1 flex flex-col min-w-0">
          <AdminTopbar locale={locale} />
          <main className="flex-1 p-4 md:p-6">{children}</main>
        </div>

        <CommandPalette locale={locale} />
      </div>
    </AdminGuard>
  );
}
