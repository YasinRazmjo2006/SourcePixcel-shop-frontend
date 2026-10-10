"use client";

import { motion } from "framer-motion";
import { ProductCardSkeleton, Skeleton } from "@/components/common";

export default function Loading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
      {/* Hero skeleton */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <Skeleton variant="rect" className="w-full h-[200px] md:h-[300px] rounded-xl" />
      </motion.div>

      {/* Service badges skeleton */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <div className="grid grid-cols-3 md:grid-cols-5 gap-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="flex flex-col items-center gap-2"
            >
              <Skeleton variant="circle" width={48} height={48} />
              <Skeleton variant="text" width={60} height={12} />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Category circles skeleton */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <Skeleton variant="text" width={100} height={20} className="mb-4" />
        <div className="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-12 gap-3">
          {Array.from({ length: 12 }).map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: i * 0.03 }}
              className="flex flex-col items-center gap-2"
            >
              <Skeleton variant="circle" width={64} height={64} />
              <Skeleton variant="text" width={50} height={10} />
            </motion.div>
          ))}
        </div>
      </div>

      {/* Product grid skeleton */}
      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4">
        <Skeleton variant="text" width={120} height={20} className="mb-4" />
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
            >
              <ProductCardSkeleton />
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
