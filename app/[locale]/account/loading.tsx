"use client";

import { Skeleton } from "@/components/common";

export default function AccountLoading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] p-4 space-y-3">
            <div className="flex items-center gap-3 pb-3 border-b border-[#E0E0E2] dark:border-[#2A2A2E]">
              <Skeleton variant="circle" width={48} height={48} />
              <div className="flex-1 space-y-2">
                <Skeleton variant="text" width="80%" height={14} />
                <Skeleton variant="text" width="60%" height={12} />
              </div>
            </div>
            {[1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} variant="text" width="100%" height={36} />
            ))}
          </div>
        </div>

        <div className="lg:col-span-3 space-y-4">
          <Skeleton variant="rect" width="100%" height={100} className="rounded-xl" />
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[1, 2, 3, 4].map((i) => (
              <Skeleton key={i} variant="rect" width="100%" height={100} className="rounded-xl" />
            ))}
          </div>
          <Skeleton variant="rect" width="100%" height={200} className="rounded-xl" />
        </div>
      </div>
    </div>
  );
}
