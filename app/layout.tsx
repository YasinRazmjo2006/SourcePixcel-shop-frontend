import "./globals.css";

export const metadata = {
  title: "SourcePixcel",
  description: "Bilingual e-commerce store (Persian/English)",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
