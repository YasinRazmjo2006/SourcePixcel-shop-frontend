import Skeleton from "./Skeleton";

export default function ProductCardSkeleton() {
  return (
    <div className="bg-white dark:bg-[#1A1A1E] rounded-lg border border-[#E0E0E2] dark:border-[#2A2A2E] p-3">
      <Skeleton variant="rect" className="w-full aspect-square mb-3" />
      <Skeleton variant="text" className="w-full h-4 mb-2" />
      <Skeleton variant="text" className="w-2/3 h-4 mb-3" />
      <Skeleton variant="text" className="w-1/2 h-3" />
    </div>
  );
}
