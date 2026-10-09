# create_beautiful_images.py
# Creates beautiful SVG product images with gradients, category colors, and product names
import os
import urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE, "public", "images", "products")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Category-specific color gradients
CATEGORY_COLORS = {
    "mobile":       {"from": "#EF4056", "to": "#FF6B7D", "icon": "📱"},
    "laptop":       {"from": "#00BFFF", "to": "#4DD0FF", "icon": "💻"},
    "tablet":       {"from": "#8B5CF6", "to": "#A78BFA", "icon": "📲"},
    "audio":        {"from": "#F59E0B", "to": "#FBBF24", "icon": "🎧"},
    "camera":       {"from": "#22C55E", "to": "#4ADE80", "icon": "📷"},
    "smartwatch":   {"from": "#EC4899", "to": "#F472B6", "icon": "⌚"},
    "gaming":       {"from": "#06B6D4", "to": "#22D3EE", "icon": "🎮"},
    "accessories":  {"from": "#6B7280", "to": "#9CA3AF", "icon": "🔌"},
    "clothing":     {"from": "#F97316", "to": "#FB923C", "icon": "👕"},
    "shoes":        {"from": "#10B981", "to": "#34D399", "icon": "👟"},
    "home":         {"from": "#6366F1", "to": "#818CF8", "icon": "🏠"},
    "books":        {"from": "#84CC16", "to": "#A3E635", "icon": "📚"},
}

