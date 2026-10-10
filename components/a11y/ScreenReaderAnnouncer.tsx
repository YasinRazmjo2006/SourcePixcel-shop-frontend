"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";

/**
 * ScreenReaderAnnouncer — announces page changes to screen readers.
 * Improves SPA navigation accessibility.
 */
export default function ScreenReaderAnnouncer() {
  const pathname = usePathname();
  const [announcement, setAnnouncement] = useState("");

  useEffect(() => {
    // Extract page name from pathname
    const segments = pathname.split("/").filter(Boolean);
    const page = segments[segments.length - 1] ?? "home";
    setAnnouncement(`Navigated to ${page}`);
  }, [pathname]);

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  );
}
