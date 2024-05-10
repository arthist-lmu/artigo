import { nextTick } from 'vue'
import { createRouter, createWebHistory, RouterView } from 'vue-router'
import i18n from '@/plugins/i18n'
import store from '@/store'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import AccountLayout from '@/layouts/AccountLayout.vue'

const { locale: currentLocale } = i18n.global

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: `/${currentLocale.value}`
    },
    {
      path: '/:locale',
      component: RouterView,
      beforeEnter(to, from, next) {
        const { locale } = to.params
        if (!['en', 'de'].includes(locale)) {
          return next('en')
        }
        if (currentLocale.value !== locale) {
          currentLocale.value = locale
        }
        return next()
      },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
          meta: {
            layout: DefaultLayout,
            darkMode: true
          }
        },
        {
          path: 'imprint',
          name: 'imprint',
          beforeEnter: () => {
            window.open('https://www.kunstgeschichte.uni-muenchen.de/funktionen/impressum', '_blank')
            return false
          }
        },
        {
          path: 'institute',
          name: 'institute',
          beforeEnter: () => {
            window.open('https://www.kunstgeschichte.uni-muenchen.de/', '_blank')
            return false
          }
        },
        {
          path: 'privacy-policy',
          name: 'privacyPolicy',
          beforeEnter: () => {
            window.open('https://www.kunstgeschichte.uni-muenchen.de/funktionen/datenschutz', '_blank')
            return false
          }
        },
        {
          path: 'about',
          name: 'about',
          component: () => import('@/views/AboutView.vue'),
          meta: {
            title: 'about.title',
            layout: DefaultLayout,
            darkMode: true
          }
        },
        {
          path: 'search',
          name: 'search',
          component: () => import('@/views/SearchView.vue'),
          meta: {
            title: 'search.title',
            layout: DefaultLayout,
            hideSearchBar: true
          }
        },
        {
          path: 'collections',
          name: 'collections',
          component: () => import('@/views/CollectionsView.vue'),
          meta: {
            title: 'collections.title',
            layout: DefaultLayout
          }
        },
        {
          path: 'sessions',
          name: 'sessions',
          component: () => import('@/views/SessionsView.vue'),
          meta: {
            title: 'sessions.title',
            layout: DefaultLayout
          }
        },
        {
          path: 'game/:id/',
          name: 'session',
          component: () => import('@/views/SessionView.vue'),
          meta: {
            title: 'game.title',
            layout: DefaultLayout,
            opaque: true
          }
        },
        {
          path: 'game',
          name: 'game',
          component: () => import('@/views/GameView.vue'),
          meta: {
            title: 'game.title',
            layout: DefaultLayout,
            opaque: true
          }
        },
        {
          path: 'login',
          name: 'login',
          component: () => import('@/views/LoginView.vue'),
          meta: {
            title: 'user.login.title',
            layout: AccountLayout,
            darkMode: true
          }
        },
        {
          path: 'register',
          name: 'register',
          component: () => import('@/views/RegisterView.vue'),
          meta: {
            title: 'user.register.title',
            layout: AccountLayout,
            darkMode: true
          }
        },
        {
          path: 'password/reset/confirm/:uid/:token/',
          name: 'password-reset-confirm',
          component: () => import('@/views/PasswordResetConfirmView.vue'),
          meta: {
            title: 'user.passwordReset.title',
            layout: AccountLayout,
            darkMode: true
          }
        },
        {
          path: ':pathMatch(.*)',
          name: 'notFound',
          component: () => import('@/views/NotFoundView.vue'),
          meta: {
            title: 'notFound.title',
            layout: DefaultLayout
          }
        }
      ]
    }
  ]
})

router.beforeResolve((to, from, next) => {
  if (to.name) {
    const status = { loading: true, error: false }
    store.dispatch('utils/setStatus', status, { root: true })
  }
  next()
})

router.afterEach((to) => {
  nextTick(() => {
    let title = 'ARTigo – Social Image Tagging'
    if (Object.keys(to.meta).length && to.meta.title) {
      title = `${i18n.global.t(to.meta.title)} | ${title}`
    }
    document.title = title
    const status = { loading: false, error: false }
    store.dispatch('utils/setStatus', status, { root: true })
  })
})

export default router
