# 47_admin_settings.py
# Step 10: Settings & Polish (Final Step)
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
files = []

# ============================================================
# lib/stores/admin-settings.ts
# ============================================================
files.append(("lib/stores/admin-settings.ts", '''"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface SiteSettings {
  siteName: string;
  siteNameFa: string;
  siteDescription: string;
  siteDescriptionFa: string;
  contactEmail: string;
  contactPhone: string;
  contactAddress: string;
  contactAddressFa: string;
  instagramUrl: string;
  twitterUrl: string;
  linkedinUrl: string;
  youtubeUrl: string;
}

export interface PaymentSettings {
  zarinpalEnabled: boolean;
  idpayEnabled: boolean;
  nextpayEnabled: boolean;
  codEnabled: boolean;
  zarinpalMerchantId: string;
  idpayApiKey: string;
  nextpayApiKey: string;
}

export interface ShippingSettings {
  postEnabled: boolean;
  tipaxEnabled: boolean;
  pickupEnabled: boolean;
  postCost: number;
  tipaxCost: number;
  freeShippingThreshold: number;
}

export interface AdminSettingsState {
  site: SiteSettings;
  payment: PaymentSettings;
  shipping: ShippingSettings;
  updateSite: (settings: Partial<SiteSettings>) => void;
  updatePayment: (settings: Partial<PaymentSettings>) => void;
  updateShipping: (settings: Partial<ShippingSettings>) => void;
  reset: () => void;
}

const DEFAULT_SITE: SiteSettings = {
  siteName: "SourcePixcel",
  siteNameFa: "سورس پیکسل",
  siteDescription: "Modern online store for all your needs",
  siteDescriptionFa: "فروشگاه آنلاین مدرن برای تمام نیازهای شما",
  contactEmail: "support@sourcepixcel.com",
  contactPhone: "021-12345678",
  contactAddress: "Tehran, Valiasr St., No. 123",
  contactAddressFa: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  instagramUrl: "https://instagram.com/sourcepixcel",
  twitterUrl: "https://twitter.com/sourcepixcel",
  linkedinUrl: "https://linkedin.com/company/sourcepixcel",
  youtubeUrl: "https://youtube.com/@sourcepixcel",
};

const DEFAULT_PAYMENT: PaymentSettings = {
  zarinpalEnabled: true,
  idpayEnabled: true,
  nextpayEnabled: false,
  codEnabled: true,
  zarinpalMerchantId: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  idpayApiKey: "",
  nextpayApiKey: "",
};

const DEFAULT_SHIPPING: ShippingSettings = {
  postEnabled: true,
  tipaxEnabled: true,
  pickupEnabled: true,
  postCost: 45000,
  tipaxCost: 85000,
  freeShippingThreshold: 5000000,
};

export const useAdminSettingsStore = create<AdminSettingsState>()(
  persist(
    (set) => ({
      site: DEFAULT_SITE,
      payment: DEFAULT_PAYMENT,
      shipping: DEFAULT_SHIPPING,

      updateSite: (settings) =>
        set((state) => ({ site: { ...state.site, ...settings } })),

      updatePayment: (settings) =>
        set((state) => ({ payment: { ...state.payment, ...settings } })),

      updateShipping: (settings) =>
        set((state) => ({ shipping: { ...state.shipping, ...settings } })),

      reset: () =>
        set({
          site: DEFAULT_SITE,
          payment: DEFAULT_PAYMENT,
          shipping: DEFAULT_SHIPPING,
        }),
    }),
    { name: "sourcepixcel-admin-settings" }
  )
);
'''))

