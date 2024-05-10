<template>
  <div class="tag-container">
    <v-chip
      v-for="tag in tagSizes"
      :key="tag.id"
      :title="tag.name"
      :style="{ 'font-size': tag.size + 'px' }"
      class="mr-1 mb-1"
      color="primary"
      variant="flat"
      size="x-small"
      @click.stop="search(tag.name)"
    >
      <span class="clip">
        {{ tag.name }}
      </span>
    </v-chip>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import keyInObj from '@/composables/useKeyInObj'

const store = useStore()

const props = defineProps({
  tags: {
    type: Array,
    default: null
  }
})

function search(value) {
  const query = { tags: value }
  store.dispatch('search/post', { query })
}

const tagSizes = computed(() => {
  const locale = i18n.global.locale.value
  const tagMap = {}
  props.tags.forEach(({
    id, language, name, count,
  }) => {
    let size = 12
    if (count > 4) {
      size += 3
    } else if (count > 9) {
      size += 6
    } else if (count > 14) {
      size += 9
    }
    if (language === locale || language === undefined) {
      if (!keyInObj(id, tagMap)) {
        tagMap[id] = { id, name, size }
      }
    }
  })
  const tags = Object.values(tagMap)
  return tags.length > 10 ? tags.slice(0, 10) : tags
})
</script>

<style scoped>
.tag-container {
  display: -webkit-box;
  overflow: hidden;
  color: transparent;
  white-space: break-spaces;
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.v-chip--size-x-small {
  height: 20px;
}
</style>
