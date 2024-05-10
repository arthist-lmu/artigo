<template>
  <component
    :is="layout"
    v-if="token"
    :opaque="opaque"
    :dark-mode="darkMode"
    :hide-search-bar="hideSearchBar"
  >
    <RouterView />
  </component>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import isArray from '@/composables/useIsArray'

const route = useRoute()
const store = useStore()
const { locale } = i18n.global

const layout = computed(() => route.meta.layout || 'div')
const darkMode = computed(() => route.meta.darkMode)
const opaque = computed(() => route.meta.opaque)
const hideSearchBar = computed(() => route.meta.hideSearchBar)

function registerAnonymous() {
  const params = { is_anonymous: true }
  store.dispatch('user/register', params)
}

const token = computed(() => store.state.user.token)
watch(token, (value) => {
  if (value) {
    store.dispatch('user/get')
  } else {
    registerAnonymous()
  }
}, { immediate: true })

const isInvalidToken = computed(() => {
  const { details } = store.state.utils.message
  if (isArray(details)) {
    return details.includes('invalid_token')
  }
  return false
})
watch(isInvalidToken, (value) => {
  if (value) {
    registerAnonymous()
  }
})

watch(locale, (value) => {
  document.documentElement.lang = value
})
document.documentElement.lang = locale.value
</script>
