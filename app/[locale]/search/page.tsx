import { Suspense } from "react";
import type { Locale } from "@/lib/types";
import { SearchPage } from "@/components/search";
import LoadingScreen from "@/components/common/LoadingScreen";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SearchRoute({ params }: PageProps) {
  const { locale } = await params;
  return (
    <Suspense
      fallback={
        <LoadingScreen label={locale === "fa" ? "در حال جستجو..." : "Searching..."} />
      }
    >
      <SearchPage locale={locale as Locale} />
    </Suspense>
  );
}
