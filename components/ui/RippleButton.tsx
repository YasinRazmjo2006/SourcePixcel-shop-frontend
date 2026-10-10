"use client";

import { useState, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface Ripple {
  id: number;
  x: number;
  y: number;
  size: number;
}

interface RippleButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "success" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
  rippleColor?: string;
}

export default function RippleButton({
  children,
  variant = "primary",
  size = "md",
  fullWidth = false,
  rippleColor,
  className,
  onClick,
  disabled,
  ...props
}: RippleButtonProps) {
  const [ripples, setRipples] = useState<Ripple[]>([]);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleClick = useCallback(
    (e: React.MouseEvent<HTMLButtonElement>) => {
      if (disabled) return;

      const button = buttonRef.current;
      if (button) {
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height) * 2;
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        const id = Date.now();
        setRipples((prev) => [...prev, { id, x, y, size }]);

        setTimeout(() => {
          setRipples((prev) => prev.filter((r) => r.id !== id));
        }, 600);
      }

      onClick?.(e);
    },
    [disabled, onClick]
  );

  const variantClasses = {
    primary: "bg-[#EF4056] text-white hover:bg-[#d63850]",
    secondary:
      "bg-[#00BFFF] text-white hover:bg-[#0099cc]",
    success: "bg-[#22C55E] text-white hover:bg-[#1da34d]",
    danger: "bg-[#EF4444] text-white hover:bg-[#d63030]",
    ghost:
      "bg-transparent text-[#3F4064] dark:text-[#E5E5EA] hover:bg-[#F5F5F5] dark:hover:bg-[#2A2A2E]",
  };

  const sizeClasses = {
    sm: "h-9 px-4 text-[12px]",
    md: "h-11 px-6 text-[13px]",
    lg: "h-12 px-8 text-[14px]",
  };

  const defaultRippleColor = rippleColor ?? "rgba(255, 255, 255, 0.5)";

  return (
    <motion.button
      ref={buttonRef}
      onClick={handleClick}
      disabled={disabled}
      whileHover={!disabled ? { scale: 1.02 } : {}}
      whileTap={!disabled ? { scale: 0.98 } : {}}
      className={`relative overflow-hidden rounded-lg font-bold transition-colors flex items-center justify-center gap-2 ${
        variantClasses[variant]
      } ${sizeClasses[size]} ${fullWidth ? "w-full" : ""} ${
        disabled ? "opacity-40 cursor-not-allowed" : ""
      } ${className ?? ""}`}
      {...props}
    >
      <AnimatePresence>
        {ripples.map((ripple) => (
          <motion.span
            key={ripple.id}
            initial={{ scale: 0, opacity: 1 }}
            animate={{ scale: 1, opacity: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="absolute rounded-full pointer-events-none"
            style={{
              left: ripple.x,
              top: ripple.y,
              width: ripple.size,
              height: ripple.size,
              backgroundColor: defaultRippleColor,
            }}
          />
        ))}
      </AnimatePresence>

      <span className="relative z-10 flex items-center gap-2">{children}</span>
    </motion.button>
  );
}
