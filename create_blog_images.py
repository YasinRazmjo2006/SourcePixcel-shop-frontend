# create_blog_images.py
# Creates beautiful SVG cover images for blog posts
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE, "public", "images", "blog")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Blog posts metadata
BLOGS = {
    1: {
        "slug": "best-smartphones-2024",
        "titleFa": "بهترین گوشی‌های هوشمند ۲۰۲۴",
        "titleEn": "Best Smartphones 2024",
        "categoryFa": "فناوری",
        "categoryEn": "Technology",
        "emoji": "📱",
        "colorFrom": "#EF4056",
        "colorTo": "#FF7B8A",
    },
    2: {
        "slug": "laptop-buying-guide",
        "titleFa": "راهنمای خرید لپ‌تاپ",
        "titleEn": "Laptop Buying Guide",
        "categoryFa": "راهنما",
        "categoryEn": "Guide",
        "emoji": "💻",
        "colorFrom": "#00BFFF",
        "colorTo": "#4DD0FF",
    },
    3: {
        "slug": "audio-headphones-review",
        "titleFa": "بررسی هدفون‌های بی‌سیم",
        "titleEn": "Wireless Headphones Review",
        "categoryFa": "بررسی",
        "categoryEn": "Review",
        "emoji": "🎧",
        "colorFrom": "#8B5CF6",
        "colorTo": "#A78BFA",
    },
    4: {
        "slug": "camera-for-beginners",
        "titleFa": "دوربین برای مبتدیان",
        "titleEn": "Cameras for Beginners",
        "categoryFa": "راهنما",
        "categoryEn": "Guide",
        "emoji": "📷",
        "colorFrom": "#22C55E",
        "colorTo": "#4ADE80",
    },
    5: {
        "slug": "gaming-consoles-2024",
        "titleFa": "مقایسه کنسول‌های بازی",
        "titleEn": "Gaming Consoles Comparison",
        "categoryFa": "گیمینگ",
        "categoryEn": "Gaming",
        "emoji": "🎮",
        "colorFrom": "#06B6D4",
        "colorTo": "#22D3EE",
    },
    6: {
        "slug": "smartwatch-comparison",
        "titleFa": "مقایسه ساعت‌های هوشمند",
        "titleEn": "Smartwatch Comparison",
        "categoryFa": "مقایسه",
        "categoryEn": "Comparison",
        "emoji": "⌚",
        "colorFrom": "#EC4899",
        "colorTo": "#F472B6",
    },
}


def create_svg(blog_id: int) -> str:
    data = BLOGS[blog_id]
    emoji = data["emoji"]
    c1 = data["colorFrom"]
    c2 = data["colorTo"]
    title_fa = data["titleFa"]
    title_en = data["titleEn"]
    cat_fa = data["categoryFa"]
    cat_en = data["categoryEn"]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <linearGradient id="bg-{blog_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{c1}"/>
      <stop offset="100%" style="stop-color:{c2}"/>
    </linearGradient>
    <filter id="shadow-{blog_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="20" flood-color="rgba(0,0,0,0.3)"/>
    </filter>
  </defs>

  <!-- Background gradient -->
  <rect width="1200" height="600" fill="url(#bg-{blog_id})"/>

  <!-- Decorative circles -->
  <circle cx="1050" cy="100" r="180" fill="white" opacity="0.08"/>
  <circle cx="150" cy="520" r="140" fill="white" opacity="0.06"/>
  <circle cx="950" cy="520" r="100" fill="white" opacity="0.05"/>
  <circle cx="200" cy="100" r="80" fill="white" opacity="0.04"/>

  <!-- Category badge -->
  <rect x="60" y="60" width="200" height="48" rx="24" fill="white" opacity="0.25"/>
  <text x="160" y="92" font-family="Tahoma, Arial, sans-serif" font-size="22" font-weight="bold"
        fill="white" text-anchor="middle">{cat_fa}</text>

  <!-- Emoji icon (huge) -->
  <text x="950" y="380" font-size="320" text-anchor="middle" dominant-baseline="middle" filter="url(#shadow-{blog_id})">{emoji}</text>

  <!-- Persian title -->
  <text x="60" y="380" font-family="Tahoma, Arial, sans-serif" font-size="54" font-weight="bold"
        fill="white" text-anchor="start" direction="rtl">{title_fa}</text>

  <!-- English title -->
  <text x="60" y="450" font-family="Arial, sans-serif" font-size="32" font-weight="500"
        fill="white" opacity="0.85" text-anchor="start">{title_en}</text>

  <!-- Bottom accent line -->
  <rect x="60" y="500" width="120" height="6" rx="3" fill="white" opacity="0.7"/>
</svg>'''
    return svg


print("=" * 60)
print("Creating blog cover images...")
print("=" * 60)
print(f"Output: {OUTPUT_DIR}\n")

count = 0
for blog_id in BLOGS:
    svg_content = create_svg(blog_id)
    filepath = os.path.join(OUTPUT_DIR, f"blog-{blog_id}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"  [OK] blog-{blog_id}.svg")
    count += 1

print(f"\n{'=' * 60}")
print(f"Created {count} blog cover images!")
print("=" * 60)
print("\nNext: Update lib/data/mock-blog.ts to use local images")