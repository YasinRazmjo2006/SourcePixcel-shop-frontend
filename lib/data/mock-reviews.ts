// lib/data/mock-reviews.ts
import type { Review } from "@/lib/types";

export const mockReviews: Review[] = [
  {
    id: "rev-1",
    productId: 1,
    authorName: "علی محمدی",
    authorInitial: "ع",
    rating: 5,
    title: "کیفیت فوق‌العاده",
    body: "دوربین این گوشی واقعاً بی‌نظیره. توی نور کم هم عکس‌های عالی می‌گیره. باتری هم تا آخر روز دووم میاره. کاملاً راضی هستم و به همه پیشنهاد می‌کنم.",
    date: "1403/06/15",
    helpful: 42,
    notHelpful: 3,
    verified: true,
    adminResponse: {
      body: "ممنون از نظر مثبت شما. خوشحالیم که راضی هستید.",
      date: "1403/06/16",
    },
  },
  {
    id: "rev-2",
    productId: 1,
    authorName: "سارا احمدی",
    authorInitial: "س",
    rating: 4,
    title: "خوب ولی گرون",
    body: "به طور کلی گوشی خوبیه ولی قیمتش یه کم بالاست. طراحی و صفحه‌نمایشش عالیه. فقط ای کاش باتریش کمی قوی‌تر بود.",
    date: "1403/06/08",
    helpful: 28,
    notHelpful: 5,
    verified: true,
  },
  {
    id: "rev-3",
    productId: 1,
    authorName: "رضا کریمی",
    authorInitial: "ر",
    rating: 5,
    title: "ارسال سریع و بسته‌بندی عالی",
    body: "بسته‌بندی خیلی حرفه‌ای بود. گوشی کاملاً سالم و اورجینال رسید. پشتیبانی هم خیلی سریع جواب داد. ممنون SourcePixcel.",
    date: "1403/05/25",
    helpful: 35,
    notHelpful: 1,
    verified: true,
  },
  {
    id: "rev-4",
    productId: 1,
    authorName: "مریم رضایی",
    authorInitial: "م",
    rating: 3,
    title: "متوسط",
    body: "انتظار بیشتری داشتم. دوربین خوبه ولی رابط کاربری یکم پیچیده‌ست. برای این قیمت می‌شد بهتر باشه.",
    date: "1403/05/18",
    helpful: 12,
    notHelpful: 8,
    verified: false,
  },
  {
    id: "rev-5",
    productId: 2,
    authorName: "حسین نوری",
    authorInitial: "ح",
    rating: 5,
    title: "بهترین خریدم",
    body: "iPhone 15 Pro Max واقعاً ارزشش رو داره. دوربین، سرعت، کیفیت ساخت، همه چیز عالیه. هیچ ایرادی نمی‌تونم بگیرم.",
    date: "1403/06/20",
    helpful: 56,
    notHelpful: 2,
    verified: true,
  },
  {
    id: "rev-6",
    productId: 2,
    authorName: "نازنین صادقی",
    authorInitial: "ن",
    rating: 4,
    title: "خوب",
    body: "کیفیت ساخت عالیه. فقط به نظرم نسبت به نسخه قبلی تغییرات زیادی نداشته. ولی در کل راضی هستم.",
    date: "1403/06/05",
    helpful: 18,
    notHelpful: 4,
    verified: true,
  },
];

export const getReviewsByProduct = (productId: number): Review[] => {
  return mockReviews.filter((r) => r.productId === productId);
};

// Generic fallback reviews for products without specific reviews
export const getGenericReviews = (): Review[] => {
  return [
    {
      id: "rev-generic-1",
      productId: 0,
      authorName: "کاربر SourcePixcel",
      authorInitial: "ک",
      rating: 5,
      title: "کیفیت عالی",
      body: "محصول با کیفیت و مطابق توضیحات بود. ارسال سریع انجام شد و بسته‌بندی عالی بود. حتماً دوباره خرید می‌کنم.",
      date: "1403/06/10",
      helpful: 24,
      notHelpful: 2,
      verified: true,
    },
    {
      id: "rev-generic-2",
      productId: 0,
      authorName: "محمد رحیمی",
      authorInitial: "م",
      rating: 4,
      title: "خوب و مقرون به صرفه",
      body: "نسبت به قیمتش کیفیت خوبی داره. فقط کمی زودتر از انتظارم رسید که باعث شد کمی گیج بشم. در کل راضی هستم.",
      date: "1403/06/02",
      helpful: 15,
      notHelpful: 3,
      verified: true,
    },
    {
      id: "rev-generic-3",
      productId: 0,
      authorName: "فاطمه حسینی",
      authorInitial: "ف",
      rating: 5,
      title: "پیشنهاد می‌کنم",
      body: "از خریدم کاملاً راضی هستم. محصول اورجینال و باکیفیت. پشتیبانی SourcePixcel هم عالی بود.",
      date: "1403/05/22",
      helpful: 31,
      notHelpful: 1,
      verified: true,
    },
  ];
};

export const getReviewsForProduct = (productId: number): Review[] => {
  const specific = getReviewsByProduct(productId);
  if (specific.length > 0) return specific;
  // Return generic reviews with adjusted productId
  return getGenericReviews().map((r) => ({ ...r, productId }));
};
