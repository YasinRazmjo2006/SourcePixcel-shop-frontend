import AnalyticsView from "@/components/admin/AnalyticsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminAnalyticsPage({ params }: PageProps) {
  const { locale } = await params;
  return <AnalyticsView locale={locale as "fa" | "en"} />;
}
