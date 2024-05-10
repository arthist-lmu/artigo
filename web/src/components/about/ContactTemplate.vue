<template>
  <div>
    <span
      v-for="(item, i) in items"
      :key="i"
    >
      <a
        :href="item.url"
        target="_blank"
        rel="noopener noreferrer"
      >
        <!-- eslint-disable vue/no-v-html -->
        <span
          class="mr-1"
          v-html="item.text"
        />
        <!--eslint-enable-->
      </a>

      <v-icon
        color="accent"
        class="ml-1"
        size="x-small"
      >
        {{ item.icon }}
      </v-icon>
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const items = computed(() => {
  return [
    {
      text: t('contact.texts.cooperate'),
      url: 'https://www.kunstgeschichte.uni-muenchen.de/personen/wiss_ma/schneider/index.html',
      icon: 'mdi-email-outline'
    },
    {
      text: t('contact.texts.press'),
      url: '/assets/press-kit.zip',
      icon: 'mdi-link-variant'
    },
    {
      text: t('contact.texts.bugs'),
      url: 'https://github.com/arthist-lmu/artigo/issues',
      icon: 'mdi-link-variant'
    }
  ]
})
</script>

<style scoped>
div > span::after {
  content: '. ';
}
</style>
