# 16_blog.py
# ساخت بخش بلاگ
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

files = []

# ============================================================
# lib/data/mock-blog.ts
# ============================================================
files.append(("lib/data/mock-blog.ts", """// lib/data/mock-blog.ts

export interface BlogPost {
  id: number;
  slug: string;
  titleFa: string;
  titleEn: string;
  excerptFa: string;
  excerptEn: string;
  contentFa: string;
  contentEn: string;
  cover: string;
  categoryFa: string;
  categoryEn: string;
  authorFa: string;
  authorEn: string;
  dateFa: string;
  dateEn: string;
  readTimeFa: string;
  readTimeEn: string;
  tags: string[];
}

export const blogPosts: BlogPost[] = [
  {
    id: 1,
    slug: "best-smartphones-2024",
    titleFa: "بهترین گوشی‌های هوشمند سال ۲۰۲۴",
    titleEn: "Best Smartphones of 2024",
    excerptFa: "نگاهی کامل به بهترین گوشی‌های هوشمند بازار در سال ۲۰۲۴ و مقایسه آن‌ها از نظر قیمت، کیفیت و امکانات.",
    excerptEn: "A complete look at the best smartphones of 2024 and a comparison of their price, quality, and features.",
    contentFa: "در سال ۲۰۲۴، بازار گوشی‌های هوشمند شاهد رقابت بسیار شدیدی بین برندهای مطرح بود. از سامسونگ و اپل گرفته تا شیائومی و هواوی، همه سعی کردند محصولات باکیفیت‌تری را روانه بازار کنند.\\n\\nدر این مقاله، به بررسی بهترین گوشی‌های هوشمند سال ۲۰۲۴ می‌پردازیم و ویژگی‌های کلیدی هر یک را مرور می‌کنیم. از دوربین‌های پیشرفته و صفحه‌نمایش‌های باکیفیت تا پردازنده‌های قدرتمند و باتری‌های پرظرفیت.\\n\\nگوشی سامسونگ Galaxy S24 Ultra با دوربین ۲۰۰ مگاپیکسلی و قلم S-Pen، یکی از بهترین انتخاب‌ها برای کاربران حرفه‌ای است. از طرف دیگر، Apple iPhone 15 Pro Max با تراشه A17 Pro عملکرد فوق‌العاده‌ای در بازی و پردازش‌های سنگین ارائه می‌دهد.\\n\\nدر رده میان‌رده، گوشی‌هایی مثل Xiaomi Redmi Note 13 Pro و Samsung Galaxy A55 گزینه‌های اقتصادی و بسیار خوبی هستند.\\n\\nدر نهایت، انتخاب گوشی مناسب بستگی به نیازها و بودجه شما دارد. امیدواریم این مقاله به شما در انتخاب بهتر کمک کند.",
    contentEn: "In 2024, the smartphone market witnessed intense competition among major brands. From Samsung and Apple to Xiaomi and Huawei, everyone tried to release higher-quality products.\\n\\nIn this article, we review the best smartphones of 2024 and discuss the key features of each. From advanced cameras and high-quality displays to powerful processors and long-lasting batteries.\\n\\nThe Samsung Galaxy S24 Ultra with its 200MP camera and S-Pen is one of the best choices for professional users. On the other hand, the Apple iPhone 15 Pro Max with the A17 Pro chip delivers excellent performance in gaming and heavy tasks.\\n\\nIn the mid-range segment, phones like the Xiaomi Redmi Note 13 Pro and Samsung Galaxy A55 are excellent budget-friendly options.\\n\\nUltimately, choosing the right phone depends on your needs and budget. We hope this article helps you make a better choice.",
    cover: "https://picsum.photos/seed/blog1/800/500",
    categoryFa: "فناوری",
    categoryEn: "Technology",
    authorFa: "علی محمدی",
    authorEn: "Ali Mohammadi",
    dateFa: "۱۴۰۳/۰۶/۱۵",
    dateEn: "Sep 5, 2024",
    readTimeFa: "۵ دقیقه",
    readTimeEn: "5 min read",
    tags: ["موبایل", "مقایسه", "فناوری"],
  },
  {
    id: 2,
    slug: "laptop-buying-guide",
    titleFa: "راهنمای خرید لپ‌تاپ در سال ۲۰۲۴",
    titleEn: "Laptop Buying Guide 2024",
    excerptFa: "همه چیز درباره انتخاب لپ‌تاپ مناسب: از پردازنده و رم گرفته تا صفحه‌نمایش و باتری.",
    excerptEn: "Everything you need to know about choosing the right laptop: from CPU and RAM to display and battery.",
    contentFa: "خرید لپ‌تاپ یکی از مهم‌ترین تصمیمات در دنیای دیجیتال امروز است. برای انتخاب درست، باید به چند نکته کلیدی توجه کنید.\\n\\nابتدا نوع کاربری خود را مشخص کنید: آیا برای بازی، کار حرفه‌ای، یا استفاده روزمره به لپ‌تاپ نیاز دارید؟ این موضوع به شما کمک می‌کند تا پردازنده و کارت گرافیک مناسب را انتخاب کنید.\\n\\nپردازنده یکی از مهم‌ترین اجزای لپ‌تاپ است. برای کاربری حرفه‌ای و بازی، Intel Core i7 یا i9 و AMD Ryzen 7 یا 9 گزینه‌های مناسبی هستند.\\n\\nرم (RAM) نیز نقش مهمی در سرعت سیستم دارد. حداقل ۸ گیگابایت و برای کارهای حرفه‌ای ۱۶ یا ۳۲ گیگابایت توصیه می‌شود.\\n\\nصفحه‌نمایش را جدی بگیرید. رزولوشن Full HD حداقل استاندارد امروز است. اگر کار گرافیکی می‌کنید، به سراغ صفحه‌نمایش‌های 4K یا OLED بروید.\\n\\nباتری هم فاکتور مهمی است. اگر زیاد سفر می‌کنید، به دنبال لپ‌تاپ‌هایی با باتری ۸ ساعت یا بیشتر باشید.",
    contentEn: "Buying a laptop is one of the most important decisions in today's digital world. To make the right choice, you need to pay attention to several key points.\\n\\nFirst, determine your use case: do you need a laptop for gaming, professional work, or daily use? This helps you choose the right CPU and GPU.\\n\\nThe processor is one of the most important components. For professional use and gaming, Intel Core i7 or i9 and AMD Ryzen 7 or 9 are good choices.\\n\\nRAM also plays an important role in system speed. At least 8GB, and for professional tasks 16 or 32GB is recommended.\\n\\nTake the display seriously. Full HD resolution is the minimum standard today. If you do graphics work, go for 4K or OLED displays.\\n\\nBattery is also a key factor. If you travel a lot, look for laptops with 8 hours of battery or more.",
    cover: "https://picsum.photos/seed/blog2/800/500",
    categoryFa: "راهنما",
    categoryEn: "Guide",
    authorFa: "سارا احمدی",
    authorEn: "Sara Ahmadi",
    dateFa: "۱۴۰۳/۰۶/۱۰",
    dateEn: "Aug 31, 2024",
    readTimeFa: "۷ دقیقه",
    readTimeEn: "7 min read",
    tags: ["لپ‌تاپ", "راهنما", "خرید"],
  },
  {
    id: 3,
    slug: "audio-headphones-review",
    titleFa: "بررسی بهترین هدفون‌های بی‌سیم",
    titleEn: "Best Wireless Headphones Review",
    excerptFa: "مقایسه بهترین هدفون‌های بی‌سیم از نظر کیفیت صدا، نویز کنسلینگ و باتری.",
    excerptEn: "Comparing the best wireless headphones in terms of sound quality, noise cancelling, and battery.",
    contentFa: "هدفون‌های بی‌سیم در سال‌های اخیر به یکی از محبوب‌ترین لوازم جانبی تبدیل شده‌اند. با پیشرفت فناوری، امروزه هدفون‌های بی‌سیم کیفیت صدایی تقریباً برابر با هدفون‌های سیمی دارند.\\n\\nSony WH-1000XM5 یکی از بهترین گزینه‌ها در بازار است که با نویز کنسلینگ فعال فوق‌العاده، تجربه‌ای بی‌نظیر فراهم می‌کند. باتری این هدفون تا ۳۰ ساعت در حالت نویز کنسلینگ دوام دارد.\\n\\nBose QuietComfort 45 نیز یکی از رقبای سرسخت سونی است که کیفیت صدای بی‌نقص و راحتی عالی دارد.\\n\\nبرای کاربران اپل، AirPods Pro 2 با تراشه H2 و قابلیت Spatial Audio یک انتخاب عالی است.\\n\\nدر نهایت، انتخاب هدفون مناسب بستگی به ترجیحات شما دارد. اگر به دنبال بهترین نویز کنسلینگ هستید، Sony انتخاب اول است. اگر راحتی برایتان مهم‌تر است، Bose گزینه بهتری است.",
    contentEn: "Wireless headphones have become one of the most popular accessories in recent years. With advances in technology, wireless headphones now offer sound quality nearly equal to wired ones.\\n\\nThe Sony WH-1000XM5 is one of the best options on the market, offering an unmatched experience with excellent active noise cancelling. Its battery lasts up to 30 hours with noise cancelling on.\\n\\nThe Bose QuietComfort 45 is also a strong competitor with flawless sound quality and excellent comfort.\\n\\nFor Apple users, the AirPods Pro 2 with the H2 chip and Spatial Audio is an excellent choice.\\n\\nUltimately, choosing the right headphones depends on your preferences. If you want the best noise cancelling, Sony is the top choice. If comfort matters more, Bose is a better option.",
    cover: "https://picsum.photos/seed/blog3/800/500",
    categoryFa: "بررسی",
    categoryEn: "Review",
    authorFa: "رضا کریمی",
    authorEn: "Reza Karimi",
    dateFa: "۱۴۰۳/۰۵/۲۸",
    dateEn: "Aug 18, 2024",
    readTimeFa: "۴ دقیقه",
    readTimeEn: "4 min read",
    tags: ["هدفون", "صوت", "بررسی"],
  },
  {
    id: 4,
    slug: "camera-for-beginners",
    titleFa: "بهترین دوربین‌ها برای مبتدیان",
    titleEn: "Best Cameras for Beginners",
    excerptFa: "اگر به تازگی وارد دنیای عکاسی شده‌اید، این مقاله به شما در انتخاب دوربین مناسب کمک می‌کند.",
    excerptEn: "If you're new to photography, this article helps you choose the right camera.",
    contentFa: "ورود به دنیای عکاسی نیازمند انتخاب دوربین مناسب است. برای مبتدیان، دوربین‌های Mirrorless گزینه بهتری نسبت به DSLR هستند زیرا سبک‌تر، کوچک‌تر و آسان‌تر برای استفاده هستند.\\n\\nCanon EOS R50 یکی از بهترین دوربین‌ها برای مبتدیان است. این دوربین با سنسور APS-C و پردازنده DIGIC X، تصاویر باکیفیتی ثبت می‌کند.\\n\\nNikon Z30 نیز گزینه مناسبی است، به ویژه برای تولید محتوا و ولاگ.\\n\\nSony Alpha A6100 از دیگر گزینه‌های محبوب است که با فوکوس خودکار سریع و قابلیت فیلم‌برداری 4K، انتخابی عالی برای مبتدیان است.\\n\\nتوصیه ما این است که قبل از خرید دوربین، به لنز آن هم توجه کنید. لنزهای 18-55mm برای شروع بسیار مناسب هستند.",
    contentEn: "Entering the world of photography requires choosing the right camera. For beginners, mirrorless cameras are a better option than DSLRs as they are lighter, smaller, and easier to use.\\n\\nThe Canon EOS R50 is one of the best cameras for beginners. With an APS-C sensor and DIGIC X processor, it captures high-quality images.\\n\\nThe Nikon Z30 is also a good choice, especially for content creation and vlogging.\\n\\nThe Sony Alpha A6100 is another popular option with fast autofocus and 4K video recording, making it an excellent choice for beginners.\\n\\nWe recommend paying attention to the lens before buying a camera. 18-55mm lenses are great for starting out.",
    cover: "https://picsum.photos/seed/blog4/800/500",
    categoryFa: "راهنما",
    categoryEn: "Guide",
    authorFa: "مریم رضایی",
    authorEn: "Maryam Rezaei",
    dateFa: "۱۴۰۳/۰۵/۱۵",
    dateEn: "Aug 5, 2024",
    readTimeFa: "۶ دقیقه",
    readTimeEn: "6 min read",
    tags: ["دوربین", "عکاسی", "راهنما"],
  },
  {
    id: 5,
    slug: "gaming-consoles-2024",
    titleFa: "مقایسه کنسول‌های بازی ۲۰۲۴",
    titleEn: "Gaming Consoles Comparison 2024",
    excerptFa: "PS5، Xbox Series X یا Nintendo Switch؟ کدام برای شما مناسب است؟",
    excerptEn: "PS5, Xbox Series X, or Nintendo Switch? Which one is right for you?",
    contentFa: "بازار کنسول‌های بازی در سال ۲۰۲۴ شاهد رقابت شدید بین سه غول بزرگ است: Sony، Microsoft و Nintendo.\\n\\nPlayStation 5 با بازی‌های انحصاری فوق‌العاده مثل God of War Ragnarok و Spider-Man 2، یکی از بهترین انتخاب‌ها است. دسته DualSense با بازخورد لمسی، تجربه بازی را کاملاً متحول کرده است.\\n\\nXbox Series X با قدرت پردازش بالا و سرویس Game Pass، ارزش فوق‌العاده‌ای ارائه می‌دهد. اگر به دنبال کتابخانه بزرگی از بازی‌ها با قیمت مناسب هستید، Xbox انتخاب بهتر است.\\n\\nNintendo Switch OLED برای بازی‌های خانوادگی و قابل حمل، انتخابی بی‌نظیر است. بازی‌هایی مثل Zelda و Mario هرگز قدیمی نمی‌شوند.\\n\\nدر نهایت، انتخاب کنسول بستگی به سبک بازی و بودجه شما دارد.",
    contentEn: "The gaming console market in 2024 sees intense competition among three giants: Sony, Microsoft, and Nintendo.\\n\\nThe PlayStation 5 with amazing exclusives like God of War Ragnarok and Spider-Man 2 is one of the best choices. The DualSense controller with haptic feedback has completely transformed the gaming experience.\\n\\nThe Xbox Series X with high processing power and the Game Pass service offers exceptional value. If you're looking for a large library of games at reasonable prices, Xbox is the better choice.\\n\\nThe Nintendo Switch OLED is an unmatched choice for family and portable gaming. Games like Zelda and Mario never get old.\\n\\nUltimately, choosing a console depends on your gaming style and budget.",
    cover: "https://picsum.photos/seed/blog5/800/500",
    categoryFa: "گیمینگ",
    categoryEn: "Gaming",
    authorFa: "حسین نوری",
    authorEn: "Hossein Nouri",
    dateFa: "۱۴۰۳/۰۵/۰۵",
    dateEn: "Jul 26, 2024",
    readTimeFa: "۵ دقیقه",
    readTimeEn: "5 min read",
    tags: ["گیمینگ", "کنسول", "مقایسه"],
  },
  {
    id: 6,
    slug: "smartwatch-comparison",
    titleFa: "مقایسه ساعت‌های هوشمند محبوب",
    titleEn: "Popular Smartwatch Comparison",
    excerptFa: "Apple Watch، Galaxy Watch یا Garmin؟ کدام ساعت هوشمند برای شما بهتر است؟",
    excerptEn: "Apple Watch, Galaxy Watch, or Garmin? Which smartwatch is better for you?",
    contentFa: "ساعت‌های هوشمند در سال‌های اخیر بسیار پیشرفته شده‌اند و امروزه به یکی از لوازم ضروری زندگی روزمره تبدیل شده‌اند.\\n\\nApple Watch Series 9 با تراشه S9 و قابلیت Double Tap، یکی از بهترین ساعت‌های هوشمند بازار است. اگر کاربر آیفون هستید، این ساعت بهترین انتخاب است.\\n\\nSamsung Galaxy Watch 6 Classic با طراحی کلاسیک و قابلیت چرخشی، برای کاربران اندروید انتخابی عالی است.\\n\\nGarmin Fēnix 7 برای ورزشکاران حرفه‌ای طراحی شده و با GPS دقیق و باتری طولانی‌مدت (تا ۱۸ روز)، انتخابی بی‌نظیر است.\\n\\nدر نهایت، اگر ورزشکار هستید Garmin، اگر کاربر اپل هستید Apple Watch و اگر کاربر اندروید هستید Galaxy Watch بهترین گزینه‌ها هستند.",
    contentEn: "Smartwatches have become very advanced in recent years and are now essential in daily life.\\n\\nThe Apple Watch Series 9 with the S9 chip and Double Tap feature is one of the best smartwatches on the market. If you're an iPhone user, this is the best choice.\\n\\nThe Samsung Galaxy Watch 6 Classic with its classic design and rotating bezel is an excellent choice for Android users.\\n\\nThe Garmin Fēnix 7 is designed for professional athletes and with accurate GPS and long battery life (up to 18 days), it's an unmatched choice.\\n\\nUltimately, if you're an athlete choose Garmin, if you're an Apple user choose Apple Watch, and if you're an Android user choose Galaxy Watch.",
    cover: "https://picsum.photos/seed/blog6/800/500",
    categoryFa: "مقایسه",
    categoryEn: "Comparison",
    authorFa: "نازنین صادقی",
    authorEn: "Nazanin Sadeghi",
    dateFa: "۱۴۰۳/۰۴/۲۰",
    dateEn: "Jul 11, 2024",
    readTimeFa: "۴ دقیقه",
    readTimeEn: "4 min read",
    tags: ["ساعت هوشمند", "مقایسه", "گجت"],
  },
];

export const getBlogPostBySlug = (slug: string): BlogPost | undefined =>
  blogPosts.find((p) => p.slug === slug);

export const getRecentBlogPosts = (count: number = 3): BlogPost[] =>
  blogPosts.slice(0, count);

export const getRelatedBlogPosts = (slug: string, count: number = 3): BlogPost[] =>
  blogPosts.filter((p) => p.slug !== slug).slice(0, count);
"""))

