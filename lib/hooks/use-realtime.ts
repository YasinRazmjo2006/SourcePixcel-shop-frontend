"use client";

import { useEffect, useRef } from "react";
import { useLiveActivityStore } from "@/lib/stores";
import type { AdminActivity, ActivityType } from "@/lib/types";
import {
  PERSIAN_FIRST_NAMES,
  PERSIAN_LAST_NAMES,
  intBetween,
} from "@/lib/data";

const ACTIVITY_TEMPLATES: Array<{
  type: ActivityType;
  titleFa: string;
  titleEn: string;
  descFa: (name: string, amount?: number) => string;
  descEn: (name: string, amount?: number) => string;
  withAmount?: boolean;
}> = [
  {
    type: "order",
    titleFa: "سفارش جدید",
    titleEn: "New order",
    descFa: (n, a) => `${n} سفارش جدید به مبلغ ${a?.toLocaleString("fa-IR")} تومان ثبت کرد`,
    descEn: (n, a) => `${n} placed an order for ${a?.toLocaleString("en-US")} Toman`,
    withAmount: true,
  },
  {
    type: "user",
    titleFa: "کاربر جدید",
    titleEn: "New user",
    descFa: (n) => `${n} عضو جدید فروشگاه شد`,
    descEn: (n) => `${n} just joined the store`,
  },
  {
    type: "review",
    titleFa: "نظر جدید",
    titleEn: "New review",
    descFa: (n) => `${n} یک نظر جدید ثبت کرد`,
    descEn: (n) => `${n} submitted a new review`,
  },
  {
    type: "payment",
    titleFa: "پرداخت موفق",
    titleEn: "Payment received",
    descFa: (n, a) => `پرداخت ${a?.toLocaleString("fa-IR")} تومان از ${n} دریافت شد`,
    descEn: (n, a) => `Payment of ${a?.toLocaleString("en-US")} Toman received from ${n}`,
    withAmount: true,
  },
  {
    type: "product",
    titleFa: "موجودی کم",
    titleEn: "Low stock",
    descFa: () => `موجودی یکی از محصولات کمتر از ۵ عدد شد`,
    descEn: () => `A product's stock dropped below 5`,
  },
];

function generateRandomActivity(): AdminActivity {
  const template =
    ACTIVITY_TEMPLATES[Math.floor(Math.random() * ACTIVITY_TEMPLATES.length)];
  const firstName =
    PERSIAN_FIRST_NAMES[Math.floor(Math.random() * PERSIAN_FIRST_NAMES.length)];
  const lastName =
    PERSIAN_LAST_NAMES[Math.floor(Math.random() * PERSIAN_LAST_NAMES.length)];
  const fullName = `${firstName} ${lastName}`;
  const amount = template.withAmount
    ? intBetween(200_000, 50_000_000, Math.random)
    : undefined;

  return {
    id: `live-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    type: template.type,
    titleFa: template.titleFa,
    titleEn: template.titleEn,
    descriptionFa: template.descFa(fullName, amount),
    descriptionEn: template.descEn(fullName, amount),
    timestamp: Date.now(),
    user: { name: fullName },
    amount,
  };
}

/**
 * Simulated WebSocket connection that generates live activities.
 * In production, replace with actual WebSocket / Socket.io.
 */
export function useRealtime(enabled = true, intervalMs = 8000) {
  const addActivity = useLiveActivityStore((s) => s.addActivity);
  const setOnlineUsers = useLiveActivityStore((s) => s.setOnlineUsers);
  const setConnected = useLiveActivityStore((s) => s.setConnected);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const onlineIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!enabled) return;

    // Simulate connection
    setConnected(true);
    setOnlineUsers(intBetween(120, 350, Math.random));

    // First activity after 3 seconds
    const firstTimeout = setTimeout(() => {
      addActivity(generateRandomActivity());
    }, 3000);

    // Then regular intervals
    intervalRef.current = setInterval(() => {
      addActivity(generateRandomActivity());
    }, intervalMs);

    // Update online users every 5 seconds
    onlineIntervalRef.current = setInterval(() => {
      setOnlineUsers(intBetween(120, 350, Math.random));
    }, 5000);

    return () => {
      clearTimeout(firstTimeout);
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (onlineIntervalRef.current) clearInterval(onlineIntervalRef.current);
      setConnected(false);
    };
  }, [enabled, intervalMs, addActivity, setOnlineUsers, setConnected]);
}
