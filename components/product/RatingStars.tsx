import { Star } from "lucide-react";

interface RatingStarsProps {
  rating: number;
  size?: number;
  showValue?: boolean;
}

export default function RatingStars({
  rating,
  size = 12,
  showValue = false,
}: RatingStarsProps) {
  const full = Math.floor(rating);
  const hasHalf = rating - full >= 0.5;
  const empty = 5 - full - (hasHalf ? 1 : 0);

  return (
    <div className="flex items-center gap-1">
      <div className="flex items-center gap-[1px]">
        {Array.from({ length: full }).map((_, i) => (
          <Star
            key={`full-${i}`}
            size={size}
            className="fill-[#F9A825] text-[#F9A825]"
          />
        ))}
        {hasHalf && (
          <div className="relative" style={{ width: size, height: size }}>
            <Star size={size} className="text-[#E0E0E2] absolute inset-0" />
            <div
              className="absolute inset-0 overflow-hidden"
              style={{ width: size / 2 }}
            >
              <Star
                size={size}
                className="fill-[#F9A825] text-[#F9A825]"
              />
            </div>
          </div>
        )}
        {Array.from({ length: empty }).map((_, i) => (
          <Star key={`empty-${i}`} size={size} className="text-[#E0E0E2]" />
        ))}
      </div>
      {showValue && (
        <span className="text-[11px] text-[#A1A3A8] mr-1">
          {rating.toFixed(1)}
        </span>
      )}
    </div>
  );
}
