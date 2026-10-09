import type { Locale } from "@/lib/types";
import { AuthCard, ForgotPasswordForm } from "@/components/auth";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ForgotPasswordPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AuthCard
      locale={typedLocale}
      titleFa="بازیابی رمز عبور"
      titleEn="Reset your password"
      subtitleFa="شماره موبایل خود را وارد کنید تا کد بازیابی برای شما ارسال شود."
      subtitleEn="Enter your mobile number to receive a reset code."
    >
      <ForgotPasswordForm locale={typedLocale} />
    </AuthCard>
  );
}
