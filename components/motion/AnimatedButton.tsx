"use client";

import { motion, type HTMLMotionProps } from "framer-motion";
import { buttonTapVariants } from "@/lib/motion";

interface AnimatedButtonProps extends HTMLMotionProps<"button"> {
  children: React.ReactNode;
}

export default function AnimatedButton({
  children,
  ...props
}: AnimatedButtonProps) {
  return (
    <motion.button
      variants={buttonTapVariants}
      initial="rest"
      whileHover="hover"
      whileTap="tap"
      {...props}
    >
      {children}
    </motion.button>
  );
}
