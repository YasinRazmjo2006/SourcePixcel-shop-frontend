"use client";

import { useState } from "react";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface ProductGalleryProps {
  images: string[];
  alt: string;
}

export default function ProductGallery({ images, alt }: ProductGalleryProps) {
  const [active, setActive] = useState(0);

  const next = () => setActive((p) => (p + 1) % images.length);
  const prev = () => setActive((p) => (p - 1 + images.length) % images.length);

  return (
    <div className="flex flex-col-reverse md:flex-row gap-3">
      {/* Thumbnails */}
      <div className="flex md:flex-col gap-2 overflow-x-auto md:overflow-visible">
        {images.map((img, i) => (
          <button
            key={i}
            onClick={() => setActive(i)}
            className={`w-14 h-14 md:w-16 md:h-16 shrink-0 rounded-lg border-2 overflow-hidden transition-colors ${
              i === active
                ? "border-[#EF4056]"
                : "border-[#E0E0E2] hover:border-[#A1A3A8]"
            }`}
            aria-label={`Image ${i + 1}`}
          >
            <Image
              src={img}
              alt={`${alt} thumbnail ${i + 1}`}
              width={64}
              height={64}
              className="w-full h-full object-cover"
            />
          </button>
        ))}
      </div>

      {/* Main image */}
      <div className="flex-1 relative group">
        <div className="aspect-square bg-white rounded-lg border border-[#E0E0E2] overflow-hidden relative">
          <Image
            src={images[active]}
            alt={alt}
            fill
            sizes="(max-width: 768px) 100vw, 50vw"
            className="object-contain p-4"
            priority
          />
        </div>

        {images.length > 1 && (
          <>
            <button
              onClick={prev}
              aria-label="Previous image"
              className="absolute top-1/2 -translate-y-1/2 right-2 w-9 h-9 rounded-full bg-white/90 backdrop-blur flex items-center justify-center text-[#3F4064] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronRight size={18} />
            </button>
            <button
              onClick={next}
              aria-label="Next image"
              className="absolute top-1/2 -translate-y-1/2 left-2 w-9 h-9 rounded-full bg-white/90 backdrop-blur flex items-center justify-center text-[#3F4064] opacity-0 group-hover:opacity-100 transition-opacity shadow-md"
            >
              <ChevronLeft size={18} />
            </button>
          </>
        )}
      </div>
    </div>
  );
}
