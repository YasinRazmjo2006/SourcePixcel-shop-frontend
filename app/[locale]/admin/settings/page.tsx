import SettingsView from "@/components/admin/SettingsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminSettingsPage({ params }: PageProps) {
  const { locale } = await params;
  return <SettingsView locale={locale as "fa" | "en"} />;
}
