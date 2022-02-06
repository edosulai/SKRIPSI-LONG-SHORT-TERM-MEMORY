const defaultTheme = require('tailwindcss/defaultTheme')
const plugin = require('tailwindcss/plugin')

module.exports = {
    // future: {
    //     removeDeprecatedGapUtilities: true,
    //     purgeLayersByDefault: true,
    // },
    mode: 'jit',
    content: [
        '../**/templates/*.html',
        '../**/templates/**/*.html'
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Nunito', ...defaultTheme.fontFamily.sans],
            },
            // backgroundImage: {
            //     'hero-pattern': "url('/static/images/random-shapes.svg')"
            // }
        },
    },

    variants: {},
    plugins: [
        require('@tailwindcss/forms'),
        plugin(function ({ addUtilities }) {
            addUtilities({
                '.text-shadow': {
                    'text-shadow': '0 2px 5px rgba(0, 0, 0, 0.5)'
                }
            }, ['responsive', 'hover'])
        }),
    ],
    darkMode: 'class',
}