# Product metadata: id -> (category, nameFa, nameEn)
PRODUCTS = {
    # Mobile
    1:  ("mobile", "گوشی سامسونگ S24 Ultra", "Samsung Galaxy S24 Ultra"),
    2:  ("mobile", "گوشی اپل iPhone 15 Pro Max", "Apple iPhone 15 Pro Max"),
    3:  ("mobile", "گوشی شیائومی 14 Pro", "Xiaomi 14 Pro"),
    4:  ("mobile", "گوشی سامسونگ Galaxy A55", "Samsung Galaxy A55"),
    5:  ("mobile", "گوشی اپل iPhone 15", "Apple iPhone 15"),
    6:  ("mobile", "گوشی شیائومی Redmi Note 13", "Xiaomi Redmi Note 13 Pro"),
    7:  ("mobile", "گوشی هواوی P60 Pro", "Huawei P60 Pro"),
    8:  ("mobile", "گوشی تاشو Galaxy Z Fold 5", "Samsung Galaxy Z Fold 5"),
    9:  ("mobile", "گوشی اپل iPhone 14", "Apple iPhone 14"),
    10: ("mobile", "گوشی شیائومی Poco X6 Pro", "Xiaomi Poco X6 Pro"),
    # Laptop
    11: ("laptop", "لپ‌تاپ ایسوس ROG Strix", "Asus ROG Strix G16"),
    12: ("laptop", "لپ‌تاپ اپل MacBook Pro 14", "Apple MacBook Pro 14 M3"),
    13: ("laptop", "لپ‌تاپ لنوو ThinkPad X1", "Lenovo ThinkPad X1 Carbon"),
    14: ("laptop", "لپ‌تاپ دل XPS 15", "Dell XPS 15"),
    15: ("laptop", "لپ‌تاپ اچ‌پی Spectre x360", "HP Spectre x360"),
    16: ("laptop", "لپ‌تاپ ایسوس ZenBook 14", "Asus ZenBook 14 OLED"),
    17: ("laptop", "لپ‌تاپ لنوو IdeaPad Gaming", "Lenovo IdeaPad Gaming 3"),
    18: ("laptop", "لپ‌تاپ Surface Laptop 5", "Microsoft Surface Laptop 5"),
    # Tablet
    19: ("tablet", "تبلت اپل iPad Pro 12.9", "Apple iPad Pro 12.9 M4"),
    20: ("tablet", "تبلت سامسونگ Tab S9", "Samsung Galaxy Tab S9"),
    21: ("tablet", "تبلت شیائومی Pad 6 Pro", "Xiaomi Pad 6 Pro"),
    22: ("tablet", "تبلت اپل iPad Air 5", "Apple iPad Air 5"),
    23: ("tablet", "تبلت Surface Pro 9", "Microsoft Surface Pro 9"),
    # Audio
    24: ("audio", "هدفون سونی WH-1000XM5", "Sony WH-1000XM5"),
    25: ("audio", "ایرپاد پرو اپل نسل ۲", "Apple AirPods Pro 2"),
    26: ("audio", "هدفون بوز QC45", "Bose QuietComfort 45"),
    27: ("audio", "اسپیکر JBL Charge 5", "JBL Charge 5"),
    28: ("audio", "ایربادز سامسونگ Buds2 Pro", "Samsung Galaxy Buds2 Pro"),
    29: ("audio", "هدفون سنهایزر HD 560S", "Sennheiser HD 560S"),
    30: ("audio", "اسپیکر JBL Flip 6", "JBL Flip 6"),
    31: ("audio", "ایربادز شیائومی Buds 5", "Xiaomi Redmi Buds 5 Pro"),
    # Camera
    32: ("camera", "دوربین کانن EOS R6 II", "Canon EOS R6 Mark II"),
    33: ("camera", "دوربین سونی Alpha A7 IV", "Sony Alpha A7 IV"),
    34: ("camera", "دوربین نیکون Z50", "Nikon Z50"),
    35: ("camera", "دوربین گوپرو HERO 12", "GoPro HERO 12 Black"),
    36: ("camera", "دوربین کانن EOS 850D", "Canon EOS 850D"),
    # Smartwatch
    37: ("smartwatch", "ساعت اپل Watch Series 9", "Apple Watch Series 9"),
    38: ("smartwatch", "ساعت سامسونگ Watch 6", "Samsung Galaxy Watch 6"),
    39: ("smartwatch", "ساعت گارمین Fēnix 7", "Garmin Fēnix 7"),
    40: ("smartwatch", "مچ‌بند شیائومی Mi Band 8", "Xiaomi Mi Band 8"),
    41: ("smartwatch", "ساعت هواوی Watch GT 4", "Huawei Watch GT 4"),
    # Gaming
    42: ("gaming", "کنسول PlayStation 5", "Sony PlayStation 5"),
    43: ("gaming", "کنسول Nintendo Switch", "Nintendo Switch OLED"),
    44: ("gaming", "ماوس لاجیتک G502 X", "Logitech G502 X Plus"),
    45: ("gaming", "دسته DualSense Edge", "Sony DualSense Edge"),
    46: ("gaming", "هدست لاجیتک G733", "Logitech G733 Headset"),
    47: ("gaming", "کنسول Xbox Series X", "Microsoft Xbox Series X"),
    # Accessories
    48: ("accessories", "شارژر انکر 736", "Anker 736 Nano II"),
    49: ("accessories", "پاوربانک باسئوس 20000", "Baseus 20000mAh"),
    50: ("accessories", "شارژر MagSafe", "Apple MagSafe 15W"),
    51: ("accessories", "کابل Type-C 240W", "Baseus 240W USB-C"),
    52: ("accessories", "قاب S24 Ultra", "Samsung Clear Case"),
    # Clothing
    53: ("clothing", "هودی نایک Tech Fleece", "Nike Tech Fleece Hoodie"),
    54: ("clothing", "تی‌شرت آدیداس Originals", "Adidas Originals T-Shirt"),
    55: ("clothing", "جاکت نایک Windrunner", "Nike Windrunner Jacket"),
    56: ("clothing", "کتونی آدیداس Ultraboost", "Adidas Ultraboost 22"),
    57: ("clothing", "کتونی نایک Air Max 270", "Nike Air Max 270"),
    58: ("clothing", "کتونی پوما RS-X", "Puma RS-X"),
    59: ("clothing", "کتونی نیوبالانس 574", "New Balance 574"),
    # Home
    60: ("home", "سرخ‌کن فیلیپس XL", "Philips Airfryer XL"),
    61: ("home", "ماهیتابه تفال", "Tefal Non-Stick Pan"),
    62: ("home", "جاروبرقی دایسون V15", "Dyson V15 Detect"),
    63: ("home", "تلویزیون ال‌جی OLED C3", "LG OLED C3 TV"),
    64: ("home", "تلویزیون شیائومی A2", "Xiaomi Smart TV A2"),
    # Books
    65: ("books", "کتاب Clean Code", "Clean Code Book"),
    66: ("books", "کتاب The Pragmatic Programmer", "The Pragmatic Programmer"),
    67: ("books", "رمان ۱۹۸۴", "Novel 1984"),
    68: ("books", "کتاب عادت‌های اتمی", "Atomic Habits"),
}


