import Link from "next/link";
import type { Locale } from "@/lib/types";

interface AuthCardProps {
  locale: Locale;
  titleFa: string;
  titleEn: string;
  subtitleFa?: string;
  subtitleEn?: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export default function AuthCard({
  locale,
  titleFa,
  titleEn,
  subtitleFa,
  subtitleEn,
  children,
  footer,
}: AuthCardProps) {
  const isFa = locale === "fa";

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center px-4 py-8 bg-[#F5F5F5]">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl border border-[#E0E0E2] p-6 md:p-8 shadow-sm">
          {/* Logo */}
          <Link
            href={`/${locale}`}
            className="flex items-center justify-center mb-6"
          >
            <span className="text-[#EF4056] font-bold text-2xl">
              SourcePixcel
            </span>
          </Link>

          {/* Header */}
          <div className="text-center mb-6">
            <h1 className="text-[18px] font-bold text-[#3F4064] mb-2">
              {isFa ? titleFa : titleEn}
            </h1>
            {(subtitleFa || subtitleEn) && (
              <p className="text-[12px] text-[#62666D] leading-5">
                {isFa ? subtitleFa : subtitleEn}
              </p>
            )}
          </div>

          {children}
        </div>

        {footer && <div className="mt-4">{footer}</div>}
      </div>
    </div>
  );
}
