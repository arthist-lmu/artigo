import Vue from 'vue';
import VueRouter from 'vue-router';
import i18n from '@/plugins/i18n';
import Home from '@/views/Home.vue';
import Resource from '@/views/Resource.vue';
import Collection from '@/views/Collection.vue';
import NotFound from '@/views/NotFound.vue';
import RouterView from '@/views/RouterView.vue';

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
        { path: '', name: 'Home', component: Home },
        {
          path: 'resource/:id/',
          name: 'Resource',
          component: Resource,
        },
        {
          path: 'collection/:name/',
          name: 'Collection',
          component: Collection,
        },
      ],
    },
    { path: '*', name: 'NotFound', component: NotFound },
  ],
});
export default router;
