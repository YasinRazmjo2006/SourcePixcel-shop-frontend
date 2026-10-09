import type { Locale } from "@/lib/types";
import { WishlistView } from "@/components/account";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function WishlistPage({ params }: PageProps) {
  const { locale } = await params;
  return <WishlistView locale={locale as Locale} />;
}
