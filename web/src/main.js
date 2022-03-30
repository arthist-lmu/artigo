import Vue from 'vue';
import i18n from '@/plugins/i18n';
import vuetify from '@/plugins/vuetify';
import App from '@/App.vue';
import store from '@/store';
import router from '@/router';
import mixins from '@/mixins';
import '@/styles/custom.css';

Vue.mixin(mixins);
const ARTigo = Vue.extend({
  computed: {
    token() {
      return this.$store.state.user.token;
    },
  },
  watch: {
    token: {
      handler(token) {
        if (token) {
          this.$store.dispatch('user/get');
        } else {
          const params = { is_anonymous: true };
          this.$store.dispatch('user/register', params);
        }
      },
      immediate: true,
    },
  },
});

new ARTigo({
  vuetify,
  router,
  store,
  i18n,
  render: (h) => h(App),
})
  .$mount('#app');
