"use client";

interface DotsLoaderProps {
  color?: string;
  size?: number;
}

export default function DotsLoader({
  color = "#EF4056",
  size = 8,
}: DotsLoaderProps) {
  return (
    <div className="flex items-center gap-1.5" role="status" aria-label="Loading">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="rounded-full animate-bounce"
          style={{
            width: size,
            height: size,
            backgroundColor: color,
            animationDelay: `${i * 0.15}s`,
            animationDuration: "0.6s",
          }}
        />
      ))}
    </div>
  );
}