def shorten(text: str, max_len: int = 22) -> str:
    """Shorten text for SVG display."""
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "…"


def create_svg(product_id: int) -> str:
    data = PRODUCTS.get(product_id)
    if not data:
        return ""

    category, name_fa, name_en = data
    colors = CATEGORY_COLORS.get(category, CATEGORY_COLORS["accessories"])
    color_from = colors["from"]
    color_to = colors["to"]
    icon = colors["icon"]

    short_fa = shorten(name_fa, 20)
    short_en = shorten(name_en, 24)

    # SVG with modern gradient, icon, and product names
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bg-{product_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color_from};stop-opacity:0.08"/>
      <stop offset="100%" style="stop-color:{color_to};stop-opacity:0.15"/>
    </linearGradient>
    <linearGradient id="icon-bg-{product_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{color_from}"/>
      <stop offset="100%" style="stop-color:{color_to}"/>
    </linearGradient>
    <filter id="shadow-{product_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="{color_from}" flood-opacity="0.25"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="600" height="600" fill="url(#bg-{product_id})"/>

  <!-- Decorative circles -->
  <circle cx="500" cy="100" r="120" fill="{color_from}" opacity="0.05"/>
  <circle cx="80" cy="520" r="90" fill="{color_to}" opacity="0.08"/>
  <circle cx="560" cy="480" r="60" fill="{color_from}" opacity="0.06"/>

  <!-- Icon card -->
  <rect x="180" y="130" width="240" height="240" rx="60" fill="white" opacity="0.9" filter="url(#shadow-{product_id})"/>
  <rect x="180" y="130" width="240" height="240" rx="60" fill="url(#icon-bg-{product_id})" opacity="0.15"/>

  <!-- Icon -->
  <text x="300" y="265" font-size="130" text-anchor="middle" dominant-baseline="middle">{icon}</text>

  <!-- Product name Persian -->
  <text x="300" y="420" font-family="Tahoma, Arial, sans-serif" font-size="26" font-weight="bold"
        fill="#3F4064" text-anchor="middle" direction="rtl">{short_fa}</text>

  <!-- Product name English -->
  <text x="300" y="460" font-family="Arial, sans-serif" font-size="18"
        fill="#62666D" text-anchor="middle">{short_en}</text>

  <!-- Category badge -->
  <rect x="220" y="500" width="160" height="36" rx="18" fill="{color_from}" opacity="0.15"/>
  <text x="300" y="523" font-family="Arial, sans-serif" font-size="14" font-weight="bold"
        fill="{color_from}" text-anchor="middle" letter-spacing="1">{category.upper()}</text>
</svg>'''
    return svg


print("=" * 60)
print("Creating beautiful product images...")
print("=" * 60)
print(f"Output: {OUTPUT_DIR}\n")

count = 0
for product_id in range(1, 69):
    svg_content = create_svg(product_id)
    if not svg_content:
        continue

    # Save SVG
    filepath = os.path.join(OUTPUT_DIR, f"product-{product_id}.svg")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)

    print(f"  [OK] product-{product_id}.svg")
    count += 1

print(f"\n{'=' * 60}")
print(f"Created {count} beautiful SVG images!")
print("=" * 60)