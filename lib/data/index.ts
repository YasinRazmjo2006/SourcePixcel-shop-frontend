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

// ═══════════════════════════════════════════════════════════════
// ADMIN DATA
// ═══════════════════════════════════════════════════════════════

export {
  adminUsers,
  getAdminUserById,
  getAdminUserStats,
  ADMIN_USERS_TOTAL,
} from "./mock-admin-users";

export {
  adminOrders,
  getAdminOrderById,
  getAdminOrderStats,
  ADMIN_ORDERS_TOTAL,
} from "./mock-admin-orders";

export {
  analyticsOverview,
  monthlySales,
  categorySales,
  dailyVisitors,
  hourlyActivity,
  salesFunnel,
  topProducts,
} from "./mock-analytics";

export {
  adminActivities,
  getRecentActivities,
  getActivitiesByType,
} from "./mock-activities";

export {
  seededRandom,
  pick,
  pickMany,
  intBetween,
  floatBetween,
  weightedPick,
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
  PERSIAN_CITIES,
  PERSIAN_STREETS,
} from "./admin-generators";
