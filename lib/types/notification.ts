// lib/types/notification.ts
export type NotificationType = "order" | "promo" | "system" | "message";

export interface AppNotification {
  id: string;
  type: NotificationType;
  titleFa: string;
  titleEn: string;
  bodyFa: string;
  bodyEn: string;
  dateFa: string;
  dateEn: string;
  read: boolean;
  href?: string;
}
