import { createApp } from 'vue'
import App from '@/App.vue'
import i18n from '@/plugins/i18n'
import vuetify from '@/plugins/vuetify'
import router from '@/router'
import store from '@/store'
import VueTouch from 'vue-touch'
import '@/styles/main.css'

createApp(App)
  .use(i18n)
  .use(vuetify)
  .use(router)
  .use(store)
  .use(VueTouch, { name: 'v-touch' })
  .mount('#app')
