import 'vuetify/styles' 
import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        variables: {

        },
        colors: {
          primary: '#424798',
          'primary-darken-1': '#000',
          secondary: '#cdcdcd',
          accent: '#f7f8fb',
          error: '#e26162',
          surface: '#f7f8fb',
          'surface-light': '#f7f8fb',
          'surface-variant': '#fff',
          background: '#f7f8fb'
        }
      },
      dark: {
        dark: true,
        variables: {

        },
        colors: {
          primary: '#fff',
          'primary-darken-1': '#fff',
          secondary: '#fff',
          surface: '#424798',
          'surface-light': '#424798',
          'surface-variant': '#000',
          background: '#424798'
        }
      }
    }
  }
})
