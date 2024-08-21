/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html", // Adjust this path based on your project structure
        "./static/js/**/*.js"    // Include any JavaScript files if they contain Tailwind classes
    ], // Add your HTML file here
    theme: {
      extend: {},
    },
    plugins: [require('daisyui')],
  }
  