"use client";

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
