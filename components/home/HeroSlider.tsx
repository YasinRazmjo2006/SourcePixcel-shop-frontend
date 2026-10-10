"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, ArrowLeft, ArrowRight } from "lucide-react";
import type { Locale } from "@/lib/types";
import { slideVariants } from "@/lib/motion";

interface Slide {
  id: number;
  bgFrom: string;
  bgTo: string;
  emoji: string;
  titleFa: string;
  titleEn: string;
  subtitleFa: string;
  subtitleEn: string;
  ctaFa: string;
  ctaEn: string;
  href: string;
}

const SLIDES: Slide[] = [
  {
    id: 1,
    bgFrom: "#EF4056",
    bgTo: "#FF7B8A",
    emoji: "📱",
    titleFa: "جشنواره موبایل",
    titleEn: "Mobile Festival",
    subtitleFa: "تا ۴۰٪ تخفیف روی گوشی‌های پرچمدار",
    subtitleEn: "Up to 40% off on flagship phones",
    ctaFa: "مشاهده تخفیف‌ها",
    ctaEn: "See Discounts",
    href: "/category/mobile",
  },
  {
    id: 2,
    bgFrom: "#00BFFF",
    bgTo: "#4DD0FF",
    emoji: "💻",
    titleFa: "لپ‌تاپ‌های حرفه‌ای",
    titleEn: "Pro Laptops",
    subtitleFa: "جدیدترین مدل‌های ایسوس، اپل و لنوو",
    subtitleEn: "Latest Asus, Apple, and Lenovo models",
    ctaFa: "خرید کنید",
    ctaEn: "Shop Now",
    href: "/category/laptop",
  },
  {
    id: 3,
    bgFrom: "#8B5CF6",
    bgTo: "#A78BFA",
    emoji: "🎧",
    titleFa: "صدای بی‌نظیر",
    titleEn: "Ultimate Sound",
    subtitleFa: "هدفون‌های بی‌سیم با نویز کنسلینگ",
    subtitleEn: "Wireless headphones with noise cancelling",
    ctaFa: "مشاهده محصولات",
    ctaEn: "View Products",
    href: "/category/audio",
  },
];

interface HeroSliderProps {
  locale: Locale;
}

export default function HeroSlider({ locale }: HeroSliderProps) {
  const isFa = locale === "fa";
  const [current, setCurrent] = useState(0);
  const [direction, setDirection] = useState(1);

  useEffect(() => {
    const timer = setInterval(() => {
      setDirection(1);
      setCurrent((prev) => (prev + 1) % SLIDES.length);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  const goTo = (i: number) => {
    setDirection(i > current ? 1 : -1);
    setCurrent(i);
  };

  const next = () => {
    setDirection(1);
    setCurrent((prev) => (prev + 1) % SLIDES.length);
  };

  const prev = () => {
    setDirection(-1);
    setCurrent((prev) => (prev - 1 + SLIDES.length) % SLIDES.length);
  };

  const slide = SLIDES[current];

  return (
    <div className="relative w-full h-[180px] md:h-[280px] lg:h-[350px] rounded-xl overflow-hidden group">
      {/* Background gradient */}
      <motion.div
        key={`bg-${current}`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="absolute inset-0"
        style={{
          background: `linear-gradient(135deg, ${slide.bgFrom} 0%, ${slide.bgTo} 100%)`,
        }}
      />

      {/* Decorative circles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{ scale: [1, 1.1, 1], opacity: [0.1, 0.15, 0.1] }}
          transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
          className="absolute -top-20 -right-20 w-80 h-80 rounded-full bg-white"
        />
        <motion.div
          animate={{ scale: [1, 1.05, 1], opacity: [0.05, 0.08, 0.05] }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1,
          }}
          className="absolute -bottom-24 -left-24 w-96 h-96 rounded-full bg-white"
        />
      </div>

      {/* Content */}
      <AnimatePresence mode="wait" custom={direction}>
        <motion.div
          key={current}
          custom={direction}
          variants={slideVariants}
          initial="enter"
          animate="center"
          exit="exit"
          className="relative h-full flex items-center justify-between px-6 md:px-12 lg:px-16"
        >
          {/* Text side */}
          <div className="flex-1 text-white z-10 max-w-lg">
            <motion.h2
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.5 }}
              className="text-[22px] md:text-[34px] lg:text-[42px] font-bold mb-2 md:mb-3 drop-shadow-lg"
            >
              {isFa ? slide.titleFa : slide.titleEn}
            </motion.h2>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.5 }}
              className="text-[12px] md:text-[15px] lg:text-[17px] text-white/90 mb-4 md:mb-6 drop-shadow"
            >
              {isFa ? slide.subtitleFa : slide.subtitleEn}
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.5 }}
            >
              <Link
                href={`/${locale}${slide.href}`}
                className="inline-flex items-center gap-2 bg-white text-[#3F4064] font-bold text-[12px] md:text-[14px] px-5 md:px-6 py-2.5 md:py-3 rounded-lg hover:bg-white/90 hover:scale-105 transition-all shadow-lg"
              >
                {isFa ? slide.ctaFa : slide.ctaEn}
                {isFa ? <ArrowLeft size={16} /> : <ArrowRight size={16} />}
              </Link>
            </motion.div>
          </div>

          {/* Icon side */}
          <div className="hidden md:flex items-center justify-center shrink-0">
            <motion.div
              animate={{
                y: [0, -10, 0],
                rotate: [0, 3, -3, 0],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut",
              }}
              className="text-[140px] lg:text-[200px] drop-shadow-2xl select-none"
            >
              {slide.emoji}
            </motion.div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Arrows */}
      <button
        onClick={prev}
        aria-label="Previous slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 md:w-11 md:h-11 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white hover:bg-white/30 opacity-0 group-hover:opacity-100 transition-opacity z-20 ${
          isFa ? "right-3" : "left-3"
        }`}
      >
        {isFa ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>
      <button
        onClick={next}
        aria-label="Next slide"
        className={`absolute top-1/2 -translate-y-1/2 w-9 h-9 md:w-11 md:h-11 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center text-white hover:bg-white/30 opacity-0 group-hover:opacity-100 transition-opacity z-20 ${
          isFa ? "left-3" : "right-3"
        }`}
      >
        {isFa ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>

      {/* Dots */}
      <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2 z-20">
        {SLIDES.map((_, i) => (
          <button
            key={i}
            onClick={() => goTo(i)}
            aria-label={`Slide ${i + 1}`}
            className={`h-1.5 rounded-full transition-all ${
              i === current
                ? "bg-white w-8"
                : "bg-white/50 w-2 hover:bg-white/70"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
