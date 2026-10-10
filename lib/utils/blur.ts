// lib/utils/blur.ts

/**
 * Generate a tiny base64 SVG placeholder for next/image blur effect.
 * Uses category color for a beautiful gradient shimmer.
 */
export function generateBlurPlaceholder(
  color: string = "#EF4056",
  width: number = 16,
  height: number = 16
): string {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="${color}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="${color}" stop-opacity="0.1"/>
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#g)"/>
</svg>`;
  const base64 = Buffer.from(svg).toString("base64");
  return `data:image/svg+xml;base64,${base64}`;
}

/**
 * Map a product category to its color for consistent placeholders.
 */
export const CATEGORY_COLORS: Record<string, string> = {
  mobile: "#EF4056",
  laptop: "#00BFFF",
  tablet: "#8B5CF6",
  audio: "#F59E0B",
  camera: "#22C55E",
  smartwatch: "#EC4899",
  gaming: "#06B6D4",
  accessories: "#6B7280",
  clothing: "#F97316",
  shoes: "#10B981",
  home: "#6366F1",
  books: "#84CC16",
};

export function getCategoryColor(category: string): string {
  return CATEGORY_COLORS[category] ?? "#EF4056";
}

export function getProductBlur(category: string): string {
  return generateBlurPlaceholder(getCategoryColor(category));
}
