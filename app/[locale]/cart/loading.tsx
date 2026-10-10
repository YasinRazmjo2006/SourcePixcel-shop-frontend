"use client";

import { motion } from "framer-motion";
import { Skeleton } from "@/components/common";

export default function CartLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Skeleton variant="text" width={120} height={20} className="mb-4" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 space-y-3">
          {[1, 2, 3].map((i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 flex gap-4"
            >
              <Skeleton variant="rect" width={100} height={100} className="shrink-0" />
              <div className="flex-1 space-y-3">
                <Skeleton variant="text" width="80%" height={16} />
                <Skeleton variant="text" width="40%" height={12} />
                <div className="flex items-center justify-between pt-2">
                  <Skeleton variant="rect" width={90} height={32} />
                  <Skeleton variant="text" width={80} height={16} />
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 space-y-3">
            <Skeleton variant="text" width={120} height={20} className="mb-4" />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="text" width="100%" height={16} />
            <Skeleton variant="rect" width="100%" height={44} className="mt-4" />
          </div>
        </div>
      </div>
    </div>
  );
}
