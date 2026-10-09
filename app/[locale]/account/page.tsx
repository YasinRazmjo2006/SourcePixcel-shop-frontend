import type { Locale } from "@/lib/types";
import { DashboardView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AccountPage({ params }: PageProps) {
  const { locale } = await params;
  return <DashboardView locale={locale as Locale} />;
}
