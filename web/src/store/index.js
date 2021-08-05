import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate';
import modules from './modules';

Vue.use(Vuex);
Vue.config.devtools = true;
export default new Vuex.Store({
  modules,
  plugins: [
    createPersistedState({
      paths: [],
    }),
  ],
});
