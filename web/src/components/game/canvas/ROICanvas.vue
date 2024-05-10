<template>
  <DefaultCanvas
    :tool="tool"
    :entry="entry"
    @update="onUpdate"
  >
    <template #prepend-item>
      <v-row
        class="absolute mx-0 my-3"
        justify="center"
      >
        <v-col cols="auto">
          <v-slide-group
            v-model="tagIndex"
            mandatory
          >
            <v-slide-group-item
              v-for="tag in tags"
              :key="tag.name"
              v-slot="{ isSelected, toggle }"
            >
              <v-chip
                :color="isSelected ? 'primary' : 'surface'"
                class="mx-1"
                variant="flat"
                @click="toggle"
              >
                {{ tag.name }}
              </v-chip>
            </v-slide-group-item>
          </v-slide-group>
        </v-col>
      </v-row>
    </template>
  </DefaultCanvas>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import DefaultCanvas from '@/components/game/canvas/DefaultCanvas.vue'

const store = useStore()
const { locale } = i18n.global

const props = defineProps({
  tool: {
    type: String,
    default: 'brush'
  },
  entry: {
    type: Object,
    default: null
  }
})

const tags = computed(() => props.entry.input_tags)
const emit = defineEmits(['error'])
watch(tags, (value) => {
  if (value.length === 0) {
    emit('error')
  }
})

const tagIndex = ref(0)
function onUpdate(values) {
  const params = {
    tag: {
      name: tags.value[tagIndex.value].name,
      ...values
    },
    language: locale.value,
    resource_id: props.entry.resource_id
  }
  store.dispatch('game/post', params)
}

function onKeyDown({ key }) {
  if (['ArrowLeft', 'a'].includes(key)) {
    if (tagIndex.value == 0) {
      tagIndex.value = tags.value.length - 1
    } else {
      tagIndex.value -= 1
    }
  }
  if (['ArrowRight', 'd'].includes(key)) {
    if (tagIndex.value + 1 == tags.value.length) {
      tagIndex.value = 0
    } else {
      tagIndex.value += 1
    }
  }
}
window.addEventListener('keydown', onKeyDown)
onUnmounted(() => window.removeEventListener('keydown', onKeyDown))
</script>

<style scoped>
.v-row.absolute {
  position: absolute;
  width: 100%;
  z-index: 99;
}
</style>
