# 40c_admin_dashboard.py
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

files.append(("components/admin/dashboard/TopProductsTable.tsx", """import Link from \"next/link\";
import Image from \"next/image\";
import { Trophy, Star, ArrowLeft, ArrowRight } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";
import { topProducts } from \"@/lib/data\";
import { formatCompact } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";

interface TopProductsTableProps { locale: Locale; }

export default function TopProductsTable({ locale }: TopProductsTableProps) {
  const isFa = locale === \"fa\";
  return (
    <ChartCard
      titleFa=\"پرفروش‌ترین محصولات\"
      titleEn=\"Top Products\"
      subtitleFa=\"بر اساس درآمد\"
      subtitleEn=\"By revenue\"
      icon={Trophy}
      delay={0.3}
      action={
        <Link href={`/${locale}/admin/products`} className=\"text-[11px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors shrink-0\">
          {isFa ? \"همه\" : \"All\"}
          {isFa ? <ArrowLeft size={12} /> : <ArrowRight size={12} />}
        </Link>
      }
    >
      <div className=\"space-y-3\">
        {topProducts.map((product, i) => (
          <div key={product.id} className=\"flex items-center gap-3 group hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 -mx-2 px-2 py-1.5 rounded-lg transition-colors\">
            <div className={`w-7 h-7 rounded-lg flex items-center justify-center text-[11px] font-bold shrink-0 ${i === 0 ? \"bg-gradient-to-br from-amber-400 to-amber-600 text-white\" : i === 1 ? \"bg-gradient-to-br from-slate-300 to-slate-500 text-white\" : i === 2 ? \"bg-gradient-to-br from-orange-400 to-orange-600 text-white\" : \"bg-[#F5F5F5] dark:bg-[#2A2A2E] text-[#62666D] dark:text-[#A1A3A8]\"}`}>
              {isFa ? (i + 1).toLocaleString(\"fa-IR\") : i + 1}
            </div>
            <div className=\"w-11 h-11 rounded-lg bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden relative shrink-0\">
              <Image src={product.image} alt={isFa ? product.titleFa : product.titleEn} fill sizes=\"44px\" className=\"object-cover\" />
            </div>
            <div className=\"flex-1 min-w-0\">
              <div className=\"text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] truncate\">{isFa ? product.titleFa : product.titleEn}</div>
              <div className=\"flex items-center gap-2 mt-0.5\">
                <span className=\"flex items-center gap-0.5 text-[10px] text-amber-500\">
                  <Star size={9} className=\"fill-current\" />
                  {product.rating}
                </span>
                <span className=\"text-[10px] text-[#A1A3A8]\">{product.sales.toLocaleString(isFa ? \"fa-IR\" : \"en-US\")} {isFa ? \"فروش\" : \"sold\"}</span>
              </div>
            </div>
            <div className=\"text-end shrink-0\">
              <div className=\"text-[12px] font-bold text-[#EF4056] tabular-nums\">{formatCompact(product.revenue, locale)}</div>
              <div className=\"text-[9px] text-[#A1A3A8]\">{isFa ? \"تومان\" : \"Toman\"}</div>
            </div>
          </div>
        ))}
      </div>
    </ChartCard>
  );
}
"""))

