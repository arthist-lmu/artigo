import Vue from 'vue';
import VueTouch from 'vue-touch';
import i18n from '@/plugins/i18n';
import vuetify from '@/plugins/vuetify';
import App from '@/App.vue';
import store from '@/store';
import router from '@/router';
import mixins from '@/mixins';
import '@/styles/custom.css';

Vue.mixin(mixins);
Vue.use(VueTouch, { name: 'v-touch' });

const ARTigo = Vue.extend({
  methods: {
    registerAnonymous() {
      const params = { is_anonymous: true };
      this.$store.dispatch('user/register', params);
    },
  },
  computed: {
    token() {
      return this.$store.state.user.token;
    },
    invalidToken() {
      const { details } = this.$store.state.utils.message;
      if (this.isArray(details)) {
        return details.includes('invalid_token');
      }
      return false;
    },
  },
  watch: {
    token: {
      handler(token) {
        if (token) {
          this.$store.dispatch('user/get');
        } else {
          this.registerAnonymous();
        }
      },
      immediate: true,
    },
    invalidToken(value) {
      if (value) {
        this.registerAnonymous();
      }
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
