import OrdersView from "@/components/admin/OrdersView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminOrdersPage({ params }: PageProps) {
  const { locale } = await params;
  return <OrdersView locale={locale} />;
}
