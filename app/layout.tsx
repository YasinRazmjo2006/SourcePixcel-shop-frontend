import "./globals.css";
import ThemeProvider from "@/components/common/ThemeProvider";

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
    >
      <head>
        {/* Preconnect for faster font loading */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />

        {/* Vazirmatn (Persian) */}
        <link
          href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap"
          rel="stylesheet"
        />

        {/* Inter (English) */}
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
          rel="stylesheet"
        />

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