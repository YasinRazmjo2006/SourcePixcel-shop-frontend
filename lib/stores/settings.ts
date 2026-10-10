"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export type FontFamily = "auto" | "vazirmatn" | "inter";
export type FontSize = "small" | "medium" | "large";
export type LineHeight = "compact" | "normal" | "relaxed";

interface SettingsState {
  // Appearance
  fontFamily: FontFamily;
  fontSize: FontSize;
  lineHeight: LineHeight;
  reduceMotion: boolean;

  // Notifications
  emailNotifications: boolean;
  pushNotifications: boolean;

  // Behavior
  autoPlayVideos: boolean;
  showPrices: boolean;
}

interface SettingsActions {
  setFontFamily: (value: FontFamily) => void;
  setFontSize: (value: FontSize) => void;
  setLineHeight: (value: LineHeight) => void;
  setReduceMotion: (value: boolean) => void;
  setEmailNotifications: (value: boolean) => void;
  setPushNotifications: (value: boolean) => void;
  setAutoPlayVideos: (value: boolean) => void;
  setShowPrices: (value: boolean) => void;
  reset: () => void;
}

const DEFAULTS: SettingsState = {
  fontFamily: "auto",
  fontSize: "medium",
  lineHeight: "normal",
  reduceMotion: false,
  emailNotifications: true,
  pushNotifications: false,
  autoPlayVideos: false,
  showPrices: true,
};

export const useSettingsStore = create<SettingsState & SettingsActions>()(
  persist(
    (set) => ({
      ...DEFAULTS,
      setFontFamily: (value) => set({ fontFamily: value }),
      setFontSize: (value) => set({ fontSize: value }),
      setLineHeight: (value) => set({ lineHeight: value }),
      setReduceMotion: (value) => set({ reduceMotion: value }),
      setEmailNotifications: (value) => set({ emailNotifications: value }),
      setPushNotifications: (value) => set({ pushNotifications: value }),
      setAutoPlayVideos: (value) => set({ autoPlayVideos: value }),
      setShowPrices: (value) => set({ showPrices: value }),
      reset: () => set(DEFAULTS),
    }),
    { name: "sourcepixcel-settings" }
  )
);
