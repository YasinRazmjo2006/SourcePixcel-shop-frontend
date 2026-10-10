interface SkeletonProps {
  className?: string;
  variant?: "text" | "circle" | "rect";
  width?: string | number;
  height?: string | number;
}

export default function Skeleton({
  className = "",
  variant = "rect",
  width,
  height,
}: SkeletonProps) {
  const base =
    "bg-[#E0E0E2] dark:bg-[#2A2A2E] relative overflow-hidden skeleton-shimmer";
  const shape =
    variant === "circle"
      ? "rounded-full"
      : variant === "text"
      ? "rounded"
      : "rounded-lg";

  return (
    <div
      className={`${base} ${shape} ${className}`}
      style={{ width, height }}
    />
  );
}
