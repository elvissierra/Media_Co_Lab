import { createVuetify } from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#6C757D',
          accent: '#00BCD4',
          success: '#4CAF50',
          warning: '#FF9800',
          error: '#F44336',
          info: '#2196F3',
          surface: '#FFFFFF',
          background: '#F5F5F5',
        },
      },
      dark: {
        colors: {
          primary: '#BB86FC',
          secondary: '#03DAC6',
          accent: '#00BCD4',
          success: '#4CAF50',
          warning: '#FF9800',
          error: '#CF6679',
          info: '#90CAF9',
          surface: '#1E1E1E',
          background: '#121212',
        },
      },
    },
  },
})

export default vuetify