"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface SettingsState {
  // Appearance
  reduceMotion: boolean;
  fontSize: "small" | "medium" | "large";
  // Notifications
  emailNotifications: boolean;
  pushNotifications: boolean;
  // Behavior
  autoPlayVideos: boolean;
  showPrices: boolean;
}

interface SettingsActions {
  setReduceMotion: (value: boolean) => void;
  setFontSize: (value: "small" | "medium" | "large") => void;
  setEmailNotifications: (value: boolean) => void;
  setPushNotifications: (value: boolean) => void;
  setAutoPlayVideos: (value: boolean) => void;
  setShowPrices: (value: boolean) => void;
  reset: () => void;
}

const DEFAULTS: SettingsState = {
  reduceMotion: false,
  fontSize: "medium",
  emailNotifications: true,
  pushNotifications: false,
  autoPlayVideos: false,
  showPrices: true,
};

export const useSettingsStore = create<SettingsState & SettingsActions>()(
  persist(
    (set) => ({
      ...DEFAULTS,
      setReduceMotion: (value) => set({ reduceMotion: value }),
      setFontSize: (value) => set({ fontSize: value }),
      setEmailNotifications: (value) => set({ emailNotifications: value }),
      setPushNotifications: (value) => set({ pushNotifications: value }),
      setAutoPlayVideos: (value) => set({ autoPlayVideos: value }),
      setShowPrices: (value) => set({ showPrices: value }),
      reset: () => set(DEFAULTS),
    }),
    { name: "sourcepixcel-settings" }
  )
);
