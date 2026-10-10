"use client";

import { motion } from "framer-motion";
import { cardHoverVariants } from "@/lib/motion";

interface AnimatedCardProps {
  children: React.ReactNode;
  className?: string;
  disabled?: boolean;
}

export default function AnimatedCard({
  children,
  className,
  disabled = false,
}: AnimatedCardProps) {
  if (disabled) {
    return <div className={className}>{children}</div>;
  }

  return (
    <motion.div
      variants={cardHoverVariants}
      initial="rest"
      whileHover="hover"
      animate="rest"
      className={className}
    >
      {children}
    </motion.div>
  );
}
