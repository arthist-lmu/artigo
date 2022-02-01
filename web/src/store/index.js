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
      paths: [
        'settings.display',
      ],
      getState(key, storage) {
        let value = storage.getItem(key);
        try {
          value = JSON.parse(value);
        } catch (error) {
          return undefined;
        }
        if (value && Object.keys(value).length) {
          return value;
        }
        return undefined;
      },
    }),
  ],
});
