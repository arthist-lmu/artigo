<template>
  <v-card flat>
    <v-img
      v-if="showImage"
      :src="item.path"
      class="bg-grey-lighten-2"
      :max-height="imageHeight"
      contain
    >
      <template #placeholder>
        <v-row
          class="fill-height ma-0"
          justify="center"
          align="center"
        >
          <v-progress-circular indeterminate />
        </v-row>
      </template>
    </v-img>

    <v-card-item>
      <v-card-title>
        <span class="text-h5">
          {{ title }}
        </span>

        <ReconcileButton
          :items="[item]"
          type="resource"
          class="ml-1"
        />
      </v-card-title>

      <v-card-subtitle>
        <span
          v-for="creator in creators"
          :key="creator"
          class="text-h6"
        >
          {{ creator }}

          <v-btn
            class="ml-1"
            variant="plain"
            density="comfortable"
            icon="mdi-magnify"
            size="small"
            @click="search(creator, 'creators')"
            @keydown="search(creator, 'creators')"
          />

          <ReconcileButton
            :items="[item]"
            field="creator"
          />
        </span>
      </v-card-subtitle>
    </v-card-item>

    <v-card-text class="pb-6">
      <div
        v-if="filteredTags.length"
        class="mb-8"
      >
        <v-chip
          v-for="tag in filteredTags"
          :key="tag.id"
          :title="tag.name"
          class="mr-1 mb-1"
          color="primary"
          variant="flat"
          @click="search(tag.name, 'tags')"
        >
          {{ tag.name }}

          <v-avatar
            v-if="tag.count > 1"
            :title="$t('resource.metadata.fields.hasTag', { tag: tag.name, n: tag.count })"
            color="primary"
            class="ml-1 mr-n2"
          >
            {{ tag.count }}
          </v-avatar>
        </v-chip>

        <v-btn
          v-if="showAllTags"
          class="mb-1"
          variant="plain"
          density="comfortable"
          icon="mdi-tag-minus"
          size="small"
          @click="showAllTags = false;"
        />
        <v-btn
          v-else
          class="mb-1"
          variant="plain"
          density="comfortable"
          icon="mdi-tag-plus"
          size="small"
          @click="showAllTags = true;"
        />
      </div>

      <v-expansion-panels
        v-if="Object.keys(metadata).length"
        v-model="panels"
        variant="accordion"
        theme="dark"
        multiple
        flat
      >
        <v-expansion-panel>
          <v-expansion-panel-title>
            <v-icon
              class="mr-2"
              size="small"
            >
              mdi-information-outline
            </v-icon>

            <span class="text-subtitle-1">
              {{ $t("resource.metadata.title") }}
            </span>
          </v-expansion-panel-title>

          <v-expansion-panel-text>
            <v-row
              v-for="(value, field) in metadata"
              :key="`${field}:${value}`"
              no-gutters
            >
              <v-col cols="4">
                <span class="capitalize">
                  {{ $t(`resource.metadata.fields.${field}`) }}
                </span>
              </v-col>

              <v-col cols="8">
                <v-chip
                  :title="value"
                  class="ml-1 mb-1"
                  border="secondary md opacity-100"
                  color="primary-darken-1"
                  variant="outlined"
                  theme="light"
                  @click="search(value, field)"
                >
                  <span class="clip">{{ value }}</span>
                </v-chip>
              </v-col>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import useResource from '@/composables/useResource'
import ReconcileButton from '@/components/ReconcileButton.vue'

const store = useStore()

const props = defineProps({
  item: {
    type: Object,
    default: null
  },
  showImage: {
    type: Boolean,
    default: true
  }
})

const {
  title,
  creators,
  orderedTags,
  metadata
} = useResource(props.item)

const panels = ref([0])

const filteredTags = ref([])
const showAllTags = ref(false)
watch(showAllTags, (value) => {
  filteredTags.value = value ? orderedTags.value : orderedTags.value.slice(0, 15)
}, { immediate: true })

const imageHeight = ref(500)
window.addEventListener('resize', setImageHeight)
function setImageHeight() {
  imageHeight.value = window.innerHeight / 3
}
onMounted(() => setImageHeight())
onBeforeUnmount(() => window.removeEventListener('resize', setImageHeight))

const emit = defineEmits(['close'])
function search(value, field) {
  const query = { [field]: value }
  store.dispatch('search/post', { query })
  emit('close')
}
</script>
