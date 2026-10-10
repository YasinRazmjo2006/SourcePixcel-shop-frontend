"use client";

import Image, { type ImageProps } from "next/image";
import { useState } from "react";
import { getCategoryColor } from "@/lib/utils";

interface SmartImageProps extends Omit<ImageProps, "onLoad" | "onError"> {
  /** Optional category to pick color for placeholder */
  category?: string;
  /** Optional wrapper className */
  wrapperClassName?: string;
}

/**
 * SmartImage — next/image with automatic blur placeholder
 * and smooth fade-in on load.
 */
export default function SmartImage({
  category,
  wrapperClassName,
  className,
  alt,
  ...props
}: SmartImageProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  const color = category ? getCategoryColor(category) : "#EF4056";
  const blurDataURL = `data:image/svg+xml;base64,${Buffer.from(
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="${color}" stop-opacity="0.3"/><stop offset="100%" stop-color="${color}" stop-opacity="0.1"/></linearGradient></defs><rect width="16" height="16" fill="url(#g)"/></svg>`
  ).toString("base64")}`;

  return (
    <div className={`relative w-full h-full ${wrapperClassName ?? ""}`}>
      {/* Colored placeholder while loading */}
      {!isLoaded && !hasError && (
        <div
          className="absolute inset-0 animate-pulse"
          style={{
            background: `linear-gradient(135deg, ${color}20 0%, ${color}10 100%)`,
          }}
        />
      )}

      {/* Error fallback */}
      {hasError && (
        <div
          className="absolute inset-0 flex items-center justify-center"
          style={{ backgroundColor: `${color}10` }}
        >
          <span className="text-[10px] text-[#A1A3A8]">⚠</span>
        </div>
      )}

      {/* Image */}
      <Image
        {...props}
        alt={alt}
        placeholder="blur"
        blurDataURL={blurDataURL}
        onLoad={() => setIsLoaded(true)}
        onError={() => setHasError(true)}
        className={`${className ?? ""} transition-opacity duration-500 ${
          isLoaded ? "opacity-100" : "opacity-0"
        }`}
      />
    </div>
  );
}
