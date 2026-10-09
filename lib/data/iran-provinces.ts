// lib/data/iran-provinces.ts
// List of Iranian provinces and major cities (for shipping forms)

export interface Province {
  id: string;
  nameFa: string;
  nameEn: string;
  cities: { id: string; nameFa: string; nameEn: string }[];
}

export const iranProvinces: Province[] = [
  {
    id: "tehran",
    nameFa: "تهران",
    nameEn: "Tehran",
    cities: [
      { id: "tehran", nameFa: "تهران", nameEn: "Tehran" },
      { id: "karaj", nameFa: "کرج", nameEn: "Karaj" },
      { id: "varamin", nameFa: "ورامین", nameEn: "Varamin" },
      { id: "shahriar", nameFa: "شهریار", nameEn: "Shahriar" },
    ],
  },
  {
    id: "isfahan",
    nameFa: "اصفهان",
    nameEn: "Isfahan",
    cities: [
      { id: "isfahan", nameFa: "اصفهان", nameEn: "Isfahan" },
      { id: "kashan", nameFa: "کاشان", nameEn: "Kashan" },
      { id: "najafabad", nameFa: "نجف‌آباد", nameEn: "Najafabad" },
    ],
  },
  {
    id: "fars",
    nameFa: "فارس",
    nameEn: "Fars",
    cities: [
      { id: "shiraz", nameFa: "شیراز", nameEn: "Shiraz" },
      { id: "marvdasht", nameFa: "مرودشت", nameEn: "Marvdasht" },
      { id: "jahrom", nameFa: "جهرم", nameEn: "Jahrom" },
    ],
  },
  {
    id: "khorasan-razavi",
    nameFa: "خراسان رضوی",
    nameEn: "Khorasan Razavi",
    cities: [
      { id: "mashhad", nameFa: "مشهد", nameEn: "Mashhad" },
      { id: "neyshabur", nameFa: "نیشابور", nameEn: "Neyshabur" },
      { id: "sabzevar", nameFa: "سبزوار", nameEn: "Sabzevar" },
    ],
  },
  {
    id: "azerbaijan-east",
    nameFa: "آذربایجان شرقی",
    nameEn: "East Azerbaijan",
    cities: [
      { id: "tabriz", nameFa: "تبریز", nameEn: "Tabriz" },
      { id: "maragheh", nameFa: "مراغه", nameEn: "Maragheh" },
      { id: "marand", nameFa: "مرند", nameEn: "Marand" },
    ],
  },
  {
    id: "khuzestan",
    nameFa: "خوزستان",
    nameEn: "Khuzestan",
    cities: [
      { id: "ahvaz", nameFa: "اهواز", nameEn: "Ahvaz" },
      { id: "abadan", nameFa: "آبادان", nameEn: "Abadan" },
      { id: "dezful", nameFa: "دزفول", nameEn: "Dezful" },
    ],
  },
  {
    id: "gilan",
    nameFa: "گیلان",
    nameEn: "Gilan",
    cities: [
      { id: "rasht", nameFa: "رشت", nameEn: "Rasht" },
      { id: "anzali", nameFa: "انزلی", nameEn: "Anzali" },
      { id: "lahijan", nameFa: "لاهیجان", nameEn: "Lahijan" },
    ],
  },
  {
    id: "mazandaran",
    nameFa: "مازندران",
    nameEn: "Mazandaran",
    cities: [
      { id: "sari", nameFa: "ساری", nameEn: "Sari" },
      { id: "babol", nameFa: "بابل", nameEn: "Babol" },
      { id: "amol", nameFa: "آمل", nameEn: "Amol" },
    ],
  },
];

export const getProvinceById = (id: string) =>
  iranProvinces.find((p) => p.id === id);

export const getCitiesByProvince = (provinceId: string) =>
  getProvinceById(provinceId)?.cities ?? [];
