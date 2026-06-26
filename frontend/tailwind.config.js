/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "#0B0F19",       // Deep trading desk navy/black
        darkCard: "#161E2E",     // Gray-blue premium card background
        darkCardHover: "#202A3E",
        textPrimary: "#F9FAFB",  // Soft white
        textSecondary: "#9CA3AF" // Muted gray
      }
    },
  },
  plugins: [],
}
