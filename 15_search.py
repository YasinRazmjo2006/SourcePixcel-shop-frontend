# 15_search.py
# ساخت صفحه جستجو و صفحات تکمیلی
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# components/search/SearchPage.tsx
# ============================================================
files.append(("components/search/SearchPage.tsx", """"use client";

import { useState, useMemo, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { Search as SearchIcon, X } from "lucide-react";
import type { Locale, Product, SortOption } from "@/lib/types";
import { products as allProducts } from "@/lib/data";
import ProductCard from "@/components/product/ProductCard";
import ProductSort from "@/components/product/ProductSort";
import Pagination from "@/components/common/Pagination";
import EmptyState from "@/components/common/EmptyState";
import { Breadcrumb } from "@/components/common";

interface SearchPageProps {
  locale: Locale;
}

const PER_PAGE = 12;

export default function SearchPage({ locale }: SearchPageProps) {
  const isFa = locale === "fa";
  const params = useSearchParams();

  const initialQuery = params.get("q") ?? "";
  const [query, setQuery] = useState(initialQuery);
  const [inputValue, setInputValue] = useState(initialQuery);
  const [sort, setSort] = useState<SortOption>("popular");
  const [page, setPage] = useState(1);

  useEffect(() => {
    setInputValue(query);
  }, [query]);

  const results = useMemo(() => {
    if (!query.trim()) return [];
    const q = query.toLowerCase().trim();
    let result = allProducts.filter((p) => {
      const titleFa = p.titleFa.toLowerCase();
      const titleEn = p.titleEn.toLowerCase();
      const brand = p.brand.toLowerCase();
      const tags = p.tags.join(" ").toLowerCase();
      return (
        titleFa.includes(q) ||
        titleEn.includes(q) ||
        brand.includes(q) ||
        tags.includes(q)
      );
    });

    switch (sort) {
      case "newest":
        result.sort((a, b) => b.id - a.id);
        break;
      case "price-asc":
        result.sort((a, b) => a.finalPrice - b.finalPrice);
        break;
      case "price-desc":
        result.sort((a, b) => b.finalPrice - a.finalPrice);
        break;
      case "rating":
        result.sort((a, b) => b.rating - a.rating);
        break;
      default:
        result.sort((a, b) => b.reviewCount - a.reviewCount);
    }

    return result;
  }, [query, sort]);

  useEffect(() => {
    setPage(1);
  }, [query, sort]);

  const totalPages = Math.ceil(results.length / PER_PAGE);
  const paginated = results.slice((page - 1) * PER_PAGE, page * PER_PAGE);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setQuery(inputValue.trim());
  };

  const clearSearch = () => {
    setInputValue("");
    setQuery("");
  };

  const t = {
    title: isFa ? "جستجو" : "Search",
    placeholder: isFa ? "جستجو در SourcePixcel" : "Search in SourcePixcel",
    hint: isFa
      ? "نام محصول، برند یا دسته‌بندی خود را وارد کنید."
      : "Enter a product name, brand, or category.",
    resultsFor: isFa ? "نتایج برای" : "Results for",
    clear: isFa ? "پاک کردن" : "Clear",
  };

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "جستجو", labelEn: "Search" }]}
      />

      <h1 className="text-[20px] font-bold text-[#3F4064] mb-4">{t.title}</h1>

      {/* Search input */}
      <form onSubmit={handleSubmit} className="mb-5">
        <div className="relative max-w-2xl">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={t.placeholder}
            autoFocus
            className="w-full h-12 rounded-lg bg-white border border-[#E0E0E2] text-[14px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none focus:border-[#EF4056] transition-colors"
            style={{
              paddingRight: isFa ? 100 : 16,
              paddingLeft: isFa ? 16 : 100,
            }}
          />
          <div
            className="absolute top-1/2 -translate-y-1/2 flex items-center gap-1"
            style={{ [isFa ? "left" : "right"]: 8 } as React.CSSProperties}
          >
            {inputValue && (
              <button
                type="button"
                onClick={clearSearch}
                aria-label={t.clear}
                className="w-8 h-8 rounded-lg flex items-center justify-center text-[#A1A3A8] hover:bg-[#F5F5F5]"
              >
                <X size={16} />
              </button>
            )}
            <button
              type="submit"
              className="h-9 px-3 rounded-lg bg-[#EF4056] text-white flex items-center justify-center hover:bg-[#d63850] transition-colors"
            >
              <SearchIcon size={16} />
            </button>
          </div>
        </div>
      </form>

      {/* No query */}
      {!query && (
        <div className="bg-white rounded-lg border border-[#E0E0E2] py-16 px-4 text-center">
          <div className="w-16 h-16 rounded-full bg-[#F5F5F5] flex items-center justify-center mx-auto mb-4">
            <SearchIcon size={28} className="text-[#A1A3A8]" />
          </div>
          <p className="text-[13px] text-[#62666D] max-w-md mx-auto">
            {t.hint}
          </p>
        </div>
      )}

      {/* Results */}
      {query && (
        <>
          <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
            <h2 className="text-[14px] text-[#62666D]">
              {t.resultsFor}{" "}
              <span className="font-bold text-[#3F4064]">"{query}"</span>
            </h2>
          </div>

          {paginated.length === 0 ? (
            <div className="bg-white rounded-lg border border-[#E0E0E2]">
              <EmptyState
                locale={locale}
                titleFa="نتیجه‌ای یافت نشد"
                titleEn="No results found"
                messageFa="متأسفانه محصولی با این عبارت پیدا نشد. عبارت دیگری را امتحان کنید."
                messageEn="No products matched your search. Try another keyword."
              />
            </div>
          ) : (
            <>
              <ProductSort
                value={sort}
                onChange={setSort}
                locale={locale}
                resultCount={results.length}
              />

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mt-3">
                {paginated.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                    locale={locale}
                  />
                ))}
              </div>

              <Pagination
                currentPage={page}
                totalPages={totalPages}
                onPageChange={setPage}
                locale={locale}
              />
            </>
          )}
        </>
      )}
    </div>
  );
}
"""))

