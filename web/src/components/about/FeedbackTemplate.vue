<template>
  <div>
    <v-carousel
      :show-arrows="false"
      :height="350"
      color="secondary"
      hide-delimiter-background
      cycle
    >
      <v-carousel-item
        v-for="(item, i) in items"
        :key="i"
      >
        <v-sheet height="100%">
          <v-row>
            <v-col>
              <div
                style="line-height: 1.5;"
                class="text-h4"
              >
                {{ item.text }}
              </div>
            </v-col>
          </v-row>

          <v-row class="justify-end">
            <v-col
              align="right"
              cols="6"
            >
              <div class="text-h5">
                {{ item.title }}
              </div>
            </v-col>
          </v-row>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const items = computed(() => {
  return [
    {
      title: t('feedback.texts.example1.name'),
      text: t('feedback.texts.example1.value')
    },
    {
      title: t('feedback.texts.example2.name'),
      text: t('feedback.texts.example2.value')
    },
    {
      title: t('feedback.texts.example3.name'),
      text: t('feedback.texts.example3.value')
    },
    {
      title: t('feedback.texts.example4.name'),
      text: t('feedback.texts.example4.value')
    }
  ]
})
</script>
