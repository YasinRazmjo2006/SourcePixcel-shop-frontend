import type { Locale } from "@/lib/types";
import { OrdersView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function OrdersPage({ params }: PageProps) {
  const { locale } = await params;
  return <OrdersView locale={locale as Locale} />;
}
