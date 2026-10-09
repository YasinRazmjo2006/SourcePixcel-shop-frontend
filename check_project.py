# check_project.py
# Self-check script — verifies all critical files exist
import os

BASE = os.path.dirname(os.path.abspath(__file__))

CRITICAL_FILES = [
    # Config
    "package.json",
    "next.config.js",
    "tsconfig.json",
    "tailwind.config.ts",
    "postcss.config.js",

    # Root app
    "app/layout.tsx",
    "app/page.tsx",
    "app/globals.css",
    "app/not-found.tsx",
    "app/sitemap.ts",
    "app/robots.ts",
    "app/manifest.ts",

    # Locale
    "app/[locale]/layout.tsx",
    "app/[locale]/page.tsx",
    "app/[locale]/loading.tsx",
    "app/[locale]/error.tsx",
    "app/[locale]/not-found.tsx",

    # Types
    "lib/types/product.ts",
    "lib/types/blog.ts",
    "lib/types/index.ts",

    # Data
    "lib/data/products.ts",
    "lib/data/mock-orders.ts",
    "lib/data/mock-blog.ts",
    "lib/data/iran-provinces.ts",
    "lib/data/index.ts",

    # Stores
    "lib/stores/cart.ts",
    "lib/stores/wishlist.ts",
    "lib/stores/auth.ts",
    "lib/stores/compare.ts",
    "lib/stores/theme.ts",
    "lib/stores/toast.ts",
    "lib/stores/index.ts",

    # Utils
    "lib/utils/format.ts",
    "lib/utils/validators.ts",
    "lib/utils/seo.ts",
    "lib/utils/index.ts",

    # Layout
    "components/layout/Header.tsx",
    "components/layout/Footer.tsx",

    # Home
    "components/home/HeroSlider.tsx",
    "components/home/CategoryCircles.tsx",
    "components/home/AmazingOffer.tsx",
    "components/home/ProductSection.tsx",
    "components/home/BrandLogos.tsx",
    "components/home/ServiceBadges.tsx",
    "components/home/index.ts",

    # Product
    "components/product/ProductCard.tsx",
    "components/product/RatingStars.tsx",
    "components/product/PriceTag.tsx",
    "components/product/ProductFilters.tsx",
    "components/product/ProductSort.tsx",
    "components/product/ProductGallery.tsx",
    "components/product/ProductDetail.tsx",
    "components/product/ProductTabs.tsx",
    "components/product/QuantitySelector.tsx",
    "components/product/RelatedProducts.tsx",
    "components/product/CompareButton.tsx",
    "components/product/index.ts",

    # Cart
    "components/cart/CartPage.tsx",
    "components/cart/CartLine.tsx",
    "components/cart/CartSummary.tsx",
    "components/cart/EmptyCart.tsx",
    "components/cart/index.ts",

    # Checkout
    "components/checkout/CheckoutPage.tsx",
    "components/checkout/StepIndicator.tsx",
    "components/checkout/ShippingForm.tsx",
    "components/checkout/ShippingMethod.tsx",
    "components/checkout/PaymentStep.tsx",
    "components/checkout/OrderReview.tsx",
    "components/checkout/OrderSuccess.tsx",
    "components/checkout/index.ts",

    # Auth
    "components/auth/AuthCard.tsx",
    "components/auth/LoginForm.tsx",
    "components/auth/RegisterForm.tsx",
    "components/auth/ForgotPasswordForm.tsx",
    "components/auth/index.ts",

    # Account
    "components/account/AccountSidebar.tsx",
    "components/account/AccountGuard.tsx",
    "components/account/DashboardView.tsx",
    "components/account/OrdersView.tsx",
    "components/account/OrderDetailView.tsx",
    "components/account/WishlistView.tsx",
    "components/account/AddressesView.tsx",
    "components/account/ProfileView.tsx",
    "components/account/OrderStatusBadge.tsx",
    "components/account/index.ts",

    # Blog
    "components/blog/BlogCard.tsx",
    "components/blog/BlogList.tsx",
    "components/blog/BlogPostDetail.tsx",
    "components/blog/index.ts",

    # Compare
    "components/compare/ComparePage.tsx",
    "components/compare/CompareTable.tsx",
    "components/compare/CompareEmpty.tsx",
    "components/compare/index.ts",

    # Search
    "components/search/SearchPage.tsx",
    "components/search/index.ts",

    # Common
    "components/common/Breadcrumb.tsx",
    "components/common/Pagination.tsx",
    "components/common/EmptyState.tsx",
    "components/common/StaticPage.tsx",
    "components/common/ThemeProvider.tsx",
    "components/common/ThemeToggle.tsx",
    "components/common/JsonLd.tsx",
    "components/common/ToastContainer.tsx",
    "components/common/Skeleton.tsx",
    "components/common/ProductCardSkeleton.tsx",
    "components/common/ErrorBoundary.tsx",
    "components/common/index.ts",
]

print("=" * 60)
print("SourcePixcel — Self-Check")
print("=" * 60)
print(f"Base: {BASE}\n")

missing = []
present = 0

for path in CRITICAL_FILES:
    full = os.path.join(BASE, *path.split("/"))
    if os.path.exists(full):
        present += 1
    else:
        missing.append(path)

print(f"Present: {present}/{len(CRITICAL_FILES)}")

if missing:
    print(f"\nMissing ({len(missing)} files):")
    for path in missing:
        print(f"  ✗ {path}")
    print("\n" + "=" * 60)
    print("INCOMPLETE")
    print("=" * 60)
else:
    print("\n" + "=" * 60)
    print("✅ ALL FILES PRESENT!")
    print("=" * 60)
    print("\nProject is complete. Run: npm run dev")
