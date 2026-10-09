import type { Locale } from "@/lib/types";
import { CheckoutPage } from "@/components/checkout";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CheckoutRoute({ params }: PageProps) {
  const { locale } = await params;
  return <CheckoutPage locale={locale as Locale} />;
}
