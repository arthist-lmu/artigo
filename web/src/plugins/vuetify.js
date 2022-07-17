import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import 'vuetify/dist/vuetify.min.css';
import '@mdi/font/css/materialdesignicons.css';

Vue.use(Vuetify);

export default new Vuetify({
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
