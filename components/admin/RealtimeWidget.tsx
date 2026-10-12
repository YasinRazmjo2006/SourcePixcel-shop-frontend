"use client";

import type { Locale } from "@/lib/types";
import { useRealtime } from "@/lib/hooks";
import { OnlineUsersCard, LiveActivityFeed, LiveOrdersCard } from "./realtime";

interface RealtimeWidgetProps {
  locale: Locale;
  enabled?: boolean;
}

export default function RealtimeWidget({
  locale,
  enabled = true,
}: RealtimeWidgetProps) {
  useRealtime(enabled);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="lg:col-span-1 space-y-4">
        <OnlineUsersCard locale={locale} />
      </div>
      <div className="lg:col-span-2">
        <LiveActivityFeed locale={locale} />
      </div>
    </div>
  );
}
