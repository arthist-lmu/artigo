<template>
  <v-navigation-drawer
    style="height: 100vh; overflow-y: auto;"
    :permanent="mdAndUp"
    :width="width"
    theme="light"
    order="0"
    floating
  >
    <v-container class="px-6">
      <v-row class="ma-0" />

      <v-row
        v-for="entry in homeData"
        :key="entry.path"
        style="flex: 0;"
      >
        <v-col>
          <NavigationDrawerCard :entry="entry" />
        </v-col>
      </v-row>

      <v-row class="ma-0" />
    </v-container>
  </v-navigation-drawer>
</template>

<script setup>
import { computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import { useDisplay } from 'vuetify'
import NavigationDrawerCard from './NavigationDrawerCard.vue'

const route = useRoute()
const store = useStore()
const { locale } = i18n.global
const { mdAndUp } = useDisplay()

function get(name = null) {
  store.dispatch('statistics/get').then(() => {
    const params = { lang: locale.value, name }
    store.dispatch('home/get', params)
  })
}

const homeData = computed(() => store.state.home.data)
const width = computed(() => mdAndUp ? 350 : 300)

watch(route.query.collection, (name) => {
  get(name)
})

onMounted(() => get(route.query.collection))
</script>

<style scoped>
.container {
  flex-direction: column;
  display: flex;
  height: 100%;
}

.row:nth-last-child(2) {
  padding-bottom: 12px;
}

.row:first-child + .row {
  margin-top: 0;
}
</style>