files.append(("components/admin/dashboard/RecentOrdersTable.tsx", """import Link from \"next/link\";
import { ShoppingCart, ArrowLeft, ArrowRight } from \"lucide-react\";
import type { Locale, AdminOrderStatus } from \"@/lib/types\";
import { adminOrders } from \"@/lib/data\";
import { formatPrice, formatRelativeTime } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";

interface RecentOrdersTableProps { locale: Locale; }

const STATUS: Record<AdminOrderStatus, { bg: string; fa: string; en: string }> = {
  pending: { bg: \"#F59E0B\", fa: \"در انتظار\", en: \"Pending\" },
  processing: { bg: \"#00BFFF\", fa: \"در حال پردازش\", en: \"Processing\" },
  shipped: { bg: \"#8B5CF6\", fa: \"ارسال شده\", en: \"Shipped\" },
  delivered: { bg: \"#22C55E\", fa: \"تحویل شده\", en: \"Delivered\" },
  cancelled: { bg: \"#EF4444\", fa: \"لغو شده\", en: \"Cancelled\" },
  refunded: { bg: \"#94A3B8\", fa: \"مرجوع\", en: \"Refunded\" },
};

export default function RecentOrdersTable({ locale }: RecentOrdersTableProps) {
  const isFa = locale === \"fa\";
  const recent = adminOrders.slice(0, 6);

  return (
    <ChartCard
      titleFa=\"سفارشات اخیر\"
      titleEn=\"Recent Orders\"
      subtitleFa=\"۶ سفارش آخر\"
      subtitleEn=\"Last 6 orders\"
      icon={ShoppingCart}
      delay={0.35}
      action={
        <Link href={`/${locale}/admin/orders`} className=\"text-[11px] text-[#00BFFF] hover:text-[#EF4056] flex items-center gap-1 transition-colors shrink-0\">
          {isFa ? \"همه\" : \"All\"}
          {isFa ? <ArrowLeft size={12} /> : <ArrowRight size={12} />}
        </Link>
      }
    >
      <div className=\"overflow-x-auto -mx-4 md:-mx-5 px-4 md:px-5\">
        <table className=\"w-full min-w-[500px]\">
          <thead>
            <tr className=\"text-[10px] text-[#A1A3A8] uppercase border-b border-[#F5F5F5] dark:border-[#2A2A2E]\">
              <th className=\"text-start pb-2 font-medium\">{isFa ? \"شماره\" : \"ID\"}</th>
              <th className=\"text-start pb-2 font-medium\">{isFa ? \"مشتری\" : \"Customer\"}</th>
              <th className=\"text-start pb-2 font-medium\">{isFa ? \"مبلغ\" : \"Total\"}</th>
              <th className=\"text-start pb-2 font-medium\">{isFa ? \"وضعیت\" : \"Status\"}</th>
            </tr>
          </thead>
          <tbody className=\"divide-y divide-[#F5F5F5] dark:divide-[#2A2A2E]\">
            {recent.map((order) => {
              const s = STATUS[order.status];
              return (
                <tr key={order.id} className=\"hover:bg-[#FAFAFA] dark:hover:bg-[#2A2A2E]/50 transition-colors\">
                  <td className=\"py-2.5\">
                    <div className=\"text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA]\" dir=\"ltr\">{order.id}</div>
                    <div className=\"text-[9px] text-[#A1A3A8]\">{formatRelativeTime(new Date(order.createdAt).getTime(), locale)}</div>
                  </td>
                  <td className=\"py-2.5\"><div className=\"text-[11px] text-[#62666D] dark:text-[#A1A3A8] truncate max-w-[120px]\">{order.customerName}</div></td>
                  <td className=\"py-2.5 text-[11px] font-bold text-[#3F4064] dark:text-[#E5E5EA] tabular-nums\">{formatPrice(order.total, locale)}</td>
                  <td className=\"py-2.5\">
                    <span className=\"text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap\" style={{ backgroundColor: `${s.bg}15`, color: s.bg }}>
                      {isFa ? s.fa : s.en}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </ChartCard>
  );
}
"""))

files.append(("components/admin/dashboard/ActivityTimeline.tsx", """import { Activity, Package, Users, Star, CreditCard, AlertTriangle, Settings as SettingsIcon, type LucideIcon } from \"lucide-react\";
import type { Locale, ActivityType } from \"@/lib/types\";
import { getRecentActivities } from \"@/lib/data\";
import { formatRelativeTime } from \"@/lib/utils\";
import ChartCard from \"../charts/ChartCard\";

interface ActivityTimelineProps { locale: Locale; }

const CONFIG: Record<ActivityType, { icon: LucideIcon; color: string }> = {
  order: { icon: Package, color: \"#22C55E\" },
  user: { icon: Users, color: \"#00BFFF\" },
  review: { icon: Star, color: \"#F59E0B\" },
  payment: { icon: CreditCard, color: \"#8B5CF6\" },
  product: { icon: AlertTriangle, color: \"#EF4056\" },
  system: { icon: SettingsIcon, color: \"#94A3B8\" },
};

export default function ActivityTimeline({ locale }: ActivityTimelineProps) {
  const isFa = locale === \"fa\";
  const activities = getRecentActivities(8);

  return (
    <ChartCard titleFa=\"فعالیت‌های اخیر\" titleEn=\"Recent Activity\" subtitleFa=\"آخرین رویدادها\" subtitleEn=\"Latest events\" icon={Activity} delay={0.4}>
      <div className=\"relative\">
        <div className=\"absolute top-2 bottom-2 right-[15px] w-px bg-gradient-to-b from-[#EF4056]/30 via-[#E0E0E2] to-transparent dark:via-[#2A2A2E]\" />
        <div className=\"space-y-4 relative\">
          {activities.map((activity) => {
            const config = CONFIG[activity.type];
            const Icon = config.icon;
            return (
              <div key={activity.id} className=\"flex gap-3 relative\">
                <div className=\"w-8 h-8 rounded-full flex items-center justify-center shrink-0 border-2 border-white dark:border-[#1A1A1E] z-10\" style={{ backgroundColor: `${config.color}20` }}>
                  <Icon size={14} style={{ color: config.color }} />
                </div>
                <div className=\"flex-1 min-w-0 pb-1\">
                  <div className=\"flex items-start justify-between gap-2\">
                    <div className=\"text-[12px] font-medium text-[#3F4064] dark:text-[#E5E5EA] leading-5\">{isFa ? activity.titleFa : activity.titleEn}</div>
                    <span className=\"text-[10px] text-[#A1A3A8] shrink-0 whitespace-nowrap\">{formatRelativeTime(activity.timestamp, locale)}</span>
                  </div>
                  <p className=\"text-[11px] text-[#62666D] dark:text-[#A1A3A8] leading-5 line-clamp-2 mt-0.5\">{isFa ? activity.descriptionFa : activity.descriptionEn}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </ChartCard>
  );
}
"""))

