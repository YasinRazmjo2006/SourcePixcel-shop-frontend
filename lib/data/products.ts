// lib/data/products.ts
import type { Brand, Category, Product } from "@/lib/types";
import { getProductImage } from "./product-images";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fp(price: number, discount: number): number {
  return Math.round(price * (1 - discount / 100));
}

function img(id: number): string {
  return getProductImage(id);
}

// ─── Categories ───────────────────────────────────────────────────────────────

export const categories: Category[] = [
  {
    id: "mobile",
    nameFa: "موبایل",
    nameEn: "Mobile",
    slug: "mobile",
    icon: "Smartphone",
    subcategories: [
      { id: "android", nameFa: "اندروید", nameEn: "Android" },
      { id: "ios", nameFa: "آیفون", nameEn: "iPhone" },
    ],
  },
  {
    id: "laptop",
    nameFa: "لپ‌تاپ",
    nameEn: "Laptop",
    slug: "laptop",
    icon: "Laptop",
    subcategories: [
      { id: "gaming-laptop", nameFa: "گیمینگ", nameEn: "Gaming" },
      { id: "ultrabook", nameFa: "اولترابوک", nameEn: "Ultrabook" },
      { id: "workstation", nameFa: "ورک‌استیشن", nameEn: "Workstation" },
    ],
  },
  {
    id: "tablet",
    nameFa: "تبلت",
    nameEn: "Tablet",
    slug: "tablet",
    icon: "Tablet",
    subcategories: [
      { id: "ipad", nameFa: "آیپد", nameEn: "iPad" },
      { id: "android-tablet", nameFa: "تبلت اندروید", nameEn: "Android Tablet" },
    ],
  },
  {
    id: "audio",
    nameFa: "صوت و تصویر",
    nameEn: "Audio & Video",
    slug: "audio",
    icon: "Headphones",
    subcategories: [
      { id: "headphone", nameFa: "هدفون", nameEn: "Headphone" },
      { id: "earbuds", nameFa: "ایرباد", nameEn: "Earbuds" },
      { id: "speaker", nameFa: "اسپیکر", nameEn: "Speaker" },
    ],
  },
  {
    id: "camera",
    nameFa: "دوربین",
    nameEn: "Camera",
    slug: "camera",
    icon: "Camera",
    subcategories: [
      { id: "dslr", nameFa: "دوربین DSLR", nameEn: "DSLR" },
      { id: "mirrorless", nameFa: "میرورلس", nameEn: "Mirrorless" },
      { id: "action", nameFa: "اکشن کم", nameEn: "Action Cam" },
    ],
  },
  {
    id: "smartwatch",
    nameFa: "ساعت هوشمند",
    nameEn: "Smartwatch",
    slug: "smartwatch",
    icon: "Watch",
    subcategories: [
      { id: "apple-watch", nameFa: "اپل واچ", nameEn: "Apple Watch" },
      { id: "android-watch", nameFa: "ساعت اندروید", nameEn: "Android Watch" },
      { id: "fitness-band", nameFa: "بند ورزشی", nameEn: "Fitness Band" },
    ],
  },
  {
    id: "gaming",
    nameFa: "گیمینگ",
    nameEn: "Gaming",
    slug: "gaming",
    icon: "Gamepad2",
    subcategories: [
      { id: "console", nameFa: "کنسول", nameEn: "Console" },
      { id: "controller", nameFa: "دسته", nameEn: "Controller" },
      { id: "gaming-mouse", nameFa: "ماوس گیمینگ", nameEn: "Gaming Mouse" },
      { id: "gaming-headset", nameFa: "هدست گیمینگ", nameEn: "Gaming Headset" },
    ],
  },
  {
    id: "accessories",
    nameFa: "لوازم جانبی",
    nameEn: "Accessories",
    slug: "accessories",
    icon: "Cable",
    subcategories: [
      { id: "charger", nameFa: "شارژر", nameEn: "Charger" },
      { id: "case", nameFa: "کاور و قاب", nameEn: "Case & Cover" },
      { id: "cable", nameFa: "کابل", nameEn: "Cable" },
      { id: "powerbank", nameFa: "پاوربانک", nameEn: "Power Bank" },
    ],
  },
  {
    id: "clothing",
    nameFa: "پوشاک",
    nameEn: "Clothing",
    slug: "clothing",
    icon: "Shirt",
    subcategories: [
      { id: "tshirt", nameFa: "تی‌شرت", nameEn: "T-Shirt" },
      { id: "hoodie", nameFa: "هودی", nameEn: "Hoodie" },
      { id: "jacket", nameFa: "جاکت", nameEn: "Jacket" },
    ],
  },
  {
    id: "shoes",
    nameFa: "کفش و کتونی",
    nameEn: "Shoes & Sneakers",
    slug: "shoes",
    icon: "Footprints",
    subcategories: [
      { id: "sneaker", nameFa: "کتونی", nameEn: "Sneaker" },
      { id: "sport-shoe", nameFa: "کفش ورزشی", nameEn: "Sport Shoe" },
      { id: "formal-shoe", nameFa: "کفش رسمی", nameEn: "Formal Shoe" },
    ],
  },
  {
    id: "home",
    nameFa: "خانه و آشپزخانه",
    nameEn: "Home & Kitchen",
    slug: "home",
    icon: "Home",
    subcategories: [
      { id: "kitchen", nameFa: "آشپزخانه", nameEn: "Kitchen" },
      { id: "decor", nameFa: "دکوراسیون", nameEn: "Decor" },
      { id: "vacuum", nameFa: "جاروبرقی", nameEn: "Vacuum" },
    ],
  },
  {
    id: "books",
    nameFa: "کتاب",
    nameEn: "Books",
    slug: "books",
    icon: "BookOpen",
    subcategories: [
      { id: "tech-book", nameFa: "فناوری", nameEn: "Technology" },
      { id: "novel", nameFa: "رمان", nameEn: "Novel" },
      { id: "self-help", nameFa: "توسعه فردی", nameEn: "Self-Help" },
    ],
  },
];

