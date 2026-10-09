import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#EF4056",
        secondary: "#00BFFF",
        dark: "#3F4064",
        muted: "#62666D",
        light: "#A1A3A8",
        border: "#E0E0E2",
        bg: "#F5F5F5",
      },
      fontFamily: {
        sans: ["system-ui", "-apple-system", "Segoe UI", "Tahoma", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
