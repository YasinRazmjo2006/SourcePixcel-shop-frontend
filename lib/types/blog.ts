// lib/types/blog.ts
export interface BlogPost {
  id: number;
  slug: string;
  titleFa: string;
  titleEn: string;
  excerptFa: string;
  excerptEn: string;
  contentFa: string;
  contentEn: string;
  cover: string;
  categoryFa: string;
  categoryEn: string;
  authorFa: string;
  authorEn: string;
  dateFa: string;
  dateEn: string;
  readTimeFa: string;
  readTimeEn: string;
  tags: string[];
}
