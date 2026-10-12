// lib/utils/index.ts
export {
  formatPrice,
  formatPriceWithCurrency,
  calcFinalPrice,
  formatDiscount,
  formatRating,
  formatReviewCount,
  truncate,
  getProductTitle,
  getCategoryName,
  getBrandName,
  formatDate,
  localePath,
  cn,
  getStockLabel,
  scrollToTop,
} from "./format";

export {
  isValidIranianMobile,
  normalizeMobile,
  formatMobileDisplay,
  isValidEmail,
  isValidIranianNationalId,
  isValidIranianPostalCode,
  getPasswordStrength,
  isValidPassword,
} from "./validators";

export {
  buildMetadata,
  buildProductSchema,
  buildOrganizationSchema,
  buildWebSiteSchema,
  buildBreadcrumbSchema,
  SITE_NAME_EXPORT,
  SITE_URL_EXPORT,
} from "./seo";

export {
  generateBlurPlaceholder,
  getCategoryColor,
  getProductBlur,
  CATEGORY_COLORS,
} from "./blur";

export {
  formatCompact,
  formatPercent,
  formatRelativeTime,
} from "./number-format";

export { exportToCSV, downloadBlob } from "./export-csv";
export type { CsvColumn } from "./export-csv";

export { exportToExcel } from "./export-excel";
export { exportToPDF } from "./export-pdf";
export type { PdfOptions } from "./export-pdf";