# ============================================================
# lib/data/index.ts (updated)
# ============================================================
files.append(("lib/data/index.ts", """// lib/data/index.ts
export {
  categories,
  brands,
  products,
  getProductBySlug,
  getProductsByCategory,
  getProductsByBrand,
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
  getCategoryById,
  getBrandById,
  getProductsBySubcategory,
} from "./products";

export {
  mockOrders,
  getOrderById,
} from "./mock-orders";
export type { MockOrder, OrderItem } from "./mock-orders";

export {
  blogPosts,
  getBlogPostBySlug,
  getRecentBlogPosts,
  getRelatedBlogPosts,
} from "./mock-blog";
export type { BlogPost } from "./mock-blog";
"""))

# ============================================================
# components/blog/BlogCard.tsx
# ============================================================
files.append(("components/blog/BlogCard.tsx", """import Link from "next/link";
import Image from "next/image";
import { Calendar, Clock, User } from "lucide-react";
import type { BlogPost, Locale } from "@/lib/types";

interface BlogCardProps {
  post: BlogPost;
  locale: Locale;
  featured?: boolean;
}

export default function BlogCard({ post, locale, featured = false }: BlogCardProps) {
  const isFa = locale === "fa";

  const title = isFa ? post.titleFa : post.titleEn;
  const excerpt = isFa ? post.excerptFa : post.excerptEn;
  const category = isFa ? post.categoryFa : post.categoryEn;
  const author = isFa ? post.authorFa : post.authorEn;
  const date = isFa ? post.dateFa : post.dateEn;
  const readTime = isFa ? post.readTimeFa : post.readTimeEn;

  return (
    <Link
      href={`/${locale}/blog/${post.slug}`}
      className="group bg-white rounded-lg border border-[#E0E0E2] overflow-hidden hover:shadow-lg transition-shadow flex flex-col"
    >
      {/* Cover */}
      <div className={`relative ${featured ? "aspect-[16/7]" : "aspect-video"} overflow-hidden`}>
        <Image
          src={post.cover}
          alt={title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover group-hover:scale-105 transition-transform duration-500"
        />
        <span className="absolute top-3 bg-[#EF4056] text-white text-[10px] font-medium px-2 py-1 rounded"
          style={{ [isFa ? "right" : "left"]: 12 } as React.CSSProperties}
        >
          {category}
        </span>
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-[14px] md:text-[15px] font-bold text-[#3F4064] leading-6 mb-2 line-clamp-2 group-hover:text-[#EF4056] transition-colors">
          {title}
        </h3>

        <p className="text-[12px] text-[#62666D] leading-6 line-clamp-2 mb-3 flex-1">
          {excerpt}
        </p>

        {/* Meta */}
        <div className="flex items-center gap-3 text-[10px] text-[#A1A3A8] pt-3 border-t border-[#F5F5F5] flex-wrap">
          <span className="flex items-center gap-1">
            <User size={11} />
            {author}
          </span>
          <span className="flex items-center gap-1">
            <Calendar size={11} />
            {date}
          </span>
          <span className="flex items-center gap-1">
            <Clock size={11} />
            {readTime}
          </span>
        </div>
      </div>
    </Link>
  );
}
"""))

