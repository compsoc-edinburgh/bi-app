const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  theme: {
    extend: {
      borderRadius: {
        xl: "40px",
        card: "20px"
      },
      fontFamily: {
        sans: ["Inter var", ...defaultTheme.fontFamily.sans],
        display: ["fippsregular", ...defaultTheme.fontFamily.sans],
        filled: ["fipps_filledregular", ...defaultTheme.fontFamily.sans],
        mono: ["CascadiaCode", ...defaultTheme.fontFamily.mono]
      },
      colors: {
        primary: "#d3371e"
      }
    }
  },

  plugins: [require("@tailwindcss/typography")]
};
