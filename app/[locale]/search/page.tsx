import { Suspense } from "react";
import type { Locale } from "@/lib/types";
import { SearchPage } from "@/components/search";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SearchRoute({ params }: PageProps) {
  const { locale } = await params;
  return (
    <Suspense
      fallback={
        <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
          Loading...
        </div>
      }
    >
      <SearchPage locale={locale as Locale} />
    </Suspense>
  );
}
