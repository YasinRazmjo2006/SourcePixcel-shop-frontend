# 01_base.py
# ساخت پایه پروژه SourcePixcel
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# package.json
# ============================================================
files.append(("package.json", """{
  "name": "sourcepixcel",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "15.5.9",
    "react": "19.2.0",
    "react-dom": "19.2.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^19",
    "@types/react-dom": "^19",
    "typescript": "^5",
    "tailwindcss": "^3.4.0",
    "postcss": "^8",
    "autoprefixer": "^10"
  }
}"""))

# ============================================================
# next.config.js
# ============================================================
files.append(("next.config.js", """/** @type {import('next').NextConfig} */
const nextConfig = {
  images: { unoptimized: true },
};
module.exports = nextConfig;
"""))

# ============================================================
# tsconfig.json
# ============================================================
files.append(("tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}"""))

# ============================================================
# tailwind.config.ts
# ============================================================
files.append(("tailwind.config.ts", """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#EF4056",
        secondary: "#00BFFF",
        dark: "#3F4064",
        muted: "#62666D",
        light: "#A1A3A8",
        border: "#E0E0E2",
        bg: "#F5F5F5",
      },
      fontFamily: {
        sans: ["system-ui", "-apple-system", "Segoe UI", "Tahoma", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
"""))

# ============================================================
# postcss.config.js
# ============================================================
files.append(("postcss.config.js", """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
"""))

# ============================================================
# .gitignore
# ============================================================
files.append((".gitignore", """node_modules
.next
out
.env
.env.local
*.log
.DS_Store
"""))

# ============================================================
# app/globals.css
# ============================================================
files.append(("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  box-sizing: border-box;
}

html,
body {
  padding: 0;
  margin: 0;
  font-family: system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
  background: #F5F5F5;
  color: #3F4064;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  cursor: pointer;
}

[dir="rtl"] {
  text-align: right;
}

[dir="ltr"] {
  text-align: left;
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #F5F5F5;
}
::-webkit-scrollbar-thumb {
  background: #E0E0E2;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #A1A3A8;
}
"""))

# ============================================================
# app/layout.tsx (ROOT — only file with <html>/<body>)
# ============================================================
files.append(("app/layout.tsx", """import "./globals.css";

export const metadata = {
  title: "SourcePixcel",
  description: "Bilingual e-commerce store (Persian/English)",
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
"""))

# ============================================================
# app/page.tsx (redirect / -> /fa)
# ============================================================
files.append(("app/page.tsx", """import { redirect } from "next/navigation";

export default function Home() {
  redirect("/fa");
}
"""))

# ============================================================
# app/not-found.tsx
# ============================================================
files.append(("app/not-found.tsx", """import Link from "next/link";

export default function NotFound() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        padding: 32,
        textAlign: "center",
      }}
    >
      <h1 style={{ fontSize: 72, fontWeight: "bold", color: "#EF4056", margin: 0 }}>
        404
      </h1>
      <p style={{ marginTop: 16, color: "#62666D", fontSize: 18 }}>
        صفحه‌ای که دنبالش هستید پیدا نشد.
      </p>
      <p style={{ color: "#A1A3A8", fontSize: 14 }}>
        The page you are looking for was not found.
      </p>
      <Link
        href="/fa"
        style={{
          marginTop: 24,
          color: "#EF4056",
          textDecoration: "underline",
          fontSize: 16,
        }}
      >
        بازگشت به خانه / Back to home
      </Link>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/layout.tsx (locale wrapper — NO html/body)
