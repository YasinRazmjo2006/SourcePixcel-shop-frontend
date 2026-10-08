#!/usr/bin/env python3

import json
import os
from pathlib import Path

PROJECT_NAME = "SourcePixcel"
PROJECT_ROOT = os.path.join(os.getcwd(), PROJECT_NAME)

DIRECTORIES = [
    "app/[locale]",
    "components/ui",
    "lib",
    "messages",
    "public/images",
]

PACKAGE_JSON = {
    "name": "sourcepixcel",
    "version": "1.0.0",
    "private": True,
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint",
        "typecheck": "tsc --noEmit",
    },
    "dependencies": {
        "next": "15.5.9",
        "react": "19.1.1",
        "react-dom": "19.1.1",
        "class-variance-authority": "0.7.1",
        "clsx": "2.1.1",
        "tailwind-merge": "3.3.1",
        "@radix-ui/react-slot": "1.2.3",
        "@radix-ui/react-dialog": "1.1.15",
        "@radix-ui/react-dropdown-menu": "2.1.16",
        "@radix-ui/react-select": "2.2.6",
        "@radix-ui/react-tabs": "1.1.13",
        "@radix-ui/react-accordion": "1.2.12",
        "@radix-ui/react-checkbox": "1.3.3",
        "@radix-ui/react-switch": "1.2.6",
        "@radix-ui/react-slider": "1.3.6",
        "@radix-ui/react-tooltip": "1.2.8",
        "@radix-ui/react-popover": "1.1.15",
        "@radix-ui/react-label": "2.1.7",
        "@radix-ui/react-separator": "1.1.7",
        "@radix-ui/react-avatar": "1.1.10",
        # Radix has no react-badge primitive. This npm alias preserves the
        # requested package key; build Badge as a local shadcn/ui component.
        "@radix-ui/react-badge": "npm:@radix-ui/react-primitive@2.1.3",
        "@radix-ui/react-progress": "1.1.7",
        "lucide-react": "0.468.0",
        "next-intl": "3.26.5",
        "zustand": "5.0.8",
        "react-hook-form": "7.62.0",
        "@hookform/resolvers": "5.2.1",
        "zod": "4.1.5",
        "date-fns": "4.1.0",
        "date-fns-jalali": "4.1.0-0",
        "embla-carousel-react": "8.6.0",
        "embla-carousel-autoplay": "8.6.0",
        "framer-motion": "12.23.12",
    },
    "devDependencies": {
        "typescript": "5.9.2",
        "@types/node": "22.18.6",
        "@types/react": "19.1.10",
        "@types/react-dom": "19.1.7",
        "tailwindcss": "4.1.12",
        "@tailwindcss/postcss": "4.1.12",
        "postcss": "8.5.6",
        "autoprefixer": "10.4.21",
    },
}

FILES = {
    "package.json": json.dumps(PACKAGE_JSON, ensure_ascii=False, indent=2) + "\n",
    "tsconfig.json": '''{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", \".next/types/**/*.ts\", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
''',
    "next.config.js": '''/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
};

module.exports = nextConfig;
''',
    "tailwind.config.ts": '''// Tailwind CSS v4 legacy JS config; load using @config from global CSS.
const config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#EF4056",
        secondary: "#00BFFF",
        success: "#22C55E",
        warning: "#F59E0B",
        danger: "#EF4444",
        background: { page: "#F5F5F5", card: "#FFFFFF", muted: "#F0F0F1" },
        text: { heading: "#3F4064", body: "#62666D", muted: "#A1A3A8" },
        border: "#E0E0E2",
      },
      fontFamily: {
        sans: ["Vazirmatn", "Inter", "sans-serif"],
        vazirmatn: ["Vazirmatn", "sans-serif"],
        inter: ["Inter", "sans-serif"],
      },
    },
  },
};

export default config;
''',
    "postcss.config.js": '''module.exports = {
  plugins: {
    "@tailwindcss/postcss": {},
    autoprefixer: {},
  },
};
''',
    ".env.example": '''# Copy to .env.local and configure values for your environment.
NEXT_PUBLIC_APP_NAME=SourcePixcel
NEXT_PUBLIC_APP_URL=http://localhost:3000
''',
    ".gitignore": '''/node_modules
/.pnp
.pnp.*
/.next/
/out/
/build/
.env*
!.env.example
*.tsbuildinfo
next-env.d.ts
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*
.vscode/
.idea/
.DS_Store
''',
}


def create_base_project():
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    print(f"Created project directory: {PROJECT_ROOT}")
    for relative_dir in DIRECTORIES:
        os.makedirs(os.path.join(PROJECT_ROOT, relative_dir), exist_ok=True)
        print(f"Created directory: {relative_dir}")
    for relative_path, contents in FILES.items():
        path = os.path.join(PROJECT_ROOT, relative_path)
        with open(path, "w", encoding="utf-8") as file:
            file.write(contents)
        print(f"Wrote file: {relative_path}")
    print(f"\nBase configuration created successfully in: {PROJECT_ROOT}")


