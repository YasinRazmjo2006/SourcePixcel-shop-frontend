# 06_footer.py
# ساخت فوتر Digikala-style
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/layout/Footer.tsx
# ============================================================
files.append(("components/layout/Footer.tsx", """import Link from "next/link";
import {
  Instagram,
  Twitter,
  Linkedin,
  Youtube,
  Phone,
  Mail,
  MapPin,
  ShieldCheck,
  Truck,
  RotateCcw,
  Headphones,
  Award,
} from "lucide-react";
import type { Locale } from "@/lib/types";

interface FooterProps {
  locale: Locale;
}

export default function Footer({ locale }: FooterProps) {
  const isFa = locale === "fa";

  const t = {
    aboutTitle: isFa ? "درباره SourcePixcel" : "About SourcePixcel",
    aboutText: isFa
      ? "SourcePixcel یک فروشگاه اینترنتی مدرن است که با هدف ارائه بهترین تجربه خرید آنلاین برای کاربران ایرانی طراحی شده است."
      : "SourcePixcel is a modern online store designed to provide the best online shopping experience for Iranian users.",
    customerService: isFa ? "خدمات مشتریان" : "Customer Service",
    quickLinks: isFa ? "دسترسی سریع" : "Quick Links",
    followUs: isFa ? "با ما همراه باشید" : "Follow Us",
    contact: isFa ? "تماس با ما" : "Contact Us",
    faq: isFa ? "سوالات متداول" : "FAQ",
    returns: isFa ? "رویه بازگرداندن کالا" : "Return Policy",
    shipping: isFa ? "شرایط ارسال" : "Shipping Info",
    privacy: isFa ? "حریم خصوصی" : "Privacy Policy",
    terms: isFa ? "شرایط استفاده" : "Terms of Use",
    about: isFa ? "درباره ما" : "About Us",
    contactLink: isFa ? "تماس با ما" : "Contact Us",
    blog: isFa ? "وبلاگ" : "Blog",
    careers: isFa ? "فرصت‌های شغلی" : "Careers",
    freeShipping: isFa ? "ارسال سریع" : "Fast Shipping",
    securePayment: isFa ? "پرداخت امن" : "Secure Payment",
    returnGuarantee: isFa ? "۷ روز ضمانت بازگشت" : "7-Day Return",
    support: isFa ? "پشتیبانی ۲۴/۷" : "24/7 Support",
    authentic: isFa ? "ضمانت اصالت کالا" : "Authentic Products",
    copyright: isFa
      ? "تمامی حقوق مادی و معنوی این سایت متعلق به SourcePixcel می‌باشد."
      : "All rights reserved by SourcePixcel.",
  };

  const serviceBadges = [
    { icon: Truck, label: t.freeShipping },
    { icon: ShieldCheck, label: t.securePayment },
    { icon: RotateCcw, label: t.returnGuarantee },
    { icon: Headphones, label: t.support },
    { icon: Award, label: t.authentic },
  ];

  const customerServiceLinks = [
    { href: `/${locale}/faq`, label: t.faq },
    { href: `/${locale}/returns`, label: t.returns },
    { href: `/${locale}/shipping`, label: t.shipping },
    { href: `/${locale}/contact`, label: t.contactLink },
  ];

  const quickLinks = [
    { href: `/${locale}/about`, label: t.about },
    { href: `/${locale}/contact`, label: t.contactLink },
    { href: `/${locale}/blog`, label: t.blog },
    { href: `/${locale}/careers`, label: t.careers },
  ];

  const legalLinks = [
    { href: `/${locale}/privacy`, label: t.privacy },
    { href: `/${locale}/terms`, label: t.terms },
  ];

  const socialLinks = [
    { icon: Instagram, href: "https://instagram.com", label: "Instagram" },
    { icon: Twitter, href: "https://twitter.com", label: "Twitter" },
    { icon: Linkedin, href: "https://linkedin.com", label: "LinkedIn" },
    { icon: Youtube, href: "https://youtube.com", label: "YouTube" },
  ];

  return (
    <footer className="bg-white border-t border-[#E0E0E2] mt-12">
      {/* ── Service badges row ──────────────────────────────────────── */}
      <div className="border-b border-[#E0E0E2]">
        <div className="max-w-[1400px] mx-auto px-4 py-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {serviceBadges.map((badge, i) => {
              const Icon = badge.icon;
              return (
                <div
                  key={i}
                  className="flex flex-col items-center gap-2 text-center"
                >
                  <div className="w-12 h-12 rounded-full bg-[#F5F5F5] flex items-center justify-center">
                    <Icon size={22} className="text-[#62666D]" />
                  </div>
                  <span className="text-[12px] text-[#62666D]">
                    {badge.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* ── Main footer columns ────────────────────────────────────── */}
      <div className="max-w-[1400px] mx-auto px-4 py-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] mb-4">
              {t.aboutTitle}
            </h3>
            <p className="text-[12px] text-[#62666D] leading-6">
              {t.aboutText}
            </p>
          </div>

          {/* Customer Service */}
          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] mb-4">
              {t.customerService}
            </h3>
            <ul className="space-y-2">
              {customerServiceLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-[12px] text-[#62666D] hover:text-[#EF4056] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] mb-4">
              {t.quickLinks}
            </h3>
            <ul className="space-y-2">
              {quickLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-[12px] text-[#62666D] hover:text-[#EF4056] transition-colors"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact + Social */}
          <div>
            <h3 className="text-[14px] font-bold text-[#3F4064] mb-4">
              {t.contact}
            </h3>
            <ul className="space-y-3 mb-6">
              <li className="flex items-center gap-2 text-[12px] text-[#62666D]">
                <Phone size={14} className="text-[#A1A3A8] shrink-0" />
                <span dir="ltr">021-12345678</span>
              </li>
              <li className="flex items-center gap-2 text-[12px] text-[#62666D]">
                <Mail size={14} className="text-[#A1A3A8] shrink-0" />
                <span dir="ltr">support@sourcepixcel.com</span>
              </li>
              <li className="flex items-start gap-2 text-[12px] text-[#62666D]">
                <MapPin size={14} className="text-[#A1A3A8] shrink-0 mt-0.5" />
                <span>
                  {isFa
                    ? "تهران، خیابان ولیعصر، پلاک ۱۲۳"
                    : "Tehran, Valiasr St., No. 123"}
                </span>
              </li>
            </ul>

            <h3 className="text-[14px] font-bold text-[#3F4064] mb-3">
              {t.followUs}
            </h3>
            <div className="flex items-center gap-3">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.label}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={social.label}
                    className="w-9 h-9 rounded-full bg-[#F5F5F5] flex items-center justify-center text-[#62666D] hover:bg-[#EF4056] hover:text-white transition-colors"
                  >
                    <Icon size={16} />
                  </a>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* ── Trust badges + Legal ──────────────────────────────────── */}
      <div className="border-t border-[#E0E0E2]">
        <div className="max-w-[1400px] mx-auto px-4 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            {/* Trust badges */}
            <div className="flex items-center gap-4 flex-wrap justify-center">
              <div className="w-16 h-16 bg-[#F5F5F5] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "نماد اعتماد" : "Trust Seal"}
              </div>
              <div className="w-16 h-16 bg-[#F5F5F5] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "ساماندهی" : "Regulated"}
              </div>
              <div className="w-16 h-16 bg-[#F5F5F5] rounded-lg flex items-center justify-center text-[10px] text-[#A1A3A8] text-center leading-tight">
                {isFa ? "اتحادیه" : "Union"}
              </div>
            </div>

            {/* Legal links */}
            <div className="flex items-center gap-4 flex-wrap justify-center">
              {legalLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="text-[12px] text-[#62666D] hover:text-[#EF4056] transition-colors"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* ── Copyright ─────────────────────────────────────────────── */}
      <div className="border-t border-[#E0E0E2] bg-[#F5F5F5]">
        <div className="max-w-[1400px] mx-auto px-4 py-4 text-center">
          <p className="text-[12px] text-[#A1A3A8]">
            © {new Date().getFullYear()} SourcePixcel — {t.copyright}
          </p>
        </div>
      </div>
    </footer>
  );
}
"""))

# ============================================================
# app/[locale]/layout.tsx (updated to use Footer)
# ============================================================
files.append(("app/[locale]/layout.tsx", """import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import type { Locale } from "@/lib/types";

export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div
      dir={locale === "fa" ? "rtl" : "ltr"}
      lang={locale}
      style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}
    >
      <Header locale={locale as Locale} />
      <main style={{ flex: 1 }}>{children}</main>
      <Footer locale={locale as Locale} />
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 06: Footer")
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

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("Next: run 07_product_card.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()