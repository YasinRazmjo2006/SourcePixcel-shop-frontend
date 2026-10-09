import AdminLoginForm from "@/components/admin/AdminLoginForm";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminLoginPage({ params }: PageProps) {
  const { locale } = await params;
  return <AdminLoginForm locale={locale} />;
}
