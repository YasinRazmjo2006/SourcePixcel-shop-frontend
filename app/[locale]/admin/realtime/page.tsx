import RealtimeView from "@/components/admin/realtime/RealtimeView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminRealtimePage({ params }: PageProps) {
  const { locale } = await params;
  return <RealtimeView locale={locale as "fa" | "en"} />;
}
