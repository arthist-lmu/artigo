<template>
  <v-menu>
    <template #activator="{ props: activatorProps }">
      <v-list-item v-bind="activatorProps">
        <v-list-item-title>
          {{ $t("language.title") }}
        </v-list-item-title>

        <template #append>
          <v-icon>
            mdi-chevron-right
          </v-icon>
        </template>
      </v-list-item>
    </template>

    <v-list density="compact">
      <v-list-item
        v-for="locale in locales"
        :key="locale"
        @click="changeLocale(locale)"
      >
        <template #prepend>
          <v-icon v-if="locale === currentLocale">
            mdi-check
          </v-icon>
          <v-icon v-else />
        </template>

        <v-list-item-title>
          {{ $t(`language.fields.${locale}`) }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import i18n from '@/plugins/i18n'

const route = useRoute()
const router = useRouter()
const { locale: currentLocale } = i18n.global

const locales = [
  'en',
  'de'
]

function changeLocale(locale) {
  currentLocale.value = locale
  router.replace({
    name: route.name,
    params: {
      ...route.params,
      locale
    }
  })
}
</script>
