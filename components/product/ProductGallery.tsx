"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronLeft, ChevronRight, ZoomIn } from "lucide-react";
import { SmartImage } from "@/components/common";

interface ProductGalleryProps {
  images: string[];
  alt: string;
  category?: string;
}

export default function ProductGallery({
  images,
  alt,
  category,
}: ProductGalleryProps) {
  const [active, setActive] = useState(0);

  const next = () => setActive((p) => (p + 1) % images.length);
  const prev = () => setActive((p) => (p - 1 + images.length) % images.length);

  return (
    <div className="flex flex-col-reverse md:flex-row gap-3">
      {/* Thumbnails */}
      <div className="flex md:flex-col gap-2 overflow-x-auto md:overflow-visible pb-1 md:pb-0">
        {images.map((img, i) => (
          <motion.button
            key={i}
            onClick={() => setActive(i)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`w-14 h-14 md:w-16 md:h-16 shrink-0 rounded-lg border-2 overflow-hidden transition-colors relative ${
              i === active
                ? "border-[#EF4056]"
                : "border-[#E0E0E2] dark:border-[#2A2A2E] hover:border-[#A1A3A8]"
            }`}
            aria-label={`Image ${i + 1}`}
          >
            <SmartImage
              src={img}
              alt={`${alt} thumbnail ${i + 1}`}
              fill
              sizes="64px"
              className="object-cover"
              category={category}
            />
          </motion.button>
        ))}
      </div>

      {/* Main image */}
      <div className="flex-1 relative group">
        <div className="aspect-square bg-white dark:bg-[#1A1A1E] rounded-xl border border-[#E0E0E2] dark:border-[#2A2A2E] overflow-hidden relative">
          <AnimatePresence mode="wait">
            <motion.div
              key={active}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
              className="absolute inset-0"
            >
              <SmartImage
                src={images[active]}
                alt={alt}
                fill
                sizes="(max-width: 768px) 100vw, 50vw"
                className="object-contain p-4"
                priority
                category={category}
              />
            </motion.div>
          </AnimatePresence>
        </div>

        {images.length > 1 && (
          <>
            <motion.button
              onClick={prev}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              aria-label="Previous image"
              className="absolute top-1/2 -translate-y-1/2 right-2 w-9 h-9 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronRight size={18} />
            </motion.button>
            <motion.button
              onClick={next}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              aria-label="Next image"
              className="absolute top-1/2 -translate-y-1/2 left-2 w-9 h-9 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#3F4064] dark:text-[#E5E5EA] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronLeft size={18} />
            </motion.button>
          </>
        )}

        {/* Zoom hint */}
        <div
          className="absolute top-3 opacity-0 group-hover:opacity-100 transition-opacity"
          style={{ left: 12 }}
        >
          <div className="w-8 h-8 rounded-full bg-white/90 dark:bg-[#1A1A1E]/90 backdrop-blur flex items-center justify-center text-[#62666D] shadow-md">
            <ZoomIn size={14} />
          </div>
        </div>
      </div>
    </div>
  );
}
