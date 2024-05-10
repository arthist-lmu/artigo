<template>
  <div>
    <template
      v-for="(item, i) in items"
      :key="i"
    >
      <!-- eslint-disable vue/no-v-html -->
      <p v-html="item.text" />
      <!--eslint-enable-->

      <v-list
        v-if="item.fields"
        class="my-6"
        density="comfortable"
      >
        <v-list-item
          v-for="(field, j) in item.fields"
          :key="`${i}-${j}`"
          variant="text"
        >
          <template #prepend>
            <v-icon color="error">
              mdi-database-outline
            </v-icon>
          </template>

          <v-list-item-content>
            <!-- eslint-disable vue/no-v-html -->
            <span v-html="field" />
            <!--eslint-enable-->
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const items = computed(() => {
  return [
    {
      text: t('collections.texts.preface')
    },
    {
      text: t('collections.texts.principle')
    },
    {
      text: t('collections.texts.mapping'),
      fields: [
        t('collections.texts.filePath'),
        t('collections.texts.title'),
        t('collections.texts.creator'),
        t('collections.texts.created'),
        t('collections.texts.location'),
        t('collections.texts.source'),
        t('collections.texts.tags')
      ]
    },
    {
      text: t('collections.texts.access')
    }
  ]
})
</script>

<style scoped>
.v-list-item .v-list-item__content span {
  line-height: 24px;
}

.v-list-item .v-list-item__content span::after {
  content: ";";
}

.v-list-item:last-child .v-list-item__content span::after {
  content: ".";
}
</style>