# ============================================================
# components/search/index.ts
# ============================================================
files.append(("components/search/index.ts", """// components/search/index.ts
export { default as SearchPage } from "./SearchPage";
"""))

# ============================================================
# components/common/StaticPage.tsx
# ============================================================
files.append(("components/common/StaticPage.tsx", """import type { Locale } from "@/lib/types";
import Breadcrumb from "./Breadcrumb";

interface StaticPageProps {
  locale: Locale;
  titleFa: string;
  titleEn: string;
  breadcrumbFa: string;
  breadcrumbEn: string;
  children: React.ReactNode;
}

export default function StaticPage({
  locale,
  titleFa,
  titleEn,
  breadcrumbFa,
  breadcrumbEn,
  children,
}: StaticPageProps) {
  const isFa = locale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: breadcrumbFa, labelEn: breadcrumbEn }]}
      />

      <div className="bg-white rounded-lg border border-[#E0E0E2] p-6 md:p-8">
        <h1 className="text-[22px] font-bold text-[#3F4064] mb-6">
          {isFa ? titleFa : titleEn}
        </h1>
        <div className="prose prose-sm max-w-none text-[13px] text-[#62666D] leading-7 space-y-4">
          {children}
        </div>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/common/index.ts (updated)
# ============================================================
files.append(("components/common/index.ts", """// components/common/index.ts
export { default as Breadcrumb } from "./Breadcrumb";
export { default as Pagination } from "./Pagination";
export { default as EmptyState } from "./EmptyState";
export { default as StaticPage } from "./StaticPage";
"""))

# ============================================================
# app/[locale]/search/page.tsx
# ============================================================
files.append(("app/[locale]/search/page.tsx", """import { Suspense } from "react";
import type { Locale } from "@/lib/types";
import { SearchPage } from "@/components/search";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function SearchRoute({ params }: PageProps) {
  const { locale } = await params;
  return (
    <Suspense
      fallback={
        <div className="max-w-[1400px] mx-auto px-4 py-8 text-center text-[#A1A3A8]">
          Loading...
        </div>
      }
    >
      <SearchPage locale={locale as Locale} />
    </Suspense>
  );
}
"""))

# ============================================================
# app/[locale]/about/page.tsx
# ============================================================
files.append(("app/[locale]/about/page.tsx", """import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AboutPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="درباره ما"
      titleEn="About Us"
      breadcrumbFa="درباره ما"
      breadcrumbEn="About"
    >
      {isFa ? (
        <>
          <p>
            <strong>SourcePixcel</strong> یک فروشگاه اینترنتی مدرن است که با هدف
            ارائه بهترین تجربه خرید آنلاین برای کاربران ایرانی طراحی شده است. ما
            با تمرکز بر کیفیت، اصالت کالا و خدمات مشتریان، تلاش می‌کنیم تا
            خرید آنلاین را برای شما ساده‌تر، سریع‌تر و مطمئن‌تر کنیم.
          </p>
          <h2 className="text-[16px] font-bold text-[#3F4064] mt-6 mb-2">
            چرا SourcePixcel؟
          </h2>
          <ul className="list-disc pr-5 space-y-1">
            <li>ارسال سریع به سراسر کشور</li>
            <li>ضمانت اصالت و سلامت کالا</li>
            <li>۷ روز مهلت بازگشت بدون قید و شرط</li>
            <li>پشتیبانی ۲۴ ساعته در ۷ روز هفته</li>
            <li>پرداخت امن از طریق درگاه‌های معتبر</li>
          </ul>
          <h2 className="text-[16px] font-bold text-[#3F4064] mt-6 mb-2">
            چشم‌انداز ما
          </h2>
          <p>
            ما می‌خواهیم به بزرگ‌ترین و معتبرترین فروشگاه آنلاین ایران تبدیل
            شویم و تجربه‌ای بی‌نظیر برای میلیون‌ها کاربر ایرانی فراهم کنیم.
          </p>
        </>
      ) : (
        <>
          <p>
            <strong>SourcePixcel</strong> is a modern online store designed to
            provide the best online shopping experience for Iranian users. With
            a focus on quality, authenticity, and customer service, we strive
            to make online shopping simpler, faster, and safer.
          </p>
          <h2 className="text-[16px] font-bold text-[#3F4064] mt-6 mb-2">
            Why SourcePixcel?
          </h2>
          <ul className="list-disc pl-5 space-y-1">
            <li>Fast shipping across the country</li>
            <li>Authenticity and health guarantee</li>
            <li>7-day no-questions-asked return</li>
            <li>24/7 support, 7 days a week</li>
            <li>Secure payment through trusted gateways</li>
          </ul>
          <h2 className="text-[16px] font-bold text-[#3F4064] mt-6 mb-2">
            Our Vision
          </h2>
          <p>
            We aim to become the largest and most trusted online store in Iran,
            providing an unmatched experience for millions of Iranian users.
          </p>
        </>
      )}
    </StaticPage>
  );
}
"""))

# ============================================================
# app/[locale]/contact/page.tsx
# ============================================================
files.append(("app/[locale]/contact/page.tsx", """import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";
import { Phone, Mail, MapPin, Clock } from "lucide-react";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function ContactPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  const items = [
    {
      icon: Phone,
      fa: { label: "تلفن پشتیبانی", value: "021-12345678" },
      en: { label: "Support Phone", value: "021-12345678" },
    },
    {
      icon: Mail,
      fa: { label: "ایمیل", value: "support@sourcepixcel.com" },
      en: { label: "Email", value: "support@sourcepixcel.com" },
    },
    {
      icon: MapPin,
      fa: { label: "آدرس", value: "تهران، خیابان ولیعصر، پلاک ۱۲۳" },
      en: { label: "Address", value: "Tehran, Valiasr St., No. 123" },
    },
    {
      icon: Clock,
      fa: { label: "ساعات پاسخگویی", value: "۲۴ ساعته، ۷ روز هفته" },
      en: { label: "Hours", value: "24/7" },
    },
  ];

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="تماس با ما"
      titleEn="Contact Us"
      breadcrumbFa="تماس با ما"
      breadcrumbEn="Contact"
    >
      <p>
        {isFa
          ? "تیم پشتیبانی SourcePixcel به صورت شبانه‌روزی آماده پاسخگویی به سوالات و مشکلات شماست."
          : "SourcePixcel support team is available 24/7 to answer your questions and help with any issues."}
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 not-prose mt-4">
        {items.map((item, i) => {
          const Icon = item.icon;
          const data = isFa ? item.fa : item.en;
          return (
            <div
              key={i}
              className="flex items-start gap-3 p-4 rounded-lg border border-[#E0E0E2] bg-[#FAFAFA]"
            >
              <div className="w-10 h-10 rounded-lg bg-white border border-[#E0E0E2] flex items-center justify-center shrink-0">
                <Icon size={18} className="text-[#EF4056]" />
              </div>
              <div>
                <div className="text-[11px] text-[#A1A3A8] mb-1">
                  {data.label}
                </div>
                <div className="text-[13px] text-[#3F4064] font-medium" dir={i < 2 ? "ltr" : "auto"}>
                  {data.value}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </StaticPage>
  );
}
"""))

# ============================================================
# app/[locale]/faq/page.tsx
# ============================================================
files.append(("app/[locale]/faq/page.tsx", """import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";

interface PageProps {
  params: Promise<{ locale: string }>;
}

const FAQ_ITEMS = [
  {
    fa: {
      q: "چطور می‌توانم سفارش خود را پیگیری کنم؟",
      a: "پس از ثبت سفارش، کد پیگیری از طریق پیامک برای شما ارسال می‌شود. می‌توانید از بخش «سفارشات من» در پنل کاربری نیز وضعیت سفارش را مشاهده کنید.",
    },
    en: {
      q: "How can I track my order?",
      a: "After placing an order, a tracking code is sent to you via SMS. You can also check your order status in the 'My Orders' section of your account.",
    },
  },
  {
    fa: {
      q: "شرایط بازگشت کالا چیست؟",
      a: "شما تا ۷ روز پس از دریافت کالا، در صورت عدم رضایت یا وجود مشکل، می‌توانید درخواست بازگشت ثبت کنید. کالا باید در بسته‌بندی اصلی و بدون آسیب باشد.",
    },
    en: {
      q: "What is the return policy?",
      a: "You can request a return within 7 days of receiving the product if you're not satisfied or if there's an issue. The product must be in its original packaging without damage.",
    },
  },
  {
    fa: {
      q: "هزینه ارسال چگونه محاسبه می‌شود؟",
      a: "هزینه ارسال بر اساس روش انتخابی و مقصد محاسبه می‌شود. برای سفارشات بالای ۵ میلیون تومان، ارسال رایگان است.",
    },
    en: {
      q: "How is the shipping cost calculated?",
      a: "Shipping cost depends on your selected method and destination. Orders above 5 million Toman qualify for free shipping.",
    },
  },
  {
    fa: {
      q: "آیا امکان پرداخت در محل وجود دارد؟",
      a: "در حال حاضر فقط پرداخت آنلاین از طریق درگاه‌های معتبر (زرین‌پال) پذیرفته می‌شود.",
    },
    en: {
      q: "Is cash on delivery available?",
      a: "Currently, only online payment through trusted gateways (Zarinpal) is accepted.",
    },
  },
  {
    fa: {
      q: "چگونه می‌توانم رمز عبور خود را بازیابی کنم؟",
      a: "از صفحه ورود، روی «رمز عبور را فراموش کرده‌اید؟» کلیک کنید و شماره موبایل خود را وارد کنید. کد بازیابی برای شما ارسال می‌شود.",
    },
    en: {
      q: "How can I recover my password?",
      a: "From the login page, click 'Forgot password?' and enter your mobile number. A reset code will be sent to you.",
    },
  },
];

export default async function FAQPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="سوالات متداول"
      titleEn="Frequently Asked Questions"
      breadcrumbFa="سوالات متداول"
      breadcrumbEn="FAQ"
    >
      <div className="not-prose space-y-3">
        {FAQ_ITEMS.map((item, i) => {
          const data = isFa ? item.fa : item.en;
          return (
            <details
              key={i}
              className="group border border-[#E0E0E2] rounded-lg overflow-hidden"
            >
              <summary className="cursor-pointer p-4 text-[13px] font-bold text-[#3F4064] hover:bg-[#F5F5F5] flex items-center justify-between">
                <span>{data.q}</span>
                <span className="text-[#EF4056] text-[16px] group-open:rotate-45 transition-transform">
                  +
                </span>
              </summary>
              <div className="px-4 pb-4 text-[12px] text-[#62666D] leading-6 border-t border-[#F5F5F5] pt-3">
                {data.a}
              </div>
            </details>
          );
        })}
      </div>
    </StaticPage>
  );
}
"""))

# ============================================================
# app/[locale]/terms/page.tsx
# ============================================================
files.append(("app/[locale]/terms/page.tsx", """import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function TermsPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="شرایط و قوانین"
      titleEn="Terms and Conditions"
      breadcrumbFa="شرایط و قوانین"
      breadcrumbEn="Terms"
    >
      {isFa ? (
        <>
          <p>
            استفاده از خدمات SourcePixcel به معنای پذیرش کامل قوانین و مقررات
            زیر است. لطفاً پیش از ثبت سفارش، این شرایط را به دقت مطالعه کنید.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۱. ثبت سفارش
          </h2>
          <p>
            کلیه سفارشات پس از تایید نهایی و پرداخت موفق، وارد مرحله پردازش
            می‌شوند. SourcePixcel مجاز است در صورت بروز مشکل در موجودی یا قیمت،
            سفارش را لغو و مبلغ را بازگرداند.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۲. قیمت‌ها و پرداخت
          </h2>
          <p>
            کلیه قیمت‌ها به تومان و شامل مالیات بر ارزش افزوده است. پرداخت از
            طریق درگاه‌های امن انجام می‌شود و SourcePixcel مسئولیتی در قبال
            اطلاعات کارت بانکی کاربران ندارد.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۳. ارسال و تحویل
          </h2>
          <p>
            زمان ارسال بر اساس روش انتخابی و مقصد متفاوت است. SourcePixcel
            تلاش می‌کند سفارشات را در سریع‌ترین زمان ارسال کند، اما در شرایط
            خاص (تعطیلات، حوادث غیرمترقبه) ممکن است تاخیر رخ دهد.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            ۴. بازگشت کالا
          </h2>
          <p>
            در صورت مغایرت کالا با توضیحات یا وجود ایراد فنی، تا ۷ روز پس از
            دریافت، امکان بازگشت وجود دارد. کالا باید در بسته‌بندی اصلی و سالم
            باشد.
          </p>
        </>
      ) : (
        <>
          <p>
            Using SourcePixcel services means full acceptance of the following
            terms and conditions. Please read them carefully before placing an
            order.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            1. Ordering
          </h2>
          <p>
            All orders enter the processing stage after final confirmation and
            successful payment. SourcePixcel may cancel an order and refund the
            amount if there's an issue with stock or pricing.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            2. Prices and Payment
          </h2>
          <p>
            All prices are in Toman and include VAT. Payments are made through
            secure gateways, and SourcePixcel is not responsible for users'
            banking card information.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            3. Shipping and Delivery
          </h2>
          <p>
            Delivery time varies based on the selected method and destination.
            SourcePixcel aims to ship orders as quickly as possible, but delays
            may occur under special circumstances.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            4. Returns
          </h2>
          <p>
            In case of a product mismatch or technical defect, a return can be
            requested within 7 days of receipt. The product must be in its
            original packaging and undamaged.
          </p>
        </>
      )}
    </StaticPage>
  );
}
"""))

# ============================================================
# app/[locale]/privacy/page.tsx
# ============================================================
files.append(("app/[locale]/privacy/page.tsx", """import type { Locale } from "@/lib/types";
import { StaticPage } from "@/components/common";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function PrivacyPage({ params }: PageProps) {
  const { locale } = await params;
  const typedLocale = locale as Locale;
  const isFa = typedLocale === "fa";

  return (
    <StaticPage
      locale={typedLocale}
      titleFa="حریم خصوصی"
      titleEn="Privacy Policy"
      breadcrumbFa="حریم خصوصی"
      breadcrumbEn="Privacy"
    >
      {isFa ? (
        <>
          <p>
            SourcePixcel متعهد به حفظ حریم خصوصی کاربران خود است. این سند
            نحوه جمع‌آوری، استفاده و محافظت از اطلاعات شخصی شما را توضیح می‌دهد.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            اطلاعاتی که جمع‌آوری می‌کنیم
          </h2>
          <ul className="list-disc pr-5 space-y-1">
            <li>نام و نام خانوادگی</li>
            <li>شماره موبایل و ایمیل</li>
            <li>آدرس ارسال سفارش</li>
            <li>تاریخچه سفارشات و بازدیدها</li>
          </ul>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            نحوه استفاده از اطلاعات
          </h2>
          <p>
            اطلاعات شما فقط برای پردازش سفارشات، ارسال، پشتیبانی و بهبود
            خدمات استفاده می‌شود. ما هیچ‌گاه اطلاعات شما را با اشخاص ثالث به
            اشتراک نمی‌گذاریم، مگر در چارچوب قانون.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            امنیت اطلاعات
          </h2>
          <p>
            کلیه اطلاعات از طریق پروتکل SSL رمزنگاری می‌شود و دسترسی به
            اطلاعات شما فقط برای کارکنان مجاز امکان‌پذیر است.
          </p>
        </>
      ) : (
        <>
          <p>
            SourcePixcel is committed to protecting the privacy of its users.
            This document explains how we collect, use, and protect your
            personal information.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            Information We Collect
          </h2>
          <ul className="list-disc pl-5 space-y-1">
            <li>Full name</li>
            <li>Mobile number and email</li>
            <li>Shipping address</li>
            <li>Order and browsing history</li>
          </ul>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            How We Use Information
          </h2>
          <p>
            Your information is used only to process orders, ship, provide
            support, and improve our services. We never share your information
            with third parties, except as required by law.
          </p>
          <h2 className="text-[15px] font-bold text-[#3F4064] mt-6 mb-2">
            Data Security
          </h2>
          <p>
            All information is encrypted via SSL, and access to your data is
            restricted to authorized personnel only.
          </p>
        </>
      )}
    </StaticPage>
  );
}
"""))

# ============================================================
# app/[locale]/not-found.tsx (updated 404)
# ============================================================
files.append(("app/[locale]/not-found.tsx", """import Link from "next/link";

