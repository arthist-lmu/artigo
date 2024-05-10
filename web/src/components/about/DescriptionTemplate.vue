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
              mdi-trophy-outline
            </v-icon>
          </template>

          <v-list-item-content>
            <span>{{ field }}</span>
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
      text: t('description.texts.preface')
    },
    {
      text: t('description.texts.principle'),
      fields: [
        t('description.texts.scoreValidated', 5),
        t('description.texts.scoreOpponent', 5),
        t('description.texts.scoreFirst', 5)
      ],
    },
    {
      text: t('description.texts.motivation')
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
