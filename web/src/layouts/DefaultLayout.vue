<template>
  <v-app :theme="darkMode ? 'dark' : 'light'">
    <v-layout>
      <NavigationDrawer v-if="darkMode" />

      <HeaderBar
        :opaque="opaque"
        :hide-search-bar="hideSearchBar"
        @mounted="mounted = true;"
      />

      <v-main
        v-if="mounted"
        style="height: 100vh; overflow-y: auto;"
      >
        <slot />
      </v-main>

      <FooterBar :opaque="opaque" />
    </v-layout>

    <LoaderTemplate />
    <ToasterBar />

    <ResourceDialog />
    <ReconcileDialog />
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import HeaderBar from '@/components/HeaderBar.vue'
import FooterBar from '@/components/FooterBar.vue'
import ToasterBar from '@/components/ToasterBar.vue'
import LoaderTemplate from '@/components/LoaderTemplate.vue'
import ResourceDialog from '@/components/ResourceDialog.vue'
import ReconcileDialog from '@/components/ReconcileDialog.vue'
import NavigationDrawer from '@/components/game/NavigationDrawer.vue'

defineProps({
  opaque: {
    type: Boolean,
    default: false
  },
  darkMode: {
    type: Boolean,
    default: false
  },
  hideSearchBar: {
    type: Boolean,
    default: false
  }
})

const mounted = ref(false)
</script>
