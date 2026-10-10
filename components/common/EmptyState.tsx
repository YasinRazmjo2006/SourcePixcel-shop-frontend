"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import type { Locale } from "@/lib/types";
import { RippleButton } from "@/components/ui";

type IllustrationType =
  | "search"
  | "cart"
  | "wishlist"
  | "orders"
  | "compare"
  | "error"
  | "offline"
  | "404"
  | "empty-box"
  | "no-results";

interface EmptyStateProps {
  locale: Locale;
  type?: IllustrationType;
  titleFa?: string;
  titleEn?: string;
  messageFa?: string;
  messageEn?: string;
  actionLabelFa?: string;
  actionLabelEn?: string;
  actionHref?: string;
  onAction?: () => void;
}

const ILLUSTRATIONS: Record<
  IllustrationType,
  { emoji: string; color: string; bg: string }
> = {
  search: { emoji: "🔍", color: "#00BFFF", bg: "#00BFFF" },
  cart: { emoji: "🛒", color: "#EF4056", bg: "#EF4056" },
  wishlist: { emoji: "💝", color: "#EC4899", bg: "#EC4899" },
  orders: { emoji: "📦", color: "#8B5CF6", bg: "#8B5CF6" },
  compare: { emoji: "⚖️", color: "#F59E0B", bg: "#F59E0B" },
  error: { emoji: "⚠️", color: "#EF4444", bg: "#EF4444" },
  offline: { emoji: "📡", color: "#6B7280", bg: "#6B7280" },
  "404": { emoji: "🗺️", color: "#EF4056", bg: "#EF4056" },
  "empty-box": { emoji: "📭", color: "#A1A3A8", bg: "#A1A3A8" },
  "no-results": { emoji: "🔎", color: "#00BFFF", bg: "#00BFFF" },
};

export default function EmptyState({
  locale,
  type = "empty-box",
  titleFa,
  titleEn,
  messageFa,
  messageEn,
  actionLabelFa,
  actionLabelEn,
  actionHref,
  onAction,
}: EmptyStateProps) {
  const isFa = locale === "fa";
  const illustration = ILLUSTRATIONS[type];

  return (
    <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
      {/* Illustration container with animated circles */}
      <div className="relative mb-6">
        {/* Outer pulse ring */}
        <motion.div
          animate={{ scale: [1, 1.15, 1], opacity: [0.15, 0.05, 0.15] }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut",
          }}
          className="absolute inset-0 rounded-full"
          style={{
            backgroundColor: illustration.color,
            width: 120,
            height: 120,
          }}
        />

        {/* Middle ring */}
        <motion.div
          animate={{ scale: [1, 1.08, 1], opacity: [0.1, 0.2, 0.1] }}
          transition={{
            duration: 2.5,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 0.3,
          }}
          className="absolute inset-0 rounded-full"
          style={{
            backgroundColor: illustration.color,
            width: 120,
            height: 120,
          }}
        />

        {/* Emoji circle */}
        <motion.div
          initial={{ scale: 0, rotate: -10 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{
            type: "spring",
            stiffness: 300,
            damping: 20,
          }}
          className="relative w-[120px] h-[120px] rounded-full flex items-center justify-center"
          style={{ backgroundColor: `${illustration.bg}15` }}
        >
          <motion.span
            animate={{ y: [0, -6, 0] }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            className="text-[52px] select-none"
          >
            {illustration.emoji}
          </motion.span>
        </motion.div>

        {/* Decorative dots */}
        <motion.div
          animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, delay: 0.5 }}
          className="absolute w-2 h-2 rounded-full"
          style={{
            backgroundColor: illustration.color,
            top: 10,
            right: 10,
          }}
        />
        <motion.div
          animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.8, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, delay: 0.8 }}
          className="absolute w-1.5 h-1.5 rounded-full"
          style={{
            backgroundColor: illustration.color,
            bottom: 15,
            left: 8,
          }}
        />
      </div>

      {/* Title */}
      <motion.h3
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15, duration: 0.3 }}
        className="text-[18px] font-bold text-[#3F4064] dark:text-[#E5E5EA] mb-2"
      >
        {isFa ? titleFa : titleEn}
      </motion.h3>

      {/* Message */}
      <motion.p
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.3 }}
        className="text-[13px] text-[#62666D] dark:text-[#A1A3A8] mb-6 max-w-md leading-6"
      >
        {isFa ? messageFa : messageEn}
      </motion.p>

      {/* Action */}
      {(actionHref || onAction) && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25, duration: 0.3 }}
        >
          {actionHref ? (
            <Link href={actionHref}>
              <RippleButton size="md">
                {isFa ? actionLabelFa : actionLabelEn}
              </RippleButton>
            </Link>
          ) : (
            <RippleButton onClick={onAction} size="md">
              {isFa ? actionLabelFa : actionLabelEn}
            </RippleButton>
          )}
        </motion.div>
      )}
    </div>
  );
}