files.append(("components/admin/dashboard/QuickActions.tsx", """\"use client\";

import Link from \"next/link\";
import { motion } from \"framer-motion\";
import { Plus, Tag, Upload, Download, FileText, Users, Settings as SettingsIcon, type LucideIcon } from \"lucide-react\";
import type { Locale } from \"@/lib/types\";

interface QuickActionsProps { locale: Locale; }

export default function QuickActions({ locale }: QuickActionsProps) {
  const isFa = locale === \"fa\";
  const actions: Array<{ id: string; href: string; icon: LucideIcon; labelFa: string; labelEn: string; color: string }> = [
    { id: \"add-product\", href: \"/admin/products/new\", icon: Plus, labelFa: \"محصول جدید\", labelEn: \"New Product\", color: \"#EF4056\" },
    { id: \"add-discount\", href: \"/admin/discounts\", icon: Tag, labelFa: \"تخفیف جدید\", labelEn: \"New Discount\", color: \"#22C55E\" },
    { id: \"upload\", href: \"/admin/products\", icon: Upload, labelFa: \"آپلود محصولات\", labelEn: \"Upload Products\", color: \"#00BFFF\" },
    { id: \"export\", href: \"/admin/reports\", icon: Download, labelFa: \"دانلود گزارش\", labelEn: \"Download Report\", color: \"#8B5CF6\" },
    { id: \"reports\", href: \"/admin/reports\", icon: FileText, labelFa: \"گزارشات\", labelEn: \"Reports\", color: \"#F59E0B\" },
    { id: \"users\", href: \"/admin/users\", icon: Users, labelFa: \"مدیریت کاربران\", labelEn: \"Manage Users\", color: \"#EC4899\" },
    { id: \"settings\", href: \"/admin/settings\", icon: SettingsIcon, labelFa: \"تنظیمات\", labelEn: \"Settings\", color: \"#94A3B8\" },
  ];

  return (
    <div className=\"bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4\">
      <h3 className=\"text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3\">{isFa ? \"دسترسی سریع\" : \"Quick Actions\"}</h3>
      <div className=\"grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-2\">
        {actions.map((action, i) => {
          const Icon = action.icon;
          return (
            <motion.div key={action.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.04 }}>
              <Link href={`/${locale}${action.href}`} className=\"flex flex-col items-center gap-2 p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] hover:shadow-md hover:border-transparent transition-all group\" style={{ backgroundColor: `${action.color}05` }}>
                <div className=\"w-9 h-9 rounded-lg flex items-center justify-center transition-transform group-hover:scale-110\" style={{ backgroundColor: `${action.color}15` }}>
                  <Icon size={16} style={{ color: action.color }} />
                </div>
                <span className=\"text-[10px] text-[#3F4064] dark:text-[#E5E5EA] font-medium text-center leading-tight\">{isFa ? action.labelFa : action.labelEn}</span>
              </Link>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
"""))

files.append(("components/admin/dashboard/index.ts", """// components/admin/dashboard/index.ts
export { default as KpiCards } from \"./KpiCards\";
export { default as SalesChart } from \"./SalesChart\";
export { default as CategoryChart } from \"./CategoryChart\";
export { default as SharePieChart } from \"./SharePieChart\";
export { default as VisitorsChart } from \"./VisitorsChart\";
export { default as TopProductsTable } from \"./TopProductsTable\";
export { default as RecentOrdersTable } from \"./RecentOrdersTable\";
export { default as ActivityTimeline } from \"./ActivityTimeline\";
export { default as QuickActions } from \"./QuickActions\";
"""))

