"use client";

import { motion } from "framer-motion";
import { Skeleton } from "@/components/common";

export default function ProductLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <Skeleton variant="text" width={200} height={16} className="mb-4" />

      <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 md:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Gallery skeleton */}
          <div className="flex flex-col-reverse md:flex-row gap-3">
            <div className="flex md:flex-col gap-2">
              {[1, 2, 3, 4].map((i) => (
                <Skeleton
                  key={i}
                  variant="rect"
                  width={64}
                  height={64}
                  className="shrink-0"
                />
              ))}
            </div>
            <Skeleton
              variant="rect"
              className="flex-1 aspect-square rounded-xl"
            />
          </div>

          {/* Info skeleton */}
          <div className="space-y-4">
            <Skeleton variant="text" width="40%" height={14} />
            <Skeleton variant="text" width="100%" height={24} />
            <Skeleton variant="text" width="60%" height={18} />
            <Skeleton variant="rect" width="100%" height={1} />
            <Skeleton variant="text" width="50%" height={32} />
            <Skeleton variant="rect" width={120} height={32} />
            <Skeleton variant="rect" width="100%" height={44} />
            <div className="space-y-2 pt-3">
              <Skeleton variant="text" width="100%" height={14} />
              <Skeleton variant="text" width="100%" height={14} />
              <Skeleton variant="text" width="80%" height={14} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
