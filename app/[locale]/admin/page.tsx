import DashboardView from "@/components/admin/DashboardView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminDashboardPage({ params }: PageProps) {
  const { locale } = await params;
  return <DashboardView locale={locale} />;
}
