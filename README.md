# SourcePixcel

Bilingual (Persian / English) e-commerce frontend built with Next.js 15.

## Stack

- Next.js 15.5.9 (App Router)
- React 19.2.0
- TypeScript 5
- Tailwind CSS 3.4
- Zustand 5 (state management)
- lucide-react (icons)

## Features

- Bilingual support (Persian RTL / English LTR)
- 68 mock products, 12 categories, 30 brands
- Product listing with filters + sort + pagination
- Product detail with gallery, tabs, reviews
- Cart with localStorage persistence
- Multi-step checkout + **simulated Zarinpal payment gateway**
- Auth pages (login, register, forgot password)
- User dashboard (orders, wishlist, addresses, profile)
- Product comparison (up to 4 products)
- Blog with list + detail
- Search with live autocomplete
- Dark mode with localStorage
- Toast notifications
- Skeleton loaders
- Error boundaries
- **Admin panel** (dashboard, products, orders)
- **Notification system** with badge
- **Bottom navigation** (mobile)
- **Keyboard shortcuts** (Ctrl+K, Ctrl+H, Ctrl+C, Shift+?)
- **Offline detection banner**
- **Invoice printing** for orders
- SEO: sitemap, robots, JSON-LD, Open Graph
- PWA manifest

## Installation

    npm install --registry=https://mirror-npm.runflare.com

## Development

    npm run dev

## Build

    npm run build
    npm start

## Test Credentials

### User
- Any valid Iranian mobile (`09XXXXXXXXX`)
- Any password with 6+ characters

### Admin Panel
- URL: `/{locale}/admin/login`
- Username: `admin`
- Password: `admin123`

### Coupon
- Code: `SOURCE10` (10% off)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + K | Focus search |
| Ctrl + H | Go home |
| Ctrl + C | Cart |
| Ctrl + W | Wishlist |
| Ctrl + A | Account |
| Ctrl + P | Admin panel |
| Shift + ? | Show help |
| Esc | Close dialogs |

## URLs

### Persian
- Home: /fa
- Categories: /fa/categories
- Cart: /fa/cart
- Checkout: /fa/checkout
- Login: /fa/auth/login
- Account: /fa/account
- Compare: /fa/compare
- Blog: /fa/blog
- Search: /fa/search
- Admin: /fa/admin

### English
Replace `/fa/` with `/en/`.

## SEO URLs

- Sitemap: /sitemap.xml
- Robots: /robots.txt
- Manifest: /manifest.webmanifest

## Project Structure

    app/
      [locale]/
        admin/         Admin panel
        account/       User dashboard
        auth/          Login, Register
        blog/          Blog
        cart/          Cart
        checkout/      Checkout + Payment
        compare/       Compare
        product/       Product detail
        search/        Search
        ... (about, contact, faq, terms, privacy)
    components/
      admin/           Admin panel components
      account/         User dashboard + Invoice
      auth/            Auth forms
      blog/            Blog components
      cart/            Cart components
      checkout/        Checkout components
      common/          Shared (Breadcrumb, Skeleton, Toast, etc.)
      compare/         Compare components
      home/            Home page sections
      layout/          Header, Footer, BottomNav
      notifications/   Notification bell
      payment/         Zarinpal gateway + callback
      product/         Product components
      search/          Search + autocomplete
    lib/
      data/            Mock data
      stores/          Zustand stores
      types/           TypeScript types
      utils/           Helpers

## License

Demo project. All rights reserved.
