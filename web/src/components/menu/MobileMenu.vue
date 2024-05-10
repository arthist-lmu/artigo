<template>
  <v-menu
    min-width="225"
    max-width="225"
    offset-y
    bottom
  >
    <template #activator="{ props: activatorProps }">
      <v-btn
        v-bind="activatorProps"
        class="ml-2"
        :color="theme.global.name.value === 'dark' ? 'accent' : 'primary'"
        icon="mdi-menu"
      />
    </template>

    <v-list density="comfortable">
      <v-list-item @click="goTo('search')">
        <v-list-item-content>
          {{ $t("search.title") }}
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup>
import { useTheme } from 'vuetify'
import goTo from '@/composables/useGoTo'

const theme = useTheme()
</script>
