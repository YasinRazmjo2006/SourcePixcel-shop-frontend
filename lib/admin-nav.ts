// lib/admin-nav.ts
import {
  LayoutDashboard,
  BarChart3,
  Package,
  ShoppingCart,
  Users,
  Tag,
  Star,
  FileText,
  Settings,
  Layers,
  Radio,
  type LucideIcon,
} from "lucide-react";

export interface AdminNavItem {
  id: string;
  href: string;
  labelFa: string;
  labelEn: string;
  icon: LucideIcon;
  badge?: number | "dynamic";
  children?: AdminNavItem[];
  exact?: boolean;
}

export const ADMIN_NAV: AdminNavItem[] = [
  {
    id: "dashboard",
    href: "/admin",
    labelFa: "داشبورد",
    labelEn: "Dashboard",
    icon: LayoutDashboard,
    exact: true,
  },
  {
    id: "realtime",
    href: "/admin/realtime",
    labelFa: "پایش زنده",
    labelEn: "Real-time",
    icon: Radio,
    badge: "dynamic",
  },
  {
    id: "analytics",
    href: "/admin/analytics",
    labelFa: "آنالیتیکس",
    labelEn: "Analytics",
    icon: BarChart3,
  },
  {
    id: "products",
    href: "/admin/products",
    labelFa: "محصولات",
    labelEn: "Products",
    icon: Package,
    children: [
      {
        id: "products-list",
        href: "/admin/products",
        labelFa: "لیست محصولات",
        labelEn: "Products List",
        icon: Package,
        exact: true,
      },
      {
        id: "categories",
        href: "/admin/categories",
        labelFa: "دسته‌بندی‌ها",
        labelEn: "Categories",
        icon: Layers,
      },
    ],
  },
  {
    id: "orders",
    href: "/admin/orders",
    labelFa: "سفارشات",
    labelEn: "Orders",
    icon: ShoppingCart,
    badge: 4,
  },
  {
    id: "users",
    href: "/admin/users",
    labelFa: "کاربران",
    labelEn: "Users",
    icon: Users,
  },
  {
    id: "discounts",
    href: "/admin/discounts",
    labelFa: "تخفیف‌ها",
    labelEn: "Discounts",
    icon: Tag,
  },
  {
    id: "reviews",
    href: "/admin/reviews",
    labelFa: "نظرات",
    labelEn: "Reviews",
    icon: Star,
  },
  {
    id: "reports",
    href: "/admin/reports",
    labelFa: "گزارشات",
    labelEn: "Reports",
    icon: FileText,
  },
  {
    id: "settings",
    href: "/admin/settings",
    labelFa: "تنظیمات",
    labelEn: "Settings",
    icon: Settings,
  },
];

export interface FlatNavItem {
  id: string;
  href: string;
  labelFa: string;
  labelEn: string;
  icon: LucideIcon;
}

export const FLAT_ADMIN_NAV: FlatNavItem[] = ADMIN_NAV.flatMap((item) => {
  const self = {
    id: item.id,
    href: item.href,
    labelFa: item.labelFa,
    labelEn: item.labelEn,
    icon: item.icon,
  };
  const children = (item.children ?? []).map((child) => ({
    id: child.id,
    href: child.href,
    labelFa: child.labelFa,
    labelEn: child.labelEn,
    icon: child.icon,
  }));
  return [self, ...children];
});