# ============================================================
# components/blog/BlogList.tsx
# ============================================================
files.append(("components/blog/BlogList.tsx", """import type { BlogPost, Locale } from "@/lib/types";
import { Breadcrumb } from "@/components/common";
import BlogCard from "./BlogCard";

interface BlogListProps {
  locale: Locale;
  posts: BlogPost[];
}

export default function BlogList({ locale, posts }: BlogListProps) {
  const isFa = locale === "fa";
  const featured = posts[0];
  const rest = posts.slice(1);

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[{ labelFa: "وبلاگ", labelEn: "Blog" }]}
      />

      <h1 className="text-[22px] font-bold text-[#3F4064] mb-6">
        {isFa ? "وبلاگ SourcePixcel" : "SourcePixcel Blog"}
      </h1>

      {/* Featured post */}
      {featured && (
        <div className="mb-8">
          <BlogCard post={featured} locale={locale} featured />
        </div>
      )}

      {/* Rest */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {rest.map((post) => (
          <BlogCard key={post.id} post={post} locale={locale} />
        ))}
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/blog/BlogPostDetail.tsx
# ============================================================
files.append(("components/blog/BlogPostDetail.tsx", """import Link from "next/link";
import Image from "next/image";
import { Calendar, Clock, User, Tag, ArrowRight, ArrowLeft } from "lucide-react";
import type { BlogPost, Locale } from "@/lib/types";
import { Breadcrumb } from "@/components/common";
import BlogCard from "./BlogCard";

interface BlogPostDetailProps {
  locale: Locale;
  post: BlogPost;
  related: BlogPost[];
}

export default function BlogPostDetail({
  locale,
  post,
  related,
}: BlogPostDetailProps) {
  const isFa = locale === "fa";

  const title = isFa ? post.titleFa : post.titleEn;
  const content = isFa ? post.contentFa : post.contentEn;
  const category = isFa ? post.categoryFa : post.categoryEn;
  const author = isFa ? post.authorFa : post.authorEn;
  const date = isFa ? post.dateFa : post.dateEn;
  const readTime = isFa ? post.readTimeFa : post.readTimeEn;

  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Breadcrumb
        locale={locale}
        items={[
          { labelFa: "وبلاگ", labelEn: "Blog", href: `/${locale}/blog` },
          { labelFa: post.titleFa, labelEn: post.titleEn },
        ]}
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main content */}
        <article className="lg:col-span-2 bg-white rounded-lg border border-[#E0E0E2] overflow-hidden">
          {/* Cover */}
          <div className="relative aspect-video">
            <Image
              src={post.cover}
              alt={title}
              fill
              sizes="(max-width: 1024px) 100vw, 66vw"
              className="object-cover"
              priority
            />
          </div>

          <div className="p-5 md:p-7">
            {/* Category */}
            <div className="mb-3">
              <Link
                href={`/${locale}/blog`}
                className="inline-block bg-[#EF4056]/10 text-[#EF4056] text-[11px] font-medium px-2 py-1 rounded"
              >
                {category}
              </Link>
            </div>

            {/* Title */}
            <h1 className="text-[22px] md:text-[26px] font-bold text-[#3F4064] leading-9 mb-4">
              {title}
            </h1>

            {/* Meta */}
            <div className="flex items-center gap-4 text-[11px] text-[#A1A3A8] pb-4 mb-5 border-b border-[#E0E0E2] flex-wrap">
              <span className="flex items-center gap-1">
                <User size={12} />
                {author}
              </span>
              <span className="flex items-center gap-1">
                <Calendar size={12} />
                {date}
              </span>
              <span className="flex items-center gap-1">
                <Clock size={12} />
                {readTime}
              </span>
            </div>

            {/* Content */}
            <div className="text-[13px] md:text-[14px] text-[#3F4064] leading-8 whitespace-pre-line">
              {content}
            </div>

            {/* Tags */}
            {post.tags.length > 0 && (
              <div className="flex items-center gap-2 mt-8 pt-5 border-t border-[#E0E0E2] flex-wrap">
                <Tag size={14} className="text-[#A1A3A8]" />
                {post.tags.map((tag, i) => (
                  <span
                    key={i}
                    className="text-[11px] bg-[#F5F5F5] text-[#62666D] px-2 py-1 rounded"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Back */}
            <div className="mt-6">
              <Link
                href={`/${locale}/blog`}
                className="inline-flex items-center gap-2 text-[12px] text-[#00BFFF] hover:text-[#EF4056] transition-colors"
              >
                {isFa ? <ArrowRight size={14} /> : <ArrowLeft size={14} />}
                {isFa ? "بازگشت به وبلاگ" : "Back to blog"}
              </Link>
            </div>
          </div>
        </article>

        {/* Sidebar - related posts */}
        <aside className="lg:col-span-1">
          <div className="bg-white rounded-lg border border-[#E0E0E2] p-4 sticky top-24">
            <h2 className="text-[14px] font-bold text-[#3F4064] mb-4">
              {isFa ? "مطالب مرتبط" : "Related Posts"}
            </h2>
            <div className="space-y-3">
              {related.map((rp) => (
                <Link
                  key={rp.id}
                  href={`/${locale}/blog/${rp.slug}`}
                  className="flex gap-3 group"
                >
                  <div className="w-20 h-16 rounded-lg bg-[#F5F5F5] overflow-hidden relative shrink-0">
                    <Image
                      src={rp.cover}
                      alt={isFa ? rp.titleFa : rp.titleEn}
                      fill
                      sizes="80px"
                      className="object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-[12px] font-medium text-[#3F4064] leading-5 line-clamp-2 group-hover:text-[#EF4056] transition-colors">
                      {isFa ? rp.titleFa : rp.titleEn}
                    </h3>
                    <div className="text-[10px] text-[#A1A3A8] mt-1">
                      {isFa ? rp.dateFa : rp.dateEn}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
"""))

# ============================================================
# components/blog/index.ts
# ============================================================
files.append(("components/blog/index.ts", """// components/blog/index.ts
export { default as BlogCard } from "./BlogCard";
export { default as BlogList } from "./BlogList";
export { default as BlogPostDetail } from "./BlogPostDetail";
"""))

# ============================================================
# lib/types/product.ts (add BlogPost)
# ============================================================
files.append(("lib/types/blog.ts", """// lib/types/blog.ts
export interface BlogPost {
  id: number;
  slug: string;
  titleFa: string;
  titleEn: string;
  excerptFa: string;
  excerptEn: string;
  contentFa: string;
  contentEn: string;
  cover: string;
  categoryFa: string;
  categoryEn: string;
  authorFa: string;
  authorEn: string;
  dateFa: string;
  dateEn: string;
  readTimeFa: string;
  readTimeEn: string;
  tags: string[];
}
"""))

# ============================================================
# lib/types/index.ts (updated)
# ============================================================
files.append(("lib/types/index.ts", """// lib/types/index.ts
export type {
  Subcategory,
  Category,
  Brand,
  Product,
  CartItem,
  WishlistItem,
  CompareItem,
  FilterState,
  SortOption,
  Locale,
} from "./product";

export type { BlogPost } from "./blog";
"""))

# ============================================================
# app/[locale]/blog/page.tsx
# ============================================================
files.append(("app/[locale]/blog/page.tsx", """import type { Locale } from "@/lib/types";
import { blogPosts } from "@/lib/data";
import { BlogList } from "@/components/blog";

interface PageProps {
  params: Promise<{ locale: string }>;
}

export const metadata = {
  title: "Blog — SourcePixcel",
  description: "Read the latest articles and guides on SourcePixcel blog.",
};

export default async function BlogPage({ params }: PageProps) {
  const { locale } = await params;
  return <BlogList locale={locale as Locale} posts={blogPosts} />;
}
"""))

# ============================================================
# app/[locale]/blog/[slug]/page.tsx
# ============================================================
files.append(("app/[locale]/blog/[slug]/page.tsx", """import { notFound } from "next/navigation";
import type { Locale } from "@/lib/types";
import {
  blogPosts,
  getBlogPostBySlug,
  getRelatedBlogPosts,
} from "@/lib/data";
import { BlogPostDetail } from "@/components/blog";

interface PageProps {
  params: Promise<{ locale: string; slug: string }>;
}

export async function generateStaticParams() {
  const locales = ["fa", "en"];
  return locales.flatMap((locale) =>
    blogPosts.map((post) => ({ locale, slug: post.slug }))
  );
}

export async function generateMetadata({ params }: PageProps) {
  const { slug } = await params;
  const post = getBlogPostBySlug(slug);
  if (!post) return { title: "Post not found" };
  return {
    title: `${post.titleEn} — SourcePixcel Blog`,
    description: post.excerptEn,
  };
}

export default async function BlogPostPage({ params }: PageProps) {
  const { locale, slug } = await params;
  const typedLocale = locale as Locale;

  const post = getBlogPostBySlug(slug);
  if (!post) notFound();

  const related = getRelatedBlogPosts(slug, 3);

  return (
    <BlogPostDetail
      locale={typedLocale}
      post={post}
      related={related}
    />
  );
}
"""))

# ============================================================
# RUN
# ============================================================
def main():
    print("=" * 60)
    print("SourcePixcel — Step 16: Blog")
    print("=" * 60)
    print(f"Base: {BASE}\n")

    created = 0
    failed = 0

    for path, content in files:
        full_path = os.path.join(BASE, *path.split("/"))
        directory = os.path.dirname(full_path)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  [OK]   {path}")
            created += 1
        except Exception as e:
            print(f"  [FAIL] {path} -> {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Created: {created} files")
    print(f"Failed:  {failed} files")
    print("=" * 60)

    if failed == 0:
        print("\nSUCCESS!")
        print("Now run: npm run dev")
        print("Open: http://localhost:3000/fa/blog")
        print("\nNext: run 17_compare.py")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()