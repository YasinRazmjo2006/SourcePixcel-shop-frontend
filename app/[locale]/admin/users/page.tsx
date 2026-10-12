import UsersView from "@/components/admin/UsersView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminUsersPage({ params }: PageProps) {
  const { locale } = await params;
  return <UsersView locale={locale as "fa" | "en"} />;
}
