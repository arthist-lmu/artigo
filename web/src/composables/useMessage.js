import { computed } from 'vue'
import isArray from '@/composables/useIsArray'
import keyInObj from '@/composables/useKeyInObj'

export default function useMessage(tags) {
  const filteredTags = computed(() => {
    if (isArray(tags.value)) {
      return [...tags.value]
    }
    return []
  })

  function tagsToMessages(senderName, newTags, oldTags) {
    if (oldTags === undefined) oldTags = []
    if (newTags.length <= oldTags.length) return []
    const additionalTagsCount = newTags.length - oldTags.length
    const additionalTags = newTags.slice(-additionalTagsCount)
    const messages = additionalTags.map((tag) => {
      const message = {
        from: senderName,
        text: tag.name || null,
        score: tag.score || 0,
        valid: tag.valid || false
      }
      if (keyInObj('suggest', tag)) {
        message.suggest = tag.suggest
      }
      if (keyInObj('highlight', tag)) {
        message.highlight = tag.highlight
      }
      return message
    })
    return messages
  }

  return {
    filteredTags,
    tagsToMessages
  }
}
