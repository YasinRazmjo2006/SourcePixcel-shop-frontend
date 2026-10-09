// lib/data/index.ts
export {
  categories,
  brands,
  products,
  getProductBySlug,
  getProductsByCategory,
  getProductsByBrand,
  getFeaturedProducts,
  getNewProducts,
  getDiscountedProducts,
  getCategoryById,
  getBrandById,
  getProductsBySubcategory,
} from "./products";

export {
  mockOrders,
  getOrderById,
} from "./mock-orders";
export type { MockOrder, OrderItem } from "./mock-orders";

export {
  blogPosts,
  getBlogPostBySlug,
  getRecentBlogPosts,
  getRelatedBlogPosts,
} from "./mock-blog";
export type { BlogPost } from "./mock-blog";

export {
  mockReviews,
  getReviewsByProduct,
  getGenericReviews,
  getReviewsForProduct,
} from "./mock-reviews";

export { getProductImage } from "./product-images";
