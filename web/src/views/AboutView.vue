<template>
  <v-container>
    <v-row>
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("about.fields.summary", { images, taggings, users }) }}
        </div>
      </v-col>
    </v-row>

    <v-row id="description">
      <v-col :class="paddingClass">
        <DescriptionTemplate />
      </v-col>
    </v-row>

    <v-row id="feedback">
      <v-col :class="paddingClass">
        <FeedbackTemplate />
      </v-col>
    </v-row>

    <v-row id="collections">
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("collections.title") }}
        </div>

        <CollectionsTemplate />
      </v-col>
    </v-row>

    <v-row id="contributors">
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("contributors.title") }}
        </div>

        <ContributorsTemplate />
      </v-col>
    </v-row>

    <v-row id="contact">
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("contact.title") }}
        </div>

        <ContactTemplate />
      </v-col>
    </v-row>

    <v-row id="history">
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("history.title") }}
        </div>

        <HistoryTemplate />
      </v-col>
    </v-row>

    <v-row id="publications">
      <v-col :class="paddingClass">
        <div :class="textClass">
          {{ $t("publications.title") }}
        </div>

        <PublicationsTemplate />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'
import i18n from '@/plugins/i18n'
import keyInObj from '@/composables/useKeyInObj'
import ContactTemplate from '@/components/about/ContactTemplate.vue'
import HistoryTemplate from '@/components/about/HistoryTemplate.vue'
import FeedbackTemplate from '@/components/about/FeedbackTemplate.vue'
import DescriptionTemplate from '@/components/about/DescriptionTemplate.vue'
import CollectionsTemplate from '@/components/about/CollectionsTemplate.vue'
import ContributorsTemplate from '@/components/about/ContributorsTemplate.vue'
import PublicationsTemplate from '@/components/about/PublicationsTemplate.vue'

const store = useStore()

const { name, mdAndDown } = useDisplay()
const textClass = computed(() => {
  const values = ['text-accent', 'mb-6'];
  switch (name.value) {
    case 'xs':
      values.push('text-h4')
      break
    case 'sm':
      values.push('text-h3')
      break
    default:
      values.push('text-h2')
      break
  }
  return values
})
const paddingClass = computed(() => {
  if (mdAndDown.value) {
    return ['px-4', 'py-6']
  }
  return ['pa-14']
})

const statisticsData = computed(() => store.state.statistics.data)
const users = computed(() => {
  if (keyInObj('users', statisticsData.value)) {
    const { n } = statisticsData.value.users
    return n.toLocaleString(i18n.global.locale.value)
  }
  return 0
})
const images = computed(() => {
  if (keyInObj('resources', statisticsData.value)) {
    const { n } = statisticsData.value.resources
    return n.toLocaleString(i18n.global.locale.value)
  }
  return 0
})
const taggings = computed(() => {
  if (keyInObj('taggings', statisticsData.value)) {
    const { n } = statisticsData.value.taggings
    return n.toLocaleString(i18n.global.locale.value)
  }
  return 0
})

onMounted(() => {
  // see: @/components/game/NavigationDrawer.vue
  // store.dispatch('statistics/get')
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.text-h2 {
  line-height: 4.75rem;
}

.text-h3 {
  line-height: 3.75rem;
}

.text-h4 {
  line-height: 2.75rem;
}
</style>
