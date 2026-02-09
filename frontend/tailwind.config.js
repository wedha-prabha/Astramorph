/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            colors: {
                medical: {
                    primary: '#0f766e', // Teal-700
                    secondary: '#e0f2fe', // Sky-100
                    accent: '#ef4444', // Red-500
                    bg: '#f8fafc', // Slate-50
                    surface: '#ffffff',
                    text: '#1e293b', // Slate-800
                    muted: '#64748b', // Slate-500
                }
            }
        },
    },
    plugins: [],
}
