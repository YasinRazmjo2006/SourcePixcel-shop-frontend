// lib/data/product-images.ts
import { withBasePath } from "@/lib/utils/paths";

export function getProductImage(id: number, _width = 600, _height = 600): string {
  return withBasePath(`/images/products/product-${id}.svg`);
}
