import { createStore } from 'vuex'
import Cookies from 'js-cookie'
import createPersistedState from 'vuex-persistedstate'
import modules from '@/store/modules'

export default createStore({
  modules,
  plugins: [
    createPersistedState({
      paths: [
        'user.token',
        'settings.display',
      ],
      storage: {
        getItem: (key) => Cookies.get(key),
        setItem: (key, value) => {
          Cookies.set(key, value, {
            expires: 3,
            secure: false
          })
        },
        removeItem: (key) => Cookies.remove(key)
      }
    })
  ]
})
