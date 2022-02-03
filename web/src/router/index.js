import Vue from 'vue';
import VueRouter from 'vue-router';
import i18n from '@/plugins/i18n';
import store from '@/store';
import RouterView from '@/views/RouterView.vue';

const InstituteUrl = 'https://www.kunstgeschichte.uni-muenchen.de';

Vue.use(VueRouter);
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/:lang',
      component: RouterView,
      beforeEnter(to, from, next) {
        const { lang } = to.params;
        if (!['en', 'de'].includes(lang)) {
          return next('en');
        }
        if (i18n.locale !== lang) {
          i18n.locale = lang;
        }
        return next();
      },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/Home.vue'),
        },
        {
          path: 'resource/:id/',
          name: 'resource',
          component: () => import('@/views/Resource.vue'),
        },
        {
          path: 'collection/:name/',
          name: 'collection',
          component: () => import('@/views/Collection.vue'),
        },
        {
          path: 'imprint',
          name: 'imprint',
          beforeEnter() {
            window.open(`${InstituteUrl}/funktionen/impressum/index.html`, '_blank');
          },
          component: () => import('@/views/Imprint.vue'),
        },
        {
          path: 'privacy-policy',
          name: 'privacy-policy',
          beforeEnter() {
            window.open(`${InstituteUrl}/funktionen/datenschutz/index.html`, '_blank');
          },
          component: () => import('@/views/PrivacyPolicy.vue'),
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('@/views/Register.vue'),
          meta: { title: 'register.title' },
        },
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/Login.vue'),
          meta: { title: 'login.title' },
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/About.vue'),
          meta: { title: 'about.title' },
        },
        {
          path: 'highscore',
          name: 'highscore',
          component: () => import('@/views/Highscore.vue'),
          meta: { title: 'highscore.title' },
        },
        {
          path: 'search',
          name: 'search',
          component: () => import('@/views/Search.vue'),
          meta: { title: 'search.title' },
        },
        {
          path: 'game',
          name: 'game',
          component: () => import('@/views/Game.vue'),
          meta: { title: 'game.title' },
        },
      ],
    },
    {
      path: '*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
    },
  ],
});

const routerPush = VueRouter.prototype.push;
VueRouter.prototype.push = function push(location) {
  return new Promise((resolve, reject) => {
    routerPush.call(this, location, () => {
      resolve(this.currentRoute);
    }, (error) => {
      if (error.name === 'NavigationDuplicated') {
        resolve(this.currentRoute);
      } else {
        reject(error);
      }
    });
  });
};

router.beforeResolve((to, from, next) => {
  if (to.name) {
    const status = { loading: true, error: false };
    store.dispatch('utils/setStatus', status, { root: true });
  }
  next();
});

router.afterEach((to) => {
  Vue.nextTick(() => {
    let title = 'ARTigo – Social Image Tagging';
    if (to.meta) {
      title = `${i18n.t(to.meta.title)} | ${title}`;
    }
    document.title = title;
    const status = { loading: false, error: false };
    store.dispatch('utils/setStatus', status, { root: true });
  });
});
export default router;