# ============================================================
# lib/stores/index.ts (updated)
# ============================================================
files.append(("lib/stores/index.ts", '''// lib/stores/index.ts
export { useCartStore } from "./cart";
export { useWishlistStore } from "./wishlist";
export { useAuthStore } from "./auth";
export { useCompareStore, COMPARE_MAX } from "./compare";
export { useThemeStore } from "./theme";
export { useToastStore } from "./toast";
export { useReviewsStore } from "./reviews";
export { useAdminStore } from "./admin";
export { useAdminUIStore } from "./admin-ui";
export { useAdminProductsStore } from "./admin-products";
export { useAdminOrdersStore } from "./admin-orders";
export { useAdminReportsStore } from "./admin-reports";
export { useAdminSettingsStore } from "./admin-settings";
export { useLiveActivityStore } from "./live-activity";
export { useNotificationsStore } from "./notifications";
export { usePaymentStore } from "./payment";
export { useSettingsStore } from "./settings";
export type { AuthUser } from "./auth";
export type { ThemeMode } from "./theme";
export type { Toast, ToastType } from "./toast";
export type { PaymentTransaction } from "./payment";
export type { SavedReport, ReportType, ReportFormat } from "./admin-reports";
export type { SiteSettings, PaymentSettings, ShippingSettings } from "./admin-settings";
'''))

