"use client";

interface AdminImageProps {
  src: string;
  alt: string;
  size?: number;
  className?: string;
  rounded?: "sm" | "md" | "lg" | "full" | "none";
}

export default function AdminImage({
  src,
  alt,
  size = 48,
  className,
  rounded = "md",
}: AdminImageProps) {
  const roundedClass =
    rounded === "full"
      ? "rounded-full"
      : rounded === "lg"
      ? "rounded-xl"
      : rounded === "sm"
      ? "rounded"
      : rounded === "none"
      ? ""
      : "rounded-lg";

  return (
    <div
      className={`bg-[#F5F5F5] dark:bg-[#2A2A2E] overflow-hidden shrink-0 ${roundedClass} ${className ?? ""}`}
      style={{ width: size, height: size }}
    >
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={src}
        alt={alt}
        width={size}
        height={size}
        className="w-full h-full object-cover"
        loading="lazy"
        onError={(e) => {
          (e.target as HTMLImageElement).src =
            "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%23F5F5F5' width='100' height='100'/%3E%3Ctext x='50' y='55' font-size='30' text-anchor='middle' fill='%23A1A3A8'%3E%F0%9F%93%A6%3C/text%3E%3C/svg%3E";
        }}
      />
    </div>
  );
}