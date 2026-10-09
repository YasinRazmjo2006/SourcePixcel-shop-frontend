import type { Locale } from "@/lib/types";
import { ComparePage } from "@/components/compare";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export const metadata = {
  title: "Compare — SourcePixcel",
  description: "Compare products side by side.",
};

export default async function CompareRoute({ params }: PageProps) {
  const { locale } = await params;
  return <ComparePage locale={locale as Locale} />;
}
