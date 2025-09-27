/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",  // scan all React files
  ],
  theme: {
    extend: {
        colors: {
            'primary': '#5060FF',
            'secondary': '#8A94FF'

        },
      fontFamily: {
        poppins: ["Poppins", "sans-serif"], // custom font
      },
      
    },
  },
  plugins: [],
}
