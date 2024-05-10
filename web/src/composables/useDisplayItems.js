import { computed } from 'vue'
import { useStore } from 'vuex'
import { useDisplay } from 'vuetify'

export default function useDisplayItems(storeName) {
  const store = useStore()
  
  const itemsPerPage = computed(() => store.state[storeName].itemsPerPage)

  const { name } = useDisplay()
  const itemsPerRow = computed(() => {
    switch (name.value) {
      case 'xs': return 1
      case 'sm': return 2
      case 'md': return 3
      case 'lg': return 4
      default: return 6
    }
  })
  const noDataCols = computed(() => {
    switch (name.value) {
      case 'xs': return 12
      case 'sm': return 9
      case 'md': return 6
      case 'lg': return 4
      default: return 3
    }
  })

  return {
    itemsPerPage,
    itemsPerRow,
    noDataCols
  }
}
