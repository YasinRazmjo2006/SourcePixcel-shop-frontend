import type { Locale } from "@/lib/types";
import { AuthCard, LoginForm } from "@/components/auth";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function LoginPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AuthCard
      locale={typedLocale}
      titleFa="ورود به حساب کاربری"
      titleEn="Sign in to your account"
      subtitleFa="برای دسترسی به حساب کاربری، شماره موبایل و رمز عبور خود را وارد کنید."
      subtitleEn="Enter your mobile number and password to access your account."
    >
      <LoginForm locale={typedLocale} />
    </AuthCard>
  );
}
