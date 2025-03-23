/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../**/templates/**/*.{html,js,jsx,ts,tsx}",
    "./static/css/input.css"],
  theme: {
    extend: {
      colors: {
        primary: {
          300: '#b3b3b3',
          600: '#666666',
          700: '#4d4d4d',
          800: '#333333',
        },
      },
    },
  },
  plugins: [],
}
