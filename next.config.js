/** @type {import('next').NextConfig} */
const nextConfig = {
  // Output
  reactStrictMode: true,
  poweredByHeader: false,

  // Compression
  compress: true,

  // Source maps (disable in production for smaller bundle)
  productionBrowserSourceMaps: false,

  // Images
  images: {
    unoptimized: true,
    formats: ["image/avif", "image/webp"],
    remotePatterns: [
      { protocol: "https", hostname: "loremflickr.com", pathname: "/**" },
      { protocol: "https", hostname: "picsum.photos", pathname: "/**" },
      { protocol: "https", hostname: "images.unsplash.com", pathname: "/**" },
    ],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy: "default-src 'self'; script-src 'none'; sandbox;",
    minimumCacheTTL: 60 * 60 * 24 * 365,
  },

  // Experimental optimizations
  experimental: {
    optimizePackageImports: [
      "lucide-react",
      "framer-motion",
      "date-fns",
    ],
  },

  // Compiler options
  compiler: {
    removeConsole:
      process.env.NODE_ENV === "production"
        ? { exclude: ["error", "warn"] }
        : false,
  },

  // ⚠️ headers() حذف شد — با static export سازگار نیست
  // Cache headers از طریق Cloudflare تنظیم می‌شوند

  // Webpack customizations
  webpack: (config, { isServer, dev }) => {
    if (!dev && !isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: "all",
          cacheGroups: {
            default: false,
            vendors: false,
            vendor: {
              name: "vendor",
              chunks: "all",
              test: /node_modules/,
              priority: 20,
            },
            framerMotion: {
              name: "framer-motion",
              test: /[\\/]node_modules[\\/]framer-motion[\\/]/,
              chunks: "all",
              priority: 30,
            },
            lucide: {
              name: "lucide",
              test: /[\\/]node_modules[\\/]lucide-react[\\/]/,
              chunks: "all",
              priority: 30,
            },
            common: {
              name: "common",
              minChunks: 2,
              chunks: "all",
              priority: 10,
              reuseExistingChunk: true,
            },
          },
        },
      };
    }

    return config;
  },

  // Static export
  output: "export",
  trailingSlash: true,
};

module.exports = nextConfig;