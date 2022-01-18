import Vue from 'vue';
import VueRouter from 'vue-router';
import i18n from '@/plugins/i18n';
import RouterView from '@/views/RouterView.vue';

import Home from '@/views/Home.vue';
import Resource from '@/views/Resource.vue';
import Collection from '@/views/Collection.vue';

import Imprint from '@/views/Imprint.vue';
import PrivacyPolicy from '@/views/PrivacyPolicy.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';

import About from '@/views/About.vue';
import Highscore from '@/views/Highscore.vue';
import Search from '@/views/Search.vue';
import Game from '@/views/Game.vue';

import NotFound from '@/views/NotFound.vue';

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
          component: Home,
        },
        {
          path: 'resource/:id/',
          name: 'resource',
          component: Resource,
        },
        {
          path: 'collection/:name/',
          name: 'collection',
          component: Collection,
        },
        {
          path: 'imprint',
          name: 'imprint',
          component: Imprint,
          meta: { title: 'imprint.title' },
        },
        {
          path: 'privacy-policy',
          name: 'privacy-policy',
          component: PrivacyPolicy,
          meta: { title: 'privacy-policy.title' },
        },
        {
          path: 'register',
          name: 'register',
          component: Register,
          meta: { title: 'register.title' },
        },
        {
          path: 'login',
          name: 'login',
          component: Login,
          meta: { title: 'login.title' },
        },
        {
          path: 'about',
          name: 'about',
          component: About,
          meta: { title: 'about.title' },
        },
        {
          path: 'highscore',
          name: 'highscore',
          component: Highscore,
          meta: { title: 'highscore.title' },
        },
        {
          path: 'search',
          name: 'search',
          component: Search,
          meta: { title: 'search.title' },
        },
        {
          path: 'game',
          name: 'game',
          component: Game,
          meta: { title: 'game.title' },
        },
      ],
    },
    {
      path: '*',
      name: 'not-found',
      component: NotFound,
      meta: { title: 'Not Found' },
    },
  ],
});

router.afterEach((to) => {
  Vue.nextTick(() => {
    let title = 'ARTigo – Social Image Tagging';
    if (to.meta) {
      title = `${i18n.t(to.meta.title)} | ${title}`;
    }
    document.title = title;
  });
});
export default router;
