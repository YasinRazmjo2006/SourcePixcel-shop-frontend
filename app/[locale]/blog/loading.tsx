"use client";

import { motion } from "framer-motion";
import { Skeleton } from "@/components/common";

export default function BlogLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Skeleton variant="text" width={150} height={20} className="mb-6" />

      {/* Featured */}
      <div className="mb-8">
        <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden">
          <Skeleton variant="rect" className="w-full aspect-[16/7]" />
          <div className="p-4 space-y-3">
            <Skeleton variant="text" width="30%" height={14} />
            <Skeleton variant="text" width="80%" height={24} />
            <Skeleton variant="text" width="100%" height={14} />
            <Skeleton variant="text" width="60%" height={14} />
          </div>
        </div>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden"
          >
            <Skeleton variant="rect" className="w-full aspect-video" />
            <div className="p-4 space-y-3">
              <Skeleton variant="text" width="30%" height={12} />
              <Skeleton variant="text" width="100%" height={18} />
              <Skeleton variant="text" width="100%" height={14} />
              <Skeleton variant="text" width="80%" height={14} />
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
