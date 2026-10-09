import type { Locale } from "@/lib/types";
import { ProfileView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ProfilePage({ params }: PageProps) {
  const { locale } = await params;
  return <ProfileView locale={locale as Locale} />;
}
