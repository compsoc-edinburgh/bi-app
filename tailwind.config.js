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
  variants: {
    width: ["responsive", "hover", "focus", "group-hover"],
    height: ["responsive", "hover", "focus", "group-hover"],
    scale: ["responsive", "hover", "focus", "active", "group-hover"],
    textColor: ["responsive", "hover", "focus", "group-hover"],
    fontWeight: ["responsive", "hover", "focus", "group-focus", "active"],
    backgroundColor: ["responsive", "hover", "focus", "checked"]
  },
  plugins: [require("@tailwindcss/typography")]
};
