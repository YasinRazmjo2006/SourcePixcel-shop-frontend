import ReportsView from "@/components/admin/ReportsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminReportsPage({ params }: PageProps) {
  const { locale } = await params;
  return <ReportsView locale={locale as "fa" | "en"} />;
}
