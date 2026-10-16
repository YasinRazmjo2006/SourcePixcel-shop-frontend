// lib/data/product-images.ts
import { withBasePath } from "@/lib/utils/paths";

export function getProductImage(id: number, _width = 600, _height = 600): string {
  const photoId = ((id - 1) % 12) + 1;
  return withBasePath(`/images/photos/photo-${photoId}.webp`);
}
