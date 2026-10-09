import type { Locale } from "@/lib/types";
import { AddressesView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AddressesPage({ params }: PageProps) {
  const { locale } = await params;
  return <AddressesView locale={locale as Locale} />;
}
