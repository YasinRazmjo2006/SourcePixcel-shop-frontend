"use client";

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
