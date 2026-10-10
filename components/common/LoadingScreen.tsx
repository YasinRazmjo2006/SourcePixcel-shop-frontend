"use client";

import { motion } from "framer-motion";

interface LoadingScreenProps {
  label?: string;
}

export default function LoadingScreen({ label = "Loading..." }: LoadingScreenProps) {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-4">
      {/* Animated logo */}
      <div className="relative mb-6">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-20 h-20 rounded-full border-4 border-[#EF4056]/20 border-t-[#EF4056]"
        />
        <motion.div
          animate={{ scale: [1, 1.1, 1] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          className="absolute inset-0 flex items-center justify-center"
        >
          <div className="w-10 h-10 rounded-xl bg-[#EF4056] flex items-center justify-center text-white text-[18px] font-bold shadow-lg">
            S
          </div>
        </motion.div>
      </div>

      {/* Dots */}
      <div className="flex items-center gap-2 mb-3">
        {[0, 1, 2].map((i) => (
          <motion.span
            key={i}
            animate={{ y: [0, -6, 0], opacity: [0.4, 1, 0.4] }}
            transition={{
              duration: 0.8,
              repeat: Infinity,
              delay: i * 0.15,
              ease: "easeInOut",
            }}
            className="w-2 h-2 rounded-full bg-[#EF4056]"
          />
        ))}
      </div>

      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="text-[12px] text-[#A1A3A8]"
      >
        {label}
      </motion.p>
    </div>
  );
}
