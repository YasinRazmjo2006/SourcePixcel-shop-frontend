"use client";

import { useIntersectionObserver } from "@/lib/hooks";
import { motion } from "framer-motion";

interface LazySectionProps {
  children: React.ReactNode;
  className?: string;
  fallback?: React.ReactNode;
  minHeight?: number;
}

/**
 * LazySection — only renders content when it enters the viewport.
 * Great for below-the-fold sections with heavy content.
 */
export default function LazySection({
  children,
  className,
  fallback,
  minHeight = 200,
}: LazySectionProps) {
  const { ref, isVisible } = useIntersectionObserver<HTMLDivElement>({
    threshold: 0.05,
    rootMargin: "100px",
  });

  return (
    <div
      ref={ref}
      className={className}
      style={!isVisible ? { minHeight } : undefined}
    >
      {isVisible ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
        >
          {children}
        </motion.div>
      ) : (
        fallback ?? (
          <div
            className="animate-pulse bg-[#E0E0E2] dark:bg-[#2A2A2E] rounded-xl"
            style={{ height: minHeight }}
          />
        )
      )}
    </div>
  );
}
