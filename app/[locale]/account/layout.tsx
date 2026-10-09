import type { Locale } from "@/lib/types";
import AccountSidebar from "@/components/account/AccountSidebar";
import AccountGuard from "@/components/account/AccountGuard";

export default async function AccountLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AccountGuard locale={typedLocale}>
      <div className="max-w-[1400px] mx-auto px-4 py-4">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <div className="lg:col-span-1">
            <AccountSidebar locale={typedLocale} />
          </div>
          <div className="lg:col-span-3">{children}</div>
        </div>
      </div>
    </AccountGuard>
  );
}