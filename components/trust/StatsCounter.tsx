"use client";

import { useEffect, useRef, useState } from "react";
import { motion, useInView } from "framer-motion";
import { Users, Package, Star, Truck } from "lucide-react";
import type { Locale } from "@/lib/types";

interface StatsCounterProps {
  locale: Locale;
}

interface StatItem {
  icon: React.ComponentType<{ size?: number; className?: string }>;
  value: number;
  suffix: string;
  labelFa: string;
  labelEn: string;
  color: string;
}

const STATS: StatItem[] = [
  {
    icon: Users,
    value: 125000,
    suffix: "+",
    labelFa: "مشتری راضی",
    labelEn: "Happy Customers",
    color: "#EF4056",
  },
  {
    icon: Package,
    value: 480000,
    suffix: "+",
    labelFa: "سفارش موفق",
    labelEn: "Successful Orders",
    color: "#22C55E",
  },
  {
    icon: Star,
    value: 4.9,
    suffix: "/5",
    labelFa: "امتیاز کاربران",
    labelEn: "User Rating",
    color: "#F59E0B",
  },
  {
    icon: Truck,
    value: 24,
    suffix: "h",
    labelFa: "میانگین ارسال",
    labelEn: "Avg Delivery",
    color: "#00BFFF",
  },
];

function AnimatedNumber({
  value,
  suffix,
  decimals = 0,
}: {
  value: number;
  suffix: string;
  decimals?: number;
}) {
  const [display, setDisplay] = useState(0);
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-50px" });

  useEffect(() => {
    if (!inView) return;

    const duration = 1500;
    const steps = 60;
    const stepTime = duration / steps;
    const increment = value / steps;
    let current = 0;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = Math.min(increment * step, value);
      setDisplay(current);

      if (step >= steps) {
        clearInterval(timer);
        setDisplay(value);
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [inView, value]);

  const formatted =
    decimals > 0
      ? display.toFixed(decimals)
      : Math.floor(display).toLocaleString("en-US");

  return (
    <span ref={ref} className="tabular-nums">
      {formatted}
      {suffix}
    </span>
  );
}

export default function StatsCounter({ locale }: StatsCounterProps) {
  const isFa = locale === "fa";

  return (
    <div className="bg-gradient-to-l from-[#EF4056] to-[#d63850] rounded-xl overflow-hidden">
      <div className="max-w-[1400px] mx-auto px-4 py-6 md:py-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {STATS.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1, duration: 0.4 }}
                className="flex flex-col items-center text-center text-white"
              >
                <div className="w-12 h-12 rounded-full bg-white/15 backdrop-blur flex items-center justify-center mb-3">
                  <Icon size={22} />
                </div>
                <div className="text-[20px] md:text-[26px] font-bold mb-1">
                  <AnimatedNumber
                    value={stat.value}
                    suffix={stat.suffix}
                    decimals={stat.value < 10 ? 1 : 0}
                  />
                </div>
                <div className="text-[11px] md:text-[12px] text-white/80">
                  {isFa ? stat.labelFa : stat.labelEn}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
