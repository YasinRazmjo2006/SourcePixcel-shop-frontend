// lib/data/mock-admin-users.ts
import type { AdminUser, AdminUserRole } from "@/lib/types";
import {
  seededRandom,
  pick,
  intBetween,
  floatBetween,
  weightedPick,
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
  PERSIAN_CITIES,
} from "./admin-generators";

const USER_SEED = 42;
const USER_COUNT = 1000;

// ═══════════════════════════════════════════════════════════════
// USER GENERATION
// ═══════════════════════════════════════════════════════════════

function generateUser(id: number, rand: () => number): AdminUser {
  const firstName = pick(PERSIAN_FIRST_NAMES, rand);
  const lastName = pick(PERSIAN_LAST_NAMES, rand);
  const fullName = `${firstName} ${lastName}`;

  const email = `user${id}@${pick(["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"], rand)}`;
  const mobile = `09${intBetween(100000000, 999999999, rand)}`;

  const role = weightedPick<AdminUserRole>(
    [
      { value: "customer", weight: 92 },
      { value: "admin", weight: 3 },
      { value: "moderator", weight: 2 },
      { value: "editor", weight: 3 },
    ],
    rand
  );

  const joinDaysAgo = intBetween(1, 730, rand);
  const joinDate = new Date(Date.now() - joinDaysAgo * 86400000);

  const lastLoginDaysAgo = intBetween(0, Math.min(joinDaysAgo, 60), rand);
  const lastLogin = new Date(Date.now() - lastLoginDaysAgo * 86400000);

  const ordersCount = intBetween(0, 50, rand);
  const totalSpent = ordersCount * intBetween(500_000, 50_000_000, rand);
  const reviewsCount = intBetween(0, 15, rand);

  return {
    id,
    fullName,
    firstName,
    lastName,
    email,
    mobile,
    avatar: `https://i.pravatar.cc/150?u=${id}`,
    role,
    isActive: rand() > 0.1,
    isVerified: rand() > 0.2,
    isBanned: rand() > 0.97,
    city: pick(PERSIAN_CITIES, rand),
    joinDate: joinDate.toISOString(),
    lastLogin: lastLogin.toISOString(),
    ordersCount,
    totalSpent,
    reviewsCount,
  };
}

// Generate all users once
const rand = seededRandom(USER_SEED);
export const adminUsers: AdminUser[] = Array.from({ length: USER_COUNT }, (_, i) =>
  generateUser(i + 1, rand)
);

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

export function getAdminUserById(id: number): AdminUser | undefined {
  return adminUsers.find((u) => u.id === id);
}

export function getAdminUserStats() {
  const total = adminUsers.length;
  const active = adminUsers.filter((u) => u.isActive).length;
  const verified = adminUsers.filter((u) => u.isVerified).length;
  const banned = adminUsers.filter((u) => u.isBanned).length;
  const admins = adminUsers.filter((u) => u.role === "admin").length;
  const totalSpent = adminUsers.reduce((sum, u) => sum + u.totalSpent, 0);
  const totalOrders = adminUsers.reduce((sum, u) => sum + u.ordersCount, 0);

  return {
    total,
    active,
    verified,
    banned,
    admins,
    totalSpent,
    totalOrders,
    averageOrderValue: totalOrders > 0 ? Math.round(totalSpent / totalOrders) : 0,
  };
}

export const ADMIN_USERS_TOTAL = USER_COUNT;
