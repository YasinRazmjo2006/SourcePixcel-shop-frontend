import { notFound } from "next/navigation";
import type { Locale } from "@/lib/types";
import { getOrderById, mockOrders } from "@/lib/data";
import { OrderDetailView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string; id: string }>;
}

// ✅ generateStaticParams — required for static export
export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    mockOrders.map((order) => ({ locale, id: order.id }))
  );
}

export default async function OrderDetailPage({ params }: PageProps) {
  const { locale, id } = await params;
  const order = getOrderById(id);
  if (!order) notFound();
  return <OrderDetailView locale={locale as Locale} order={order} />;
}