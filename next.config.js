/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true,
    remotePatterns: [
      { protocol: "https", hostname: "loremflickr.com", pathname: "/**" },
      { protocol: "https", hostname: "picsum.photos", pathname: "/**" },
      { protocol: "https", hostname: "images.unsplash.com", pathname: "/**" },
    ],
    dangerouslyAllowSVG: true,
    contentDispositionType: "attachment",
    contentSecurityPolicy:
      "default-src 'self'; script-src 'none'; sandbox;",
  },

  // Performance
  reactStrictMode: true,

  // Compression
  compress: true,

  // Production source maps
  productionBrowserSourceMaps: false,

  // Power header
  poweredByHeader: false,

  // Experimental optimizations
  experimental: {
    optimizePackageImports: ["lucide-react"],
  },

  // Webpack customizations
  webpack: (config, { isServer }) => {
    // Bundle analyzer (only when ANALYZE env is set)
    if (process.env.ANALYZE === "true") {
      const BundleAnalyzer = require("@next/bundle-analyzer");
      config.plugins.push(
        new BundleAnalyzer({
          enabled: true,
        })
      );
    }
    return config;
  },
};



module.exports = nextConfig;
