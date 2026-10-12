"use client";

import { motion } from "framer-motion";
import { Users, TrendingUp } from "lucide-react";
import type { Locale } from "@/lib/types";
import { useLiveActivityStore } from "@/lib/stores";

interface OnlineUsersCardProps {
  locale: Locale;
}

export default function OnlineUsersCard({ locale }: OnlineUsersCardProps) {
  const isFa = locale === "fa";
  const onlineUsers = useLiveActivityStore((s) => s.onlineUsers);
  const isConnected = useLiveActivityStore((s) => s.isConnected);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-gradient-to-br from-[#00BFFF] to-[#0284C7] rounded-xl p-4 text-white relative overflow-hidden"
    >
      {/* Decorative circles */}
      <div className="absolute -top-8 -right-8 w-24 h-24 rounded-full bg-white/10" />
      <div className="absolute -bottom-6 -left-6 w-20 h-20 rounded-full bg-white/5" />

      <div className="relative">
        <div className="flex items-center justify-between mb-3">
          <div className="w-9 h-9 rounded-lg bg-white/15 backdrop-blur flex items-center justify-center">
            <Users size={16} />
          </div>
          {isConnected && (
            <motion.div
              animate={{ opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-[10px] font-bold bg-white/15 backdrop-blur px-2 py-0.5 rounded-full flex items-center gap-1"
            >
              <TrendingUp size={10} />
              {isFa ? "زنده" : "LIVE"}
            </motion.div>
          )}
        </div>

        <div className="text-[28px] font-bold leading-none tabular-nums mb-1">
          {onlineUsers.toLocaleString(isFa ? "fa-IR" : "en-US")}
        </div>
        <div className="text-[11px] text-white/80">
          {isFa ? "کاربر آنلاین" : "Users Online"}
        </div>
      </div>
    </motion.div>
  );
}
