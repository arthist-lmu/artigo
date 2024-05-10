import { computed } from 'vue'
import store from '@/store'

export default function useTimestamp() {
  const isUpdated = computed(() => store.state.utils.status.timestamp)

  const isSuccessful = computed(() => {
    const { error, loading } = store.state.utils.status
    return !(error && loading)
  })

  return {
    isUpdated,
    isSuccessful
  }
}
