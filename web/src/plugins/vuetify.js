import { createVuetify } from 'vuetify';
import '@mdi/font/css/materialdesignicons.css';

export default createVuetify({
  theme: {
    themes: {
      light: {
        primary: '#424798',
        secondary: '#cdcdcd',
        accent: '#f7f8fb',
        error: '#e26162',
      },
    },
  },
});
