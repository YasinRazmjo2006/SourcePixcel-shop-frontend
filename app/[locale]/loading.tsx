import { ProductCardSkeleton, Skeleton } from "@/components/common";

export default function Loading() {
  return (
    <div className="max-w-[1400px] mx-auto px-4 py-4 space-y-4">
      <Skeleton variant="rect" className="w-full h-[200px] md:h-[300px]" />
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <ProductCardSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}
