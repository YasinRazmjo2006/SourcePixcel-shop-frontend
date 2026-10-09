// lib/data/mock-orders.ts
// Mock orders for demo purposes

export interface OrderItem {
  productId: number;
  quantity: number;
  priceAtPurchase: number;
}

export interface MockOrder {
  id: string;
  date: string;
  status: "pending" | "processing" | "shipped" | "delivered" | "cancelled";
  items: OrderItem[];
  total: number;
  shippingAddress: string;
}

export const mockOrders: MockOrder[] = [
  {
    id: "SP-20240001",
    date: "1403/06/15",
    status: "delivered",
    items: [
      { productId: 1, quantity: 1, priceAtPurchase: 66_240_000 },
      { productId: 24, quantity: 1, priceAtPurchase: 14_760_000 },
    ],
    total: 81_000_000,
    shippingAddress: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  },
  {
    id: "SP-20240002",
    date: "1403/06/20",
    status: "shipped",
    items: [{ productId: 37, quantity: 1, priceAtPurchase: 38_000_000 }],
    total: 38_000_000,
    shippingAddress: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  },
  {
    id: "SP-20240003",
    date: "1403/07/01",
    status: "processing",
    items: [
      { productId: 11, quantity: 1, priceAtPurchase: 90_250_000 },
      { productId: 44, quantity: 2, priceAtPurchase: 7_480_000 },
    ],
    total: 105_210_000,
    shippingAddress: "اصفهان، خیابان چهارباغ، پلاک ۴۵",
  },
  {
    id: "SP-20240004",
    date: "1403/07/10",
    status: "pending",
    items: [{ productId: 60, quantity: 1, priceAtPurchase: 10_000_000 }],
    total: 10_000_000,
    shippingAddress: "تهران، خیابان ولیعصر، پلاک ۱۲۳",
  },
];

export const getOrderById = (id: string): MockOrder | undefined =>
  mockOrders.find((o) => o.id === id);
