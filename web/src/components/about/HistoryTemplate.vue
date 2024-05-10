<template>
  <div>
    <v-timeline
      :density="smAndDown ? 'comfortable' : 'default'"
      truncate-line="start"
    >
      <v-timeline-item
        v-for="(item, i) in items"
        :key="i"
        icon-color="background"
        :size="item.icon ? undefined : 'small'"
      >
        <template
          v-if="!mdAndDown"
          #opposite
        >
          <v-row :justify="i % 2 !== 0 ? 'start' : 'end'">
            <v-col
              v-if="item.image"
              cols="5"
              :order="i % 2 === 0 ? 1 : 2"
              align-self="center"
            >
              <v-dialog max-width="750">
                <template #activator="{ props: activatorProps }">
                  <v-card
                    class="history-item"
                    flat
                  >
                    <img
                      v-bind="activatorProps"
                      :src="item.image"
                      alt=""
                    >
                  </v-card>
                </template>

                <v-card flat>
                  <v-img
                    :src="item.image"
                    alt=""
                  />
                </v-card>
              </v-dialog>
            </v-col>

            <v-col
              cols="auto"
              :order="i % 2 !== 0 ? 1 : 2"
              align-self="center"
              align="end"
            >
              <span class="font-weight-bold">
                {{ item.year }}
              </span>
            </v-col>
          </v-row>
        </template>

        <div class="py-4">
          <div
            v-if="smAndDown"
            class="mb-4 font-weight-bold"
          >
            {{ item.year }}
          </div>

          <!-- eslint-disable vue/no-v-html -->
          <div
            class="font-weight-light"
            v-html="item.text"
          />
          <!--eslint-enable-->
        </div>
      </v-timeline-item>
    </v-timeline>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useDisplay } from 'vuetify'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const {
  smAndDown,
  mdAndDown
} = useDisplay()

const items = computed(() => {
  return [
    {
      year: '2008–2009',
      text: t('history.texts.prototype'),
      image: '/assets/images/artigo-version-2008.png'
    },
    {
      year: '2010–2013',
      icon: 'mdi-rocket-launch-outline',
      text: t('history.texts.dfg'),
      image: '/assets/images/artigo-version-2010.png'
    },
    {
      year: '2012',
      text: t('history.texts.spiegel')
    },
    {
      year: '2018–2019',
      text: t('history.texts.slb'),
      image: '/assets/images/stadt-land-bild.png'
    },
    {
      year: '2021–2022',
      icon: 'mdi-star-outline',
      text: t('history.texts.relaunch')
    },
    {
      year: '2023',
      text: t('history.texts.provenance')
    },
    {
      year: '2023',
      text: t('history.texts.eu')
    }
  ]
})
</script>

<style scoped>
.history-item {
  position: relative;
  overflow: hidden;
}

.history-item > img {
  transition: all 0.5s ease;
  filter: grayscale(100%);
  transform: scale(1.05);
  object-position: top;
  object-fit: cover;
  cursor: pointer;
  width: 100%;
  min-width: 100%;
  max-width: 100%;
  display: block;
  height: 100%;
}

.history-item:hover > img {
  transform: scale(1.3);
  filter: grayscale(0%);
}
</style>
