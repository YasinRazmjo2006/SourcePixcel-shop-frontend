"use client";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: string;
}

export default function Spinner({
  size = "md",
  color = "#EF4056",
}: SpinnerProps) {
  const sizes = {
    sm: 16,
    md: 24,
    lg: 40,
  };

  const px = sizes[size];

  return (
    <div
      className="relative inline-block"
      style={{ width: px, height: px }}
      role="status"
      aria-label="Loading"
    >
      <div
        className="absolute inset-0 rounded-full border-2 opacity-20"
        style={{ borderColor: color }}
      />
      <div
        className="absolute inset-0 rounded-full border-2 border-transparent animate-spin"
        style={{
          borderTopColor: color,
          animationDuration: "0.7s",
        }}
      />
    </div>
  );
}
