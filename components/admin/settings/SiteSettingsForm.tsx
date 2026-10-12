"use client";

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