// ─── Brands ───────────────────────────────────────────────────────────────────

export const brands: Brand[] = [
  { id: "samsung",     nameEn: "Samsung",     nameFa: "سامسونگ",     categories: ["mobile", "laptop", "tablet", "audio", "accessories"] },
  { id: "apple",       nameEn: "Apple",       nameFa: "اپل",          categories: ["mobile", "laptop", "tablet", "smartwatch", "audio"] },
  { id: "xiaomi",      nameEn: "Xiaomi",      nameFa: "شیائومی",      categories: ["mobile", "tablet", "smartwatch", "accessories"] },
  { id: "huawei",      nameEn: "Huawei",      nameFa: "هواوی",        categories: ["mobile", "laptop", "tablet", "smartwatch"] },
  { id: "sony",        nameEn: "Sony",        nameFa: "سونی",         categories: ["audio", "camera", "gaming"] },
  { id: "lg",          nameEn: "LG",          nameFa: "ال‌جی",        categories: ["audio", "home"] },
  { id: "asus",        nameEn: "Asus",        nameFa: "ایسوس",        categories: ["laptop", "gaming"] },
  { id: "lenovo",      nameEn: "Lenovo",      nameFa: "لنوو",         categories: ["laptop", "tablet"] },
  { id: "hp",          nameEn: "HP",          nameFa: "اچ‌پی",        categories: ["laptop", "accessories"] },
  { id: "dell",        nameEn: "Dell",        nameFa: "دل",           categories: ["laptop"] },
  { id: "microsoft",   nameEn: "Microsoft",   nameFa: "مایکروسافت",   categories: ["laptop", "tablet", "gaming"] },
  { id: "canon",       nameEn: "Canon",       nameFa: "کانن",         categories: ["camera"] },
  { id: "nikon",       nameEn: "Nikon",       nameFa: "نیکون",        categories: ["camera"] },
  { id: "gopro",       nameEn: "GoPro",       nameFa: "گوپرو",        categories: ["camera"] },
  { id: "bose",        nameEn: "Bose",        nameFa: "بوز",          categories: ["audio"] },
  { id: "jbl",         nameEn: "JBL",         nameFa: "جی‌بی‌ال",    categories: ["audio"] },
  { id: "sennheiser",  nameEn: "Sennheiser",  nameFa: "زنهایزر",      categories: ["audio"] },
  { id: "garmin",      nameEn: "Garmin",      nameFa: "گارمین",       categories: ["smartwatch"] },
  { id: "nike",        nameEn: "Nike",        nameFa: "نایک",         categories: ["clothing", "shoes"] },
  { id: "adidas",      nameEn: "Adidas",      nameFa: "آدیداس",       categories: ["clothing", "shoes"] },
  { id: "puma",        nameEn: "Puma",        nameFa: "پوما",         categories: ["clothing", "shoes"] },
  { id: "newbalance",  nameEn: "New Balance", nameFa: "نیوبالانس",    categories: ["shoes"] },
  { id: "playstation", nameEn: "PlayStation", nameFa: "پلی‌استیشن",   categories: ["gaming"] },
  { id: "nintendo",    nameEn: "Nintendo",    nameFa: "نینتندو",      categories: ["gaming"] },
  { id: "logitech",    nameEn: "Logitech",    nameFa: "لاجیتک",       categories: ["gaming", "accessories"] },
  { id: "anker",       nameEn: "Anker",       nameFa: "انکر",         categories: ["accessories"] },
  { id: "baseus",      nameEn: "Baseus",      nameFa: "باسئوس",       categories: ["accessories"] },
  { id: "philips",     nameEn: "Philips",     nameFa: "فیلیپس",       categories: ["home", "audio"] },
  { id: "tefal",       nameEn: "Tefal",       nameFa: "تفال",         categories: ["home"] },
  { id: "dyson",       nameEn: "Dyson",       nameFa: "دایسون",       categories: ["home"] },
];

// ─── Products ─────────────────────────────────────────────────────────────────

