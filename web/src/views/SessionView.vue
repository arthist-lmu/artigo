<template>
  <v-container :class="{ 'px-0': mdAndDown }">
    <v-row class="mt-2 mx-n3">
      <v-col :cols="smAndDown ? 12 : 4">
        <SummaryCard
          icon="mdi-image-outline"
          :title="$t('session.fields.images')"
          :value="entries.length"
        />
      </v-col>

      <v-col
        :cols="smAndDown ? 12 : 4"
        :class="smAndDown ? 'pt-0' : undefined"
      >
        <SummaryCard
          icon="mdi-tag-outline"
          :title="$t('session.fields.tags')"
          :subtitle="$t('session.fields.perImage')"
          :value="tags.length"
          :subvalue="tags.length / entries.length"
        />
      </v-col>

      <v-col
        :cols="smAndDown ? 12 : 4"
        :class="smAndDown ? 'pt-0' : undefined"
      >
        <SummaryCard
          icon="mdi-star-outline"
          :title="$t('session.fields.score')"
          :subtitle="$t('session.fields.perImage')"
          :value="score"
          :subvalue="score / entries.length"
        />
      </v-col>
    </v-row>

    <v-row
      v-if="tags.length"
      class="aggregate pb-0"
    >
      <v-col>
        <v-slide-group
          v-model="slides"
          :title="$t('session.fields.filterTags')"
          center-active
          show-arrows
          multiple
        >
          <v-slide-group-item
            v-for="tagName in uniqueTagNames"
            :key="tagName"
            v-slot="{ isSelected, toggle }"
          >
            <v-chip
              class="mx-1"
              :border="isSelected ? 'primary md opacity-100' : 'secondary md opacity-100'"
              :color="isSelected ? 'primary' : 'secondary'"
              variant="outlined"
              rounded
              @click="toggle"
            >
              <span :class="isSelected ? 'text-primary' : 'text-primary-darken-1'">
                {{ tagName }}
              </span>
            </v-chip>
          </v-slide-group-item>
        </v-slide-group>
      </v-col>

      <v-col
        :cols="auto"
        align="right"
      >
        <v-dialog max-width="450">
          <template #activator="{ props: activatorProps }">
            <v-btn
              v-bind="activatorProps"
              :title="$t('user.score.title')"
              variant="text"
              density="comfortable"
              icon="mdi-trophy-outline"
            />
          </template>

          <template #default="{ isActive }">
            <ScoreCard @close="isActive.value = false" />
          </template>
        </v-dialog>

        <v-btn
          class="ml-2"
          variant="text"
          density="comfortable"
          icon="mdi-share-variant-outline"
          @click="share"
        />
      </v-col>
    </v-row>

    <v-row class="mt-5 mx-n1">
      <v-slide-group
        class="resource"
        show-arrows
      >
        <v-slide-group-item
          v-for="item in entries"
          :key="item.resource_id"
        >
          <div
            class="pa-1"
            style="width: 300px"
          >
            <OverviewResultCard
              :item="item"
              height="350"
              :opaque="!selectedEntries.includes(item.resource_id)"
            />
          </div>
        </v-slide-group-item>
      </v-slide-group>
    </v-row>

    <v-dialog
      v-model="showDialog"
      max-width="400"
    >
      <HelperCard
        :text="$t('user.score.helper')"
        icon="mdi-account-circle-outline"
        @close="showDialog = false;"
      >
        <template #button>
          <v-dialog max-width="450">
            <template #activator="{ props: activatorProps }">
              <v-btn
                v-bind="activatorProps"
                tabindex="0"
                class="bg-primary"
                rounded
                block
              >
                {{ $t("user.score.title") }}
              </v-btn>
            </template>

            <template #default="{ isActive }">
              <ScoreCard @close="isActive.value = false" />
            </template>
          </v-dialog>
        </template>
      </HelperCard>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import HelperCard from '@/components/HelperCard.vue'
import ScoreCard from '@/components/account/ScoreCard.vue'
import SummaryCard from '@/components/session/SummaryCard.vue'
import OverviewResultCard from '@/components/session/OverviewResultCard.vue'

const route = useRoute()
const store = useStore()
const { smAndDown, mdAndDown } = useDisplay()

get(route.params.id)
function get(id) {
  store.dispatch('session/get', { id })
}
watch('$route.params.id', (id) => get(id))

function share() {
  const input = document.createElement('input')
  document.body.appendChild(input)
  input.value = window.location.href
  input.select()
  document.execCommand('copy')
  document.body.removeChild(input)
  const message = {
    details: ['copied_to_clipboard'],
    timestamp: new Date()
  };
  store.dispatch('utils/setMessage', message)
}

const entries = computed(() => store.state.session.data || [])
const selectedEntries = computed(() => {
  let values = entries.value
  if (selectedTagNames.value.length) {
    values = values.filter((item) => {
      if (item.tags) {
        return item.tags.map(({ name }) => name).some((name) => selectedTagNames.value.includes(name))
      }
      return false
    })
  }
  return values.map(({ resource_id }) => resource_id)
})

const slides = ref([])
const tags = computed(() => {
  return entries.value.map(({ tags }) => tags).flat()
})
const uniqueTagNames = computed(() => {
  return [...new Set(tags.value.map(({ name }) => name))]
})
const selectedTagNames = computed(() => {
  return slides.value.map((i) => uniqueTagNames.value[i])
})
const score = computed(() => {
  const tagScores = tags.value.map(({ score }) => score)
  return tagScores.reduce((x, y) => x + y, 0)
})

const showDialog = ref(false)
if (localStorage.getItem('scoreHelper') === null) {
  localStorage.setItem('scoreHelper', true)
  showDialog.value = true
}
</script>
