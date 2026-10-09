import type { Locale } from "@/lib/types";
import { CartPage } from "@/components/cart";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function CartRoute({ params }: PageProps) {
  const { locale } = await params;
  return <CartPage locale={locale as Locale} />;
}
