import Vue from 'vue';
import VueRouter from 'vue-router';
import i18n from '@/plugins/i18n';
import store from '@/store';
import RouterView from '@/views/RouterView.vue';
import DefaultLayout from '@/layouts/Default.vue';
import AccountLayout from '@/layouts/Account.vue';

Vue.use(VueRouter);

const instituteUrl = 'https://www.kunstgeschichte.uni-muenchen.de';
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: `/${i18n.locale}`,
    },
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
          meta: {
            layout: DefaultLayout,
            dark: true,
            hideSearchBar: true,
          },
        },
        {
          path: 'imprint',
          name: 'imprint',
          beforeEnter: () => {
            window.open(`${instituteUrl}/funktionen/impressum`, '_blank');
          },
        },
        {
          path: 'privacy-policy',
          name: 'privacy-policy',
          beforeEnter: () => {
            window.open(`${instituteUrl}/funktionen/datenschutz`, '_blank');
          },
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/About.vue'),
          meta: {
            title: 'about.title',
            layout: DefaultLayout,
            dark: true,
            hideSearchBar: true,
          },
        },
        {
          path: 'search',
          name: 'search',
          component: () => import('@/views/Search.vue'),
          meta: {
            title: 'search.title',
            layout: DefaultLayout,
            hideSearchBar: true,
          },
        },
        {
          path: 'sessions',
          name: 'sessions',
          component: () => import('@/views/Sessions.vue'),
          meta: {
            title: 'sessions.title',
            layout: DefaultLayout,
          },
        },
        {
          path: 'game/:id/',
          name: 'session',
          component: () => import('@/views/Session.vue'),
          meta: {
            title: 'game.title',
            layout: DefaultLayout,
            opaque: true,
          },
        },
        {
          path: 'game',
          name: 'game',
          component: () => import('@/views/Game.vue'),
          meta: {
            title: 'game.title',
            layout: DefaultLayout,
            opaque: true,
            hideSearchBar: true,
          },
        },
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/Login.vue'),
          meta: {
            title: 'user.login.title',
            layout: AccountLayout,
            dark: true,
          },
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('@/views/Register.vue'),
          meta: {
            title: 'user.register.title',
            layout: AccountLayout,
            dark: true,
          },
        },
        {
          path: 'password/reset/confirm/:uid/:token/',
          name: 'password-reset-confirm',
          component: () => import('@/views/PasswordResetConfirm.vue'),
          meta: {
            title: 'user.password-reset.title',
            layout: AccountLayout,
            dark: true,
          },
        },
        {
          path: '404',
          name: 'not-found',
          component: () => import('@/views/NotFound.vue'),
          meta: {
            title: 'not-found.title',
            layout: DefaultLayout,
          },
        },
        {
          path: '*',
          name: 'not-found-redirect',
          beforeEnter: (to) => {
            window.location = `/${to.params.lang}/404`;
          },
        },
      ],
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
    if (Object.keys(to.meta).length && to.meta.title) {
      title = `${i18n.t(to.meta.title)} | ${title}`;
    }
    document.title = title;
    const status = { loading: false, error: false };
    store.dispatch('utils/setStatus', status, { root: true });
  });
});

export default router;