ROOT = Path.cwd()
FA_MESSAGES = json.loads('{\n  "common": {\n    "siteName": "سورس\u200cپیکسل",\n    "tagline": "خریدی هوشمند، تجربه\u200cای بهتر",\n    "header": {\n      "searchPlaceholder": "جست\u200cوجوی کالا، برند یا دسته\u200cبندی…",\n      "search": "جست\u200cوجو",\n      "account": "حساب کاربری",\n      "login": "ورود",\n      "register": "ثبت\u200cنام",\n      "loginOrRegister": "ورود | ثبت\u200cنام",\n      "cart": "سبد خرید",\n      "wishlist": "علاقه\u200cمندی\u200cها",\n      "compare": "مقایسه",\n      "menu": "منو",\n      "language": "زبان",\n      "searchResults": "نتایج جست\u200cوجو",\n      "noSearchResults": "نتیجه\u200cای پیدا نشد",\n      "viewAll": "مشاهده همه"\n    },\n    "navigation": {\n      "home": "خانه",\n      "categories": "دسته\u200cبندی\u200cها",\n      "products": "همه کالاها",\n      "blog": "مجله و مقالات",\n      "about": "درباره ما",\n      "contact": "تماس با ما",\n      "faq": "سؤالات متداول",\n      "orders": "سفارش\u200cهای من",\n      "profile": "پروفایل",\n      "logout": "خروج",\n      "offers": "پیشنهادهای ویژه"\n    },\n    "actions": {\n      "addToCart": "افزودن به سبد خرید",\n      "addedToCart": "به سبد خرید اضافه شد",\n      "buyNow": "خرید فوری",\n      "continueShopping": "ادامه خرید",\n      "viewDetails": "مشاهده جزئیات",\n      "showMore": "نمایش بیشتر",\n      "showLess": "نمایش کمتر",\n      "apply": "اعمال",\n      "clear": "پاک کردن",\n      "clearAll": "پاک کردن همه",\n      "submit": "ثبت",\n      "save": "ذخیره تغییرات",\n      "cancel": "لغو",\n      "edit": "ویرایش",\n      "delete": "حذف",\n      "remove": "حذف از فهرست",\n      "retry": "تلاش دوباره",\n      "back": "بازگشت",\n      "next": "مرحله بعد",\n      "previous": "مرحله قبل",\n      "close": "بستن",\n      "share": "اشتراک\u200cگذاری",\n      "loading": "در حال بارگذاری…",\n      "seeAll": "مشاهده همه"\n    },\n    "forms": {\n      "required": "تکمیل این فیلد الزامی است.",\n      "invalidEmail": "ایمیل واردشده معتبر نیست.",\n      "invalidPhone": "شماره همراه معتبر نیست.",\n      "password": "رمز عبور",\n      "confirmsecret-74761a59": "تکرار رمز عبور",\n      "passwordMismatch": "رمزهای عبور یکسان نیستند.",\n      "email": "آدرس ایمیل",\n      "phone": "شماره همراه",\n      "fullName": "نام و نام خانوادگی",\n      "firstName": "نام",\n      "lastName": "نام خانوادگی",\n      "address": "نشانی کامل",\n      "postalCode": "کد پستی",\n      "city": "شهر",\n      "province": "استان",\n      "message": "پیام شما",\n      "subject": "موضوع",\n      "emailPlaceholder": "example@email.com",\n      "selectOption": "انتخاب کنید",\n      "success": "اطلاعات با موفقیت ثبت شد.",\n      "error": "ثبت اطلاعات انجام نشد. دوباره تلاش کنید."\n    },\n    "footer": {\n      "description": "سورس\u200cپیکسل، همراه مطمئن شما برای خرید آنلاین کالاهای باکیفیت.",\n      "customerService": "خدمات مشتریان",\n      "quickLinks": "دسترسی سریع",\n      "guides": "راهنمای خرید",\n      "aboutUs": "درباره سورس\u200cپیکسل",\n      "contactUs": "تماس با ما",\n      "faq": "سؤالات متداول",\n      "returns": "رویه بازگشت کالا",\n      "shipping": "شیوه\u200cهای ارسال",\n      "terms": "شرایط و قوانین",\n      "privacy": "حریم خصوصی",\n      "followUs": "ما را دنبال کنید",\n      "newsletter": "عضویت در خبرنامه",\n      "newsletterText": "از تازه\u200cترین پیشنهادها و تخفیف\u200cها باخبر شوید.",\n      "newsletterPlaceholder": "ایمیل خود را وارد کنید",\n      "copyright": "تمامی حقوق این وب\u200cسایت برای سورس\u200cپیکسل محفوظ است.",\n      "trustTitle": "خریدی مطمئن و آسوده",\n      "paymentMethods": "درگاه\u200cهای پرداخت معتبر"\n    },\n    "trustBadges": {\n      "original": "ضمانت اصالت کالا",\n      "return": "۷ روز ضمانت بازگشت",\n      "secure": "پرداخت امن",\n      "support": "پشتیبانی ۲۴/۷",\n      "delivery": "ارسال سریع"\n    },\n    "serviceItems": {\n      "deliveryTitle": "ارسال سریع",\n      "deliveryText": "ارسال به سراسر ایران",\n      "originalTitle": "ضمانت اصالت",\n      "originalText": "تضمین کیفیت و اصالت کالا",\n      "returnTitle": "۷ روز بازگشت",\n      "returnText": "فرصت بررسی و بازگرداندن کالا",\n      "supportTitle": "پشتیبانی همیشگی",\n      "supportText": "پاسخ\u200cگوی شما در تمام روزهای هفته",\n      "secureTitle": "پرداخت امن",\n      "secureText": "پرداخت از درگاه\u200cهای معتبر"\n    },\n    "messages": {\n      "unexpected": "خطایی رخ داده است.",\n      "empty": "موردی برای نمایش وجود ندارد.",\n      "offline": "اتصال اینترنت خود را بررسی کنید.",\n      "notFound": "صفحه یا کالای موردنظر پیدا نشد.",\n      "success": "عملیات با موفقیت انجام شد."\n    },\n    "currency": "تومان",\n    "items": "مورد",\n    "results": "نتیجه"\n  },\n  "home": {\n    "heroSlider": {\n      "eyebrow": "تجربه\u200cای تازه از خرید آنلاین",\n      "slide1Title": "انتخاب هوشمندانه، خرید آسان",\n      "slide1Text": "محصولات محبوبتان را با بهترین قیمت پیدا کنید.",\n      "slide1Cta": "مشاهده محصولات",\n      "slide2Title": "فصل تازه، پیشنهادهای تازه",\n      "slide2Text": "برای انتخاب\u200cهای تازه، تخفیف\u200cهای ویژه منتظر شماست.",\n      "slide2Cta": "دیدن پیشنهادها",\n      "slide3Title": "تکنولوژی در کنار شما",\n      "slide3Text": "جدیدترین محصولات دیجیتال را کشف کنید.",\n      "slide3Cta": "خرید محصولات دیجیتال",\n      "previous": "اسلاید قبلی",\n      "next": "اسلاید بعدی",\n      "goToSlide": "رفتن به اسلاید شماره {number}"\n    },\n    "categoryCircles": {\n      "title": "خرید بر اساس دسته\u200cبندی",\n      "subtitle": "دسته\u200cبندی مورد علاقه\u200cتان را انتخاب کنید",\n      "electronics": "کالای دیجیتال",\n      "mobile": "موبایل",\n      "fashion": "مد و پوشاک",\n      "home": "خانه و آشپزخانه",\n      "beauty": "زیبایی و سلامت",\n      "supermarket": "سوپرمارکت",\n      "books": "کتاب و لوازم\u200cتحریر",\n      "sports": "ورزش و سفر",\n      "toys": "اسباب\u200cبازی",\n      "tools": "ابزار و خودرو",\n      "accessories": "لوازم جانبی",\n      "seeCategories": "همه دسته\u200cبندی\u200cها"\n    },\n    "amazingOffer": {\n      "title": "پیشنهاد شگفت\u200cانگیز",\n      "subtitle": "فرصتی محدود برای خریدی به\u200cصرفه",\n      "endsIn": "پایان پیشنهاد تا",\n      "hours": "ساعت",\n      "minutes": "دقیقه",\n      "seconds": "ثانیه",\n      "viewAll": "مشاهده همه پیشنهادها",\n      "discount": "تخفیف",\n      "expired": "پیشنهاد به پایان رسید"\n    },\n    "bestSellers": {\n      "title": "پرفروش\u200cترین\u200cها",\n      "subtitle": "محبوب\u200cترین انتخاب\u200cهای کاربران",\n      "viewAll": "مشاهده همه پرفروش\u200cها"\n    },\n    "newArrivals": {\n      "title": "جدیدترین\u200cها",\n      "subtitle": "تازه\u200cترین محصولات فروشگاه",\n      "viewAll": "مشاهده تازه\u200cها",\n      "new": "جدید"\n    },\n    "brands": {\n      "title": "برندهای محبوب",\n      "subtitle": "خرید از برندهای معتبر",\n      "viewAll": "همه برندها"\n    },\n    "blog": {\n      "title": "از مجله سورس\u200cپیکسل",\n      "subtitle": "راهنماها و مطالب خواندنی برای انتخاب بهتر",\n      "readMore": "ادامه مطلب",\n      "viewAll": "مشاهده همه مقالات",\n      "readingTime": "دقیقه مطالعه",\n      "latest": "تازه\u200cترین مطالب"\n    },\n    "testimonials": {\n      "title": "صدای مشتریان ما",\n      "subtitle": "تجربه خرید کاربران سورس\u200cپیکسل",\n      "verifiedPurchase": "خرید تأییدشده",\n      "previous": "نظر قبلی",\n      "next": "نظر بعدی"\n    },\n    "newsletter": {\n      "title": "از پیشنهادهای ویژه جا نمانید",\n      "subtitle": "با عضویت در خبرنامه، تازه\u200cترین تخفیف\u200cها را زودتر دریافت کنید.",\n      "placeholder": "ایمیل شما",\n      "subscribe": "عضویت در خبرنامه",\n      "success": "با موفقیت در خبرنامه عضو شدید.",\n      "alreadySubscribed": "این ایمیل قبلاً ثبت شده است.",\n      "privacy": "اطلاعات شما نزد ما محفوظ می\u200cماند."\n    }\n  },\n  "product": {\n    "details": "جزئیات محصول",\n    "description": "توضیحات محصول",\n    "specifications": "مشخصات فنی",\n    "reviews": "دیدگاه کاربران",\n    "related": "محصولات مشابه",\n    "brand": "برند",\n    "sku": "شناسه کالا",\n    "availability": "وضعیت موجودی",\n    "inStock": "موجود در انبار",\n    "outOfStock": "ناموجود",\n    "lowStock": "تنها {count} عدد باقی مانده",\n    "rating": "امتیاز",\n    "reviewCount": "{count} دیدگاه",\n    "shortSpecs": "ویژگی\u200cهای کلیدی",\n    "color": "رنگ",\n    "size": "سایز",\n    "chooseColor": "انتخاب رنگ",\n    "chooseSize": "انتخاب سایز",\n    "seller": "فروشنده",\n    "sellerName": "فروشگاه سورس\u200cپیکسل",\n    "sellerRating": "رضایت خریداران",\n    "warranty": "گارانتی",\n    "warrantyValue": "ضمانت اصالت و سلامت فیزیکی",\n    "delivery": "زمان ارسال",\n    "deliveryValue": "ارسال سریع به سراسر کشور",\n    "quantity": "تعداد",\n    "increaseQuantity": "افزایش تعداد",\n    "decreaseQuantity": "کاهش تعداد",\n    "addToWishlist": "افزودن به علاقه\u200cمندی\u200cها",\n    "removeFromWishlist": "حذف از علاقه\u200cمندی\u200cها",\n    "addToCompare": "افزودن به مقایسه",\n    "share": "اشتراک\u200cگذاری محصول",\n    "discount": "تخفیف",\n    "originalPrice": "قیمت قبل",\n    "finalPrice": "قیمت نهایی",\n    "price": "قیمت",\n    "specName": "عنوان ویژگی",\n    "specValue": "مقدار",\n    "pros": "نقاط قوت",\n    "cons": "نقاط ضعف",\n    "writeReview": "ثبت دیدگاه",\n    "yourRating": "امتیاز شما",\n    "reviewTitle": "عنوان دیدگاه",\n    "reviewText": "متن دیدگاه",\n    "reviewSubmit": "ارسال دیدگاه",\n    "reviewThankYou": "از ثبت دیدگاه شما سپاسگزاریم.",\n    "ratingBreakdown": "توزیع امتیازها",\n    "noReviews": "هنوز دیدگاهی برای این محصول ثبت نشده است.",\n    "sortReviews": "مرتب\u200cسازی دیدگاه\u200cها",\n    "newestReviews": "جدیدترین",\n    "helpfulReviews": "مفیدترین",\n    "verifiedBuyer": "خریدار این محصول",\n    "question": "سؤالی درباره این محصول دارید؟",\n    "installments": "امکان خرید اقساطی",\n    "breadcrumb": "مسیر صفحه",\n    "imageAlt": "تصویر محصول {name}"\n  },\n  "cart": {\n    "title": "سبد خرید",\n    "emptyTitle": "سبد خرید شما خالی است",\n    "emptyText": "برای شروع، محصولات مورد علاقه\u200cتان را به سبد اضافه کنید.",\n    "items": {\n      "title": "کالاهای سبد شما",\n      "quantity": "تعداد",\n      "remove": "حذف کالا",\n      "saveForLater": "انتقال به علاقه\u200cمندی\u200cها",\n      "inStock": "آماده ارسال",\n      "seller": "فروشنده",\n      "unitPrice": "قیمت هر عدد",\n      "itemCount": "{count} کالا"\n    },\n    "summary": {\n      "title": "خلاصه سفارش",\n      "subtotal": "جمع قیمت کالاها",\n      "discount": "سود شما از خرید",\n      "shipping": "هزینه ارسال",\n      "shippingFree": "رایگان",\n      "tax": "مالیات",\n      "total": "مبلغ قابل پرداخت",\n      "coupon": "کد تخفیف",\n      "couponPlaceholder": "کد تخفیف را وارد کنید",\n      "applyCoupon": "اعمال کد",\n      "couponApplied": "کد تخفیف اعمال شد.",\n      "couponInvalid": "کد تخفیف معتبر نیست.",\n      "checkout": "ادامه فرایند خرید",\n      "estimate": "هزینه ارسال در مرحله بعد مشخص می\u200cشود.",\n      "secureCheckout": "پرداخت امن"\n    },\n    "checkout": {\n      "title": "تکمیل سفارش",\n      "steps": {\n        "cart": "سبد خرید",\n        "shipping": "اطلاعات ارسال",\n        "payment": "پرداخت",\n        "confirmation": "تأیید سفارش"\n      },\n      "shippingTitle": "اطلاعات گیرنده و ارسال",\n      "paymentTitle": "روش پرداخت",\n      "reviewTitle": "بازبینی سفارش",\n      "recipient": "مشخصات گیرنده",\n      "address": "نشانی تحویل",\n      "addAddress": "افزودن نشانی جدید",\n      "deliveryMethod": "روش ارسال",\n      "standardDelivery": "ارسال عادی",\n      "expressDelivery": "ارسال سریع",\n      "deliveryDate": "زمان تحویل تقریبی",\n      "paymentOnline": "پرداخت اینترنتی",\n      "paymentOnDelivery": "پرداخت هنگام تحویل",\n      "orderNote": "توضیحات سفارش",\n      "placeOrder": "ثبت نهایی سفارش",\n      "continueToPayment": "ادامه و انتخاب پرداخت",\n      "orderSuccess": "سفارش شما با موفقیت ثبت شد.",\n      "orderNumber": "شماره سفارش",\n      "mockPayment": "این فروشگاه نمایشی است؛ پرداخت واقعی انجام نمی\u200cشود.",\n      "requiredAddress": "لطفاً نشانی تحویل را وارد کنید."\n    }\n  },\n  "account": {\n    "title": "حساب کاربری",\n    "dashboard": "پیشخوان",\n    "welcome": "سلام {name}، خوش آمدید",\n    "profile": {\n      "title": "اطلاعات حساب",\n      "edit": "ویرایش پروفایل",\n      "firstName": "نام",\n      "lastName": "نام خانوادگی",\n      "email": "ایمیل",\n      "phone": "شماره همراه",\n      "birthDate": "تاریخ تولد",\n      "gender": "جنسیت",\n      "male": "مرد",\n      "female": "زن",\n      "saveSuccess": "پروفایل شما به\u200cروزرسانی شد."\n    },\n    "orders": {\n      "title": "سفارش\u200cهای من",\n      "orderNumber": "شماره سفارش",\n      "date": "تاریخ ثبت",\n      "total": "مبلغ سفارش",\n      "status": "وضعیت",\n      "details": "جزئیات سفارش",\n      "tracking": "کد پیگیری",\n      "view": "مشاهده سفارش",\n      "empty": "هنوز سفارشی ثبت نکرده\u200cاید.",\n      "statuses": {\n        "pending": "در انتظار پرداخت",\n        "processing": "در حال آماده\u200cسازی",\n        "shipped": "ارسال\u200cشده",\n        "delivered": "تحویل\u200cشده",\n        "cancelled": "لغوشده"\n      }\n    },\n    "wishlist": {\n      "title": "فهرست علاقه\u200cمندی\u200cها",\n      "empty": "هنوز محصولی به علاقه\u200cمندی\u200cها اضافه نکرده\u200cاید.",\n      "remove": "حذف از فهرست",\n      "moveToCart": "افزودن به سبد خرید",\n      "count": "{count} محصول"\n    },\n    "addresses": "نشانی\u200cهای من",\n    "security": "امنیت حساب",\n    "signOut": "خروج از حساب"\n  },\n  "categories": {\n    "title": "دسته\u200cبندی کالاها",\n    "all": "همه دسته\u200cبندی\u200cها",\n    "breadcrumbHome": "خانه",\n    "products": "محصولات",\n    "productCount": "{count} کالا",\n    "noProducts": "محصولی در این دسته\u200cبندی پیدا نشد.",\n    "subcategories": "زیر\u200cدسته\u200cها",\n    "popular": "دسته\u200cبندی\u200cهای محبوب",\n    "electronics": "کالای دیجیتال",\n    "mobile": "موبایل و تبلت",\n    "laptop": "لپ\u200cتاپ و کامپیوتر",\n    "fashion": "مد و پوشاک",\n    "home": "خانه و آشپزخانه",\n    "beauty": "زیبایی و سلامت",\n    "supermarket": "سوپرمارکت",\n    "books": "کتاب و لوازم\u200cتحریر",\n    "sports": "ورزش و سفر",\n    "toys": "اسباب\u200cبازی و کودک",\n    "automotive": "ابزار و خودرو",\n    "jewelry": "طلا و زیورآلات"\n  },\n  "filters": {\n    "title": "فیلترها",\n    "category": "دسته\u200cبندی",\n    "brand": "برند",\n    "searchBrand": "جست\u200cوجوی برند",\n    "price": "محدوده قیمت",\n    "minPrice": "حداقل قیمت",\n    "maxPrice": "حداکثر قیمت",\n    "color": "رنگ",\n    "size": "سایز",\n    "availability": "موجودی کالا",\n    "inStockOnly": "فقط کالاهای موجود",\n    "discountOnly": "فقط کالاهای تخفیف\u200cدار",\n    "rating": "حداقل امتیاز",\n    "ratingAndUp": "و بالاتر",\n    "clear": "حذف فیلترها",\n    "showResults": "نمایش کالاها",\n    "activeFilters": "فیلترهای اعمال\u200cشده",\n    "allBrands": "همه برندها",\n    "colors": {\n      "black": "مشکی",\n      "white": "سفید",\n      "gray": "خاکستری",\n      "red": "قرمز",\n      "blue": "آبی",\n      "green": "سبز",\n      "pink": "صورتی",\n      "gold": "طلایی"\n    },\n    "noBrands": "برندی پیدا نشد"\n  },\n  "sorting": {\n    "title": "مرتب\u200cسازی",\n    "bestselling": "پرفروش\u200cترین",\n    "newest": "جدیدترین",\n    "cheapest": "ارزان\u200cترین",\n    "mostExpensive": "گران\u200cترین",\n    "popular": "محبوب\u200cترین",\n    "highestRated": "بالاترین امتیاز",\n    "mostDiscounted": "بیشترین تخفیف",\n    "relevance": "مرتبط\u200cترین"\n  },\n  "checkout": {\n    "title": "تکمیل سفارش",\n    "steps": {\n      "cart": "سبد خرید",\n      "shipping": "اطلاعات ارسال",\n      "payment": "پرداخت"\n    }\n  },\n  "errors": {\n    "notFoundTitle": "صفحه پیدا نشد",\n    "notFoundText": "صفحه\u200cای که به دنبال آن هستید وجود ندارد یا جابه\u200cجا شده است.",\n    "backHome": "بازگشت به خانه",\n    "general": "مشکلی پیش آمده است."\n  }\n}')
EN_MESSAGES = json.loads('{\n  "common": {\n    "siteName": "SourcePixcel",\n    "tagline": "Smarter shopping, better experiences",\n    "header": {\n      "searchPlaceholder": "Search products, brands, or categories…",\n      "search": "Search",\n      "account": "My account",\n      "login": "Sign in",\n      "register": "Register",\n      "loginOrRegister": "Sign in | Register",\n      "cart": "Shopping cart",\n      "wishlist": "Wishlist",\n      "compare": "Compare",\n      "menu": "Menu",\n      "language": "Language",\n      "searchResults": "Search results",\n      "noSearchResults": "No results found",\n      "viewAll": "View all"\n    },\n    "navigation": {\n      "home": "Home",\n      "categories": "Categories",\n      "products": "All products",\n      "blog": "Journal & articles",\n      "about": "About us",\n      "contact": "Contact us",\n      "faq": "FAQs",\n      "orders": "My orders",\n      "profile": "Profile",\n      "logout": "Sign out",\n      "offers": "Special offers"\n    },\n    "actions": {\n      "addToCart": "Add to cart",\n      "addedToCart": "Added to cart",\n      "buyNow": "Buy now",\n      "continueShopping": "Continue shopping",\n      "viewDetails": "View details",\n      "showMore": "Show more",\n      "showLess": "Show less",\n      "apply": "Apply",\n      "clear": "Clear",\n      "clearAll": "Clear all",\n      "submit": "Submit",\n      "save": "Save changes",\n      "cancel": "Cancel",\n      "edit": "Edit",\n      "delete": "Delete",\n      "remove": "Remove",\n      "retry": "Try again",\n      "back": "Back",\n      "next": "Next step",\n      "previous": "Previous step",\n      "close": "Close",\n      "share": "Share",\n      "loading": "Loading…",\n      "seeAll": "See all"\n    },\n    "forms": {\n      "required": "This field is required.",\n      "invalidEmail": "Please enter a valid email address.",\n      "invalidPhone": "Please enter a valid phone number.",\n      "password": "Password",\n      "confirmsecret-74761a59": "Confirm password",\n      "passwordMismatch": "Passwords do not match.",\n      "email": "Email address",\n      "phone": "Phone number",\n      "fullName": "Full name",\n      "firstName": "First name",\n      "lastName": "Last name",\n      "address": "Full address",\n      "postalCode": "Postal code",\n      "city": "City",\n      "province": "State / Province",\n      "message": "Your message",\n      "subject": "Subject",\n      "emailPlaceholder": "example@email.com",\n      "selectOption": "Select an option",\n      "success": "Your information was submitted successfully.",\n      "error": "Could not submit your information. Please try again."\n    },\n    "footer": {\n      "description": "SourcePixcel is your trusted destination for quality online shopping.",\n      "customerService": "Customer service",\n      "quickLinks": "Quick links",\n      "guides": "Shopping help",\n      "aboutUs": "About SourcePixcel",\n      "contactUs": "Contact us",\n      "faq": "FAQs",\n      "returns": "Returns policy",\n      "shipping": "Shipping information",\n      "terms": "Terms and conditions",\n      "privacy": "Privacy policy",\n      "followUs": "Follow us",\n      "newsletter": "Newsletter",\n      "newsletterText": "Get the latest offers and deals delivered to you.",\n      "newsletterPlaceholder": "Enter your email",\n      "copyright": "All rights reserved by SourcePixcel.",\n      "trustTitle": "Shop with confidence",\n      "paymentMethods": "Trusted payment methods"\n    },\n    "trustBadges": {\n      "original": "Authenticity guaranteed",\n      "return": "7-day returns",\n      "secure": "Secure payment",\n      "support": "24/7 support",\n      "delivery": "Fast delivery"\n    },\n    "serviceItems": {\n      "deliveryTitle": "Fast delivery",\n      "deliveryText": "Shipping nationwide",\n      "originalTitle": "Authenticity guaranteed",\n      "originalText": "Quality and authenticity assured",\n      "returnTitle": "7-day returns",\n      "returnText": "Time to inspect and return your order",\n      "supportTitle": "Always here to help",\n      "supportText": "Support available every day",\n      "secureTitle": "Secure payments",\n      "secureText": "Pay through trusted gateways"\n    },\n    "messages": {\n      "unexpected": "Something went wrong.",\n      "empty": "There is nothing to display.",\n      "offline": "Please check your internet connection.",\n      "notFound": "The requested page or product could not be found.",\n      "success": "Completed successfully."\n    },\n    "currency": "Toman",\n    "items": "items",\n    "results": "results"\n  },\n  "home": {\n    "heroSlider": {\n      "eyebrow": "A fresh online shopping experience",\n      "slide1Title": "Shop smarter, shop with ease",\n      "slide1Text": "Find your favorite products at great prices.",\n      "slide1Cta": "Explore products",\n      "slide2Title": "A new season, fresh deals",\n      "slide2Text": "Discover special offers for your next great find.",\n      "slide2Cta": "Explore deals",\n      "slide3Title": "Technology by your side",\n      "slide3Text": "Discover the latest digital products.",\n      "slide3Cta": "Shop digital products",\n      "previous": "Previous slide",\n      "next": "Next slide",\n      "goToSlide": "Go to slide {number}"\n    },\n    "categoryCircles": {\n      "title": "Shop by category",\n      "subtitle": "Choose a category you love",\n      "electronics": "Electronics",\n      "mobile": "Mobile phones",\n      "fashion": "Fashion",\n      "home": "Home & kitchen",\n      "beauty": "Beauty & health",\n      "supermarket": "Groceries",\n      "books": "Books & stationery",\n      "sports": "Sports & travel",\n      "toys": "Toys",\n      "tools": "Tools & automotive",\n      "accessories": "Accessories",\n      "seeCategories": "All categories"\n    },\n    "amazingOffer": {\n      "title": "Amazing offers",\n      "subtitle": "Limited-time deals you don\'t want to miss",\n      "endsIn": "Offer ends in",\n      "hours": "hours",\n      "minutes": "minutes",\n      "seconds": "seconds",\n      "viewAll": "View all offers",\n      "discount": "off",\n      "expired": "This offer has ended"\n    },\n    "bestSellers": {\n      "title": "Best sellers",\n      "subtitle": "Customer favorites, all in one place",\n      "viewAll": "View all best sellers"\n    },\n    "newArrivals": {\n      "title": "New arrivals",\n      "subtitle": "The latest products in our store",\n      "viewAll": "Explore new arrivals",\n      "new": "New"\n    },\n    "brands": {\n      "title": "Popular brands",\n      "subtitle": "Shop trusted brands",\n      "viewAll": "All brands"\n    },\n    "blog": {\n      "title": "From the SourcePixcel journal",\n      "subtitle": "Guides and stories to help you choose well",\n      "readMore": "Read more",\n      "viewAll": "View all articles",\n      "readingTime": "min read",\n      "latest": "Latest articles"\n    },\n    "testimonials": {\n      "title": "What our customers say",\n      "subtitle": "Shopping experiences from our customers",\n      "verifiedPurchase": "Verified purchase",\n      "previous": "Previous review",\n      "next": "Next review"\n    },\n    "newsletter": {\n      "title": "Don\'t miss our special offers",\n      "subtitle": "Join our newsletter to get the latest deals first.",\n      "placeholder": "Your email address",\n      "subscribe": "Subscribe",\n      "success": "You are now subscribed to our newsletter.",\n      "alreadySubscribed": "This email is already subscribed.",\n      "privacy": "Your information stays private."\n    }\n  },\n  "product": {\n    "details": "Product details",\n    "description": "Description",\n    "specifications": "Specifications",\n    "reviews": "Customer reviews",\n    "related": "You may also like",\n    "brand": "Brand",\n    "sku": "SKU",\n    "availability": "Availability",\n    "inStock": "In stock",\n    "outOfStock": "Out of stock",\n    "lowStock": "Only {count} left",\n    "rating": "Rating",\n    "reviewCount": "{count} reviews",\n    "shortSpecs": "Key features",\n    "color": "Color",\n    "size": "Size",\n    "chooseColor": "Choose a color",\n    "chooseSize": "Choose a size",\n    "seller": "Seller",\n    "sellerName": "SourcePixcel Store",\n    "sellerRating": "Customer satisfaction",\n    "warranty": "Warranty",\n    "warrantyValue": "Authenticity and physical-condition guarantee",\n    "delivery": "Delivery",\n    "deliveryValue": "Fast nationwide shipping",\n    "quantity": "Quantity",\n    "increaseQuantity": "Increase quantity",\n    "decreaseQuantity": "Decrease quantity",\n    "addToWishlist": "Add to wishlist",\n    "removeFromWishlist": "Remove from wishlist",\n    "addToCompare": "Add to compare",\n    "share": "Share product",\n    "discount": "Discount",\n    "originalPrice": "Original price",\n    "finalPrice": "Final price",\n    "price": "Price",\n    "specName": "Feature",\n    "specValue": "Value",\n    "pros": "Pros",\n    "cons": "Cons",\n    "writeReview": "Write a review",\n    "yourRating": "Your rating",\n    "reviewTitle": "Review title",\n    "reviewText": "Your review",\n    "reviewSubmit": "Submit review",\n    "reviewThankYou": "Thank you for your review.",\n    "ratingBreakdown": "Rating breakdown",\n    "noReviews": "No reviews have been posted for this product yet.",\n    "sortReviews": "Sort reviews",\n    "newestReviews": "Newest",\n    "helpfulReviews": "Most helpful",\n    "verifiedBuyer": "Verified buyer",\n    "question": "Have a question about this product?",\n    "installments": "Installment options available",\n    "breadcrumb": "Breadcrumb",\n    "imageAlt": "Image of {name}"\n  },\n  "cart": {\n    "title": "Shopping cart",\n    "emptyTitle": "Your cart is empty",\n    "emptyText": "Add your favorite products to get started.",\n    "items": {\n      "title": "Items in your cart",\n      "quantity": "Quantity",\n      "remove": "Remove item",\n      "saveForLater": "Move to wishlist",\n      "inStock": "Ready to ship",\n      "seller": "Seller",\n      "unitPrice": "Price per item",\n      "itemCount": "{count} items"\n    },\n    "summary": {\n      "title": "Order summary",\n      "subtotal": "Subtotal",\n      "discount": "You save",\n      "shipping": "Shipping",\n      "shippingFree": "Free",\n      "tax": "Tax",\n      "total": "Total due",\n      "coupon": "Discount code",\n      "couponPlaceholder": "Enter discount code",\n      "applyCoupon": "Apply code",\n      "couponApplied": "Discount code applied.",\n      "couponInvalid": "This discount code is invalid.",\n      "checkout": "Continue to checkout",\n      "estimate": "Shipping is calculated at the next step.",\n      "secureCheckout": "Secure checkout"\n    },\n    "checkout": {\n      "title": "Place your order",\n      "steps": {\n        "cart": "Cart",\n        "shipping": "Shipping details",\n        "payment": "Payment",\n        "confirmation": "Order confirmation"\n      },\n      "shippingTitle": "Recipient and shipping details",\n      "paymentTitle": "Payment method",\n      "reviewTitle": "Review your order",\n      "recipient": "Recipient details",\n      "address": "Delivery address",\n      "addAddress": "Add a new address",\n      "deliveryMethod": "Delivery method",\n      "standardDelivery": "Standard delivery",\n      "expressDelivery": "Express delivery",\n      "deliveryDate": "Estimated delivery",\n      "paymentOnline": "Pay online",\n      "paymentOnDelivery": "Pay on delivery",\n      "orderNote": "Order notes",\n      "placeOrder": "Place order",\n      "continueToPayment": "Continue to payment",\n      "orderSuccess": "Your order has been placed successfully.",\n      "orderNumber": "Order number",\n      "mockPayment": "This is a demo store; no real payment will be processed.",\n      "requiredAddress": "Please enter a delivery address."\n    }\n  },\n  "account": {\n    "title": "My account",\n    "dashboard": "Dashboard",\n    "welcome": "Hello {name}, welcome back",\n    "profile": {\n      "title": "Account details",\n      "edit": "Edit profile",\n      "firstName": "First name",\n      "lastName": "Last name",\n      "email": "Email",\n      "phone": "Phone number",\n      "birthDate": "Date of birth",\n      "gender": "Gender",\n      "male": "Male",\n      "female": "Female",\n      "saveSuccess": "Your profile has been updated."\n    },\n    "orders": {\n      "title": "My orders",\n      "orderNumber": "Order number",\n      "date": "Date placed",\n      "total": "Order total",\n      "status": "Status",\n      "details": "Order details",\n      "tracking": "Tracking number",\n      "view": "View order",\n      "empty": "You haven\'t placed any orders yet.",\n      "statuses": {\n        "pending": "Awaiting payment",\n        "processing": "Processing",\n        "shipped": "Shipped",\n        "delivered": "Delivered",\n        "cancelled": "Cancelled"\n      }\n    },\n    "wishlist": {\n      "title": "My wishlist",\n      "empty": "You haven\'t added any products to your wishlist yet.",\n      "remove": "Remove from wishlist",\n      "moveToCart": "Add to cart",\n      "count": "{count} products"\n    },\n    "addresses": "My addresses",\n    "security": "Account security",\n    "signOut": "Sign out"\n  },\n  "categories": {\n    "title": "Shop by category",\n    "all": "All categories",\n    "breadcrumbHome": "Home",\n    "products": "Products",\n    "productCount": "{count} products",\n    "noProducts": "No products found in this category.",\n    "subcategories": "Subcategories",\n    "popular": "Popular categories",\n    "electronics": "Electronics",\n    "mobile": "Mobile & tablets",\n    "laptop": "Laptops & computers",\n    "fashion": "Fashion",\n    "home": "Home & kitchen",\n    "beauty": "Beauty & health",\n    "supermarket": "Groceries",\n    "books": "Books & stationery",\n    "sports": "Sports & travel",\n    "toys": "Toys & kids",\n    "automotive": "Tools & automotive",\n    "jewelry": "Jewelry"\n  },\n  "filters": {\n    "title": "Filters",\n    "category": "Category",\n    "brand": "Brand",\n    "searchBrand": "Search brands",\n    "price": "Price range",\n    "minPrice": "Minimum price",\n    "maxPrice": "Maximum price",\n    "color": "Color",\n    "size": "Size",\n    "availability": "Availability",\n    "inStockOnly": "In-stock items only",\n    "discountOnly": "Discounted items only",\n    "rating": "Minimum rating",\n    "ratingAndUp": "and up",\n    "clear": "Clear filters",\n    "showResults": "Show products",\n    "activeFilters": "Active filters",\n    "allBrands": "All brands",\n    "colors": {\n      "black": "Black",\n      "white": "White",\n      "gray": "Gray",\n      "red": "Red",\n      "blue": "Blue",\n      "green": "Green",\n      "pink": "Pink",\n      "gold": "Gold"\n    },\n    "noBrands": "No brands found"\n  },\n  "sorting": {\n    "title": "Sort by",\n    "bestselling": "Best selling",\n    "newest": "Newest",\n    "cheapest": "Price: low to high",\n    "mostExpensive": "Price: high to low",\n    "popular": "Most popular",\n    "highestRated": "Top rated",\n    "mostDiscounted": "Biggest discount",\n    "relevance": "Most relevant"\n  },\n  "checkout": {\n    "title": "Place your order",\n    "steps": {\n      "cart": "Cart",\n      "shipping": "Shipping details",\n      "payment": "Payment"\n    }\n  },\n  "errors": {\n    "notFoundTitle": "Page not found",\n    "notFoundText": "The page you\'re looking for doesn\'t exist or has moved.",\n    "backHome": "Back to home",\n    "general": "Something went wrong."\n  }\n}')
I18N_TS = """import {getRequestConfig} from 'next-intl/server';

export const locales = ['fa', 'en'] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = 'fa';

export default getRequestConfig(async ({requestLocale}) => {
  const requested = await requestLocale;
  const locale: Locale = locales.includes(requested as Locale)
    ? (requested as Locale)
    : defaultLocale;
  return {locale, messages: (await import(`./messages/${locale}.json`)).default};
});
"""
MIDDLEWARE_TS = """import createMiddleware from 'next-intl/middleware';
import {defaultLocale, locales} from './i18n';

export default createMiddleware({locales, defaultLocale, localeDetection: true});

export const config = {matcher: ['/((?!api|_next|.*\\..*).*)']};
"""

def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def create_localization_files():
    messages = ROOT / "messages"
    messages.mkdir(parents=True, exist_ok=True)
    (ROOT / "i18n.ts").write_text(I18N_TS, encoding="utf-8")
    print("Created i18n.ts")
    (ROOT / "middleware.ts").write_text(MIDDLEWARE_TS, encoding="utf-8")
    print("Created middleware.ts")
    write_json(messages / "fa.json", FA_MESSAGES)
    print("Created messages/fa.json")
    write_json(messages / "en.json", EN_MESSAGES)
    print("Created messages/en.json")
    print("Done: locale routing and translations are ready.")

def main():
    create_base_project()
    create_localization_files()


if __name__ == "__main__":
    main()
