"use client";

import { useState } from "react";
import type { Locale } from "@/lib/types";
import { iranProvinces, getCitiesByProvince } from "@/lib/data/iran-provinces";
import { isValidIranianMobile, isValidIranianPostalCode } from "@/lib/utils";

export interface ShippingData {
  fullName: string;
  mobile: string;
  province: string;
  city: string;
  postalCode: string;
  address: string;
}

interface ShippingFormProps {
  locale: Locale;
  initialData: ShippingData;
  onSubmit: (data: ShippingData) => void;
}

const EMPTY: ShippingData = {
  fullName: "",
  mobile: "",
  province: "",
  city: "",
  postalCode: "",
  address: "",
};

export default function ShippingForm({
  locale,
  initialData,
  onSubmit,
}: ShippingFormProps) {
  const isFa = locale === "fa";
  const [data, setData] = useState<ShippingData>(initialData || EMPTY);
  const [errors, setErrors] = useState<Partial<Record<keyof ShippingData, string>>>({});

  const t = {
    fullName: isFa ? "نام و نام خانوادگی" : "Full Name",
    mobile: isFa ? "شماره موبایل" : "Mobile Number",
    province: isFa ? "استان" : "Province",
    city: isFa ? "شهر" : "City",
    postalCode: isFa ? "کد پستی" : "Postal Code",
    address: isFa ? "آدرس کامل" : "Full Address",
    select: isFa ? "انتخاب کنید" : "Select",
    next: isFa ? "ادامه" : "Continue",
    required: isFa ? "این فیلد الزامی است" : "This field is required",
    invalidMobile: isFa ? "شماره موبایل نامعتبر است" : "Invalid mobile number",
    invalidPostal: isFa ? "کد پستی نامعتبر است" : "Invalid postal code",
  };

  const cities = data.province ? getCitiesByProvince(data.province) : [];

  const update = <K extends keyof ShippingData>(
    key: K,
    value: ShippingData[K]
  ) => {
    setData((prev) => ({ ...prev, [key]: value }));
    setErrors((prev) => ({ ...prev, [key]: undefined }));
  };

  const validate = (): boolean => {
    const errs: Partial<Record<keyof ShippingData, string>> = {};
    if (!data.fullName.trim()) errs.fullName = t.required;
    if (!data.mobile.trim()) errs.mobile = t.required;
    else if (!isValidIranianMobile(data.mobile)) errs.mobile = t.invalidMobile;
    if (!data.province) errs.province = t.required;
    if (!data.city) errs.city = t.required;
    if (!data.postalCode.trim()) errs.postalCode = t.required;
    else if (!isValidIranianPostalCode(data.postalCode))
      errs.postalCode = t.invalidPostal;
    if (!data.address.trim()) errs.address = t.required;
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) onSubmit(data);
  };

  const inputClass = (field: keyof ShippingData) =>
    `w-full h-10 px-3 rounded-lg border text-[13px] text-[#3F4064] placeholder:text-[#A1A3A8] focus:outline-none transition-colors ${
      errors[field]
        ? "border-[#EF4444] focus:border-[#EF4444]"
        : "border-[#E0E0E2] focus:border-[#EF4056]"
    }`;

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg border border-[#E0E0E2] p-5">
      <h2 className="text-[16px] font-bold text-[#3F4064] mb-5">
        {isFa ? "اطلاعات ارسال" : "Shipping Information"}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Full name */}
        <div className="md:col-span-2">
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.fullName} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={data.fullName}
            onChange={(e) => update("fullName", e.target.value)}
            className={inputClass("fullName")}
            placeholder={isFa ? "مثال: علی محمدی" : "e.g. John Doe"}
          />
          {errors.fullName && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.fullName}</p>
          )}
        </div>

        {/* Mobile */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.mobile} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="tel"
            value={data.mobile}
            onChange={(e) => update("mobile", e.target.value)}
            className={inputClass("mobile")}
            placeholder="09123456789"
            dir="ltr"
          />
          {errors.mobile && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.mobile}</p>
          )}
        </div>

        {/* Postal code */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.postalCode} <span className="text-[#EF4056]">*</span>
          </label>
          <input
            type="text"
            value={data.postalCode}
            onChange={(e) => update("postalCode", e.target.value)}
            className={inputClass("postalCode")}
            placeholder="1234567890"
            dir="ltr"
          />
          {errors.postalCode && (
            <p className="text-[11px] text-[#EF4444] mt-1">
              {errors.postalCode}
            </p>
          )}
        </div>

        {/* Province */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.province} <span className="text-[#EF4056]">*</span>
          </label>
          <select
            value={data.province}
            onChange={(e) => {
              update("province", e.target.value);
              update("city", "");
            }}
            className={inputClass("province")}
          >
            <option value="">{t.select}</option>
            {iranProvinces.map((p) => (
              <option key={p.id} value={p.id}>
                {isFa ? p.nameFa : p.nameEn}
              </option>
            ))}
          </select>
          {errors.province && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.province}</p>
          )}
        </div>

        {/* City */}
        <div>
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.city} <span className="text-[#EF4056]">*</span>
          </label>
          <select
            value={data.city}
            onChange={(e) => update("city", e.target.value)}
            disabled={!data.province}
            className={`${inputClass("city")} disabled:bg-[#F5F5F5] disabled:cursor-not-allowed`}
          >
            <option value="">{t.select}</option>
            {cities.map((c) => (
              <option key={c.id} value={c.id}>
                {isFa ? c.nameFa : c.nameEn}
              </option>
            ))}
          </select>
          {errors.city && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.city}</p>
          )}
        </div>

        {/* Address */}
        <div className="md:col-span-2">
          <label className="block text-[12px] text-[#62666D] mb-1.5">
            {t.address} <span className="text-[#EF4056]">*</span>
          </label>
          <textarea
            rows={3}
            value={data.address}
            onChange={(e) => update("address", e.target.value)}
            className={`${inputClass("address")} h-auto py-2 resize-none`}
            placeholder={
              isFa
                ? "خیابان، کوچه، پلاک، واحد..."
                : "Street, alley, number, unit..."
            }
          />
          {errors.address && (
            <p className="text-[11px] text-[#EF4444] mt-1">{errors.address}</p>
          )}
        </div>
      </div>

      <div className="flex justify-end mt-6">
        <button
          type="submit"
          className="h-10 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-medium hover:bg-[#d63850] transition-colors"
        >
          {t.next}
        </button>
      </div>
    </form>
  );
}
