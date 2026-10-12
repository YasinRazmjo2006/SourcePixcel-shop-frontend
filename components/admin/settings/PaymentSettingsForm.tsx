"use client";

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