# ============================================================
# components/admin/settings/SettingsTabs.tsx
# ============================================================
files.append(("components/admin/settings/SettingsTabs.tsx", '''"use client";

import { motion } from "framer-motion";
import {
  Globe,
  CreditCard,
  Truck,
  Bell,
  Shield,
  type LucideIcon,
} from "lucide-react";
import type { Locale } from "@/lib/types";

export type SettingsTab =
  | "site"
  | "payment"
  | "shipping"
  | "notifications"
  | "security";

interface SettingsTabsProps {
  locale: Locale;
  active: SettingsTab;
  onChange: (tab: SettingsTab) => void;
}

export default function SettingsTabs({
  locale,
  active,
  onChange,
}: SettingsTabsProps) {
  const isFa = locale === "fa";

  const tabs: Array<{
    id: SettingsTab;
    icon: LucideIcon;
    fa: string;
    en: string;
  }> = [
    { id: "site", icon: Globe, fa: "اطلاعات سایت", en: "Site Info" },
    { id: "payment", icon: CreditCard, fa: "پرداخت", en: "Payment" },
    { id: "shipping", icon: Truck, fa: "ارسال", en: "Shipping" },
    { id: "notifications", icon: Bell, fa: "اعلان‌ها", en: "Notifications" },
    { id: "security", icon: Shield, fa: "امنیت", en: "Security" },
  ];

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-1.5 overflow-x-auto">
      <div className="flex items-center gap-1 min-w-max">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = active === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onChange(tab.id)}
              className={`relative flex items-center gap-2 h-10 px-4 rounded-lg text-[12px] font-medium transition-colors whitespace-nowrap ${
                isActive
                  ? "text-white"
                  : "text-[#62666D] dark:text-[#A1A3A8] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]"
              }`}
            >
              {isActive && (
                <motion.div
                  layoutId="settings-tab-bg"
                  className="absolute inset-0 bg-[#EF4056] rounded-lg"
                  transition={{ type: "spring", stiffness: 400, damping: 30 }}
                />
              )}
              <span className="relative flex items-center gap-2">
                <Icon size={14} />
                {isFa ? tab.fa : tab.en}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/settings/SiteSettingsForm.tsx
# ============================================================
files.append(("components/admin/settings/SiteSettingsForm.tsx", '''"use client";

import { useState, useEffect } from "react";
import { Save, CheckCircle2, Globe } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAdminSettingsStore, useToastStore } from "@/lib/stores";

interface SiteSettingsFormProps {
  locale: Locale;
}

export default function SiteSettingsForm({ locale }: SiteSettingsFormProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const settings = useAdminSettingsStore((s) => s.site);
  const updateSite = useAdminSettingsStore((s) => s.updateSite);

  const [form, setForm] = useState(settings);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setForm(settings);
  }, [settings]);

  const handleSave = () => {
    updateSite(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
    pushToast({
      type: "success",
      titleFa: "تنظیمات ذخیره شد",
      titleEn: "Settings saved",
    });
  };

  const inputClass = "w-full h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056] transition-colors";

  const t = {
    title: isFa ? "اطلاعات سایت" : "Site Information",
    subtitle: isFa ? "نام، توضیحات و راه‌های ارتباطی" : "Name, description and contact info",
    siteName: isFa ? "نام سایت (انگلیسی)" : "Site Name (EN)",
    siteNameFa: isFa ? "نام سایت (فارسی)" : "Site Name (FA)",
    siteDesc: isFa ? "توضیحات (انگلیسی)" : "Description (EN)",
    siteDescFa: isFa ? "توضیحات (فارسی)" : "Description (FA)",
    contactSection: isFa ? "اطلاعات تماس" : "Contact Information",
    email: isFa ? "ایمیل" : "Email",
    phone: isFa ? "تلفن" : "Phone",
    address: isFa ? "آدرس (انگلیسی)" : "Address (EN)",
    addressFa: isFa ? "آدرس (فارسی)" : "Address (FA)",
    socialSection: isFa ? "شبکه‌های اجتماعی" : "Social Media",
    instagram: "Instagram",
    twitter: "Twitter / X",
    linkedin: "LinkedIn",
    youtube: "YouTube",
    save: isFa ? "ذخیره تغییرات" : "Save Changes",
    saved: isFa ? "ذخیره شد!" : "Saved!",
  };

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-5 space-y-5">
      {/* Header */}
      <div className="flex items-center gap-3 pb-4 border-b border-[#F5F5F5] dark:border-[#2A2A2E]">
        <div className="w-10 h-10 rounded-lg bg-[#EF4056]/10 flex items-center justify-center shrink-0">
          <Globe size={18} className="text-[#EF4056]" />
        </div>
        <div>
          <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {t.title}
          </h2>
          <p className="text-[11px] text-[#A1A3A8]">{t.subtitle}</p>
        </div>
      </div>

      {/* Site Info */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.siteName}
          </label>
          <input
            type="text"
            value={form.siteName}
            onChange={(e) => setForm({ ...form, siteName: e.target.value })}
            dir="ltr"
            className={inputClass}
          />
        </div>
        <div>
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.siteNameFa}
          </label>
          <input
            type="text"
            value={form.siteNameFa}
            onChange={(e) => setForm({ ...form, siteNameFa: e.target.value })}
            className={inputClass}
          />
        </div>
        <div className="md:col-span-2">
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.siteDesc}
          </label>
          <input
            type="text"
            value={form.siteDescription}
            onChange={(e) => setForm({ ...form, siteDescription: e.target.value })}
            dir="ltr"
            className={inputClass}
          />
        </div>
        <div className="md:col-span-2">
          <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
            {t.siteDescFa}
          </label>
          <input
            type="text"
            value={form.siteDescriptionFa}
            onChange={(e) => setForm({ ...form, siteDescriptionFa: e.target.value })}
            className={inputClass}
          />
        </div>
      </div>

      {/* Contact */}
      <div className="pt-4 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
        <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
          {t.contactSection}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.email}
            </label>
            <input
              type="email"
              value={form.contactEmail}
              onChange={(e) => setForm({ ...form, contactEmail: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
          <div>
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.phone}
            </label>
            <input
              type="tel"
              value={form.contactPhone}
              onChange={(e) => setForm({ ...form, contactPhone: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.address}
            </label>
            <input
              type="text"
              value={form.contactAddress}
              onChange={(e) => setForm({ ...form, contactAddress: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.addressFa}
            </label>
            <input
              type="text"
              value={form.contactAddressFa}
              onChange={(e) => setForm({ ...form, contactAddressFa: e.target.value })}
              className={inputClass}
            />
          </div>
        </div>
      </div>

      {/* Social */}
      <div className="pt-4 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
        <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
          {t.socialSection}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.instagram}
            </label>
            <input
              type="url"
              value={form.instagramUrl}
              onChange={(e) => setForm({ ...form, instagramUrl: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
          <div>
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.twitter}
            </label>
            <input
              type="url"
              value={form.twitterUrl}
              onChange={(e) => setForm({ ...form, twitterUrl: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
          <div>
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.linkedin}
            </label>
            <input
              type="url"
              value={form.linkedinUrl}
              onChange={(e) => setForm({ ...form, linkedinUrl: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
          <div>
            <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
              {t.youtube}
            </label>
            <input
              type="url"
              value={form.youtubeUrl}
              onChange={(e) => setForm({ ...form, youtubeUrl: e.target.value })}
              dir="ltr"
              className={inputClass}
            />
          </div>
        </div>
      </div>

      {/* Save */}
      <div className="pt-4 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex items-center justify-between flex-wrap gap-2">
        {saved && (
          <div className="flex items-center gap-2 text-[12px] text-[#22C55E] font-medium">
            <CheckCircle2 size={16} />
            {t.saved}
          </div>
        )}
        <div className="flex-1" />
        <button
          onClick={handleSave}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Save size={14} />
          {t.save}
        </button>
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/settings/PaymentSettingsForm.tsx
# ============================================================
files.append(("components/admin/settings/PaymentSettingsForm.tsx", '''"use client";

import { useState, useEffect } from "react";
import { Save, CheckCircle2, CreditCard } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAdminSettingsStore, useToastStore } from "@/lib/stores";

interface PaymentSettingsFormProps {
  locale: Locale;
}

export default function PaymentSettingsForm({ locale }: PaymentSettingsFormProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const settings = useAdminSettingsStore((s) => s.payment);
  const updatePayment = useAdminSettingsStore((s) => s.updatePayment);

  const [form, setForm] = useState(settings);
  const [saved, setSaved] = useState(false);

  useEffect(() => setForm(settings), [settings]);

  const handleSave = () => {
    updatePayment(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
    pushToast({
      type: "success",
      titleFa: "تنظیمات پرداخت ذخیره شد",
      titleEn: "Payment settings saved",
    });
  };

  const inputClass = "w-full h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056] transition-colors disabled:opacity-50";

  const gateways = [
    { id: "zarinpal", label: "Zarinpal", color: "#F9A825", field: "zarinpalMerchantId", keyField: "zarinpalEnabled" },
    { id: "idpay", label: "IDPay", color: "#22C55E", field: "idpayApiKey", keyField: "idpayEnabled" },
    { id: "nextpay", label: "NextPay", color: "#8B5CF6", field: "nextpayApiKey", keyField: "nextpayEnabled" },
  ];

  const t = {
    title: isFa ? "تنظیمات پرداخت" : "Payment Settings",
    subtitle: isFa ? "درگاه‌های پرداخت و کلیدهای API" : "Payment gateways and API keys",
    gatewaysSection: isFa ? "درگاه‌های فعال" : "Active Gateways",
    apiKeys: isFa ? "کلیدهای API" : "API Keys",
    cod: isFa ? "پرداخت در محل" : "Cash on Delivery",
    save: isFa ? "ذخیره تغییرات" : "Save Changes",
    saved: isFa ? "ذخیره شد!" : "Saved!",
    enabled: isFa ? "فعال" : "Enabled",
  };

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-5 space-y-5">
      <div className="flex items-center gap-3 pb-4 border-b border-[#F5F5F5] dark:border-[#2A2A2E]">
        <div className="w-10 h-10 rounded-lg bg-[#F9A825]/10 flex items-center justify-center shrink-0">
          <CreditCard size={18} className="text-[#F9A825]" />
        </div>
        <div>
          <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {t.title}
          </h2>
          <p className="text-[11px] text-[#A1A3A8]">{t.subtitle}</p>
        </div>
      </div>

      {/* Gateways */}
      <div>
        <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
          {t.gatewaysSection}
        </h3>
        <div className="space-y-3">
          {gateways.map((gw) => (
            <div
              key={gw.id}
              className="p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] space-y-3"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-6 h-6 rounded flex items-center justify-center text-white text-[10px] font-bold"
                    style={{ backgroundColor: gw.color }}
                  >
                    {gw.label[0]}
                  </div>
                  <span className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                    {gw.label}
                  </span>
                </div>
                <label className="flex items-center gap-2 cursor-pointer">
                  <span className="text-[10px] text-[#A1A3A8]">{t.enabled}</span>
                  <input
                    type="checkbox"
                    checked={form[gw.keyField as keyof typeof form] as boolean}
                    onChange={(e) =>
                      setForm({ ...form, [gw.keyField]: e.target.checked })
                    }
                    className="w-4 h-4 accent-[#22C55E] cursor-pointer"
                  />
                </label>
              </div>
              <input
                type="text"
                value={form[gw.field as keyof typeof form] as string}
                onChange={(e) => setForm({ ...form, [gw.field]: e.target.value })}
                placeholder={`${gw.label} API Key / Merchant ID`}
                dir="ltr"
                disabled={!(form[gw.keyField as keyof typeof form] as boolean)}
                className={inputClass}
              />
            </div>
          ))}
        </div>
      </div>

      {/* COD */}
      <div className="p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E]">
        <div className="flex items-center justify-between">
          <span className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {t.cod}
          </span>
          <input
            type="checkbox"
            checked={form.codEnabled}
            onChange={(e) => setForm({ ...form, codEnabled: e.target.checked })}
            className="w-4 h-4 accent-[#22C55E] cursor-pointer"
          />
        </div>
      </div>

      {/* Save */}
      <div className="pt-4 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex items-center justify-between flex-wrap gap-2">
        {saved && (
          <div className="flex items-center gap-2 text-[12px] text-[#22C55E] font-medium">
            <CheckCircle2 size={16} />
            {t.saved}
          </div>
        )}
        <div className="flex-1" />
        <button
          onClick={handleSave}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Save size={14} />
          {t.save}
        </button>
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/settings/ShippingSettingsForm.tsx
# ============================================================
files.append(("components/admin/settings/ShippingSettingsForm.tsx", '''"use client";

import { useState, useEffect } from "react";
import { Save, CheckCircle2, Truck } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAdminSettingsStore, useToastStore } from "@/lib/stores";
import { formatPrice } from "@/lib/utils";

interface ShippingSettingsFormProps {
  locale: Locale;
}

export default function ShippingSettingsForm({ locale }: ShippingSettingsFormProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const settings = useAdminSettingsStore((s) => s.shipping);
  const updateShipping = useAdminSettingsStore((s) => s.updateShipping);

  const [form, setForm] = useState(settings);
  const [saved, setSaved] = useState(false);

  useEffect(() => setForm(settings), [settings]);

  const handleSave = () => {
    updateShipping(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
    pushToast({
      type: "success",
      titleFa: "تنظیمات ارسال ذخیره شد",
      titleEn: "Shipping settings saved",
    });
  };

  const inputClass = "w-full h-10 px-3 rounded-lg bg-white dark:bg-[#1A1A1E] border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#3F4064] dark:text-[#E5E5EA] focus:outline-none focus:border-[#EF4056] transition-colors disabled:opacity-50";

  const t = {
    title: isFa ? "تنظیمات ارسال" : "Shipping Settings",
    subtitle: isFa ? "روش‌های ارسال و هزینه‌ها" : "Shipping methods and costs",
    methods: isFa ? "روش‌های ارسال" : "Shipping Methods",
    post: isFa ? "پست پیشتاز" : "Express Post",
    tipax: isFa ? "تیپاکس" : "Tipax",
    pickup: isFa ? "تحویل حضوری" : "Store Pickup",
    postCost: isFa ? "هزینه پست (تومان)" : "Post Cost (T)",
    tipaxCost: isFa ? "هزینه تیپاکس (تومان)" : "Tipax Cost (T)",
    freeThreshold: isFa ? "آستانه ارسال رایگان (تومان)" : "Free Shipping Threshold (T)",
    freeHint: isFa ? "سفارشات بالای این مبلغ، ارسال رایگان دارند" : "Orders above this amount get free shipping",
    save: isFa ? "ذخیره تغییرات" : "Save Changes",
    saved: isFa ? "ذخیره شد!" : "Saved!",
    enabled: isFa ? "فعال" : "Enabled",
  };

  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-5 space-y-5">
      <div className="flex items-center gap-3 pb-4 border-b border-[#F5F5F5] dark:border-[#2A2A2E]">
        <div className="w-10 h-10 rounded-lg bg-[#00BFFF]/10 flex items-center justify-center shrink-0">
          <Truck size={18} className="text-[#00BFFF]" />
        </div>
        <div>
          <h2 className="text-[15px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
            {t.title}
          </h2>
          <p className="text-[11px] text-[#A1A3A8]">{t.subtitle}</p>
        </div>
      </div>

      {/* Methods */}
      <div>
        <h3 className="text-[13px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-3">
          {t.methods}
        </h3>
        <div className="space-y-3">
          {/* Post */}
          <div className="p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.post}
              </span>
              <input
                type="checkbox"
                checked={form.postEnabled}
                onChange={(e) => setForm({ ...form, postEnabled: e.target.checked })}
                className="w-4 h-4 accent-[#22C55E] cursor-pointer"
              />
            </div>
            <div>
              <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                {t.postCost}
              </label>
              <input
                type="number"
                value={form.postCost}
                onChange={(e) => setForm({ ...form, postCost: Number(e.target.value) })}
                disabled={!form.postEnabled}
                dir="ltr"
                className={inputClass}
              />
              <div className="text-[10px] text-[#A1A3A8] mt-1">
                {formatPrice(form.postCost, locale)} {isFa ? "تومان" : "Toman"}
              </div>
            </div>
          </div>

          {/* Tipax */}
          <div className="p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
                {t.tipax}
              </span>
              <input
                type="checkbox"
                checked={form.tipaxEnabled}
                onChange={(e) => setForm({ ...form, tipaxEnabled: e.target.checked })}
                className="w-4 h-4 accent-[#22C55E] cursor-pointer"
              />
            </div>
            <div>
              <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
                {t.tipaxCost}
              </label>
              <input
                type="number"
                value={form.tipaxCost}
                onChange={(e) => setForm({ ...form, tipaxCost: Number(e.target.value) })}
                disabled={!form.tipaxEnabled}
                dir="ltr"
                className={inputClass}
              />
              <div className="text-[10px] text-[#A1A3A8] mt-1">
                {formatPrice(form.tipaxCost, locale)} {isFa ? "تومان" : "Toman"}
              </div>
            </div>
          </div>

          {/* Pickup */}
          <div className="p-3 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] flex items-center justify-between">
            <span className="text-[12px] font-bold text-[#3F4064] dark:text-[#E5E5EA]">
              {t.pickup}
            </span>
            <input
              type="checkbox"
              checked={form.pickupEnabled}
              onChange={(e) => setForm({ ...form, pickupEnabled: e.target.checked })}
              className="w-4 h-4 accent-[#22C55E] cursor-pointer"
            />
          </div>
        </div>
      </div>

      {/* Free Shipping Threshold */}
      <div className="pt-4 border-t border-[#F5F5F5] dark:border-[#2A2A2E]">
        <label className="block text-[11px] text-[#62666D] dark:text-[#A1A3A8] mb-1.5">
          {t.freeThreshold}
        </label>
        <input
          type="number"
          value={form.freeShippingThreshold}
          onChange={(e) =>
            setForm({ ...form, freeShippingThreshold: Number(e.target.value) })
          }
          dir="ltr"
          className={inputClass}
        />
        <div className="text-[10px] text-[#22C55E] mt-1">
          {formatPrice(form.freeShippingThreshold, locale)} {isFa ? "تومان" : "Toman"}
        </div>
        <div className="text-[10px] text-[#A1A3A8] mt-1">{t.freeHint}</div>
      </div>

      {/* Save */}
      <div className="pt-4 border-t border-[#F5F5F5] dark:border-[#2A2A2E] flex items-center justify-between flex-wrap gap-2">
        {saved && (
          <div className="flex items-center gap-2 text-[12px] text-[#22C55E] font-medium">
            <CheckCircle2 size={16} />
            {t.saved}
          </div>
        )}
        <div className="flex-1" />
        <button
          onClick={handleSave}
          className="h-10 px-5 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-2"
        >
          <Save size={14} />
          {t.save}
        </button>
      </div>
    </div>
  );
}
'''))

# ============================================================
# components/admin/settings/index.ts
# ============================================================
files.append(("components/admin/settings/index.ts", '''// components/admin/settings/index.ts
export { default as SettingsTabs } from "./SettingsTabs";
export type { SettingsTab } from "./SettingsTabs";
export { default as SiteSettingsForm } from "./SiteSettingsForm";
export { default as PaymentSettingsForm } from "./PaymentSettingsForm";
export { default as ShippingSettingsForm } from "./ShippingSettingsForm";
'''))

# ============================================================
# components/admin/SettingsView.tsx
# ============================================================
files.append(("components/admin/SettingsView.tsx", '''"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Settings as SettingsIcon, RotateCcw } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useAdminSettingsStore, useToastStore } from "@/lib/stores";
import SettingsTabs, { type SettingsTab } from "./settings/SettingsTabs";
import SiteSettingsForm from "./settings/SiteSettingsForm";
import PaymentSettingsForm from "./settings/PaymentSettingsForm";
import ShippingSettingsForm from "./settings/ShippingSettingsForm";

interface SettingsViewProps {
  locale: Locale;
}

export default function SettingsView({ locale }: SettingsViewProps) {
  const isFa = locale === "fa";
  const pushToast = useToastStore((s) => s.push);
  const reset = useAdminSettingsStore((s) => s.reset);

  const [activeTab, setActiveTab] = useState<SettingsTab>("site");

  const handleReset = () => {
    if (confirm(isFa ? "همه تنظیمات به حالت پیش‌فرض برگردند؟" : "Reset all settings to default?")) {
      reset();
      pushToast({
        type: "info",
        titleFa: "تنظیمات بازنشانی شد",
        titleEn: "Settings reset",
      });
    }
  };

  const t = {
    title: isFa ? "تنظیمات" : "Settings",
    subtitle: isFa ? "مدیریت پیکربندی فروشگاه" : "Manage store configuration",
    reset: isFa ? "بازنشانی به پیش‌فرض" : "Reset to Default",
  };

  return (
    <div className="space-y-4 md:space-y-5">
      {/* Header */}
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-[#EF4056]/10 flex items-center justify-center shrink-0">
            <SettingsIcon size={20} className="text-[#EF4056]" />
          </div>
          <div>
            <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-0.5">
              {t.title}
            </h1>
            <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
              {t.subtitle}
            </p>
          </div>
        </div>

        <button
          onClick={handleReset}
          className="h-10 px-4 rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] text-[12px] text-[#62666D] dark:text-[#A1A3A8] hover:border-[#EF4444] hover:text-[#EF4444] transition-colors flex items-center gap-2"
        >
          <RotateCcw size={14} />
          {t.reset}
        </button>
      </div>

      {/* Tabs */}
      <SettingsTabs locale={locale} active={activeTab} onChange={setActiveTab} />

      {/* Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2 }}
        >
          {activeTab === "site" && <SiteSettingsForm locale={locale} />}
          {activeTab === "payment" && <PaymentSettingsForm locale={locale} />}
          {activeTab === "shipping" && <ShippingSettingsForm locale={locale} />}
          {activeTab === "notifications" && (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[12px] text-[#A1A3A8]">
              {isFa ? "تنظیمات اعلان‌ها به زودی..." : "Notification settings coming soon..."}
            </div>
          )}
          {activeTab === "security" && (
            <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-8 text-center text-[12px] text-[#A1A3A8]">
              {isFa ? "تنظیمات امنیتی به زودی..." : "Security settings coming soon..."}
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
'''))

# ============================================================
# app/[locale]/admin/settings/page.tsx
# ============================================================
files.append(("app/[locale]/admin/settings/page.tsx", '''import SettingsView from "@/components/admin/SettingsView";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export default async function AdminSettingsPage({ params }: PageProps) {
  const { locale } = await params;
  return <SettingsView locale={locale as "fa" | "en"} />;
}
'''))

# ============================================================
# components/admin/index.ts (updated)
# ============================================================
files.append(("components/admin/index.ts", '''// components/admin/index.ts
export { default as AdminGuard } from "./AdminGuard";
export { default as DashboardView } from "./DashboardView";
export { default as AnalyticsView } from "./AnalyticsView";
export { default as UsersView } from "./UsersView";
export { default as ProductsView } from "./ProductsView";
export { default as OrdersView } from "./OrdersView";
export { default as ReportsView } from "./ReportsView";
export { default as SettingsView } from "./SettingsView";
export { default as AdminLoginForm } from "./AdminLoginForm";
export { default as RealtimeWidget } from "./RealtimeWidget";

// Layout
export * from "./layout";

// Dashboard
export * from "./dashboard";

// Analytics
export * from "./analytics";

// Users
export * from "./users";

// Products
export * from "./products";

// Orders
export * from "./orders";

// Reports
export * from "./reports";

// Settings
export * from "./settings";

// Realtime
export * from "./realtime";

// Charts
export * from "./charts";
'''))

# ============================================================
# components/admin/DashboardView.tsx (updated with RealtimeWidget)
# ============================================================
files.append(("components/admin/DashboardView.tsx", '''"use client";

import type { Locale } from "@/lib/types";
import { useAdminStore } from "@/lib/stores";
import {
  KpiCards,
  SalesChart,
  CategoryChart,
  SharePieChart,
  VisitorsChart,
  TopProductsTable,
  RecentOrdersTable,
  ActivityTimeline,
  QuickActions,
} from "./dashboard";
import RealtimeWidget from "./RealtimeWidget";

interface DashboardViewProps {
  locale: Locale;
}

export default function DashboardView({ locale }: DashboardViewProps) {
  const isFa = locale === "fa";
  const adminName = useAdminStore((s) => s.adminName);

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return isFa ? "صبح بخیر" : "Good morning";
    if (hour < 17) return isFa ? "روز بخیر" : "Good afternoon";
    return isFa ? "شب بخیر" : "Good evening";
  };

  return (
    <div className="space-y-4 md:space-y-5">
      <div>
        <h1 className="text-[20px] md:text-[24px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-1">
          {getGreeting()}، {adminName ?? "Admin"} 👋
        </h1>
        <p className="text-[12px] text-[#62666D] dark:text-[#A1A3A8]">
          {isFa
            ? "خلاصه‌ای از عملکرد فروشگاه SourcePixcel"
            : "Overview of SourcePixcel store performance"}
        </p>
      </div>

      <QuickActions locale={locale} />
      <KpiCards locale={locale} />

      <RealtimeWidget locale={locale} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <SalesChart locale={locale} />
        </div>
        <div className="lg:col-span-1">
          <CategoryChart locale={locale} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <VisitorsChart locale={locale} />
        </div>
        <div className="lg:col-span-1">
          <SharePieChart locale={locale} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <TopProductsTable locale={locale} />
        <RecentOrdersTable locale={locale} />
      </div>

      <ActivityTimeline locale={locale} />
    </div>
  );
}
'''))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Admin Step 10: Settings (FINAL)")
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
        print("\n" + "=" * 60)
        print("🎉 ADMIN PANEL COMPLETE! 🎉")
        print("=" * 60)
        print("\nNext steps:")
        print("  1) Remove-Item -Recurse -Force .next")
        print("  2) npm run dev")
        print("  3) Open http://localhost:3000/fa/admin/settings")
        print("\nAll admin pages available:")
        print("  - /admin              (Dashboard)")
        print("  - /admin/realtime     (Live Monitoring)")
        print("  - /admin/analytics    (Analytics)")
        print("  - /admin/products     (Products)")
        print("  - /admin/orders       (Orders)")
        print("  - /admin/users        (Users)")
        print("  - /admin/reports      (Reports)")
        print("  - /admin/settings     (Settings)")

if __name__ == "__main__":
    main()