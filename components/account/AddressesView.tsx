"use client";

import { useState } from "react";
import { MapPin, Plus, Trash2, Edit2, X, Check } from "lucide-react";
import type { Locale } from "@/lib/types";
import { iranProvinces, getCitiesByProvince } from "@/lib/data/iran-provinces";

interface Address {
  id: string;
  fullName: string;
  mobile: string;
  province: string;
  city: string;
  postalCode: string;
  address: string;
  isDefault: boolean;
}

interface AddressesViewProps {
  locale: Locale;
}

export default function AddressesView({ locale }: AddressesViewProps) {
  const isFa = locale === "fa";

  const [addresses, setAddresses] = useState<Address[]>([
    {
      id: "addr-1",
      fullName: isFa ? "علی محمدی" : "Ali Mohammadi",
      mobile: "09123456789",
      province: "tehran",
      city: "tehran",
      postalCode: "1234567890",
      address: isFa
        ? "تهران، خیابان ولیعصر، پلاک ۱۲۳، واحد ۴"
        : "Tehran, Valiasr St., No. 123, Unit 4",
      isDefault: true,
    },
  ]);

  const [editing, setEditing] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const t = {
    title: isFa ? "آدرس‌های من" : "My Addresses",
    add: isFa ? "افزودن آدرس جدید" : "Add New Address",
    edit: isFa ? "ویرایش" : "Edit",
    delete: isFa ? "حذف" : "Delete",
    default: isFa ? "پیش‌فرض" : "Default",
    setDefault: isFa ? "انتخاب به عنوان پیش‌فرض" : "Set as default",
    noAddress: isFa ? "آدرسی ثبت نشده" : "No addresses yet",
    fullName: isFa ? "نام گیرنده" : "Recipient Name",
    mobile: isFa ? "شماره موبایل" : "Mobile",
    province: isFa ? "استان" : "Province",
    city: isFa ? "شهر" : "City",
    postalCode: isFa ? "کد پستی" : "Postal Code",
    address: isFa ? "آدرس کامل" : "Full Address",
    save: isFa ? "ذخیره" : "Save",
    cancel: isFa ? "انصراف" : "Cancel",
  };

  const removeAddress = (id: string) => {
    setAddresses((prev) => prev.filter((a) => a.id !== id));
  };

  const setDefault = (id: string) => {
    setAddresses((prev) =>
      prev.map((a) => ({ ...a, isDefault: a.id === id }))
    );
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h1 className="text-[18px] font-bold text-[#3F4064]">{t.title}</h1>
        <button
          onClick={() => setShowForm(true)}
          className="h-9 px-4 rounded-lg bg-[#EF4056] text-white text-[12px] font-medium hover:bg-[#d63850] transition-colors flex items-center gap-1"
        >
          <Plus size={14} />
          {t.add}
        </button>
      </div>

      {addresses.length === 0 ? (
        <div className="bg-white rounded-lg border border-[#E0E0E2] p-8 text-center">
          <MapPin size={36} className="text-[#A1A3A8] mx-auto mb-3" />
          <p className="text-[13px] text-[#62666D]">{t.noAddress}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {addresses.map((addr) => {
            const province = iranProvinces.find((p) => p.id === addr.province);
            const city = province?.cities.find((c) => c.id === addr.city);
            return (
              <div
                key={addr.id}
                className="bg-white rounded-lg border border-[#E0E0E2] p-4"
              >
                <div className="flex items-start justify-between gap-3 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[13px] font-bold text-[#3F4064]">
                      {addr.fullName}
                    </span>
                    {addr.isDefault && (
                      <span className="text-[10px] bg-[#22C55E]/10 text-[#22C55E] px-2 py-0.5 rounded-full font-medium">
                        {t.default}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => setDefault(addr.id)}
                      className="w-7 h-7 rounded-lg flex items-center justify-center text-[#22C55E] hover:bg-[#F5F5F5] transition-colors"
                      title={t.setDefault}
                    >
                      <Check size={14} />
                    </button>
                    <button
                      onClick={() => removeAddress(addr.id)}
                      className="w-7 h-7 rounded-lg flex items-center justify-center text-[#EF4444] hover:bg-[#F5F5F5] transition-colors"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                </div>

                <div className="text-[12px] text-[#62666D] leading-6 space-y-0.5">
                  <div>
                    <span className="text-[#A1A3A8]">
                      {isFa ? "موبایل: " : "Mobile: "}
                    </span>
                    <span dir="ltr">{addr.mobile}</span>
                  </div>
                  <div>
                    <span className="text-[#A1A3A8]">
                      {isFa ? "آدرس: " : "Address: "}
                    </span>
                    {isFa ? province?.nameFa : province?.nameEn},{" "}
                    {isFa ? city?.nameFa : city?.nameEn} — {addr.address}
                  </div>
                  <div>
                    <span className="text-[#A1A3A8]">
                      {isFa ? "کد پستی: " : "Postal: "}
                    </span>
                    <span dir="ltr">{addr.postalCode}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* New address modal */}
      {showForm && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
          <div
            className="absolute inset-0 bg-black/40"
            onClick={() => setShowForm(false)}
          />
          <div className="relative bg-white rounded-lg max-w-lg w-full max-h-[90vh] overflow-y-auto p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-[16px] font-bold text-[#3F4064]">
                {t.add}
              </h3>
              <button onClick={() => setShowForm(false)}>
                <X size={20} className="text-[#62666D]" />
              </button>
            </div>
            <p className="text-[12px] text-[#A1A3A8] text-center py-8">
              {isFa
                ? "فرم آدرس در این نسخه دمو قابلیت ذخیره‌سازی ندارد."
                : "This form doesn't save in the demo version."}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
