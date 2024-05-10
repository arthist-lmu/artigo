import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import i18n from '@/plugins/i18n'
import getTitle from '@/composables/useGetTitle'
import getCreators from '@/composables/useGetCreators'

export default function useResource(item, multiple = false) {
  const store = useStore()
  const { locale } = i18n.global

  const isLoaded = ref(false)
  function onLoad() {
    isLoaded.value = true
  }

  const isDisabled = ref(false)
  function onError() {
    isDisabled.value = true
  }

  function showDialog() {
    store.commit('resource/updateData', item)
  }

  const title = computed(() => getTitle(item, multiple))

  const creators = computed(() => getCreators(item))
  
  const tags = computed(() => {
    return item && item.tags ? item.tags : []
  })

  const orderedTags = computed(() => {
    const filteredTags = tags.value.reduce((accumulatedTags, { id, language, name, count = 1 }) => {
      if (!language || language === locale.value) {
        if (!accumulatedTags[id]) {
          accumulatedTags[id] = { id, name, count }
        } else {
          accumulatedTags[id].count += count
        }
      }
      return accumulatedTags
    }, {})

    const orderedTags = Object.values(filteredTags)
      .sort((a, b) => b.count - a.count)
    return orderedTags
  })

  const metadata = computed(() => {
    const filteredMetadata = {}
    if (item && item.meta) {
      const fields = new Set([
        'location',
        'institution',
        'source'
      ])
      item.meta.forEach(({ name, value_str }) => {
        if (fields.has(name) && value_str) {
          filteredMetadata[name] = value_str
        }
      })

      if (item.source && item.source.id) {
        filteredMetadata.source = item.source.name
      }
    }
    return filteredMetadata
  })

  return {
    isLoaded,
    isDisabled,
    onLoad,
    onError,
    showDialog,
    getTitle,
    title,
    getCreators,
    creators,
    tags,
    orderedTags,
    metadata
  }
}
