import Vue from 'vue';
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import '@mdi/font/css/materialdesignicons.css';

Vue.use(Vuetify);
export default new Vuetify({
    theme: {
        themes: {
          light: {
            primary: '#b7c8e0',
            secondary: '#cdcdcd',
            accent: '#2056ae',
            error: '#ab91a1',
          },
        },
      },
});