export const products: Product[] = [
  // ── Mobile ─────────────────────────────────────────────────────────────────
  {
    id: 1, slug: "samsung-galaxy-s24-ultra",
    titleFa: "گوشی سامسونگ Galaxy S24 Ultra", titleEn: "Samsung Galaxy S24 Ultra",
    brand: "samsung", category: "mobile", subcategory: "android",
    price: 72_000_000, discountPercent: 8, finalPrice: fp(72_000_000, 8),
    rating: 4.8, reviewCount: 312, image: img(1),
    inStock: true, tags: ["پرفروش", "جدید"], isNew: true, isFeatured: true,
  },
  {
    id: 2, slug: "apple-iphone-15-pro-max",
    titleFa: "گوشی اپل iPhone 15 Pro Max", titleEn: "Apple iPhone 15 Pro Max",
    brand: "apple", category: "mobile", subcategory: "ios",
    price: 95_000_000, discountPercent: 5, finalPrice: fp(95_000_000, 5),
    rating: 4.9, reviewCount: 528, image: img(2),
    inStock: true, tags: ["پرفروش"], isFeatured: true,
  },
  {
    id: 3, slug: "xiaomi-14-pro",
    titleFa: "گوشی شیائومی 14 Pro", titleEn: "Xiaomi 14 Pro",
    brand: "xiaomi", category: "mobile", subcategory: "android",
    price: 38_000_000, discountPercent: 12, finalPrice: fp(38_000_000, 12),
    rating: 4.5, reviewCount: 187, image: img(3),
    inStock: true, tags: ["تخفیف ویژه"],
  },
  {
    id: 4, slug: "samsung-galaxy-a55",
    titleFa: "گوشی سامسونگ Galaxy A55", titleEn: "Samsung Galaxy A55",
    brand: "samsung", category: "mobile", subcategory: "android",
    price: 22_000_000, discountPercent: 0, finalPrice: 22_000_000,
    rating: 4.3, reviewCount: 94, image: img(4),
    inStock: true, tags: ["میان‌رده"],
  },
  {
    id: 5, slug: "apple-iphone-15",
    titleFa: "گوشی اپل iPhone 15", titleEn: "Apple iPhone 15",
    brand: "apple", category: "mobile", subcategory: "ios",
    price: 62_000_000, discountPercent: 7, finalPrice: fp(62_000_000, 7),
    rating: 4.7, reviewCount: 261, image: img(5),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 6, slug: "xiaomi-redmi-note-13-pro",
    titleFa: "گوشی شیائومی Redmi Note 13 Pro", titleEn: "Xiaomi Redmi Note 13 Pro",
    brand: "xiaomi", category: "mobile", subcategory: "android",
    price: 18_500_000, discountPercent: 15, finalPrice: fp(18_500_000, 15),
    rating: 4.4, reviewCount: 143, image: img(6),
    inStock: true, tags: ["اقتصادی", "تخفیف"],
  },
  {
    id: 7, slug: "huawei-p60-pro",
    titleFa: "گوشی هواوی P60 Pro", titleEn: "Huawei P60 Pro",
    brand: "huawei", category: "mobile", subcategory: "android",
    price: 42_000_000, discountPercent: 10, finalPrice: fp(42_000_000, 10),
    rating: 4.6, reviewCount: 79, image: img(7),
    inStock: true, tags: [],
  },
  {
    id: 8, slug: "samsung-galaxy-z-fold5",
    titleFa: "گوشی تاشو سامسونگ Galaxy Z Fold 5", titleEn: "Samsung Galaxy Z Fold 5",
    brand: "samsung", category: "mobile", subcategory: "android",
    price: 120_000_000, discountPercent: 6, finalPrice: fp(120_000_000, 6),
    rating: 4.7, reviewCount: 55, image: img(8),
    inStock: false, tags: ["ناموجود"], isFeatured: true,
  },
  {
    id: 9, slug: "apple-iphone-14",
    titleFa: "گوشی اپل iPhone 14", titleEn: "Apple iPhone 14",
    brand: "apple", category: "mobile", subcategory: "ios",
    price: 48_000_000, discountPercent: 20, finalPrice: fp(48_000_000, 20),
    rating: 4.6, reviewCount: 408, image: img(9),
    inStock: true, tags: ["تخفیف ویژه"],
  },
  {
    id: 10, slug: "xiaomi-poco-x6-pro",
    titleFa: "گوشی شیائومی Poco X6 Pro", titleEn: "Xiaomi Poco X6 Pro",
    brand: "xiaomi", category: "mobile", subcategory: "android",
    price: 25_000_000, discountPercent: 0, finalPrice: 25_000_000,
    rating: 4.3, reviewCount: 112, image: img(10),
    inStock: true, tags: ["گیمینگ", "جدید"], isNew: true,
  },

  // ── Laptop ─────────────────────────────────────────────────────────────────
  {
    id: 11, slug: "asus-rog-strix-g16",
    titleFa: "لپ‌تاپ ایسوس ROG Strix G16", titleEn: "Asus ROG Strix G16",
    brand: "asus", category: "laptop", subcategory: "gaming-laptop",
    price: 95_000_000, discountPercent: 5, finalPrice: fp(95_000_000, 5),
    rating: 4.8, reviewCount: 98, image: img(11),
    inStock: true, tags: ["گیمینگ", "پرفروش"], isFeatured: true,
  },
  {
    id: 12, slug: "apple-macbook-pro-14",
    titleFa: "لپ‌تاپ اپل MacBook Pro 14 M3", titleEn: "Apple MacBook Pro 14 M3",
    brand: "apple", category: "laptop", subcategory: "workstation",
    price: 145_000_000, discountPercent: 0, finalPrice: 145_000_000,
    rating: 4.9, reviewCount: 201, image: img(12),
    inStock: true, tags: ["حرفه‌ای"], isFeatured: true,
  },
  {
    id: 13, slug: "lenovo-thinkpad-x1-carbon",
    titleFa: "لپ‌تاپ لنوو ThinkPad X1 Carbon", titleEn: "Lenovo ThinkPad X1 Carbon",
    brand: "lenovo", category: "laptop", subcategory: "ultrabook",
    price: 88_000_000, discountPercent: 8, finalPrice: fp(88_000_000, 8),
    rating: 4.7, reviewCount: 76, image: img(13),
    inStock: true, tags: ["بیزینس"],
  },
  {
    id: 14, slug: "dell-xps-15",
    titleFa: "لپ‌تاپ دل XPS 15", titleEn: "Dell XPS 15",
    brand: "dell", category: "laptop", subcategory: "workstation",
    price: 110_000_000, discountPercent: 0, finalPrice: 110_000_000,
    rating: 4.7, reviewCount: 134, image: img(14),
    inStock: true, tags: ["طراحی"],
  },
  {
    id: 15, slug: "hp-spectre-x360",
    titleFa: "لپ‌تاپ اچ‌پی Spectre x360", titleEn: "HP Spectre x360",
    brand: "hp", category: "laptop", subcategory: "ultrabook",
    price: 75_000_000, discountPercent: 10, finalPrice: fp(75_000_000, 10),
    rating: 4.5, reviewCount: 88, image: img(15),
    inStock: true, tags: ["دوحالته"],
  },
  {
    id: 16, slug: "asus-zenbook-14-oled",
    titleFa: "لپ‌تاپ ایسوس ZenBook 14 OLED", titleEn: "Asus ZenBook 14 OLED",
    brand: "asus", category: "laptop", subcategory: "ultrabook",
    price: 58_000_000, discountPercent: 12, finalPrice: fp(58_000_000, 12),
    rating: 4.6, reviewCount: 65, image: img(16),
    inStock: true, tags: ["سبک", "OLED"],
  },
  {
    id: 17, slug: "lenovo-ideapad-gaming-3",
    titleFa: "لپ‌تاپ لنوو IdeaPad Gaming 3", titleEn: "Lenovo IdeaPad Gaming 3",
    brand: "lenovo", category: "laptop", subcategory: "gaming-laptop",
    price: 48_000_000, discountPercent: 0, finalPrice: 48_000_000,
    rating: 4.2, reviewCount: 143, image: img(17),
    inStock: true, tags: ["اقتصادی", "گیمینگ"],
  },
  {
    id: 18, slug: "microsoft-surface-laptop-5",
    titleFa: "لپ‌تاپ مایکروسافت Surface Laptop 5", titleEn: "Microsoft Surface Laptop 5",
    brand: "microsoft", category: "laptop", subcategory: "ultrabook",
    price: 82_000_000, discountPercent: 7, finalPrice: fp(82_000_000, 7),
    rating: 4.5, reviewCount: 57, image: img(18),
    inStock: false, tags: [],
  },

  // ── Tablet ─────────────────────────────────────────────────────────────────
  {
    id: 19, slug: "apple-ipad-pro-12-m4",
    titleFa: "تبلت اپل iPad Pro 12.9 M4", titleEn: "Apple iPad Pro 12.9 M4",
    brand: "apple", category: "tablet", subcategory: "ipad",
    price: 92_000_000, discountPercent: 0, finalPrice: 92_000_000,
    rating: 4.9, reviewCount: 174, image: img(19),
    inStock: true, tags: ["حرفه‌ای"], isFeatured: true,
  },
  {
    id: 20, slug: "samsung-galaxy-tab-s9",
    titleFa: "تبلت سامسونگ Galaxy Tab S9", titleEn: "Samsung Galaxy Tab S9",
    brand: "samsung", category: "tablet", subcategory: "android-tablet",
    price: 45_000_000, discountPercent: 10, finalPrice: fp(45_000_000, 10),
    rating: 4.7, reviewCount: 89, image: img(20),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 21, slug: "xiaomi-pad-6-pro",
    titleFa: "تبلت شیائومی Pad 6 Pro", titleEn: "Xiaomi Pad 6 Pro",
    brand: "xiaomi", category: "tablet", subcategory: "android-tablet",
    price: 28_000_000, discountPercent: 15, finalPrice: fp(28_000_000, 15),
    rating: 4.5, reviewCount: 62, image: img(21),
    inStock: true, tags: ["اقتصادی"],
  },
  {
    id: 22, slug: "apple-ipad-air-5",
    titleFa: "تبلت اپل iPad Air 5", titleEn: "Apple iPad Air 5",
    brand: "apple", category: "tablet", subcategory: "ipad",
    price: 55_000_000, discountPercent: 8, finalPrice: fp(55_000_000, 8),
    rating: 4.8, reviewCount: 213, image: img(22),
    inStock: true, tags: [],
  },
  {
    id: 23, slug: "microsoft-surface-pro-9",
    titleFa: "تبلت مایکروسافت Surface Pro 9", titleEn: "Microsoft Surface Pro 9",
    brand: "microsoft", category: "tablet", subcategory: "android-tablet",
    price: 78_000_000, discountPercent: 0, finalPrice: 78_000_000,
    rating: 4.6, reviewCount: 44, image: img(23),
    inStock: true, tags: ["دوحالته"],
  },

  // ── Audio ──────────────────────────────────────────────────────────────────
  {
    id: 24, slug: "sony-wh-1000xm5",
    titleFa: "هدفون بی‌سیم سونی WH-1000XM5", titleEn: "Sony WH-1000XM5",
    brand: "sony", category: "audio", subcategory: "headphone",
    price: 18_000_000, discountPercent: 18, finalPrice: fp(18_000_000, 18),
    rating: 4.9, reviewCount: 456, image: img(24),
    inStock: true, tags: ["پرفروش", "نویزکنسلینگ"], isFeatured: true,
  },
  {
    id: 25, slug: "apple-airpods-pro-2",
    titleFa: "ایرپاد پرو اپل نسل دوم", titleEn: "Apple AirPods Pro 2",
    brand: "apple", category: "audio", subcategory: "earbuds",
    price: 22_000_000, discountPercent: 0, finalPrice: 22_000_000,
    rating: 4.8, reviewCount: 389, image: img(25),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 26, slug: "bose-quietcomfort-45",
    titleFa: "هدفون بوز QuietComfort 45", titleEn: "Bose QuietComfort 45",
    brand: "bose", category: "audio", subcategory: "headphone",
    price: 20_000_000, discountPercent: 15, finalPrice: fp(20_000_000, 15),
    rating: 4.8, reviewCount: 278, image: img(26),
    inStock: true, tags: ["نویزکنسلینگ"],
  },
  {
    id: 27, slug: "jbl-charge-5",
    titleFa: "اسپیکر بلوتوث JBL Charge 5", titleEn: "JBL Charge 5",
    brand: "jbl", category: "audio", subcategory: "speaker",
    price: 8_500_000, discountPercent: 10, finalPrice: fp(8_500_000, 10),
    rating: 4.7, reviewCount: 321, image: img(27),
    inStock: true, tags: ["ضدآب", "پرفروش"],
  },
  {
    id: 28, slug: "samsung-galaxy-buds2-pro",
    titleFa: "ایربادز سامسونگ Galaxy Buds2 Pro", titleEn: "Samsung Galaxy Buds2 Pro",
    brand: "samsung", category: "audio", subcategory: "earbuds",
    price: 12_000_000, discountPercent: 20, finalPrice: fp(12_000_000, 20),
    rating: 4.6, reviewCount: 167, image: img(28),
    inStock: true, tags: ["تخفیف"],
  },
  {
    id: 29, slug: "sennheiser-hd560s",
    titleFa: "هدفون سنهایزر HD 560S", titleEn: "Sennheiser HD 560S",
    brand: "sennheiser", category: "audio", subcategory: "headphone",
    price: 14_000_000, discountPercent: 0, finalPrice: 14_000_000,
    rating: 4.7, reviewCount: 89, image: img(29),
    inStock: true, tags: ["استودیو"],
  },
  {
    id: 30, slug: "jbl-flip-6",
    titleFa: "اسپیکر بلوتوث JBL Flip 6", titleEn: "JBL Flip 6",
    brand: "jbl", category: "audio", subcategory: "speaker",
    price: 5_800_000, discountPercent: 5, finalPrice: fp(5_800_000, 5),
    rating: 4.6, reviewCount: 244, image: img(30),
    inStock: true, tags: ["ضدآب"],
  },
  {
    id: 31, slug: "xiaomi-redmi-buds-5-pro",
    titleFa: "ایربادز شیائومی Redmi Buds 5 Pro", titleEn: "Xiaomi Redmi Buds 5 Pro",
    brand: "xiaomi", category: "audio", subcategory: "earbuds",
    price: 4_200_000, discountPercent: 0, finalPrice: 4_200_000,
    rating: 4.3, reviewCount: 198, image: img(31),
    inStock: true, tags: ["اقتصادی"],
  },

  // ── Camera ─────────────────────────────────────────────────────────────────
  {
    id: 32, slug: "canon-eos-r6-mark-ii",
    titleFa: "دوربین کانن EOS R6 Mark II", titleEn: "Canon EOS R6 Mark II",
    brand: "canon", category: "camera", subcategory: "mirrorless",
    price: 145_000_000, discountPercent: 0, finalPrice: 145_000_000,
    rating: 4.9, reviewCount: 63, image: img(32),
    inStock: true, tags: ["حرفه‌ای"], isFeatured: true,
  },
  {
    id: 33, slug: "sony-alpha-a7iv",
    titleFa: "دوربین سونی Alpha A7 IV", titleEn: "Sony Alpha A7 IV",
    brand: "sony", category: "camera", subcategory: "mirrorless",
    price: 168_000_000, discountPercent: 5, finalPrice: fp(168_000_000, 5),
    rating: 4.9, reviewCount: 88, image: img(33),
    inStock: true, tags: ["حرفه‌ای"],
  },
  {
    id: 34, slug: "nikon-z50",
    titleFa: "دوربین نیکون Z50", titleEn: "Nikon Z50",
    brand: "nikon", category: "camera", subcategory: "mirrorless",
    price: 58_000_000, discountPercent: 8, finalPrice: fp(58_000_000, 8),
    rating: 4.6, reviewCount: 47, image: img(34),
    inStock: true, tags: ["مبتدی"],
  },
  {
    id: 35, slug: "gopro-hero-12",
    titleFa: "دوربین گوپرو HERO 12 Black", titleEn: "GoPro HERO 12 Black",
    brand: "gopro", category: "camera", subcategory: "action",
    price: 28_000_000, discountPercent: 12, finalPrice: fp(28_000_000, 12),
    rating: 4.7, reviewCount: 132, image: img(35),
    inStock: true, tags: ["اکشن", "5K"],
  },
  {
    id: 36, slug: "canon-eos-850d",
    titleFa: "دوربین کانن EOS 850D", titleEn: "Canon EOS 850D",
    brand: "canon", category: "camera", subcategory: "dslr",
    price: 45_000_000, discountPercent: 0, finalPrice: 45_000_000,
    rating: 4.5, reviewCount: 74, image: img(36),
    inStock: true, tags: ["مبتدی", "DSLR"],
  },

  // ── Smartwatch ─────────────────────────────────────────────────────────────
  {
    id: 37, slug: "apple-watch-series-9",
    titleFa: "ساعت هوشمند اپل Watch Series 9", titleEn: "Apple Watch Series 9",
    brand: "apple", category: "smartwatch", subcategory: "apple-watch",
    price: 38_000_000, discountPercent: 0, finalPrice: 38_000_000,
    rating: 4.8, reviewCount: 345, image: img(37),
    inStock: true, tags: ["پرفروش"], isFeatured: true,
  },
  {
    id: 38, slug: "samsung-galaxy-watch6-classic",
    titleFa: "ساعت سامسونگ Galaxy Watch 6 Classic", titleEn: "Samsung Galaxy Watch 6 Classic",
    brand: "samsung", category: "smartwatch", subcategory: "android-watch",
    price: 28_000_000, discountPercent: 10, finalPrice: fp(28_000_000, 10),
    rating: 4.7, reviewCount: 156, image: img(38),
    inStock: true, tags: [],
  },
  {
    id: 39, slug: "garmin-fenix-7",
    titleFa: "ساعت گارمین Fēnix 7", titleEn: "Garmin Fēnix 7",
    brand: "garmin", category: "smartwatch", subcategory: "android-watch",
    price: 55_000_000, discountPercent: 0, finalPrice: 55_000_000,
    rating: 4.8, reviewCount: 78, image: img(39),
    inStock: true, tags: ["ورزشی", "GPS"],
  },
  {
    id: 40, slug: "xiaomi-mi-band-8",
    titleFa: "مچ‌بند هوشمند شیائومی Mi Band 8", titleEn: "Xiaomi Mi Band 8",
    brand: "xiaomi", category: "smartwatch", subcategory: "fitness-band",
    price: 2_800_000, discountPercent: 0, finalPrice: 2_800_000,
    rating: 4.5, reviewCount: 512, image: img(40),
    inStock: true, tags: ["اقتصادی", "پرفروش"],
  },
  {
    id: 41, slug: "huawei-watch-gt4",
    titleFa: "ساعت هواوی Watch GT 4", titleEn: "Huawei Watch GT 4",
    brand: "huawei", category: "smartwatch", subcategory: "android-watch",
    price: 18_000_000, discountPercent: 8, finalPrice: fp(18_000_000, 8),
    rating: 4.6, reviewCount: 94, image: img(41),
    inStock: true, tags: [],
  },

  // ── Gaming ─────────────────────────────────────────────────────────────────
  {
    id: 42, slug: "sony-playstation-5",
    titleFa: "کنسول سونی PlayStation 5", titleEn: "Sony PlayStation 5",
    brand: "playstation", category: "gaming", subcategory: "console",
    price: 45_000_000, discountPercent: 0, finalPrice: 45_000_000,
    rating: 4.9, reviewCount: 723, image: img(42),
    inStock: false, tags: ["ناموجود"], isFeatured: true,
  },
  {
    id: 43, slug: "nintendo-switch-oled",
    titleFa: "کنسول نینتندو Switch OLED", titleEn: "Nintendo Switch OLED",
    brand: "nintendo", category: "gaming", subcategory: "console",
    price: 22_000_000, discountPercent: 5, finalPrice: fp(22_000_000, 5),
    rating: 4.8, reviewCount: 411, image: img(43),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 44, slug: "logitech-g502-x-plus",
    titleFa: "ماوس گیمینگ لاجیتک G502 X Plus", titleEn: "Logitech G502 X Plus",
    brand: "logitech", category: "gaming", subcategory: "gaming-mouse",
    price: 8_500_000, discountPercent: 12, finalPrice: fp(8_500_000, 12),
    rating: 4.7, reviewCount: 189, image: img(44),
    inStock: true, tags: ["بی‌سیم"],
  },
  {
    id: 45, slug: "sony-dualsense-edge",
    titleFa: "دسته بازی سونی DualSense Edge", titleEn: "Sony DualSense Edge",
    brand: "playstation", category: "gaming", subcategory: "controller",
    price: 18_000_000, discountPercent: 0, finalPrice: 18_000_000,
    rating: 4.7, reviewCount: 98, image: img(45),
    inStock: true, tags: ["حرفه‌ای"],
  },
  {
    id: 46, slug: "logitech-g733-headset",
    titleFa: "هدست گیمینگ لاجیتک G733", titleEn: "Logitech G733 Headset",
    brand: "logitech", category: "gaming", subcategory: "gaming-headset",
    price: 9_200_000, discountPercent: 15, finalPrice: fp(9_200_000, 15),
    rating: 4.5, reviewCount: 134, image: img(46),
    inStock: true, tags: ["بی‌سیم", "RGB"],
  },
  {
    id: 47, slug: "microsoft-xbox-series-x",
    titleFa: "کنسول مایکروسافت Xbox Series X", titleEn: "Microsoft Xbox Series X",
    brand: "microsoft", category: "gaming", subcategory: "console",
    price: 40_000_000, discountPercent: 0, finalPrice: 40_000_000,
    rating: 4.8, reviewCount: 287, image: img(47),
    inStock: true, tags: ["4K"],
  },

  // ── Accessories ────────────────────────────────────────────────────────────
  {
    id: 48, slug: "anker-736-charger",
    titleFa: "شارژر انکر 736 نانو II 100W", titleEn: "Anker 736 Nano II 100W",
    brand: "anker", category: "accessories", subcategory: "charger",
    price: 3_200_000, discountPercent: 0, finalPrice: 3_200_000,
    rating: 4.8, reviewCount: 267, image: img(48),
    inStock: true, tags: ["GaN", "پرفروش"],
  },
  {
    id: 49, slug: "baseus-powerbank-20000",
    titleFa: "پاوربانک باسئوس 20000 mAh 65W", titleEn: "Baseus 20000 mAh 65W",
    brand: "baseus", category: "accessories", subcategory: "powerbank",
    price: 4_800_000, discountPercent: 10, finalPrice: fp(4_800_000, 10),
    rating: 4.6, reviewCount: 198, image: img(49),
    inStock: true, tags: ["سریع"],
  },
  {
    id: 50, slug: "apple-magsafe-charger",
    titleFa: "شارژر اپل MagSafe 15W", titleEn: "Apple MagSafe 15W",
    brand: "apple", category: "accessories", subcategory: "charger",
    price: 2_500_000, discountPercent: 0, finalPrice: 2_500_000,
    rating: 4.5, reviewCount: 312, image: img(50),
    inStock: true, tags: [],
  },
  {
    id: 51, slug: "baseus-usbc-cable-240w",
    titleFa: "کابل Type-C باسئوس 240W", titleEn: "Baseus 240W USB-C Cable",
    brand: "baseus", category: "accessories", subcategory: "cable",
    price: 980_000, discountPercent: 0, finalPrice: 980_000,
    rating: 4.6, reviewCount: 441, image: img(51),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 52, slug: "samsung-galaxy-s24-clear-case",
    titleFa: "قاب شفاف سامسونگ Galaxy S24 Ultra", titleEn: "Samsung Clear Case S24 Ultra",
    brand: "samsung", category: "accessories", subcategory: "case",
    price: 1_200_000, discountPercent: 0, finalPrice: 1_200_000,
    rating: 4.2, reviewCount: 88, image: img(52),
    inStock: true, tags: [],
  },

  // ── Clothing ───────────────────────────────────────────────────────────────
  {
    id: 53, slug: "nike-tech-fleece-hoodie",
    titleFa: "هودی نایک Tech Fleece", titleEn: "Nike Tech Fleece Hoodie",
    brand: "nike", category: "clothing", subcategory: "hoodie",
    price: 4_500_000, discountPercent: 20, finalPrice: fp(4_500_000, 20),
    rating: 4.7, reviewCount: 223, image: img(53),
    inStock: true, tags: ["تخفیف"],
  },
  {
    id: 54, slug: "adidas-originals-tshirt",
    titleFa: "تی‌شرت آدیداس Originals", titleEn: "Adidas Originals T-Shirt",
    brand: "adidas", category: "clothing", subcategory: "tshirt",
    price: 1_800_000, discountPercent: 0, finalPrice: 1_800_000,
    rating: 4.4, reviewCount: 176, image: img(54),
    inStock: true, tags: [],
  },
  {
    id: 55, slug: "nike-windrunner-jacket",
    titleFa: "جاکت نایک Windrunner", titleEn: "Nike Windrunner Jacket",
    brand: "nike", category: "clothing", subcategory: "jacket",
    price: 6_200_000, discountPercent: 15, finalPrice: fp(6_200_000, 15),
    rating: 4.6, reviewCount: 87, image: img(55),
    inStock: true, tags: ["تخفیف"],
  },
  {
    id: 56, slug: "adidas-ultraboost-22",
    titleFa: "کتونی آدیداس Ultraboost 22", titleEn: "Adidas Ultraboost 22",
    brand: "adidas", category: "shoes", subcategory: "sneaker",
    price: 5_800_000, discountPercent: 10, finalPrice: fp(5_800_000, 10),
    rating: 4.7, reviewCount: 312, image: img(56),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 57, slug: "nike-air-max-270",
    titleFa: "کتونی نایک Air Max 270", titleEn: "Nike Air Max 270",
    brand: "nike", category: "shoes", subcategory: "sneaker",
    price: 4_900_000, discountPercent: 0, finalPrice: 4_900_000,
    rating: 4.5, reviewCount: 428, image: img(57),
    inStock: true, tags: [],
  },
  {
    id: 58, slug: "puma-rs-x",
    titleFa: "کتونی پوما RS-X", titleEn: "Puma RS-X",
    brand: "puma", category: "shoes", subcategory: "sneaker",
    price: 3_700_000, discountPercent: 8, finalPrice: fp(3_700_000, 8),
    rating: 4.4, reviewCount: 156, image: img(58),
    inStock: true, tags: [],
  },
  {
    id: 59, slug: "newbalance-574",
    titleFa: "کتونی نیوبالانس 574", titleEn: "New Balance 574",
    brand: "newbalance", category: "shoes", subcategory: "sneaker",
    price: 4_200_000, discountPercent: 0, finalPrice: 4_200_000,
    rating: 4.6, reviewCount: 241, image: img(59),
    inStock: true, tags: ["کلاسیک"],
  },
  {
    id: 60, slug: "philips-airfryer-xl",
    titleFa: "سرخ‌کن فیلیپس Airfryer XL", titleEn: "Philips Airfryer XL",
    brand: "philips", category: "home", subcategory: "kitchen",
    price: 12_500_000, discountPercent: 20, finalPrice: fp(12_500_000, 20),
    rating: 4.8, reviewCount: 567, image: img(60),
    inStock: true, tags: ["پرفروش", "تخفیف"],
  },
  {
    id: 61, slug: "tefal-nonstick-pan",
    titleFa: "ماهیتابه تفال نچسب", titleEn: "Tefal Non-Stick Pan",
    brand: "tefal", category: "home", subcategory: "kitchen",
    price: 2_800_000, discountPercent: 0, finalPrice: 2_800_000,
    rating: 4.5, reviewCount: 189, image: img(61),
    inStock: true, tags: [],
  },
  {
    id: 62, slug: "dyson-v15-detect",
    titleFa: "جاروبرقی دایسون V15 Detect", titleEn: "Dyson V15 Detect",
    brand: "dyson", category: "home", subcategory: "vacuum",
    price: 38_000_000, discountPercent: 5, finalPrice: fp(38_000_000, 5),
    rating: 4.9, reviewCount: 134, image: img(62),
    inStock: true, tags: ["حرفه‌ای"],
  },
  {
    id: 63, slug: "lg-oled-c3-tv",
    titleFa: "تلویزیون ال‌جی OLED C3", titleEn: "LG OLED C3 TV",
    brand: "lg", category: "home", subcategory: "decor",
    price: 85_000_000, discountPercent: 10, finalPrice: fp(85_000_000, 10),
    rating: 4.9, reviewCount: 98, image: img(63),
    inStock: true, tags: ["4K", "OLED"],
  },
  {
    id: 64, slug: "xiaomi-smart-tv-a2",
    titleFa: "تلویزیون هوشمند شیائومی A2", titleEn: "Xiaomi Smart TV A2",
    brand: "xiaomi", category: "home", subcategory: "decor",
    price: 22_000_000, discountPercent: 15, finalPrice: fp(22_000_000, 15),
    rating: 4.4, reviewCount: 187, image: img(64),
    inStock: true, tags: ["اقتصادی"],
  },
  {
    id: 65, slug: "tech-book-clean-code",
    titleFa: "کتاب Clean Code", titleEn: "Clean Code Book",
    brand: "philips", category: "books", subcategory: "tech-book",
    price: 850_000, discountPercent: 0, finalPrice: 850_000,
    rating: 4.9, reviewCount: 423, image: img(65),
    inStock: true, tags: ["پرفروش"],
  },
  {
    id: 66, slug: "tech-book-pragmatic-programmer",
    titleFa: "کتاب The Pragmatic Programmer", titleEn: "The Pragmatic Programmer",
    brand: "philips", category: "books", subcategory: "tech-book",
    price: 950_000, discountPercent: 5, finalPrice: fp(950_000, 5),
    rating: 4.8, reviewCount: 312, image: img(66),
    inStock: true, tags: [],
  },
  {
    id: 67, slug: "novel-1984",
    titleFa: "رمان ۱۹۸۴", titleEn: "Novel 1984",
    brand: "philips", category: "books", subcategory: "novel",
    price: 450_000, discountPercent: 0, finalPrice: 450_000,
    rating: 4.9, reviewCount: 789, image: img(67),
    inStock: true, tags: ["کلاسیک"],
  },
  {
    id: 68, slug: "self-help-atomic-habits",
    titleFa: "کتاب عادت‌های اتمی", titleEn: "Atomic Habits",
    brand: "philips", category: "books", subcategory: "self-help",
    price: 620_000, discountPercent: 10, finalPrice: fp(620_000, 10),
    rating: 4.9, reviewCount: 1024, image: img(68),
    inStock: true, tags: ["پرفروش"],
  },
];

// ─── Helper Exports ───────────────────────────────────────────────────────────

export const getProductBySlug = (slug: string): Product | undefined =>
  products.find((p) => p.slug === slug);

export const getProductsByCategory = (categoryId: string): Product[] =>
  products.filter((p) => p.category === categoryId);

export const getProductsByBrand = (brandId: string): Product[] =>
  products.filter((p) => p.brand === brandId);

export const getFeaturedProducts = (): Product[] =>
  products.filter((p) => p.isFeatured);

export const getNewProducts = (): Product[] =>
  products.filter((p) => p.isNew);

export const getDiscountedProducts = (): Product[] =>
  products.filter((p) => p.discountPercent > 0);

export const getCategoryById = (id: string): Category | undefined =>
  categories.find((c) => c.id === id);

export const getBrandById = (id: string): Brand | undefined =>
  brands.find((b) => b.id === id);

export const getProductsBySubcategory = (subcategoryId: string): Product[] =>
  products.filter((p) => p.subcategory === subcategoryId);
