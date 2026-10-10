import type { MetadataRoute } from "next";
export const dynamic = "force-static";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "SourcePixcel",
    short_name: "SourcePixcel",
    description:
      "Bilingual (Persian/English) e-commerce store by SourcePixcel",
    start_url: "/fa",
    display: "standalone",
    background_color: "#F5F5F5",
    theme_color: "#EF4056",
    orientation: "portrait",
    lang: "fa",
    dir: "rtl",
    icons: [
      {
        src: "/favicon.svg",
        sizes: "any",
        type: "image/svg+xml",
        purpose: "any",
      },
    ],
  };
}
