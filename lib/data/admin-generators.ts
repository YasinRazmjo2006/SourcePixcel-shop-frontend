// lib/data/admin-generators.ts
// Seeded random generator — deterministic mock data

// Mulberry32 PRNG — fast, deterministic
function createRandom(seed: number) {
  let state = seed;
  return function random(): number {
    state |= 0;
    state = (state + 0x6d2b79f5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function seededRandom(seed: number) {
  return createRandom(seed);
}

export function pick<T>(arr: T[], rand: () => number): T {
  return arr[Math.floor(rand() * arr.length)];
}

export function pickMany<T>(arr: T[], count: number, rand: () => number): T[] {
  const shuffled = [...arr].sort(() => rand() - 0.5);
  return shuffled.slice(0, count);
}

export function intBetween(min: number, max: number, rand: () => number): number {
  return Math.floor(rand() * (max - min + 1)) + min;
}

export function floatBetween(min: number, max: number, rand: () => number, decimals = 2): number {
  const value = rand() * (max - min) + min;
  return Number(value.toFixed(decimals));
}

export function weightedPick<T>(
  items: { value: T; weight: number }[],
  rand: () => number
): T {
  const totalWeight = items.reduce((sum, item) => sum + item.weight, 0);
  let random = rand() * totalWeight;
  for (const item of items) {
    random -= item.weight;
    if (random <= 0) return item.value;
  }
  return items[items.length - 1].value;
}

// ═══════════════════════════════════════════════════════════════
// PERSIAN DATA
// ═══════════════════════════════════════════════════════════════

export const PERSIAN_FIRST_NAMES = [
  "علی", "محمد", "رضا", "حسین", "امیر", "مهدی", "سعید", "حسن", "مجید", "کاظم",
  "سارا", "مریم", "زهرا", "فاطمه", "نرگس", "الهام", "شیما", "نیلوفر", "پریسا", "نازنین",
  "احمد", "یاسر", "پویا", "آرش", "کاوه", "بهرام", "داریوش", "کوروش", "سیاوش", "فریدون",
  "مینا", "لیلا", "سحر", "پگاه", "ترانه", "بهاره", "شقایق", "هستی", "نازنین", "سمیرا",
  "بهنام", "بهزاد", "بابک", "پیمان", "جمشید", "رامین", "سامان", "ساسان", "سینا", "فرشاد",
];

export const PERSIAN_LAST_NAMES = [
  "محمدی", "احمدی", "رضایی", "حسینی", "کریمی", "نوری", "رحیمی", "صادقی", "موسوی", "هاشمی",
  "علی‌پور", "مرادی", "جعفری", "قاسمی", "کاظمی", "بهرامی", "زمانی", "عباسی", "یوسفی", "امینی",
  "شریفی", "سلطانی", "باقری", "نجفی", "طاهری", "فرهادی", "زارعی", "بیات", "صالحی", "خانی",
  "ملکی", "شاهینی", "خسروی", "پناهی", "افشار", "ایرانی", "بابایی", "تقوی", "ثابتی", "جوادی",
];

export const PERSIAN_CITIES = [
  "تهران", "مشهد", "اصفهان", "کرج", "شیراز", "تبریز", "قم", "اهواز", "کرمانشاه", "ارومیه",
  "رشت", "زاهدان", "همدان", "کرمان", "یزد", "اردبیل", "بندرعباس", "اراک", "اسلام‌شهر", "زنجان",
  "ساری", "قزوین", "بوشهر", "سنندج", "گرگان", "خرم‌آباد", "بابل", "آمل", "نجف‌آباد", "سبزوار",
];

export const PERSIAN_STREETS = [
  "خیابان ولیعصر", "خیابان انقلاب", "بلوار کشاورز", "خیابان آزادی", "خیابان فردوسی",
  "بلوار میرداماد", "خیابان شریعتی", "بلوار صادقیه", "خیابان جمهوری", "بلوار نیایش",
  "خیابان مطهری", "بلوار ستارخان", "خیابان طالقانی", "بلوار پاسداران", "خیابان بهشتی",
];
