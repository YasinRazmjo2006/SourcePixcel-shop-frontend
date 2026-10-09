import type { Locale } from "@/lib/types";
import { AuthCard, RegisterForm } from "@/components/auth";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function RegisterPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;

  return (
    <AuthCard
      locale={typedLocale}
      titleFa="ایجاد حساب کاربری"
      titleEn="Create your account"
      subtitleFa="برای ثبت‌نام، فرم زیر را تکمیل کنید."
      subtitleEn="Fill in the form below to create your account."
    >
      <RegisterForm locale={typedLocale} />
    </AuthCard>
  );
}
