// frontend/tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      backgroundImage: {
        'library': "url('/bibliotheque.jpg')",
      },
      colors: {
        amber: {
          600: '#d97706',
          700: '#b45309'
        }
      }
    }
  },
  plugins: []
}