files.append(("components/admin/DashboardView.tsx", """\"use client\";

import type { Locale } from \"@/lib/types\";
import { useAdminStore } from \"@/lib/stores\";
import { KpiCards, SalesChart, CategoryChart, SharePieChart, VisitorsChart, TopProductsTable, RecentOrdersTable, ActivityTimeline, QuickActions } from \"./dashboard\";

interface DashboardViewProps { locale: Locale; }

export default function DashboardView({ locale }: DashboardViewProps) {
  const isFa = locale === \"fa\";
  const adminName = useAdminStore((s) => s.adminName);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return isFa ? \"صبح بخیر\" : \"Good morning\";
    if (hour < 17) return isFa ? \"روز بخیر\" : \"Good afternoon\";
    return isFa ? \"شب بخیر\" : \"Good evening\";
  };

  return (
    <div className=\"space-y-4 md:space-y-5\">
      <div>
        <h1 className=\"text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1\">
          {getGreeting()}، {adminName ?? \"Admin\"} 👋
        </h1>
        <p className=\"text-[12px] text-[#62666D] dark:text-[#A1A3A8]\">
          {isFa ? \"خلاصه‌ای از عملکرد فروشگاه SourcePixcel\" : \"Overview of SourcePixcel store performance\"}
        </p>
      </div>

      <QuickActions locale={locale} />
      <KpiCards locale={locale} />

      <div className=\"grid grid-cols-1 lg:grid-cols-3 gap-4\">
        <div className=\"lg:col-span-2\"><SalesChart locale={locale} /></div>
        <div className=\"lg:col-span-1\"><CategoryChart locale={locale} /></div>
      </div>

      <div className=\"grid grid-cols-1 lg:grid-cols-3 gap-4\">
        <div className=\"lg:col-span-2\"><VisitorsChart locale={locale} /></div>
        <div className=\"lg:col-span-1\"><SharePieChart locale={locale} /></div>
      </div>

      <div className=\"grid grid-cols-1 lg:grid-cols-2 gap-4\">
        <TopProductsTable locale={locale} />
        <RecentOrdersTable locale={locale} />
      </div>

      <ActivityTimeline locale={locale} />
    </div>
  );
}
"""))

files.append(("app/[locale]/admin/page.tsx", """import DashboardView from \"@/components/admin/DashboardView\";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminDashboardPage({ params }: PageProps) {
  const { locale } = await params;
  return <DashboardView locale={locale as \"fa\" | \"en\"} />;
}
"""))

# Update lib/utils/index.ts to add number-format exports
files.append(("lib/utils/index.ts", """// lib/utils/index.ts
export {
  formatPrice,
  formatPriceWithCurrency,
  calcFinalPrice,
  formatDiscount,
  formatRating,
  formatReviewCount,
  truncate,
  getProductTitle,
  getCategoryName,
  getBrandName,
  formatDate,
  localePath,
  cn,
  getStockLabel,
  scrollToTop,
} from \"./format\";

export {
  isValidIranianMobile,
  normalizeMobile,
  formatMobileDisplay,
  isValidEmail,
  isValidIranianNationalId,
  isValidIranianPostalCode,
  getPasswordStrength,
  isValidPassword,
} from \"./validators\";

export {
  buildMetadata,
  buildProductSchema,
  buildOrganizationSchema,
  buildWebSiteSchema,
  buildBreadcrumbSchema,
  SITE_NAME_EXPORT,
  SITE_URL_EXPORT,
} from \"./seo\";

export {
  generateBlurPlaceholder,
  getCategoryColor,
  getProductBlur,
  CATEGORY_COLORS,
} from \"./blur\";

export {
  formatCompact,
  formatPercent,
  formatRelativeTime,
} from \"./number-format\";
"""))

def main():
    print("=" * 60)
    print("Part 3: Tables + DashboardView")
    print("=" * 60)

    created = 0
    failed = 0
    for path, content in files:
        full = os.path.join(BASE, *path.split("/"))
        d = os.path.dirname(full)
        try:
            if d:
                os.makedirs(d, exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print(f"\nCreated: {created}, Failed: {failed}")
    if failed == 0:
        print("\n✅ Done! Run: npm run dev")

if __name__ == "__main__":
    main()