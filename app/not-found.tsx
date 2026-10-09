import Link from "next/link";
import { Home, ArrowLeft } from "lucide-react";

export default function GlobalNotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 text-center bg-[#F5F5F5]">
      <h1 className="text-[100px] font-bold text-[#EF4056] leading-none mb-4">
        404
      </h1>
      <h2 className="text-[22px] font-bold text-[#3F4064] mb-3">
        Page not found
      </h2>
      <p className="text-[13px] text-[#62666D] mb-8 max-w-md">
        The page you are looking for was not found.
      </p>
      <Link
        href="/fa"
        className="h-11 px-6 rounded-lg bg-[#EF4056] text-white text-[13px] font-bold hover:bg-[#d63850] inline-flex items-center gap-2"
      >
        <Home size={16} />
        Back to Home
      </Link>
    </div>
  );
}