# ============================================================
files.append(("app/[locale]/layout.tsx", """export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const isFa = locale === "fa";
  const dir = isFa ? "rtl" : "ltr";

  return (
    <div dir={dir} lang={locale} style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      <header
        style={{
          background: "#FFFFFF",
          padding: "0 24px",
          boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
          position: "sticky",
          top: 0,
          zIndex: 100,
        }}
      >
        <div
          style={{
            maxWidth: 1400,
            margin: "0 auto",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            height: 64,
            gap: 16,
          }}
        >
          <a
            href={`/${locale}`}
            style={{
              fontSize: 22,
              fontWeight: "bold",
              color: "#EF4056",
            }}
          >
            SourcePixcel
          </a>

          <nav style={{ display: "flex", gap: 24, fontSize: 15 }}>
            <a href={`/${locale}`} style={{ color: "#3F4064" }}>
              {isFa ? "خانه" : "Home"}
            </a>
            <a href={`/${locale}/products`} style={{ color: "#3F4064" }}>
              {isFa ? "محصولات" : "Products"}
            </a>
          </nav>

          <div style={{ display: "flex", gap: 8, fontSize: 14 }}>
            <a
              href="/fa"
              style={{
                color: isFa ? "#EF4056" : "#62666D",
                fontWeight: isFa ? "bold" : "normal",
              }}
            >
              FA
            </a>
            <span style={{ color: "#E0E0E2" }}>|</span>
            <a
              href="/en"
              style={{
                color: !isFa ? "#EF4056" : "#62666D",
                fontWeight: !isFa ? "bold" : "normal",
              }}
            >
              EN
            </a>
          </div>
        </div>
      </header>

      <main style={{ flex: 1 }}>{children}</main>

      <footer
        style={{
          background: "#FFFFFF",
          borderTop: "1px solid #E0E0E2",
          padding: "24px",
          textAlign: "center",
          color: "#62666D",
          fontSize: 13,
        }}
      >
        © {new Date().getFullYear()} SourcePixcel —{" "}
        {isFa ? "تمامی حقوق محفوظ است." : "All rights reserved."}
      </footer>
    </div>
  );
}
"""))

# ============================================================
# app/[locale]/page.tsx (home placeholder)
# ============================================================
files.append(("app/[locale]/page.tsx", """export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const isFa = locale === "fa";

  return (
    <div style={{ maxWidth: 1400, margin: "0 auto", padding: 32 }}>
      <h1 style={{ fontSize: 28, fontWeight: "bold", marginBottom: 8, marginTop: 0 }}>
        {isFa ? "به SourcePixcel خوش آمدید" : "Welcome to SourcePixcel"}
      </h1>
      <p style={{ color: "#62666D", marginBottom: 32 }}>
        {isFa ? "پایه پروژه آماده است. منتظر مرحله بعد..." : "Base project ready. Waiting for next step..."}
      </p>
    </div>
  );
}
"""))

# ============================================================
# messages/fa.json
# ============================================================
files.append(("messages/fa.json", """{
  "home": {
    "title": "SourcePixcel",
    "welcome": "به SourcePixcel خوش آمدید"
  }
}"""))

# ============================================================
# messages/en.json
# ============================================================
files.append(("messages/en.json", """{
  "home": {
    "title": "SourcePixcel",
    "welcome": "Welcome to SourcePixcel"
  }
}"""))

# ============================================================
# README.md
# ============================================================
files.append(("README.md", """# SourcePixcel

Bilingual (Persian/English) e-commerce frontend.

## Stack
- Next.js 15.5.9
- React 19.2.0
- TypeScript 5
- Tailwind CSS 3.4

## Run
    npm install --registry=https://mirror-npm.runflare.com
    npm run dev

## URLs
- Persian: http://localhost:3000/fa
- English: http://localhost:3000/en
"""))

# ============================================================
# EMPTY FOLDERS (with .gitkeep)
# ============================================================
EMPTY_FOLDERS = [
    "components/layout",
    "components/home",
    "components/product",
    "components/cart",
    "components/ui",
    "components/common",
    "lib/types",
    "lib/data",
    "lib/stores",
    "lib/utils",
    "public/images",
]

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Base Project")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\nCreating empty folders...")
    for folder in EMPTY_FOLDERS:
        full_path = os.path.join(BASE, *folder.split("/"))
        try:
            os.makedirs(full_path, exist_ok=True)
            gitkeep = os.path.join(full_path, ".gitkeep")
            if not os.path.exists(gitkeep):
                with open(gitkeep, "w") as f:
                    f.write("")
            print(f"  [DIR]  {folder}/")
        except Exception as e:
            print(f"  [FAIL] {folder} -> {e}")

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("\nNext steps:")
        print("  1) npm install --registry=https://mirror-npm.runflare.com")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa")
        print("\nThen run 02_types.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()