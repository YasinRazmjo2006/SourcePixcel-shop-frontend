import "./globals.css";
import ThemeProvider from "@/components/common/ThemeProvider";
import { vazirmatn, inter } from "@/lib/fonts";

export const metadata = {
  title: "SourcePixcel — فروشگاه آنلاین مدرن",
  description: "فروشگاه اینترنتی SourcePixcel | خرید آنلاین با ارسال سریع و ضمانت اصالت",
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
    <html
      lang="fa"
      dir="rtl"
      suppressHydrationWarning
      className={`${vazirmatn.variable} ${inter.variable}`}
    >
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function() {
                try {
                  const stored = localStorage.getItem('sourcepixcel-theme');
                  if (stored) {
                    const parsed = JSON.parse(stored);
                    if (parsed && parsed.state && parsed.state.mode === 'dark') {
                      document.documentElement.classList.add('dark');
                    }
                  }
                } catch (e) {}
              })();
            `,
          }}
        />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}
