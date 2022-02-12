import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import 'vuetify/dist/vuetify.min.css';
import '@mdi/font/css/materialdesignicons.css';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#b8c9e1',
        secondary: '#cdcdcd',
        accent: '#b7c8e0',
        error: '#ab91a1',
      },
    },
  },
});
