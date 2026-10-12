"use client";

import { create } from "zustand";
import type { AdminActivity } from "@/lib/types";

interface LiveActivityState {
  activities: AdminActivity[];
  onlineUsers: number;
  isConnected: boolean;
  addActivity: (activity: AdminActivity) => void;
  setOnlineUsers: (count: number) => void;
  setConnected: (connected: boolean) => void;
  clear: () => void;
}

export const useLiveActivityStore = create<LiveActivityState>((set) => ({
  activities: [],
  onlineUsers: 0,
  isConnected: false,

  addActivity: (activity) =>
    set((state) => ({
      activities: [activity, ...state.activities].slice(0, 50),
    })),

  setOnlineUsers: (count) => set({ onlineUsers: count }),
  setConnected: (connected) => set({ isConnected: connected }),
  clear: () => set({ activities: [] }),
}));
