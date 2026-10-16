"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    router.replace("/fa/");
  }, [router]);

  return <main><Link href="/fa/">ورود به فروشگاه</Link></main>;
}
