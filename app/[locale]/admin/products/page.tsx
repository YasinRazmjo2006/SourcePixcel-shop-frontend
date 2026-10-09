import ProductsView from "@/components/admin/ProductsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminProductsPage({ params }: PageProps) {
  const { locale } = await params;
  return <ProductsView locale={locale} />;
}
