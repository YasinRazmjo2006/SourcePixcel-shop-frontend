// lib/data/mock-admin-orders.ts
import type {
  AdminOrder,
  AdminOrderStatus,
  PaymentMethod,
  ShippingMethod,
} from "@/lib/types";
import { products } from "./products";
import {
  seededRandom,
  pick,
  pickMany,
  intBetween,
  weightedPick,
  PERSIAN_CITIES,
  PERSIAN_STREETS,
} from "./admin-generators";
import { adminUsers } from "./mock-admin-users";

const ORDER_SEED = 1234;
const ORDER_COUNT = 5000;

// ═══════════════════════════════════════════════════════════════
// ORDER GENERATION
// ═══════════════════════════════════════════════════════════════

function generateOrder(index: number, rand: () => number): AdminOrder {
  const user = adminUsers[intBetween(0, adminUsers.length - 1, rand)];

  const itemsCount = weightedPick(
    [
      { value: 1, weight: 40 },
      { value: 2, weight: 30 },
      { value: 3, weight: 20 },
      { value: 4, weight: 8 },
      { value: 5, weight: 2 },
    ],
    rand
  );

  const selectedProducts = pickMany(products, itemsCount, rand);

  const items = selectedProducts.map((p) => ({
    productId: p.id,
    titleFa: p.titleFa,
    titleEn: p.titleEn,
    image: p.image,
    price: p.finalPrice,
    quantity: intBetween(1, 3, rand),
  }));

  const subtotal = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const discount = rand() > 0.7 ? Math.round(subtotal * 0.1) : 0;
  const shipping = subtotal > 5_000_000 ? 0 : 45_000;
  const total = subtotal - discount + shipping;

  const status = weightedPick<AdminOrderStatus>(
    [
      { value: "delivered", weight: 55 },
      { value: "shipped", weight: 15 },
      { value: "processing", weight: 15 },
      { value: "pending", weight: 8 },
      { value: "cancelled", weight: 4 },
      { value: "refunded", weight: 3 },
    ],
    rand
  );

  const paymentMethod = weightedPick<PaymentMethod>(
    [
      { value: "zarinpal", weight: 70 },
      { value: "idpay", weight: 15 },
      { value: "nextpay", weight: 10 },
      { value: "cod", weight: 5 },
    ],
    rand
  );

  const shippingMethod = weightedPick<ShippingMethod>(
    [
      { value: "post", weight: 60 },
      { value: "tipax", weight: 30 },
      { value: "pickup", weight: 10 },
    ],
    rand
  );

  const daysAgo = intBetween(0, 365, rand);
  const createdAt = new Date(Date.now() - daysAgo * 86400000);
  const updatedAt = new Date(createdAt.getTime() + intBetween(0, 10, rand) * 86400000);

  const city = user.city || pick(PERSIAN_CITIES, rand);
  const street = pick(PERSIAN_STREETS, rand);
  const address = `${city}، ${street}، پلاک ${intBetween(1, 500, rand)}، واحد ${intBetween(1, 20, rand)}`;

  return {
    id: `SP-${String(100000 + index).padStart(6, "0")}`,
    userId: user.id,
    customerName: user.fullName,
    customerMobile: user.mobile,
    items,
    itemsCount: items.reduce((sum, i) => sum + i.quantity, 0),
    subtotal,
    discount,
    shipping,
    total,
    status,
    paymentMethod,
    shippingMethod,
    city,
    address,
    createdAt: createdAt.toISOString(),
    updatedAt: updatedAt.toISOString(),
    trackingCode:
      status === "shipped" || status === "delivered"
        ? `TRK${intBetween(100000000, 999999999, rand)}`
        : undefined,
  };
}

// Generate all orders once
const rand = seededRandom(ORDER_SEED);
export const adminOrders: AdminOrder[] = Array.from({ length: ORDER_COUNT }, (_, i) =>
  generateOrder(i, rand)
);

// Sort by createdAt descending
adminOrders.sort(
  (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
);

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

export function getAdminOrderById(id: string): AdminOrder | undefined {
  return adminOrders.find((o) => o.id === id);
}

export function getAdminOrderStats() {
  const total = adminOrders.length;
  const byStatus: Record<AdminOrderStatus, number> = {
    pending: 0,
    processing: 0,
    shipped: 0,
    delivered: 0,
    cancelled: 0,
    refunded: 0,
  };

  let totalRevenue = 0;
  for (const order of adminOrders) {
    byStatus[order.status]++;
    if (order.status !== "cancelled" && order.status !== "refunded") {
      totalRevenue += order.total;
    }
  }

  return {
    total,
    byStatus,
    totalRevenue,
    averageOrderValue: total > 0 ? Math.round(totalRevenue / total) : 0,
  };
}

export const ADMIN_ORDERS_TOTAL = ORDER_COUNT;
