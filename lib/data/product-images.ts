// lib/data/product-images.ts
export function getProductImage(id: number, width = 600, height = 600): string {
  return `https://picsum.photos/seed/sourcepixcel-${id}/${width}/${height}`;
}