export default async function LocaleNotFound({
  params,
}: {
  params?: Promise<{ locale: string }>;
}) {
  const locale = params ? (await params).locale : "fa";
  const isFa = locale === "fa";

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-16 text-center">
      <h1 className="text-[80px] font-bold text-[#EF4056] leading-none mb-4">
        404
      </h1>
      <h2 className="text-[20px] font-bold text-[#3F4064] mb-3">
        {isFa ? "صفحه‌ای که دنبالش هستید پیدا نشد" : "Page not found"}
      </h2>
      <p className="text-[13px] text-[#62666D] mb-8 max-w-md mx-auto">
        {isFa
          ? "ممکن است آدرس اشتباه باشد یا صفحه حذف شده باشد."
          : "The address might be incorrect, or the page may have been removed."}
      </p>
      <div className="flex items-center justify-center gap-3 flex-wrap">
        <Link
          href={`/${locale}`}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors inline-flex items-center"
        >
          {isFa ? "بازگشت به خانه" : "Back to Home"}
        </Link>
        <Link
          href={`/${locale}/search`}
          className="h-10 px-5 rounded-lg border border-[#E0E0E2] text-[13px] text-[#3F4064] hover:border-[#EF4056] hover:text-[#EF4056] transition-colors inline-flex items-center"
        >
          {isFa ? "جستجو در فروشگاه" : "Search"}
        </Link>
      </div>
    </div>
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 15: Search + Extras")
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
        print("\n" + "=" * 60)
        print("🎉 PROJECT COMPLETE! 🎉")
        print("=" * 60)
        print("\nNow run: npm run dev")
        print("\nAvailable routes:")
        print("  Home:          http://localhost:3000/fa")
        print("  Categories:    http://localhost:3000/fa/categories")
        print("  Category:      http://localhost:3000/fa/category/mobile")
        print("  Product:       http://localhost:3000/fa/product/samsung-galaxy-s24-ultra")
        print("  Cart:          http://localhost:3000/fa/cart")
        print("  Checkout:      http://localhost:3000/fa/checkout")
        print("  Login:         http://localhost:3000/fa/auth/login")
        print("  Register:      http://localhost:3000/fa/auth/register")
        print("  Account:       http://localhost:3000/fa/account")
        print("  Search:        http://localhost:3000/fa/search")
        print("  About:         http://localhost:3000/fa/about")
        print("  Contact:       http://localhost:3000/fa/contact")
        print("  FAQ:           http://localhost:3000/fa/faq")
        print("  Terms:         http://localhost:3000/fa/terms")
        print("  Privacy:       http://localhost:3000/fa/privacy")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()