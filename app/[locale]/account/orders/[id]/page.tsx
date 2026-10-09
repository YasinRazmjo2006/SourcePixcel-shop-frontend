import { notFound } from "next/navigation";
import type { Locale } from "@/lib/types";
import { getOrderById } from "@/lib/data";
import { OrderDetailView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string; id: string }>;
}

export default async function OrderDetailPage({ params }: PageProps) {
  const { locale, id } = await params;
  const order = getOrderById(id);
  if (!order) notFound();
  return <OrderDetailView locale={locale as Locale} order={order} />;
}
